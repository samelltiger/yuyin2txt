# -*- coding:utf-8 -*-  
import MySQLdb as ms
import json
import re  
import os
import shutil
from jieba import cut_for_search
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT, NUMERIC,NGRAMWORDS  
from whoosh.index import create_in,open_dir
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser,MultifieldParser
from whoosh import columns, fields, index, sorting, query
import numpy as np

# 创建一个工作数据索引
def create_job_index( ):
    try:
        conn = ms.connect(host='120.79.14.47',user='root',passwd='Kermi0116',db='58city',charset="utf8")
        cu = conn.cursor(cursorclass = ms.cursors.DictCursor)
        cu.execute("set names utf8")
        cu.execute('SELECT id,jobName,type,area_a,company_name FROM `job`')
        iterms = cu.fetchall()
        if not iterms:
            return False

        analyzer = ChineseAnalyzer()
        schema = Schema(id=NUMERIC(stored=True, unique=True),  
                        job_name=TEXT(stored=True, analyzer=analyzer),  
                        area_a=TEXT(stored=True, analyzer=analyzer),  
                        type=TEXT(stored=True, analyzer=analyzer),  
                        company_name=TEXT(stored=True, analyzer=analyzer))
        writer = create_index('job_index',schema)
        if not writer:
            return False
        

        for iterm in iterms:
            writer.add_document(id=iterm['id'],job_name=iterm['jobName'],type=iterm['type'],company_name=iterm['company_name'])  

        writer.commit()
        conn.close()
        return True
    except:
        return False

# 创建一个农产品数据索引
def create_farm_index( ):
    try:
        conn = ms.connect(host='120.79.14.47',user='root',passwd='Kermi0116',db='farm_products',charset="utf8")
        cu = conn.cursor(cursorclass = ms.cursors.DictCursor)
        cu.execute("set names utf8")
        cu.execute('SELECT id,maintype,place FROM `tendency`')
        iterms = cu.fetchall()
        if not iterms:
            return False

        analyzer = ChineseAnalyzer()
        schema = Schema(id=NUMERIC(stored=True, unique=True),  
                        maintype=TEXT(stored=True, analyzer=analyzer),  
                        place=TEXT(stored=True, analyzer=analyzer)) 
        writer = create_index('farm_products_index',schema)
        if not writer:
            return False

        for iterm in iterms:
            writer.add_document(id=iterm['id'],maintype=iterm['maintype'],place=iterm['place'])  

        writer.commit()
        conn.close()
        return True
    except:
        return False

# 创建新的索引文件
def create_index(file_name, schema):
    try:
        in_file = './index'

        if not os.path.exists(in_file):
            os.mkdir(in_file)

        if os.path.exists(in_file+'/'+file_name):
            shutil.rmtree(in_file+'/'+file_name)

        os.mkdir(in_file+'/'+file_name)
 
        ix = create_in(in_file+'/'+file_name, schema)#here to create schema  

        writer = ix.writer( )
        return writer
    except:
        return False

# 搜索关键词
def search(searchwords, search_fields , index_file):
    ix = index.open_dir(index_file)  
    # facet = sorting.FieldFacet("comment_num", reverse=True)
    searcher = ix.searcher()  

    qp = MultifieldParser(search_fields, schema=ix.schema)

    results = []
    kws = []
    if './index/farm_products_index' in index_file:
        for kw in cut_for_search(searchwords):
            q = qp.parse(kw)
            res = list(searcher.search(q, limit=50))
            if len(res):
                results.append(res)
                kws.append(kw)

    elif './index/job_index' in index_file:
        types = ['普工','服务员','快递员','货运司机','店员/营业员','保安','商务司机','送餐员','保洁','客服专员/助理','仓库管理员','收银员','促销/导购员','操作工','装卸/搬运工','专车司机','分拣员','电话客服','保姆','物流专员/助理','切割/焊工','车工/铣工','洗碗工','后厨','厨师/厨师长','电工','店长/卖场经理','网络/在线客服','学徒工','售前/售后服务']
        places = ['大连','广州','上海','深圳','北京','宁波','哈尔滨','苏州','佛山','长沙','重庆','成都','烟台','青岛','廊坊','中山','沈阳','江门','东莞','济南','杭州','福州','威海','天津','石家庄','瓦房店','惠州','厦门','荣成']
        t = np.array(list(cut_for_search(searchwords)))
        job = t[np.isin(t,types)]
        city = t[np.isin(t,places)]
        s = ' '.join(job) if job else ''
        s += ' '.join(job) if city else ''

        # cuted_s = ' '.join(job)
        q = qp.parse(s)
        r = searcher.search(q, terms=True, limit=50)
        res = list(r)
        if len(res):
            results.append(res)
            kws.append('test')
        
    return results,kws

# 将搜索到的数据以及所有结果打包
def list_to_dict(res, kws, id_field, return_ids=False):
    ids = {}
    res_dict = {}
    res_list = []

    for li,kw in zip(res,kws):
        for one in li:
            # print(one)
            res_dict[str(one[id_field])] = {'data':dict(one)}
            ids[str(one[id_field])] = ids.get(str(one[id_field]),'')+kw+','
    
    if return_ids:
        return ids

    for idx in res_dict.keys():
        res_dict[idx]['matched'] = ids.get(idx,'')
        res_list.append(res_dict[idx])
    
    return res_list,ids

# 返回json格式数据
def response_json(data,code=1):
    json_res = {}
    json_res['success'] = code
    json_res['data'] = data
    return json.dumps(json_res, ensure_ascii=False, indent=4)

# 插入索引
def insert_in(data, index_file='./index/job_index',is_job=True):
    try:
        if not isinstance(data,list): 
            return False

        analyzer = ChineseAnalyzer()
        ix = open_dir(index_file)#here to create schema  
        # print(musics)
        writer = ix.writer()

        if is_job:
            schema = Schema(id=NUMERIC(stored=True, unique=True),  
                            job_name=TEXT(stored=True, analyzer=analyzer),  
                            type=TEXT(stored=True, analyzer=analyzer),  
                            company_name=TEXT(stored=True, analyzer=analyzer))

            for iterm in data:
                writer.add_document(id=iterm['id'],job_name=iterm['jobName'],type=iterm['type'],company_name=iterm['company_name'])  
        else:
            schema = Schema(id=NUMERIC(stored=True, unique=True),  
                            maintype=TEXT(stored=True, analyzer=analyzer),  
                            place=TEXT(stored=True, analyzer=analyzer)) 
            for iterm in data:
                writer.add_document(id=iterm['id'],maintype=iterm['maintype'],place=iterm['place'])  

        writer.commit() 
        return True
    except:
        return False
