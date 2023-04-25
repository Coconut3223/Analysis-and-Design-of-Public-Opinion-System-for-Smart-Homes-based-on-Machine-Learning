import jieba
# 连入数据库
import pymysql

conn = pymysql.connect(
    host='127.0.0.1',  # ip
    port=3306,  # 端口
    user='root',  # 用户名
    password='root',  # 密码
    db='bishebili',
    charset='utf8'
)
# password：数据库密码，database：操作的数据库
cursor = conn.cursor()
# 从数据库c表中获取所有信息，储存到name里
# （为了避免出错挽救不了，直接将分词后的数据储存到新建的数据库d中，所以这里我获取全部信息
sql = '''select * from c;'''
cursor.execute(sql)
name = cursor.fetchall()


# 将停用词txt文件里停用词的返回到stopwords列表当中
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 自建字典分词
def cut(i):
    jieba.load_userdict("../userdict.txt")  # 自建字典地址
    seg_list = list(jieba.cut_for_search(i))  # 将搜索引擎模式，分词后的字符串作为链表储存
    # 将链表里的字符元素重新合成字符串
    sentence = ""
    for word in seg_list:
        if word != '\t':
            sentence += word
    return sentence


# 去停用词
def seg_sentence(sentence):
    # 再度分词
    sentence_seged = jieba.cut(sentence.strip())  # strip()：把头和尾的空格去掉，返回列表
    stopwords = stopwordslist("../stop.txt")  # 路径
    # 除停用词，返回有用的字符串
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
    return outstr


# 创建表d的sql语句
cursor.execute("drop table if EXISTS Products")
sql = """create table  products (
            id INT NOT NULL  PRIMARY KEY auto_increment，
            product VARCHAR(60),
            web VARCHAR(100),
            price FLOAT(10)
          );
          """
# int不指定任何长度否则会报错。int()×
cursor.execute(sql)

for i in name:
    pro = str(i[1])  # i = [id,product,web,price]
    sentence = cut(pro)  # 初步分词，返回字符串
    line_seg = seg_sentence(sentence)  # 去停用词
    # 将结果连接数据库储存到表d
    try:
        sql1 = "insert into Products(product,web,price)values(%s,%s,%s);"
        cursor.execute(sql1, (line_seg, i[2], i[3]))
    except:
        print("异常")  # 发生错误
conn.commit()