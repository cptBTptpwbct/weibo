from db.redis_db import Tasks
from threading import Thread
from config import get_max_thread
from logger import thread
from db.basic import eng
from sqlalchemy.orm import (sessionmaker,scoped_session)
import json
import time
import tasks
def worker(i):
    Session = scoped_session(sessionmaker(bind=eng))
    db_session = Session()
    while 1:
        redisResult = Tasks.pop_out_queue()
        if redisResult is None:
            continue
        thread.info("Thread={i} 取到空".format(i=i))
        task = json.loads(redisResult[1])
        if(task['type']==1):
            tasks.comment.crawl_comment_by_page(task['id'], task['index'], seeion=db_session)
        if(task['type']==2):
            tasks.repost.crawl_repost_page(task['id'], task['index'], seeion=db_session)
        thread.info("Thread={i} 执行 = {type} 类型任务 id={id} index= {index}".
                    format(i=i, type=task['type'], id=task['id'], index=task['index']))
        time.sleep(2)
if __name__ == '__main__':
    for i in range(0,get_max_thread()):
        Thread(target=worker, args=(i,)).start()