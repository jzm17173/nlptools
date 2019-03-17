import sys
sys.path.insert(0, "../")

import nlptools


def demo_search():
    nlptools.search(
        "files/search_sentences.txt",
        "files/search_contexts.txt",
        max_size=5)


demo_search()
