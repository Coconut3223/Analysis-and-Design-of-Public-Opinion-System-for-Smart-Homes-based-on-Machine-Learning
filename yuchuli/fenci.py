
import time
import json
import random
import re
import jieba.analyse
import jieba
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from os import path




# 词云形状图片
#WC_MASK_IMG = 'icloudmusicicon.jpg'
# 评论数据保存文件
# 词云字体
WC_FONT_PATH = '../simhei.ttf'
stopwords_path = 'stopwords.txt'
text_path = 'wen.txt'
jpg_path = 'wen.jpg'


def preprocessing():
    """
    文本预处理
    :return:
    """
    with open(text_path) as f:
        content = f.read()
    return clean_using_stopword(content)
    return content


def clean_using_stopword(text):
    """
    去除停顿词，利用常见停顿词表+自建词库
    :param text:
    :return:
    """
    mywordlist = []
    # 用精确模式来分词
    seg_list = jieba.cut(text)
    liststr = "/ ".join(seg_list)
    with open(stopwords_path) as f_stop:
        f_stop_text = f_stop.read()
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):  # 去除停顿词，生成新文档
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ''.join(mywordlist)

def extract_keywords():
    """
    利用jieba来进行中文分词。
    analyse.extract_tags采用TF-IDF算法进行关键词的提取。
    :return:
    """
    # 抽取1000个关键词，带权重，后面需要根据权重来生成词云
    allow_pos = ('nr',) # 词性
    tags = jieba.analyse.extract_tags(preprocessing(), 50, withWeight=True)
    keywords = dict()
    for i in tags:
        print("%s---%f" % (i[0], i[1]))
        keywords[i[0]] = i[1]
    return keywords





def create_word_cloud():
    """
    生成词云
    :return:
    """
    # 设置词云形状图片
   # wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, scale=4,
            max_font_size=50, random_state=42,font_path=WC_FONT_PATH)
    #wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   #max_font_size=50, random_state=42,)
    # 生成词云
    wc.generate_from_frequencies(extract_keywords())

    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()
    wc.to_file(jpg_path)



if __name__ == '__main__':

    #生成词云
    create_word_cloud()
