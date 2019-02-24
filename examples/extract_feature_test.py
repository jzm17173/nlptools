import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools


corpus = [
    "I come to China to travel",
    "This is a car polupar in China",
    "I love tea and Apple ",
    "The work is to write some papers in science"]


# tf-idf
print(nlptools.extract_feature(corpus, feature_type="tf-idf"))

# uniq
print(nlptools.extract_feature(corpus, feature_type="uniq"))

# tf
print(nlptools.extract_feature(corpus, feature_type="tf"))


print(nlptools.apply_feature('放假 了 了', ["开学", "放假", "开会", "了"]))
print(nlptools.apply_feature(
    '放假 了 了', ["开学", "放假", "开会", "了"], feature_type="tf"))
