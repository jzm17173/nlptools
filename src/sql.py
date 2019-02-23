# -*- coding:utf-8 -*-

import os


def read_file(file, encoding="utf-8"):
    if os.path.exists(file):
        with open(file, mode="r", encoding=encoding) as f:
            return f.read()
    else:
        return None


def write_file(file, text, encoding="utf-8"):
    with open(file, mode="w", encoding=encoding) as f:
        f.write(text)


def make_stopwords(file, word_type):
    data = read_file("{}.txt".format(file)).split("\n")
    data = [item.strip() for item in data if item.strip() != ""]

    sql = ""
    for item in data:
        insert_sql = """
            INSERT INTO `dict_clustering_stopwords` (
                `word`,
                `word_type`)
            VALUES (
                \'%s\',
                \'%s\');\n
            """ % (
                item,
                word_type)
        sql = sql + insert_sql

    write_file("{}.sql".format(file), sql)


def make_check(file):
    data = read_file("{}.txt".format(file)).split("\n")
    data = [
        [item.split()[0], ",".join(item.split()[1:])]
        for item in data
        if item.strip() != ""]

    sql = ""
    for item in data:
        insert_sql = """
            INSERT INTO `dict_clustering_check` (
                `correct_word`,
                `incorrect_word`)
            VALUES (
                \'%s\',
                \'%s\');\n
            """ % (
                item[0],
                item[1])
        sql = sql + insert_sql

    write_file("{}.sql".format(file), sql)


def make_syn(file, word_type):
    data = read_file("{}.txt".format(file)).split("\n")
    data = [
        [item.split()[0], ",".join(item.split()[1:])]
        for item in data
        if item.strip() != ""]

    sql = ""
    for item in data:
        insert_sql = """
            INSERT INTO `dict_clustering_syn` (
                `word`,
                `word_source`,
                `word_type`)
            VALUES (
                \'%s\',
                \'%s\',
                \'%s\');\n
            """ % (
                item[0],
                item[1],
                word_type)
        sql = sql + insert_sql

    write_file("{}.sql".format(file), sql)


if __name__ == "__main__":
    make_stopwords("../stopwords", "tokens")
    make_stopwords("../stopwords_raw", "raw")
    make_stopwords("../stopwords_time", "time")

    make_check("../check_raw")

    make_syn("../syn_raw", "raw")
    make_syn("../syn_tokens", "tokens")
