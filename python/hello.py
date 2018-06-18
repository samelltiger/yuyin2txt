from function.common import search, response_json, insert_in, list_to_dict
import json


# test = [{'book_id':1,'book_name':'abaf','book_desc':'this is a test recorde'}]
# if insert_in(test):
#     print('插入成功')
# else:
#     print('插入失败')

# res,kws = search('服务员',['job_name','type','company_name'],'./index/job_index')
res,kws = search('我要找一个芒果',['maintype','place'],'./index/farm_products_index')
print(list_to_dict(res,kws,'id',True))