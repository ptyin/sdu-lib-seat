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
    tomorrow = datetime.datetime.replace(datetime.datetime.today() + datetime.timedelta(days=1),  # 明天
                                         hour=delay.hour, minute=delay.minute, second=delay.second)
    delta = tomorrow - datetime.datetime.now()
    time.sleep(delta.seconds)


def prepare(userid, passwd, query_area: str, date, retry) -> Tuple[Auth, Spider]:
    auth, spider = None, None
    try:
        # Get authorized.
        auth = Auth(userid, passwd, retry)
        # Spider library, area and seat info.
        spider = Spider(query_area.split('-'), date, retry)
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
