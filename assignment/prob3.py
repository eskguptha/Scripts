import sys
import re

with open('sp08cs') as data:
    for each_line in data:
        if re.match(r'(.*)CS-[1-4].*', each_line):
            each_line = re.sub(r'\<td\>', " ", each_line)
            each_line = re.sub(r'\</td\>', " ", each_line)
            each_line = re.sub(r'\<br\>', " ", each_line)
            print each_line

