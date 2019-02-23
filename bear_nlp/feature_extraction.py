# -*- encoding=utf-8 -*-

import numpy as np

from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from .analysis_freq_dist import FreqDist


tokenizer = lambda doc: doc.split()


def extract_feature(corpus, feature_type="one"):
    u"""特征提取

    Args:
        feature_type: 'one', 'tf', 'tf-idf'
    """
    vectorizer = CountVectorizer(tokenizer=tokenizer)
    X = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()

    if feature_type == "one":
        X = csr_matrix(
            (np.ones(len(X.data), dtype=np.int), X.indices, X.indptr),
            shape=X.shape)
    elif feature_type == "tf-idf":
        transformer = TfidfTransformer()
        X = transformer.fit_transform(X)

    return (X.toarray(), feature_names)


def apply_feature(corpus, feature_names, feature_type="one"):
    u"""特征应用

    Args:
        feature_type: 'one', 'tf'
    """
    words = corpus.split()
    if feature_type == "one":
        words = list(set(words))
    dist = FreqDist(words)

    return [dist[x] for x in feature_names]
