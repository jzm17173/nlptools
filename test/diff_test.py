import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools


#nlptools.contains("files/22.txt", "files/11.txt")
#nlptools.not_contains("files/22.txt", "files/11.txt")

nlptools.contains("builtin.txt", "hk_stock_name.txt")
nlptools.not_contains("hk_stock_name_contains.txt", "hk_stock_name.txt")
