from jieba.analyse import tfidf

from db.dao import CommentOper
from jieba import analyse

if __name__ == '__main__':
    infos = CommentOper.get_all_comment_by_weibo_id(4081978523493142)
    test=""
    for info in infos:
        test+=info.comment_cont
    keyWords = tfidf(test)
    for keyWord in keyWords:
        print(keyWord)
