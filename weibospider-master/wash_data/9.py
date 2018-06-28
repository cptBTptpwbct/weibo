from jieba.analyse import tfidf
import  xlwt
from db.dao import UserOper
from jieba import analyse
import datetime
import csv
if __name__ == '__main__':
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok = True)
    lists = ['gender', 'birthday', 'location', 'verify_type', ]
    i = 0
    for list in lists:
        sheet.write(0, i, list)
        i += 1
    infos = UserOper.get_all()
    i = 1
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    for info in infos:
        sheet.write(i, 0, info.gender)
        sheet.write(i, 1, info.birthday)
        sheet.write(i, 2, info.location)
        sheet.write(i, 3, info.verify_type)
        i += 1
    book.save(r'file-' + nowTime + '.xls')
