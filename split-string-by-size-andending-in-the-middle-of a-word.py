# Truncate a string without ending in the middle of a word
# split-string-by-size-andending-in-the-middle-of a-word.py

str1 = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."
length = 30
def smart_truncate(content, length):
    if len(content) <= length:
        result = content
    else:
        result = ' '.join(content[:length+1].split(' ')[0:-1])
    return result
flag = False
output_data = []
result = smart_truncate(str1, length)
output_data.append(result)
remain = str1[len(output_data[-1]):]
if not remain:
    flag = True
while not flag:
    result = smart_truncate(remain, length)
    if result:
        output_data.append(result)
        remain = str1[sum([len(item) for item in output_data]):]
    else:
        exit()
    if remain:
        flag = False
    else:
        flag = True
print output_data
