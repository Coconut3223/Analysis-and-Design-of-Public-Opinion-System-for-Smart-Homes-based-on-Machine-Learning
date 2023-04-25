# coding:utf-8
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
from wordcloud import WordCloud, get_single_color_func
from os import path




# 词云形状图片
#WC_MASK_IMG = 'icloudmusicicon.jpg'
# 评论数据保存文件
# 词云字体
from setting import STATICFILES_DIRS,get_wordcloud_data

WC_FONT_PATH = 'simhei.ttf'
stopwords_path = path.join(STATICFILES_DIRS[0],'stopwords.txt')
jpg_path=path.join(STATICFILES_DIRS[0],'ciyuntu.png')


class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)

class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

color_to_words = {
    # words below will be colored with a single color function
    'yellow': ['特效', '演技', '设定', '剧情', ]
}
default_color=random.choice(['red', 'green', 'blue','black','purple','orange',''])
print(default_color)

#grouped_color_func = GroupedColorFunc(color_to_words, default_color)

def clean_using_stopword(text):
    """
    去除停顿词，利用常见停顿词表+自建词库
    :param text:
    :return:
    """
    print("4")
    mywordlist = []
    # 用精确模式来分词
    print("5")
    seg_list = jieba.cut(text)
    print(seg_list)
    print("6")
    liststr = "/ ".join(seg_list)
    print(liststr)
    print(stopwords_path)
    with open(stopwords_path, 'rb') as f_stop:
       f_stop_text = f_stop.read()
    print("7")
    f_stop_seg_list = f_stop_text.decode().split('\r\n')

    print("7")
    print(f_stop_seg_list)

    for myword in liststr.split('/'):  # 去除停顿词，生成新文档
        #print(myword)
        if myword.strip() not in f_stop_seg_list:
            mywordlist.append(myword.strip())
    print("8")
    #print(mywordlist)
    return ''.join(mywordlist)

def extract_keywords(content):
    """
    利用jieba来进行中文分词。
    analyse.extract_tags采用TF-IDF算法进行关键词的提取。
    :return: extract_keywords(content)
    """
    # 抽取1000个关键词，带权重，后面需要根据权重来生成词云
    #allow_pos = ('nr',) # 词性
    print("2")
    tags = jieba.analyse.extract_tags(clean_using_stopword(content), 50, withWeight=True)
    print("3")
    keywords = dict()
    for i in tags:
        print("%s---%f" % (i[0], i[1]))
        keywords[i[0]] = i[1]
    return keywords





def create_word_cloud(content):
    """
    生成词云
    :return:
    """
    # 设置词云形状图片
   # wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="#f6f6f6", #背景色
                   width=200, #(default=400),   输出的画布宽度，调成i6尺寸
                    height=200,#(default=200),
                   contour_color='#f6f6f6',#边界颜色
                   relative_scaling=0.6,
                   #mode="rgba(250,250,250,0.90)",
                   #color_func=grouped_color_func,
                    max_words=2000,
                   scale=4,
                    max_font_size=50,
                   random_state=42,
                   font_path=WC_FONT_PATH)
    #wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   #max_font_size=50, random_state=42,)
    # 生成词云
    print("1")
    wc.generate_from_frequencies(extract_keywords(content))

    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
#plt.show()
    wc.to_file(jpg_path)





content = get_wordcloud_data()
print(content)
create_word_cloud(content)


