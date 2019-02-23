import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools

def test1():
    url = "http://www.bing.com/"
    data = {
        "q": "什么是销户"
    }
    nlptools.get(url, data)


def test2():
    url = "http://192.168.73.28:8090/hsnlp-tools-server/nlp/word_segment"
    data = {
        "text": "什么是销户"
    }

    print(nlptools.post(url, data))


test1()
#test2()
