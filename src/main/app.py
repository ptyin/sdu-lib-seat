import itertools
import sys
from argparse import ArgumentParser

from lib import *

if __name__ == '__main__':
    # Configure parameters
    parser = ArgumentParser()
    parser.add_argument('--userid', type=str, help='山东大学学号')
    parser.add_argument('--passwd', type=str, help='山东大学统一身份认证密码')
    parser.add_argument('--area', type=str, help='图书馆-楼层-楼层内区域')
    parser.add_argument('--seats', type=str, nargs='*',
                        help='想要约的座位，按照倾向程度排序，如果列出的座位均已无法预约，'
                             '或没提供该参数，则在所有仍没被约用的座位进行约座')
    parser.add_argument('--time', type=str, default='06:02:00',
                        help='发起约座的时间，默认是第二天06:02分开始抢后天的位置')
    parser.add_argument('--retry', type=int, default=10, help='重试次数')
    parser.add_argument('--delta', type=int, default=0, help='运行天数差，即0代表今天运行，1代表明天运行')
    paras = parser.parse_args()

    # Configure logging settings.
    logging.basicConfig(format='%(asctime)s  %(filename)s : %(message)s',
                        level=logging.INFO, stream=sys.stdout)

    date = datetime.datetime.today() + datetime.timedelta(days=paras.delta+1)  # reservation date
    auth, spider = prepare(paras.userid, paras.passwd, paras.area, date, paras.retry)
    # ------All information has been gathered------

    # Wait until tomorrow XX:XX:XX, defined by paras.time, occupying...
    logging.info('----Waiting until {}...----'.format(paras.time))
    wait_until(days=paras.delta, delay=paras.time)  # 1 represents tomorrow

    # If either auth or spider failed today, try them tomorrow.
    if not (auth is not None and spider is not None and auth.success() and spider.success()):
        auth, spider = prepare(paras.userid, paras.passwd, paras.area, date, paras.retry)
    # Ready to work!
    count = 1
    while count <= paras.retry and not book(auth, spider, preferred_seats=paras.seats):
        logging.warning('Try {}/{} failed, do not worry. Retrying in 30 seconds...'.format(count, paras.retry))
        count += 1
        time.sleep(30)
        auth, spider = prepare(paras.userid, paras.passwd, paras.area, date, paras.retry)

    logging.info('----{}, bye.----'.format("It's working" if count <= paras.retry else 'Failed'))
