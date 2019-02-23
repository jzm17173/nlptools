import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools

from bs4 import BeautifulSoup
from nlptools import ArticleCrawler


class GuangdongCrawler(ArticleCrawler):
    u"""

    在子类中定义了__init__()方法，父类的__init__()方法会被覆盖
    因此，在子类中，父类的初始化方法并不会被自动调用，我们必须显式调用它

    在子类中没有定义__init__()方法
    """
    def parse_list_html(self, html_doc):
        data = []
        soup = BeautifulSoup(html_doc, 'html.parser')
        h1_elems = soup.find_all('h1')
        for h1_elem in h1_elems:
            a_elem = h1_elem.find('a')
            if a_elem:
                link = a_elem['href']
                title = a_elem.text
                real_link = 'http://www.gdlr.gov.cn/search/' + link

                data.append({
                    "title": title,
                    "content": "",
                    "link": real_link
                })

        return data

    def parse_content_html(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')

        self.clear_tag(soup, ["script", "style"])

        container_elem = soup.find(id='textbody')

        if container_elem is None:
            return ''
        else:
            return container_elem.text

    def get_page_links(self, pages):
        links = []

        for page in pages:
            link = 'http://www.gdlr.gov.cn/search/s?q=1&qt=%E6%88%BF%E5%9C%B0%E4%BA%A7&pageSize=10&database=all&page=' + str(page) + '#gettop'
            links.append(link)

        return links

crawler1 = GuangdongCrawler(timeout=10, data_dir='guangdong')
crawler1.get_list_data(1, 2)
crawler1.get_content_data(1, 2)
