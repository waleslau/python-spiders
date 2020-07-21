#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   nihaowua_spider.py
@Time    :   2020/07/21 19:56:26
@Author  :   waleslau 
@Version :   1.0
@Contact :   waleslau@foxmail.com
"""

import logging
import coloredlogs
import requests
import re
import pymongo
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
from conf import *

FIELD_STYLES = dict(
    asctime=dict(color="green"),
    hostname=dict(color="magenta"),
    levelname=dict(color="green"),
    filename=dict(color="magenta"),
    name=dict(color="blue"),
    threadName=dict(color="green"),
)

LEVEL_STYLES = dict(
    debug=dict(color="green"),
    info=dict(color="cyan"),
    warning=dict(color="yellow"),
    error=dict(color="red"),
    critical=dict(color="red"),
)

logger = logging.getLogger("tos")
coloredlogs.install(
    level="INFO",
    fmt="[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s",
    level_styles=LEVEL_STYLES,
    field_styles=FIELD_STYLES,
)
"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
"""


def get_random_ua():
    ua = UserAgent()
    return ua.random


headers = {"User-Agent": get_random_ua()}


def get_html(url):
    # logging.info('scraping %s...', url)
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        # response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        logging.error("get invalid status code %s while scraping %s",
                      response.status_code, url)
    except requests.RequestException:
        logging.error("error occurred while scraping %s", url, exc_info=True)


def parse(html):
    doc = pq(html)
    post = doc("section div").text()
    return {"post": post}


client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]


def save_data_to_mongo(data):
    if TYPE == 0:
        collection = db[MONGO_COLLECTION_NAME_WU]
    if TYPE == 1:
        collection = db[MONGO_COLLECTION_NAME_DU]

    collection.update_one({"post": data.get("post")}, {"$set": data},
                          upsert=True)


def main():
    global TIMES
    while TIMES > 0:
        TIMES -= 1
        if TYPE == 0:
            html = get_html("https://www.nihaowua.com")
            data = parse(html)
        if TYPE == 1:
            html = get_html("https://www.nihaowua.com/home.html")
            data = parse(html)
        logging.info("get data：\n \n \t %s\n", data["post"])
        if SAVE_TO_MONGO:
            logging.info("saving data to mongodb")
            save_data_to_mongo(data)
            logging.info("data saved successfully")
        else:
            pass


if __name__ == "__main__":
    main()
