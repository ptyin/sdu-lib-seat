import logging
import datetime
from unittest import TestCase
from core.spider import Spider
import re


class TestSpider(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        date = datetime.datetime.today()+datetime.timedelta(0)
        cls.spider = Spider(re.split(r'-(?![^()]*\))', "威海馆-图东环(3-4)-三楼阅览室"), date=date, retry=1,
                            start_time="15:00", end_time="22:30")
        logging.basicConfig(format='%(asctime)s  %(filename)s : %(message)s', level=logging.DEBUG)

    def test_get_lib(self):
        self.spider.get_lib()
        self.assertIn('中心馆', self.spider.areas)
        self.assertIn('蒋震馆', self.spider.areas)
        self.assertIn('软件园馆', self.spider.areas)
        self.assertIn('青岛馆', self.spider.areas)

    def test_get_area(self):
        date = (datetime.datetime.today()).strftime('%Y-%m-%d')
        self.spider.get_area(1, date)  # 蒋震
        self.assertIn('蒋震6楼', self.spider.areas)

    def test_gather_info(self):
        self.spider.gather_info()
        self.assertIsNotNone(self.spider.final_area)
        self.assertIsNotNone(self.spider.segment)

    def test_run(self):
        self.spider.start()
        self.spider.join()
        self.assertTrue(self.spider.success())
