# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from bs4 import BeautifulSoup

from nlptools import serialize
from nlptools import ArticleCrawler


class GuangdongCrawler(ArticleCrawler):
    def parse_list(self, result):
        data = []
        soup = BeautifulSoup(result, "html.parser")
        h1_elems = soup.find_all("h1")
        for h1_elem in h1_elems:
            a_elem = h1_elem.find("a")
            if a_elem:
                link = a_elem["href"]
                title = a_elem.text
                real_link = "http://www.gdlr.gov.cn/search/" + link

                data.append({
                    "title": title,
                    "content": "",
                    "link": real_link
                })

        return data

    def parse_content(self, result):
        soup = BeautifulSoup(result, "html.parser")

        self.clear_tag(soup, ["script", "style"])

        container_elem = soup.find(id="textbody")

        if container_elem is None:
            return ""
        else:
            return container_elem.text

    def get_list_links(self, pages):
        links = []

        for page in pages:
            search = serialize({
                "q": 1,
                "pageSize": 10,
                "database": "all",
                "page": page
            })

            link = "http://nr.gd.gov.cn/search/s?{}&qt=%E6%88%BF%E5%9C%B0%E4%BA%A7#gettop".format(search)
            links.append(link)

        return links


crawler1 = GuangdongCrawler(timeout=10, data_path="guangdong")
crawler1.get_list_data(1, 2)
crawler1.get_content_data(1, 2)
