import time

from .workers import app
from page_parse import comment
from config import conf
from page_get import get_page
from db.dao import (
    WbDataOper, CommentOper, SeedidsOper)
from db.basic import db_session
from logger import crawler
from celery.exceptions import SoftTimeLimitExceeded
from db.redis_db import Tasks

BASE_URL = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}'


def crawl_comment_by_page(mid, page_num, seeion):
    try:
        cur_url = BASE_URL.format(mid, page_num)
        html = get_page(cur_url, auth_level=1, is_ajax=True)
        comment_datas , seed_ids= comment.get_comment_list(html, mid)
    except SoftTimeLimitExceeded:
        crawler.error(
            "comment SoftTimeLimitExceeded    mid={mid} page_num={page_num}".
            format(mid=mid, page_num=page_num))
        crawl_comment_by_page(mid, page_num)
    CommentOper.add_all(comment_datas, seeion)
    SeedidsOper.insert_seeds(seed_ids, seeion)
    if page_num == 1:
        WbDataOper.set_weibo_comment_crawled(mid, seeion)
    return html, comment_datas


def crawl_comment_page(mid):
    limit = conf.get_max_comment_page() + 1
    first_page = crawl_comment_by_page(mid, 1,db_session)[0]
    total_page = comment.get_total_page(first_page)

    if total_page < limit:
        limit = total_page + 1

    for page_num in range(2, limit):
        #app.send_task('tasks.comment.crawl_comment_by_page', args=(mid, page_num), queue='comment_page_crawler',
                     # routing_key='comment_page_info')
        Tasks.push_task(1, mid, page_num)
        #crawl_comment_by_page(mid, page_num)



@app.task(ignore_result=True)
def execute_comment_task():
    weibo_datas = WbDataOper.get_weibo_comment_not_crawled(db_session)
    crawl_comment_page(4253637545362266)
