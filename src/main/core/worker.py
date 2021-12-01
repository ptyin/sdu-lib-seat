import itertools
import logging
from typing import Tuple
import urllib.parse

import requests


# noinspection HttpUrlsUsage
class Worker:
    def __init__(self, date, cookies: requests.sessions.RequestsCookieJar,
                 preferred_seats, seat_info, segment):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36",
            "Origin": "http://seat.lib.sdu.edu.cn",
            'Referer': 'http://seat.lib.sdu.edu.cn/',
            "Host": "seat.lib.sdu.edu.cn",
        }

        self.date = date
        self.cookies = cookies
        self.cookies['redirect_url'] = "/home/web/seat2/area/3/day/" + self.date

        self.preferred_seats = preferred_seats
        self.seat_info = seat_info
        self.segment = segment

        self.__logger = logging.getLogger()

    def __book(self, seat_id) -> bool:
        data = {
            "access_token": self.cookies["access_token"],
            "userid": self.cookies["userid"],
            "segment": self.segment,
            "type": "1",
            "operateChannel": "2"
        }
        res = requests.post("http://seat.lib.sdu.edu.cn/api.php/spaces/{}/book".format(seat_id),
                            headers=self.headers, cookies=self.cookies, data=data)
        self.__logger.info('Book response {}'.format(res.json()['msg']))
        return res.json()['status'] == 1

    def book(self) -> Tuple[bool, str]:
        # 先挑选参数给出的座位，如果没有再遍历所有空闲的
        for seat in itertools.chain(self.preferred_seats, self.seat_info):
            if seat in self.seat_info:
                if self.seat_info[seat]['status'] == 1 and self.__book(self.seat_info[seat]['id']):  # 空闲
                    # success
                    self.__logger.info('Seat {} has been occupied by {}-{} on date {}'.
                                       format(seat, self.cookies['userid'],
                                              urllib.parse.unquote(self.cookies['user_name']), self.date))
                    return True, seat
            else:
                self.__logger.warning('参数给出的座位名字【{}】对应有误'.format(seat))
        return False, 'No seat has been booked.'
