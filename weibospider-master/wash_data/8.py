from jieba.analyse import tfidf
import  xlwt
from db.dao import CommentOper
from jieba import analyse
from db.dao import SeedidsOper
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
        SeedidsOper.set_seed_id(info.user_id)

