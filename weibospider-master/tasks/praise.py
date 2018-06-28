import time

from .workers import app
from page_parse import praise
from logger import crawler
from config import conf
from page_get import get_page
from db.dao import (WbDataOper, PraiseOper)
from celery.exceptions import SoftTimeLimitExceeded


BASE_URL = 'http://weibo.com/aj/v6/like/big?ajwvr=6&mid={}&page={}&__rnd={}'


@app.task(ignore_result=True)
def crawl_praise_by_page(mid, page_num):
    try:
        cur_time = int(time.time() * 1000)
        cur_url = BASE_URL.format(mid, page_num, cur_time)
        html = get_page(cur_url, auth_level=2, is_ajax=True)
        praise_datas = praise.get_praise_list(html, mid)
    except SoftTimeLimitExceeded:
        crawler.error(
            "praise SoftTimeLimitExceeded    mid={mid} page_num={page_num}".
            format(mid=mid, page_num=page_num))
        crawl_praise_by_page(mid, page_num)
    PraiseOper.add_all(praise_datas)
    if page_num == 1:
        WbDataOper.set_weibo_praise_crawled(mid)
    return html, praise_datas


@app.task(ignore_result=True)
def crawl_praise_page(mid):
    # 这里为了马上拿到返回结果，采用本地调用的方式
    first_page = crawl_praise_by_page(mid, 1)[0]
    total_page = praise.get_total_page(first_page)
    for page_num in range(2, total_page + 1):
        crawl_praise_by_page(mid, page_num)
@app.task(ignore_result=True)
def execute_praise_task():
    weibo_datas = WbDataOper.get_weibo_praise_not_crawled()
    for weibo_data in weibo_datas:
        crawl_praise_page(weibo_data.weibo_id)