# -*- coding:utf-8 -*-

import os
import time
from pathlib import Path

from .fs import read_json
from .fs import write_json
from .fs import mkdir
from .http import fetch


class Crawler(object):
    def __init__(
            self,
            timeout=3,
            timesleep=3,
            data_path="data"):
        self.timeout = timeout
        self.timesleep = timesleep
        self.data_path = data_path

        self.mk_data_dir()

    def mk_data_dir(self):
        u"""创建数据目录"""
        mkdir(self.data_path)

    def sleep(self):
        u"""暂停片刻"""
        time.sleep(self.timesleep)

    @staticmethod
    def clear_tag(root_elem, tag_name):
        u"""清除标签"""
        if not isinstance(tag_name, list):
            tag_name = [tag_name]

        for item in tag_name:
            tag_elems = root_elem.find_all(item)
            for tag_elem in tag_elems:
                tag_elem.clear()


class ArticleCrawler(Crawler):
    def __init__(
            self,
            timeout=3,
            timesleep=3,
            data_path="data",
            list_method="GET",
            list_headers={},
            list_data_type=None,
            content_method="GET",
            content_headers={},
            content_data_type=None):
        super().__init__(
            timeout=timeout,
            timesleep=timesleep,
            data_path=data_path)

        self.list_method = list_method
        self.list_headers = list_headers
        self.list_data_type = list_data_type

        self.content_method = content_method
        self.content_headers = content_headers
        self.content_data_type = content_data_type

    @staticmethod
    def get_list_pages(min_page, max_page):
        u"""获取列表页的分页"""
        return range(min_page, max_page + 1)

    def get_list_links(self, pages):
        u"""获取列表页的地址"""
        raise NotImplementedError()

    def get_data_files(self, pages=None):
        u"""获取数据目录的文件"""
        files = []

        if pages is None:
            pages = os.listdir(self.data_path)

        for page in pages:
            page = page.split(".")[0]
            file = "{}/{}.json".format(self.data_path, page)
            if Path(file).is_file():
                files.append(file)

        return files

    def parse_list(self, result):
        u"""解析列表"""
        raise NotImplementedError()

    def parse_content(self, result):
        u"""解析内容"""
        raise NotImplementedError()

    def get_list_data(self, min_page, max_page):
        u"""获取列表页的数据"""
        pages = self.get_list_pages(min_page, max_page)
        links = self.get_list_links(pages)

        for i in range(len(pages)):
            page = pages[i]
            link = links[i]

            print("requesting list {} {}".format(i, link))

            result = fetch(
                link,
                headers=self.list_headers,
                timeout=self.timeout,
                method=self.list_method,
                data_type=self.list_data_type)

            if result:
                write_json(
                    "{}/{}.json".format(self.data_path, page),
                    {"data": self.parse_list(result)})

            self.sleep()

    def get_content_data(self, min_page, max_page):
        u"""获取内容页的数据"""
        pages = self.get_list_pages(min_page, max_page)
        files = self.get_data_files(pages)

        for i in range(len(files)):
            file = files[i]
            data = read_json(file)

            for j in range(len(data["data"])):
                item = data["data"][j]
                link = item["link"]

                if item["content"] == "":
                    print("requesting content {}-{} {}".format(i, j, link))

                    result = fetch(
                        link,
                        headers=self.content_headers,
                        timeout=self.timeout,
                        method=self.content_method,
                        data_type=self.content_data_type)

                    if result:
                        item["content"] = self.parse_content(result)
                        write_json(file, data)

                    self.sleep()
