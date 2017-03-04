xml to text

from xml.etree import ElementTree
import re

input_file_name = "pubmed_result.xml"
output_file_name = 'email_data.txt'

with open(input_file_name, 'rt') as f:
    tree = ElementTree.parse(f)
email_data = []

for node in tree.iter('Article'):
	for each in node.iter('AuthorList'):
		for a in each.iter('Author'):
			for b in a.iter('AffiliationInfo'):
				for e in b.iter('Affiliation'):
					if "@" in e.text:
						edata = re.findall(r'[\w\.-]+@[\w\.-]+', e.text)
						for item in edata:
							if item.endswith('.'):
								item = item[:-1]
							email_data.append("%s"%item)
print email_data

with open(output_file_name, "wb") as f:
	for each in email_data:
		f.write(each)
		f.write('\n')
