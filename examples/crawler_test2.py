import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools

import time
import os

from bs4 import BeautifulSoup

from crawler import ArticleCrawler


class XuangubaCrawler(ArticleCrawler):
    def __init__(self, root_dir='data'):
        super().__init__(root_dir=root_dir)
        self.ids = []

    def get_link(self, tailmark, msgIdMark):
        search = '?subjids=9,10,723,35,469&limit=30&tailmark=%s&msgIdMark=%s' % (tailmark, msgIdMark)
        link = 'https://api.xuangubao.cn/api/pc/msgs%s' % search
        return link

    def get_data_by_json(self, tailmark, msgIdMark):
        link = self.get_link(tailmark, msgIdMark)
        print(link)
        result = self.request_json(link)
        if result:
            file = 'xuangubao/%s_%s.json' % (tailmark, msgIdMark)
            self.write_json(file, result)
            time.sleep(self.timesleep)
            if result['TailMark'] and result['TailMsgId']:
                self.get_data_by_json(result['TailMark'], result['TailMsgId'])

    # 可能多个表多个sql
    def write_sql(self):
        paths = self.get_all_files()
        sql = ''
        for path in paths:
            data = self.read_json(path)

            for new_msg in data['NewMsgs']:
                id = new_msg['Id']
                title = new_msg['Title']
                content =  new_msg['Summary'].split('选股宝讯，')[-1]
                blocks = new_msg['BkjInfoArr']

                if id not in self.ids and blocks:
                    print(id)
                    self.ids.append(id)

                    block_info = []
                    for block in blocks:
                        block_info.append(block['Name'])

                    block_info_str = ','.join(block_info)

                    insert_sql = '''
                        INSERT INTO `xuangubao_news` (
                            `title`,
                            `content`,
                            `block`)
                        VALUES (
                            \'%s\',
                            \'%s\',
                            \'%s\');\n
                        ''' % (
                            title,
                            content,
                            block_info_str)
                    sql = sql + insert_sql

        self.write_file('%s.sql' % self.root_dir, sql)

crawler1 = XuangubaCrawler(root_dir='xuangubao')
#crawler1.get_data_by_json('1524186713', '281081')
#crawler1.write_sql()
