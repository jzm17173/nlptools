import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools


# is_int
print(nlptools.is_int("1"))

# is_float
print(nlptools.is_float("1.1"))

# is_email
print(nlptools.is_email("non@qq.com"))
