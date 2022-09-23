__author__ = 'Santhosh Emmadi'
"""
This is Application Database Repository Class and it containts All data base related CURD Operations on Selected Database.
"""

import sys

from logger_ import getAppLogger
import traceback
import pyodbc

logger = getAppLogger('DBScripts')

def splitListByChunks(inputList, n):
    n = max(1, n)
    return (inputList[i:i + n] for i in range(0, len(inputList), n))

class DBRepository():
    """DB Repository class"""

    def __init__(self, driver, server, uid, pwd, database):
        self.driver = driver
        self.server = server
        self.uid = uid
        self.pwd = pwd
        self.database = database
        self.connection = self.connect()

    def connect(self):
        """ Connect to Database """
        logger.info("Create DB connection process start")
        try:
            connection = pyodbc.connect(
                driver=self.driver,
                server=self.server,
                uid=self.uid,
                pwd=self.pwd,
                database=self.database)
            logger.info("Connected DB Successfully")
            logger.info("create connection process end")
            return connection
        except pyodbc.Error as ex:
            logger.info("create connection process failed. Exception: %s, log:: %s", ex, traceback.format_exc())
            sys.exit()

    def get(self, query):
        """ Connect to Database """
        logger.info("get records process start")
        try:
            db_cursor = self.connection.cursor()
            db_cursor.execute(query)
            records = db_cursor.fetchall()
            logger.info("get records process end")
            return True, records
        except pyodbc.Error as ex:
            logger.info("get records process failed. Exception: %s, log:: %s", ex, traceback.format_exc())
            return False, ()

    def insert(self, tbl_name, columns, record):
        """ Insert records into table """
        logger.info("Insert records into %s table Process start", tbl_name)
        try:
            db_cursor = self.connection.cursor()
            column_names = ','.join(columns).strip()
            column_values = ("?," * len(columns))[:-1]
            statement = f"INSERT INTO {tbl_name}({column_names}) VALUES ({column_values})"
            logger.info(statement)
            db_cursor.execute(statement, tuple(record))
            db_cursor.commit()
            db_cursor.close()
            logger.info("Record Inserted Successfully")
            logger.info("Insert records into %s table Process end", tbl_name)
            return True
        except pyodbc.Error as ex:
            logger.info("Record insertion process failed. Record:  %s, Exception: %s, log:: %s", record, ex,
                        traceback.format_exc())
            return False

    def bulk_insert(self, tbl_name, columns, records, batch_size=100):
        """ Insert records into table """
        logger.info("Bulk Insert records into %s table Process start", tbl_name)
        try:
            batch_list = splitListByChunks(records, batch_size)
            for each_batch in batch_list:
                db_cursor = self.connection.cursor()
                column_names = ','.join(columns).strip()
                column_values = ("?," * len(columns))[:-1].strip()
                statement = f"INSERT INTO {tbl_name}({column_names}) VALUES ({column_values})"
                logger.info(statement)
                db_cursor.executemany(statement, tuple(each_batch))
                res = db_cursor.commit()
                db_cursor.close()
            logger.info("Bulk Records Inserted Successfully")
            logger.info("Bulk Insert records into %s table Process end", tbl_name)
            return True
        except pyodbc.Error as ex:
            logger.info("Bulk Record insertion process failed. Record:  %s, Exception: %s, log:: %s", records, ex,
                        traceback.format_exc())
            return False

    def update(self, db_con, tbl_name, ):

        pass

    def delete(self):
        pass
if __name__ == '__main__':
    DB = DBRepository(driver, server, uid, pwd, database)
