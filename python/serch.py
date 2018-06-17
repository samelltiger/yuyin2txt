from function.common import search, response_json, create_index, insert_in
import json
from bottle import request, route, run, template

# 搜索功能
@route('/search',method='GET')
def index( ):
    keywords = request.query.keywords or False
    if not keywords:
        return response_json('参数不正确！',0)

    print('keywords:',keywords)
    # keywords='阅读'
    res,kws = search(keywords)

    ids = {}
    res_dict = {}
    res_list = []

    if len(res):
        for li,kw in zip(res,kws):
            for one in li:
                # print(one)
                res_dict[str(one['book_id'])] = {'data':dict(one)}
                ids[str(one['book_id'])] = ids.get(str(one['book_id']),'')+kw+','
        
        for idx in res_dict.keys():
            res_dict[idx]['matched'] = ids.get(idx,'')
            res_list.append(res_dict[idx])


        code = 1
        data = res_list
    else:
        code = 0
        data = '没有找到你想要的数据'
    js = response_json(data,code) 
    return js


# 创建索引
@route('/index',method='POST')
def creat_index():
    if create_index():
        return response_json('创建成功！')
    return response_json('创建失败！',0)

# 插入新数据
@route('/search',method='POST')
def insert():
    data_json = request.forms.get('data') or False
    if not data_json:
        return response_json('参数不正确！',0)
    data = json.loads(data_json,encoding='utf-8')
    if insert_in(data):
        return response_json('插入成功！',1)  

    return response_json('插入失败！',0)

run(host='localhost', port=8080)
# print(index())
