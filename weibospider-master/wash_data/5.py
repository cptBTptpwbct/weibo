from jieba.analyse import tfidf
import  xlwt
from db.dao import CommentOper
from jieba import analyse
import datetime
import csv
if __name__ == '__main__':
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok = True)
    lists = ['id', 'comment_id', 'comment_cont', 'comment_screen_name', 'weibo_id', 'user_id', 'create_time']
    i = 0
    for list in lists:
        sheet.write(0, i, list)
        i += 1
    infos = CommentOper.get_all_comment_by_weibo_id(4244968959004196)
    i = 1
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    for info in infos:
        sheet.write(i, 0, info.id)
        sheet.write(i, 1, info.comment_id)
        str = info.comment_cont.replace(' ', '')
        sheet.write(i, 2, str)
        sheet.write(i, 3, info.comment_screen_name)
        sheet.write(i, 4, info.weibo_id)
        sheet.write(i, 5, info.user_id)
        sheet.write(i, 6, info.create_time)
        i += 1
    book.save(r'file-' + nowTime + '.xls')
