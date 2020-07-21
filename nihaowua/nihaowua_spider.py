#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   nihaowua_spider.py
@Time    :   2020/07/21 19:56:26
@Author  :   waleslau 
@Version :   1.0
@Contact :   waleslau@foxmail.com
"""

import requests
import logging
import re
import pymongo
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
from conf import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def get_random_ua():
    ua = UserAgent()
    return ua.random


headers = {'User-Agent': get_random_ua()}


def get_html(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        # response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def parse(html):
    doc = pq(html)
    post_id = doc('section div').attr('id')
    post = doc('section div').text()
    return {'post_id': post_id, 'post': post}


client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]


def save_data(data):
    if TYPE == 0:
        collection = db[MONGO_COLLECTION_NAME_WU]
    else:
        collection = db[MONGO_COLLECTION_NAME_DU]

    collection.update_one({'post_id': data.get('post_id')}, {'$set': data},
                          upsert=True)


def main():
    global TIMES
    while TIMES > 0:
        TIMES -= 1
        if TYPE == 0:
            html = get_html('https://www.nihaowua.com')
            data = parse(html)
        if TYPE == 1:
            html = get_html('https://www.nihaowua.com/home.html')
            data = parse(html)
        logging.info('get data %s', data)
        logging.info('saving data to mongodb')
        save_data(data)
        logging.info('data saved successfully')


if __name__ == "__main__":
    main()
