import os
import xlrd
from os import path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,'static'),
)
print(STATICFILES_DIRS)



#读取excel文件
def excel(xls_path,sheetname,columns,columne):
    wb = xlrd.open_workbook(xls_path)# 打开Excel文件
    sheet = wb.sheet_by_name(sheetname)#通过excel表格名称(rank)获取工作表
    datalist = []  #创建空list
    for a in range(sheet.nrows):  #循环读取表格内容（每次读取一行数据）
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        if columns != columne:
            columnlist = []
            for b in range(columns,columne):
                data = cells[b]
                columnlist.append(data)
            datalist.append(columnlist)
        else:
            data=cells[columns]#因为表内可能存在多列数据，0代表第一列数据，1代表第二列，以此类推
            datalist.append(data) #把每次循环读取的数据插入到list
    return datalist

def get_wordcloud_data():
    wordcloud_path = path.join(STATICFILES_DIRS[0],'bili_comment1-fenci1.xls')
    wordcloud_sheet = 'bili_comment1'
    fenci_list = excel(wordcloud_path,wordcloud_sheet,0,0) #返回整个函数的值 第一列
    for i in range(20):
        print(fenci_list[i])
    content = ""
    for i in range(len(fenci_list)):
        content += fenci_list[i]
    #print(content)
    return content
def get_video_data():
    origin_path = path.join(STATICFILES_DIRS[0], 'origin_video.xls')
    x1 = xlrd.open_workbook(origin_path)
    origin_sheet = 'origin'
    sheet1 = x1.sheet_by_name(origin_sheet)
    origin_list = excel(origin_path, origin_sheet, 8,8)
    #print(origin_list[1])
    video_oids={}
    for i in range(1,sheet1.nrows):
        video_oids[origin_list[i]]=[]
    return video_oids



def get_clean_data():
    origin_path = path.join(STATICFILES_DIRS[0],'origin_comment.xls')
    x1 = xlrd.open_workbook(origin_path)
    origin_sheet = 'origin'
    sheet1 = x1.sheet_by_name(origin_sheet)
    origin_list=excel(origin_path,origin_sheet,0,int(sheet1.ncols))
    #print(origin_list[1])
    #print(origin_list[1][4])
    comment_classify = get_video_data()
    for i in range(1,sheet1.nrows):
        oid = origin_list[i][4]
        print(oid)
        if oid not in comment_classify.keys():
            comment_classify[oid]=[]
        comment_classify[oid].append(origin_list[i])
        #print(comment_classify[oid][-1][4])
        #print(comment_classify)
    # for k in comment_classify.keys():
    #     #     print('oid='+k+'content')
    #     #     print(comment_classify[k])
    return comment_classify
get_clean_data()




