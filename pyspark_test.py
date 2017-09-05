from pyspark import SparkContext
from pyspark.sql import HiveContext, Row

import json
import os

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import client
from elasticsearch import exceptions
from elasticsearch import exceptions, ImproperlyConfigured, ElasticsearchException

ES_HOST = "127.0.0.1"
ES_PORT = "9200"
BULK_INSERT_SIZE = 1
es_con = Elasticsearch("http://{0}:{1}".format(ES_HOST,ES_PORT))

sc = SparkContext('local','demo')
hive_context = HiveContext(sc)

filed_names = ['house_key','customer_account_id','current_product_mix','active_clv','iclv_vh','iclv_vc','iclv_x','iclv_h','iclv_hc','iclv_vcx','iclv_hcx','iclv_vhcx','iclv_v','iclv_c','iclv_vhx','iclv_vhc','iclv_hx','iclv_cx','iclv_vx']

def create_sqldataframe_from_csv():
    raw_data = sc.textFile("sales.csv")
    csv_data = raw_data.map(lambda l: l.split(","))
    row_data = csv_data.map(lambda p: Row(
        house_key=p[0],
        customer_account_id=p[1],
        current_product_mix=p[2],
        active_clv=p[3],
        iclv_vh=p[4],
        iclv_vc=p[5],
        iclv_x=p[6],
        iclv_h=p[7],
        iclv_hc=p[8],
        iclv_vcx=p[9],
        iclv_hcx=p[10],
        iclv_vhcx=p[11],
        iclv_v=p[12],
        iclv_c=p[13],
        iclv_vhx=p[14],
        iclv_vhc=p[15],
        iclv_hx=p[15],
        iclv_cx=p[16],
        iclv_vx=p[17]
        )
    )
    interactions_df = hive_context.createDataFrame(row_data)
    interactions_df.registerTempTable("sales_recomendations")
    return interactions_df

def create_sqldataframe_from_hive():
    interactions_df = hive_context.sql("select * from dbname.sales_recomendations")
    return interactions_df

def generate_recomendatioms(sql_df):
    f1 = open('logs/sales.log', 'w')
    sql_data = hive_context.sql('SELECT * FROM sales_recomendations')
    for row in sql_data.collect()[1:]:
        user_obj = {}
        for col in filed_names[4:]:
            user_obj[col] = row[col]
        result_data = sorted(user_obj.items(), key=lambda value: value[1])
        result_data.reverse()
        log_data = {
        "customer_account_id" : row['customer_account_id'],
        "house_key" : row['house_key'],
        "recommendations" : [ each[0] for each in result_data[:3]]
        }
        f1.write(json.dumps(log_data)+'\n')
    f1.close()


def write_to_es():
    """
    input parmeter : filename
    Write user documents of a logfile into ES
    """
    log_file_list = [fileName for fileName in os.listdir("logs") if fileName.endswith(".log")]
    for file_name in log_file_list:
        try:
            # Get file in folder
            log_dir = os.path.join('logs',file_name)
            f = open(log_dir, 'r')
            # read file
            es_doc_list = []
            for each_dict in f:
                try:
                    user_dict = json.loads(each_dict)
                    document_id = int(user_dict['house_key'])
                    index_name = user_dict['customer_account_id']                
                    try:
                        # Find all indices
                        index_client = client.IndicesClient(es_con)
                        #check Index exist or not on list of indices
                        if not index_client.exists(index=index_name):
                            # create new mapping for new index
                            body_dict = {
                                      "mappings": {
                                        "user": {
                                          "dynamic_templates": [
                                            {
                                              "string_template": {
                                                "match_mapping_type": "string",
                                                "mapping": {
                                                  "index": "not_analyzed",
                                                  "type": "string"
                                                },
                                                "match": "*"
                                              }
                                            }
                                          ]
                                        }
                                      }
                                    }
                            # create new index
                            index_client.create(index=index_name, body=body_dict)
                            # Refresh Index 
                            index_client.refresh(index=index_name)
                        try:
                            # check user exist or not
                            uid_exists = es_con.exists(index=index_name, doc_type="user", id=document_id)
                        except:
                            uid_exists = None

                        if uid_exists:
                            # update user doc
                            es_doc = {
                                "_index": index_name,
                                "_type": "user",
                                "_id": document_id,
                                "_source": {"recommendations" : user_dict['recommendations']}
                                
                                    }

                        else:
                            # create new user doc
                            es_doc = {
                                "_index": index_name,
                                "_type": "user",
                                "_id": document_id,
                                "_source": {"recommendations" : user_dict['recommendations']}
                                }
                        
                        es_doc_list.append(es_doc)
                        # Insert document on every BULK_INSERT_SIZE 
                        if (len(es_doc_list) == BULK_INSERT_SIZE):
                            helpers.bulk(es_con, es_doc_list)
                            es_doc_list = []
                    except (ImproperlyConfigured, ElasticsearchException) as e:
                        print (e)
                        pass
                except ValueError as e:
                    print (e)
                    pass
            # Insert remain documents
            if es_doc_list:
                helpers.bulk(es_con, es_doc_list)
                es_doc_list = []
            f.close()
        except IOError as e:
            print (e)
            pass








if __name__ == "__main__":
    csv_df = create_sqldataframe_from_csv()
    #hive_df = create_sqldataframe_from_hive()
    generate_recomendatioms(csv_df)
    write_to_es()
