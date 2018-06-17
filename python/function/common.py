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

# 创建新的索引文件
def create_index():
    try:
        analyzer = ChineseAnalyzer()  
        conn = ms.connect(host='localhost',user='root',passwd='',db="test",charset="utf8")
        cu = conn.cursor(cursorclass = ms.cursors.DictCursor)  
        cu.execute("set names utf8")
        cu.execute("SELECT book_id,book_name,book_desc FROM book")
        iterms = cu.fetchall()

        in_file = './index'
        file_name = 'indexer'

        if not os.path.exists(in_file):
            os.mkdir(in_file)

        if os.path.exists(in_file+'/'+file_name):
            shutil.rmtree(in_file+'/'+file_name)

        os.mkdir(in_file+'/'+file_name)

        schema = Schema(book_id=NUMERIC(stored=True,unique=True),  
                        book_name=TEXT(stored=True,analyzer=analyzer),  
                        book_desc=TEXT(stored=True,analyzer=analyzer))  
        ix = create_in(in_file+'/'+file_name, schema)#here to create schema  

        # print(musics)
        writer = ix.writer()  
        index=1  
        for iterm in iterms:
            # print('book_id:',iterm['book_id'], end='\t')
            # print('book_name:',iterm['book_name'], end='\t')
            # print('book_desc:',iterm['book_desc'])
            writer.add_document(book_id=iterm['book_id'],book_name=iterm['book_name'],book_desc=iterm['book_desc'],)  
            print(index )
            index = index+1  

        writer.commit() 
        conn.close()
        return True
    except:
        return False

# 搜索关键词
def search(searchwords, index_file='./index/indexer'):
    ix = index.open_dir(index_file)  
    # facet = sorting.FieldFacet("comment_num", reverse=True)
    searcher = ix.searcher()  

    qp = MultifieldParser(["book_name","book_desc"], schema=ix.schema)

    results = []
    kws = []
    for kw in cut_for_search(searchwords):
        q = qp.parse(kw)
        res = list(searcher.search(q))
        if len(res):
            results.append(res)
            kws.append(kw)

    # searcher.close()
    return results,kws

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
