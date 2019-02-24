import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools


data = nlptools.read_file("files/seg.txt").split("\n")
text = ""
for item in data:
    if item.strip() != "":
        print(item)
        text += "{}\n".format(" ".join(nlptools.seg(item.strip())))

nlptools.write_file("files/seg_.txt", text)
