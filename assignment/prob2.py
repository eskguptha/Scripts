import sys

with open('english.sorted') as data:
    for each_line in data:
        if each_line[0].isupper():
            print each_line

