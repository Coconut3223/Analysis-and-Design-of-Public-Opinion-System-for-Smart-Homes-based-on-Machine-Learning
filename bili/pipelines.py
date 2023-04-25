# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#
# class BiliPipeline:
#     def process_item(self, item, spider):
#         return item
from bili.items import VideoItem,CommentItem
import pymysql
class BiliPipeline:
    def __init__(self):
        # 建立MySQL链接对象
        self.connect = pymysql.connect(
            host='127.0.0.1',           # ip
            port=3306,                  # 端口
            user='root',                # 用户名
            password='root',       # 密码
            db ='bishebili',
            charset='utf8'              # 编码格式
        )
        self.cursor = self.connect.cursor()  # 执行命令游标
        # 判断是否存在数据库，不存在则创建，并进入数据库
        #self.cursor.execute("drop database if exists bishebili")
        #self.cursor.execute("create database if not exists bishebili character set 'utf8'")
        self.cursor.execute("use bishebili")

        #判断是否存在数据表，不存在则创建
        self.cursor.execute("drop table if exists bili_video11;")
        self.cursor.execute("drop table if exists bili_comment11;")
        video_sql = '''CREATE TABLE bili_video11(
            video_title varchar(200),
            video_like varchar(10),
            video_coin varchar(10),
            video_collect varchar(10),
            video_share varchar(10),
            video_comment varchar(10),
            video_read varchar(10),
            video_oid varchar(50),
            video_time varchar(50))
            '''
        comment_sql = '''CREATE TABLE bili_comment11(
            comment_zan varchar(10),
            comment_reply varchar(10),
            comment_content varchar(500),
            comment_level varchar(10),
            comment_oid varchar(50),
            sex varchar(10),
            ctime varchar(50),
            comment_time varchar(50)
            )
            '''
        self.cursor.execute(video_sql)
        self.cursor.execute(comment_sql)

    def process_item(self, item, spider):
        print('lllllllll')
        try:
            if isinstance(item, VideoItem):
                # 你的处理方法
                self.cursor.execute("insert into bili_video11 values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    list(dict(item).values()))  # 插入代码语句
                print('插入成功')
                pass
            elif isinstance(item, CommentItem):
                # 处理方法
                self.cursor.execute("insert into bili_comment11 values (%s,%s,%s,%s,%s,%s,%s,%s)",
                                    list(dict(item).values()))  # 插入代码语句
                print('插入成功')
                pass

            print('插入成功')
        except Exception as e:
            print('插入错误：', e)  # 打印插入错误原因
            self.connect.rollback()  # 回滚事务，不插入数据
        else:
            self.connect.commit()  # 提交事务，插入成功数据
        return item

    def close_spider(self, spider):
        self.cursor.close()  # 关闭游标
        self.connect.close()  # 关闭数据库链接
        print('爬虫已结束')
