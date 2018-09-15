# coding: utf-8
import datetime
import re
import os
from pathlib import Path
from urllib import request
import time
from multiprocessing.pool import ThreadPool
from random import randint


MOMENTUM_URL = 'https://d3cbihxaqsuq0s.cloudfront.net/'
LOCAL_DIRECTORY = 'E:\\desktop_picture\\momentums'
SLEEP_TIME = 2
my_header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/67.0.3396.99 Safari/537.36'


def spider():
    req = request.Request(
        MOMENTUM_URL,
        data=None,
        headers={
            'User-Agent': my_header
        }
    )
    context = request.urlopen(req).read().decode('utf-8')
    return context


def parse_context(c):
    if isinstance(c, bytes):
        c = str(c)
    image_keys = re.findall(r'<Key>(.+?)</Key>', c)
    return [
        MOMENTUM_URL + key for key in image_keys
    ]


def main():
    context = spider()
    images = parse_context(context)[1:]

    pool = ThreadPool(1)
    pool.map(save_img, images)
    pool.close()
    pool.join()


def save_img(img_url, file_path=LOCAL_DIRECTORY):
    opener = request.build_opener()
    opener.addheaders = [('User-agent', my_header)]
    request.install_opener(opener)
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_suffix = os.path.basename(img_url)
        filename = '{}{}{}'.format(file_path, os.sep, file_suffix)
        my_file = Path(filename)
        if my_file.exists():
            print(filename + ' already downloaded')
            return
        request.urlretrieve(img_url, filename=filename)
        now = datetime.datetime.now()
        print('{}: {}'.format(now, filename))
        sleep_time = randint(10, 100)/10
        time.sleep(sleep_time)
        print('sleep_time: ' + str(sleep_time))
    except IOError as e:
        print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    s = time.time()
    main()
    print('finished.')
    print('Total time: {}'.format(time.time() - s))
