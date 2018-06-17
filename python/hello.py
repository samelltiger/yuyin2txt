from function.common import search, response_json, create_index, insert_in
import json


test = [{'book_id':1,'book_name':'abaf','book_desc':'this is a test recorde'}]
if insert_in(test):
    print('插入成功')
else:
    print('插入失败')

# print(search('阅读'))