from function.common import *
import json
from bottle import request, route, run, template

# 搜索功能
@route('/search',method='GET')
def index( ):
    keywords = request.query.keywords or False
    type_of  = request.query.type or False
    if not keywords:
        return response_json('参数不正确！',0)

    print('keywords:',keywords)
    # keywords='阅读'

    if type_of:
        if 'job' in type_of:
            res,kws = search(keywords, ['job_name','type','company_name'],'./index/job_index')
        elif 'farm' in type_of:
            res,kws = search(keywords, ['maintype','place'],'./index/farm_products_index')
        else:
            return response_json('参数错误，type值为 job或farm',0) 

        if res:
            code = 1
            data = list_to_dict(res,kws,'id',True)
        else:
            code = 0
            data = '没有找到你想要的数据'
    else:
        code = 0
        data = '参数错误，type值为 job或farm'

    js = response_json(data, code) 
    return js


# 创建索引
@route('/index',method='POST')
def creat_index():
    type_of = request.forms.get('type') or False
    status = False
    if type_of:
        if 'job' in type_of:
            status = create_job_index()
        elif 'farm' in type_of:
            status = create_farm_index()
        elif 'both' in type_of:
            status = create_job_index() and create_farm_index()
        else:
            return response_json('参数错误，type值为 job或farm',0) 

        if status:
            code = 1
            data = '创建成功！'
        else:
            code = 0
            data = '没有找到你想要的数据'
    else:
        code = 0
        data = '参数错误，type值为 job或farm或both'

    return response_json(data, code)

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
