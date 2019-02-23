import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools

"""
nlptools.search(
    "search_data.txt",
    "search_keywords.txt",
    "search_syn.txt")
"""


data = nlptools.read_file("files/seg.txt").split("\n")
keywords = nlptools.read_file("files/seg__2.txt").split("\n")
keywords = [item.split()[0] for item in keywords if item.strip() != ""]
syn_dict = {}

nlptools.search(
    data,
    keywords,
    syn_dict,
    "files/seg__2_result.txt")
