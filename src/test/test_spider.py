import logging
import datetime
from unittest import TestCase
from core.spider import Spider


class TestSpider(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.spider = Spider(['青岛校区图书馆', '七楼', '青岛馆七楼北阅览区'], date=datetime.datetime.today())
        logging.basicConfig(format='%(asctime)s  %(filename)s : %(message)s', level=logging.DEBUG)

    def test_get_lib(self):
        self.spider.get_lib()
        self.assertIn('中心校区图书馆', self.spider.areas)
        self.assertIn('蒋震图书馆', self.spider.areas)
        self.assertIn('软件园校区图书馆', self.spider.areas)
        self.assertIn('青岛校区图书馆', self.spider.areas)

    def test_get_area(self):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.spider.get_area(1, date)  # 蒋震
        self.assertIn('蒋震6楼', self.spider.areas)

    def test_gather_info(self):
        self.spider.gather_info()
        self.assertIsNotNone(self.spider.final_area)
        self.assertIsNotNone(self.spider.segment)
