# -*- coding:utf-8 -*-

from collections import Counter
u"""Counter

class Counter(builtins.dict)

c = Counter('abcdeabcdabcaba')
c.most_common(3)

Methods inherited from builtins.dict
    items
    keys
"""


rule_dict = {
    "greater_than_or_equal": lambda x, y: x >= y,
    "greater_than": lambda x, y: x > y,
    "less_than_or_equal": lambda x, y: x <= y,
    "less_than": lambda x, y: x < y,
    "equal": lambda x, y: x == y
}


class FreqDist(Counter):
    u"""词频分布"""

    def __init__(self, samples):
        Counter.__init__(self, samples)

        self._N = None

    def N(self):
        if self._N is None:
            self._N = sum(self.values())

        return self._N

    def B(self):
        return len(self)

    def freq(self, sample):
        n = self.N()
        if n == 0:
            return 0
        return self[sample] / n

    def hapaxes(self):
        return [item for item in self if self[item] == 1]

    def filter(self, rule="greater_than_or_equal[1]"):
        rule_types = [
            "greater_than_or_equal",
            "greater_than",
            "less_than_or_equal",
            "less_than",
            "equal"
        ]

        rule_type = rule_types[0]
        rule_value = 1

        if rule.find("[") != -1:
            rule_value = rule.split("[")[1].split("]")[0]
            if rule_value.isdigit():
                rule_value = int(rule_value)

        for item in rule_types:
            if rule.find(item) != -1:
                rule_type = item
                break

        return [
            item
            for item in self.most_common()
            if rule_dict[rule_type](item[1], rule_value)]
