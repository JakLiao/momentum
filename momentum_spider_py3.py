# coding: utf-8
import re
import os
from urllib import request
import time
from multiprocessing.pool import ThreadPool

MOMENTUM_URL = 'https://d3cbihxaqsuq0s.cloudfront.net/'
LOCAL_DIRECTORY = 'E:\\desktop_picture\\momentums'
SLEEP_TIME = 2


def spider():
    context = request.urlopen(MOMENTUM_URL).read()
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
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_suffix = os.path.basename(img_url)
        filename = '{}{}{}'.format(file_path, os.sep, file_suffix)
        request.urlretrieve(img_url, filename=filename)
        print(filename)
        time.sleep(SLEEP_TIME)
    except IOError as e:
        print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    s = time.time()
    main()
    print('finished.')
    print(time.time() - s)
