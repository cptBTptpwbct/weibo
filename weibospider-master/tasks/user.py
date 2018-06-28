from .workers import app
from db.dao import SeedidsOper
from page_get import (
    get_fans_or_followers_ids,
    get_profile, get_user_profile
)
from logger import crawler
from celery.exceptions import SoftTimeLimitExceeded


@app.task(ignore_result=True)
def crawl_follower_fans(uid):
    seed = SeedidsOper.get_seed_by_id(uid)
    if seed.other_crawled == 0:
        rs = get_fans_or_followers_ids(uid, 1, 1)
        rs.extend(get_fans_or_followers_ids(uid, 2, 1))
        datas = set(rs)
        # If data already exits, just skip it
        if datas:
            SeedidsOper.insert_seeds(datas)
        SeedidsOper.set_seed_other_crawled(uid)


@app.task(ignore_result=True)
def crawl_person_infos(uid):

    if not uid:
        return

    try:
        user, is_crawled = get_profile(uid)
        # If it's enterprise user, just skip it
        if user and user.verify_type == 2:
            SeedidsOper.set_seed_other_crawled(uid)
            return

        # Crawl fans and followers
        if not is_crawled:
            crawl_follower_fans(uid)
    except SoftTimeLimitExceeded:
        crawler.error("user SoftTimeLimitExceeded    uid={uid}".format(uid=uid))
        crawl_person_infos(uid)

@app.task(ignore_result=True)
def crawl_person_infos_not_in_seed_ids(uid):
    if not uid:
        return
    get_user_profile(uid)


@app.task(ignore_result=True)
def execute_user_task():
    seeds = SeedidsOper.get_seed_ids()
    if seeds:
        for seed in seeds:
            crawl_person_infos(seed.uid)