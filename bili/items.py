# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 视频的的点赞数、浏览量、评论数、标题、作者的等级
    video_title = scrapy.Field()
    video_like = scrapy.Field()
    video_coin = scrapy.Field()
    video_collect = scrapy.Field()
    video_share = scrapy.Field()
    video_comment = scrapy.Field()
    video_read = scrapy.Field()
    video_oid = scrapy.Field()
    video_time = scrapy.Field()
    pass
class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #评论的点赞量、回复数、文本、作者的等级
    comment_zan = scrapy.Field()
    comment_reply = scrapy.Field()
    comment_content = scrapy.Field()
    comment_level = scrapy.Field()
    comment_oid = scrapy.Field()
    sex = scrapy.Field()
    ctime = scrapy.Field()
    comment_time = scrapy.Field()

    pass




