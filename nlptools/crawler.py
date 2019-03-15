# -*- coding:utf-8 -*-

import os
import time

from .fs import read_json
from .fs import write_json
from .fs import mkdir
from .http import fetch


DEFAULT_POST_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=utf-8"

clear_text_rules = [
    (" ", "&nbsp;")
]


class Crawler(object):
    def __init__(
            self,
            timeout=3,
            timesleep=3,
            data_dir="data"):

        self.timeout = timeout
        self.timesleep = timesleep
        self.data_dir = data_dir

        mkdir(data_dir)

    @staticmethod
    def clear_text(text):
        u"""清除文本"""
        for item in clear_text_rules:
            text = text.replace(item[1], item[0])

        return text

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
            data_dir="data",

            list_method="GET",
            list_req_type=None,
            list_res_type=None,
            list_content_type=DEFAULT_POST_CONTENT_TYPE,
            list_user_agent=None,
            list_referer=None,

            content_method="GET",
            content_req_type=None,
            content_res_type=None,
            content_content_type=DEFAULT_POST_CONTENT_TYPE,
            content_user_agent=None,
            content_referer=None):
        super().__init__(
            timeout=timeout,
            timesleep=timesleep,
            data_dir=data_dir)

        self.list_method = list_method
        self.list_req_type = list_req_type
        self.list_res_type = list_res_type
        self.list_content_type = list_content_type
        self.list_user_agent = list_user_agent
        self.list_referer = list_referer

        self.content_method = content_method
        self.content_req_type = content_req_type
        self.content_res_type = content_res_type
        self.content_content_type = content_content_type
        self.content_user_agent = content_user_agent
        self.content_referer = content_referer

    @staticmethod
    def get_page_indexes(min_page, max_page):
        return range(min_page, max_page + 1)

    def get_page_links(self, pages):
        raise NotImplementedError()

    def get_page_files(self, pages):
        files = []
        for page in pages:
            file = "%s/%d.json" % (self.data_dir, page)
            if os.path.exists(file):
                files.append(file)
        return files

    def parse_list_html(self, html_doc):
        raise NotImplementedError()

    def parse_content_html(self, html_doc):
        raise NotImplementedError()

    def parse_list_json(self, json_data):
        raise NotImplementedError()

    def parse_content_json(self, json_data):
        raise NotImplementedError()

    def request_list_data(self, link):
        result = fetch(
            link,
            method=self.list_method,
            req_type=self.list_req_type,
            res_type=self.list_res_type,
            timeout=self.timeout,
            content_type=self.list_content_type,
            user_agent=self.list_user_agent,
            referer=self.list_referer)

        if result is None:
            return []
        else:
            if self.list_res_type == "json":
                return self.parse_list_json(result)
            else:
                result = self.clear_text(result)
                return self.parse_list_html(result)

    def request_content_data(self, link):
        result = fetch(
            link,
            method=self.content_method,
            req_type=self.content_req_type,
            res_type=self.content_res_type,
            timeout=self.timeout,
            content_type=self.content_content_type,
            user_agent=self.content_user_agent,
            referer=self.content_referer)

        if result is None:
            return ""
        else:
            if self.content_res_type == "json":
                return self.parse_content_json(result)
            else:
                result = self.clear_text(result)
                return self.parse_content_html(result)

    def get_list_data(self, min_page, max_page):
        pages = self.get_page_indexes(min_page, max_page)
        links = self.get_page_links(pages)

        for i, page in enumerate(pages):
            link = links[i]
            print(link)

            result = self.request_list_data(link)

            if result:
                write_json(
                    "%s/%d.json" % (self.data_dir, page),
                    {"data": result})

            time.sleep(self.timesleep)

    def get_content_data(self, min_page, max_page):
        pages = self.get_page_indexes(min_page, max_page)
        files = self.get_page_files(pages)

        for file in files:
            data = read_json(file)
            for item in data["data"]:
                link = item["link"]
                if item["content"] == "":
                    print(link)
                    content = self.request_content_data(link)
                    item["content"] = content
                    write_json(file, data)

                    time.sleep(self.timesleep)
