# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from bs4 import BeautifulSoup

from nlptools import write_file
from nlptools import read_json
from nlptools import write_json
from nlptools import serialize
from nlptools import fetch
from nlptools import ArticleCrawler


class XuangubaCrawler(ArticleCrawler):
    def __init__(self, data_path="data"):
        super().__init__(data_path=data_path)

    def get_link(self, tailmark, msgIdMark):
        search = serialize({
            "subjids": "9,10,723,35,469",
            "limit": 30,
            "tailmark": tailmark,
            "msgIdMark": msgIdMark
        })

        link = "https://api.xuangubao.cn/api/pc/msgs?%s" % search
        return link

    def get_data(self, tailmark, msgIdMark):
        link = self.get_link(tailmark, msgIdMark)

        print("requesting {}".format(link))

        result = fetch(
            link,
            timeout=self.timeout,
            data_type="json")

        if result:
            file = "{}/{}_{}.json".format(self.data_path, tailmark, msgIdMark)
            write_json(file, result)

            self.sleep()

            #if result["TailMark"] and result["TailMsgId"]:
            #    self.get_data(result["TailMark"], result["TailMsgId"])

    def save_sql(self):
        files = self.get_data_files()
        sql = []
        ids = []
        for file in files:
            data = read_json(file)

            for new_msg in data["NewMsgs"]:
                id_ = new_msg["Id"]
                title = new_msg["Title"]
                content =  new_msg["Summary"].split("选股宝讯，")[-1]
                blocks = new_msg["BkjInfoArr"]

                if id_ not in ids and blocks:
                    ids.append(id_)

                    block_info = []
                    for block in blocks:
                        block_info.append(block["Name"])

                    insert_sql = """
                        INSERT INTO `xuangubao_news` (
                            `title`,
                            `content`,
                            `block`)
                        VALUES (
                            \'%s\',
                            \'%s\',
                            \'%s\');
                        """ % (
                            title,
                            content,
                            ",".join(block_info))

                    sql.append(insert_sql)

        write_file("%s/xuangubao.sql" % self.data_path, "\n\n".join(sql))


crawler1 = XuangubaCrawler(data_path="xuangubao")
crawler1.get_data("1524186713", "281081")
crawler1.save_sql()
