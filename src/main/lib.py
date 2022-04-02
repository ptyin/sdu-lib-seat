import logging
import time
from typing import Tuple
import datetime
import re

from core.auth import Auth
from core.spider import Spider
from core.worker import Worker
from core import pattern


def wait_until(days: int, delay: str):
    delay: datetime.datetime = datetime.datetime.strptime(delay, '%H:%M:%S')
    tomorrow = datetime.datetime.replace(datetime.datetime.today() + datetime.timedelta(days=days),
                                         hour=delay.hour, minute=delay.minute, second=delay.second)
    delta = tomorrow - datetime.datetime.now()
    time.sleep(delta.seconds)


def prepare(userid, passwd, query_area: str, date, retry, start_time, end_time) -> Tuple[Auth, Spider]:
    auth, spider = None, None
    try:
        # Get authorized.
        auth = Auth(userid, passwd, retry)
        # Spider library, area and seat info.
        l = query_area.index("-")
        r = query_area.rindex("-")
        area_list = [query_area[:l], query_area[l + 1:r], query_area[r + 1:]]
        spider = Spider(area_list, date, retry, start_time, end_time)
        # Start two threads concurrently.
        auth.start(), spider.start()
        auth.join(), spider.join()
    except RuntimeError as rt:
        logging.error(rt)

    return auth, spider


def book(auth: Auth, spider: Spider, preferred_seats) -> bool:
    try:
        worker = Worker(spider.date, auth.session.cookies,
                        preferred_seats,
                        spider.seats, spider.segment)
        success, seat = worker.book()
    except (TypeError, Exception) as e:
        logging.error(e)
        success = False
    return success
