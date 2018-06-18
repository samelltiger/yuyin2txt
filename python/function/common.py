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
from whoosh import columns, fields, index, sorting

# 创建一个工作数据索引
def create_job_index( ):
    try:
        conn = ms.connect(host='120.79.14.47',user='root',passwd='Kermi0116',db='58city',charset="utf8")
        cu = conn.cursor(cursorclass = ms.cursors.DictCursor)
        cu.execute("set names utf8")
        cu.execute('SELECT id,jobName,type,company_name FROM `job`')
        iterms = cu.fetchall()
        if not iterms:
            return False

        analyzer = ChineseAnalyzer()
        schema = Schema(id=NUMERIC(stored=True, unique=True),  
                        job_name=TEXT(stored=True, analyzer=analyzer),  
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
    for kw in cut_for_search(searchwords):
        q = qp.parse(kw)
        res = list(searcher.search(q))
        if len(res):
            results.append(res)
            kws.append(kw)

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
def insert_in(data, index_file='./index/indexer'):
    if not isinstance(data,list): 
        return False

    ix = open_dir(index_file)#here to create schema  
    # print(musics)
    writer = ix.writer()

    for iterm in data:
        writer.add_document(book_id=iterm['book_id'],book_name=iterm['book_name'],book_desc=iterm['book_desc'],)
    writer.commit() 
    return True