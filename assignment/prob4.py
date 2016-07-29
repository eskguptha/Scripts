import sys
import re

with open('english.sorted') as data:
    counter = 0
    for each_line in data:
        result_data = re.match("^[aA].*", each_line)
        if result_data:
            counter += 1
    print counter

