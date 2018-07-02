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
            res,kws = search(keywords, ['job_name','type','area_a','company_name'],'./index/job_index')
        elif 'farm' in type_of:
            res,kws = search(keywords, ['maintype','type','place'],'./index/farm_products_index')
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

    if code and 'farm' in type_of:
        data = sorted(data.items(),key=lambda x:len(x[1]))
        data = dict(list(reversed(data)))
        sort = list(data.keys())
        sort = ','.join(sort)
        print(sort)
        # data['sort'] = sort

    js = response_json(data, code)
    return js


# 创建索引
@route('/index',method='GET')
def creat_index():
    type_of = request.query.type or False
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
            data = '创建失败！'
    else:
        code = 0
        data = '参数错误，type值为 job或farm或both'

    return response_json(data, code)

# 插入新数据
@route('/search',method='POST')
def insert():
    data_json = request.forms.get('data') or False
    type_of = request.forms.get('type') or False
    if not data_json:
        return response_json('参数不正确！',0)
    data = json.loads(data_json, encoding='utf-8')

    if type_of:
        if 'job' in type_of:
            status = insert_in(data, index_file='./index/job_index',is_job=True)
        elif 'farm' in type_of:
            status = insert_in(data, index_file='./index/farm_products_index',is_job=False)
        else:
            return response_json('参数错误，type值为 job或farm',0) 

        if status:
            code = 1
            data = '插入成功！'
        else:
            code = 0
            data = '插入失败！'
    else:
        code = 0
        data = '参数错误，type值为 job或farm'

    return response_json(data, code)

run(host='localhost', port=8080)
