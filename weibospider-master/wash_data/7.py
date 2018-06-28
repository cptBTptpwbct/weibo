from jieba.analyse import tfidf
from aip import  AipNlp
from db.dao import CommentOper
from config import get_baidu_args
import  xlwt
import datetime
import time
if __name__ == '__main__':
    infos = CommentOper.get_all_comment_by_weibo_id(4244968959004196)
    args  = get_baidu_args()
    API_ID = args['app_id']
    API_KEY = args['api_key']
    SECRET_KEY = args['secret_key']
    client = AipNlp(str(API_ID), API_KEY, SECRET_KEY)

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok = True)
    lists = ['positive_prob', 'confidence', 'negative_prob']
    i = 0
    for list in lists:
        sheet.write(0, i, list)
        i += 1
    infos = CommentOper.get_all_comment_by_weibo_id(4244968959004196)
    i = 1
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    for info in infos:
        print(i)
        try:
            result = client.sentimentClassify(info.comment_cont)

            if result:
                item = result['items']
                print(item)
                sheet.write(i, 0, item[0]['positive_prob'])
                sheet.write(i, 1, item[0]['confidence'])
                sheet.write(i, 2, item[0]['negative_prob'])
                i += 1
            if i%5==0 :
                time.sleep(1)
        except:
            print(info.comment_cont)
book.save(r'file-' + nowTime + '.xls')