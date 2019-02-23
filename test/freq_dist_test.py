import sys
# sys.path.append("../")
sys.path.insert(0, "../")
import nlptools


dist = nlptools.FreqDist("abcdeabcdabcaba")
print(dist)  # FreqDist({'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1})

print(dist.keys())  # dict_keys(['a', 'b', 'c', 'd', 'e'])

print(dist.items())  # dict_items([('a', 5), ('b', 4), ('c', 3), ('d', 2), ('e', 1)])

print(dist["a"])  # 5

print(dist.most_common(3))  # [('a', 5), ('b', 4), ('c', 3)]
print(dist.most_common())  # [('a', 5), ('b', 4), ('c', 3), ('d', 2), ('e', 1)]

print(dist.values())  # dict_values([5, 4, 3, 2, 1])

print(dist.N())  # 15

print(dist.B())  # 5

print(dist.freq("a"))  # 0.3333333333333333

print(dist.hapaxes())  # ['e']

print(dist.filter("greater_than_or_equal[2]"))  # [('a', 5), ('b', 4), ('c', 3), ('d', 2)]
print(dist.filter("less_than_or_equal[2]"))  # [('d', 2), ('e', 1)]
print(dist.filter("equal[2]"))  # [('d', 2)]


print(list(dist.keys()))
print("".join(dist.keys()))