# -*- coding: utf-8 -*-
u"""
- [Python 库打包分发(setup.py 编写)简易指南](http://blog.konghy.cn/2018/04/29/setup-dot-py/)
- [classifiers](https://pypi.org/pypi?%3Aaction=list_classifiers)
- [pypi UserWarning: Unknown distribution option: 'install_requires'](https://stackoverflow.com/questions/8295644/pypi-userwarning-unknown-distribution-option-install-requires)
  > python setup.py uses distutils which doesn't support install_requires.

"""

from distutils.core import setup


setup(name='bear_nlp',
      version='0.1.0',
      description='NLP Tools',
      author='jzm17173',
      author_email='823458264@qq.com',
      url='https://github.com/jzm17173/Bear',
      license="MIT",
      classifiers=[
              'Intended Audience :: Developers',
              'License :: OSI Approved :: MIT License',
              'Operating System :: OS Independent',
              'Natural Language :: Chinese (Simplified)',
              'Natural Language :: Chinese (Traditional)',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3.7',
              'Programming Language :: Python :: 3 :: Only'
      ],
      keywords='NLP',
      packages=['bear_nlp', 'zhtools'],
      package_dir={'bear_nlp': 'bear_nlp', 'zhtools': 'zhtools'},
      package_data={'bear_nlp': ['*.*', 'dict/*'], 'zhtools': ['*.*']},
      # install_requires=['jieba']
      )
