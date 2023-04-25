import json
import sqlite3

import pymysql
import requests
import jieba
import PIL .Image as image
import numpy as np
from wordcloud1 import WordCloud


# ----------------------------数据爬取--------------------- #
#爬取的页数为1到2页
for i in range(1, 2):
    print("正在爬取第" + str(i) + "页")
    first = 'https://rate.tmall.com/list_detail_rate.htm?itemId=615757780162&spuId=1381233489&sellerId=725677994&order=3&currentPage='
    last = '&append=0&content=1&tagId=&posi=&picture=&ua=098%23E1hvb9vOvXWvUvCkvvvvvjiWPLzhtjlbRscU1j3mPmPhAjEhRsMp0jtPn2cO1jr89vhvHHiaUZkczHi47I50t1Aj71B4NYGBdvhvmpvhg9f3gpCQQTQCvvyvmmhHnswv4vwgvpvhvvvvv8QCvvyvmmWm6ahvH2TvvpvW7DQgYsbw7Di4cRsN29hvCvvvMMGvvpvVvvpvvhCvmvhvLvvbrpvjaE7vAWpaRoxBlwet9b8rwos6D7zhdu6DN%2B3la4mAdc9DibmxfBAKNpKYiXVvVCODN%2B3lYnezrmphQbmxfBkKNZ0QiNLW5CKIvpvUvvmvK08%2BhfoUvpvVmvvC9j3PKvhv8vvvvvCvpvvvvvv2vhCvmPgvvvWvphvW9pvvvQCvpvACvvv2vhCv2Uhgvpvhvvvvv8OCvvpvvUmm39hvCvvhvvm%2BvpvEvv9V9NbAvv9DRvhvCvvvvvmvvpvW7Ds1MgIw7Di4OWjNdvhvmpvUDIE479COquQCvC9GCheUo6%2Bv9hLBrdv%2BpbonSwVGRoDRIaVvvpvW7D%2BoORcw7Di4NJsNRvhvCvvvvvm%2BvpvEvvFRmmGSvE9IdvhvmpvWe9NNzQm69Q%3D%3D&isg=BDIyff_ehkVxOLp0KjoCm02xg3gUwzZdS4FzU_wKE-Udj9CJ5FHFbfXlfysz-671&_ksTS=1611196691540_557&callback=jsonp558'
    base_url = first + str(i) + last

# 可能还需要伪造的是
headers = {
    # 没有user-agent无法正常访问
    'Cookie': 'hng=CN%7Czh-CN%7CCNY%7C156; cna=hnmKGNeCBDkCAd/1xCq+gSl+; lid=fallen%E4%B8%B6%E7%96%BE%E9%A3%8E; enc=WYdSbebJ5kzeAAMnUUBssIO8TIk81izFrqIdDerasS98UPEKM3DBzPucm5F88LMrWB15ytjJKGEqZjSf%2FCNIWA%3D%3D; tk_trace=1; xlly_s=1; dnk=fallen%5Cu4E36%5Cu75BE%5Cu98CE; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=W5iHLLyFeYZ1WM9hVnmS&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&cookie14=Uoe1g8gImnMbcg%3D%3D&pas=0; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dCuAFakqkQbNC0B04%3D&id2=VyyX4%2BtmxDUikg%3D%3D&nk2=BdGgteHCQa7Df4lZ; tracknick=fallen%5Cu4E36%5Cu75BE%5Cu98CE; _l_g_=Ug%3D%3D; uc4=nk4=0%40B128KMppJDHlf67djbHorgOGXkeq354%3D&id4=0%40VXtYjykFesLlJ%2FuXPllnCFJDjd%2F6; unb=4065455020; lgc=fallen%5Cu4E36%5Cu75BE%5Cu98CE; cookie1=U7kD%2BlnXU%2FKoy30g%2FKHcG5WgYAc5KuoKHFTabfgHrYc%3D; login=true; cookie17=VyyX4%2BtmxDUikg%3D%3D; cookie2=11ed88e510297f72ccbad7930d8a3abc; _nk_=fallen%5Cu4E36%5Cu75BE%5Cu98CE; sgcookie=E100aCgcej%2FG%2FveU%2BxZ4gJ4vaD2XRsAVJaGhMFC58qxAnQcmRxrw%2FGlv5zOEonNh0SS46YnndBykTsDAhEZjGTqhUg%3D%3D; sg=%E9%A3%8E0f; t=d145b00cb8210daf38cb25ab3ab1e97f; csg=63252b39; _tb_token_=e5531f71e35b5; _m_h5_tk=9382ec7cb83df5e319b97cce0dc5ba21_1611205771358; _m_h5_tk_enc=5c0ad996515e3e13d1efce7af66f4564; sm4=140726; x5sec=7b22726174656d616e616765723b32223a226165663333336230303035353434393135323236663634663134343136653635434b4c4f6f344147454e666967373339315a572f39774561444451774e6a55304e5455774d6a41374d513d3d227d; tfstk=cw9dBj1BOV0nHTI90BhgP1e9F5QRZhZdrk_8emYa0Bn-Ap2RiLJDHI1mOgzdBcC..; isg=BPT0Nq1QKC_j8rxuOAS8of-nxbJmzRi3ebf1KY5URn4Q-ZBDtt-ERn__eTEhBVAP; l=eBTabYG7jOzgmj0vBO5ahurza77tqIdfGoVzaNbMiInca1ShKC_O0NCI6n6ejdtjgtfXUetzLAUwVRHD5q4U-E_ceTwntdJhA9vw-',
    'referer': 'https://chaoshi.detail.tmall.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
}


# ------------------------------创建数据库——————---------------------------- #
connect = pymysql.connect(
            host='127.0.0.1',           # ip
            port=3306,                  # 端口
            user='root',                # 用户名
            password='root',       # 密码
            db ='bishebili',
            charset='utf8'              # 编码格式
        )
# 从会话中生成游标
cursor = connect.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS try1(
        cid INTEGER PRIMARY KEY,
        rateContent TEXT,
        rateDate TEXT,
        auctionSku TEXT
    );
""")
resp = requests.get(base_url, headers=headers)
comments = resp.text
print(comments)
file = open('./淘宝评论爬取.json', mode='r', encoding='utf-8')
comments_json = file.read()
comments_obj = json.loads(comments_json)
print(comments_obj)
rateDetail = comments_obj['rateDetail']
rateList = rateDetail['rateList']
file.close()
for c in range(len(rateList)):
    cid = rateList[c]['id']
    rateContent = rateList[c]['rateContent']
    rateDate = rateList[c]['rateDate']
    auctionSku = rateList[c]['auctionSku']
    print('-' * 100)
    print(cid, rateContent)
    cursor.execute(
    """insert or ignore into try1 (cid, rateContent, rateDate, auctionSku) values (?,?,?,?);""",
    [cid, rateContent, rateDate, auctionSku])
# 提交确认（插入和更新）
connect.commit()
cursor.execute("""
    select * from try1;
""")
# 取出查询数据
rs = cursor.fetchall()
print(rs)


# ------------------------------取出数据库并进行分词——————---------------------------- #
# cursor.execute("""select * from try1 order by rateDate desc limit 0,9;""")
# comments_rs = cursor.fetchall()
# comments = [c[1] for c in comments_rs]
# comments = ''.join(comments)
# words = jieba.cut(comments, cut_all=False)
# # generator object
# comment_words_list = list(words)
#
# with open('../L05/dict/stop_words_zh.txt', mode='r', encoding='utf-8') as f:
#     stop_words = f.read().splitlines()
#
# filtered_comment_word_list = []
# for word in comment_words_list:
#     if word not in stop_words:
#         filtered_comment_word_list.append(word)
#
# comment_words_str = ' '.join(filtered_comment_word_list)
# print(comment_words_str)

# 关闭游标
cursor.close()
# 关闭数据库
connect.close()


# # ——————————————————————————————————数据可视化———————————————————————————————————————— #
# wc = WordCloud(
#         width=1000,
#         height=800,
#         max_words=500,
#         min_font_size=50,
#           ).generate(comment_words_str)
# wc.to_file('./淘宝评论词云图.png')
