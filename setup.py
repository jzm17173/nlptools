# -*- coding: utf-8 -*-

import io
import re
from distutils.core import setup


with io.open("nlptools/__init__.py", "rt", encoding="utf8") as f:
    version = re.search("__version__ = \"(.*?)\"", f.read()).group(1)

setup(
    name="nlptools",
    version=version,
    url="https://github.com/jzm17173/nlptools",
    author="jzm17173",
    author_email="823458264@qq.com",
    description="nlp utils",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only"
    ],
    packages=["nlptools"],
    package_dir={"nlptools": "nlptools"},
    package_data={"nlptools": ["*.*"]},
    install_requires=[
        "pycrypto"
    ]
)
