import logging
import time
from typing import Tuple
import datetime

from core.auth import Auth
from core.spider import Spider
from core.worker import Worker


def wait_to_tomorrow(delay: str):
    """Wait 'till tomorrow"""
    delay: datetime.datetime = datetime.datetime.strptime(delay, '%H:%M:%S')
    tomorrow = datetime.datetime.replace(datetime.datetime.today() + datetime.timedelta(days=0),  # 明天 TODO
                                         hour=delay.hour, minute=delay.minute, second=delay.second)
    delta = tomorrow - datetime.datetime.now()
    time.sleep(delta.seconds)


def prepare(userid, passwd, query_area: str, date) -> Tuple[Auth, Spider]:
    # Get authorized.
    auth = Auth(userid, passwd)
    # Spider library, area and seat info.
    spider = Spider(query_area=query_area.split('-'), date=date)

    # Start two threads concurrently.
    auth.start(), spider.start()
    auth.join(), spider.join()
    return auth, spider


def book(auth: Auth, spider: Spider, preferred_seats) -> bool:

    worker = Worker(spider.date, auth.session.cookies,
                    preferred_seats,
                    spider.seats, spider.segment)
    success, seat = worker.book()
    return success
