# piffle

Python library for generating and parsing [IIIF Image API](http://iiif.io/api/image/2.1/) URLs in an
object-oriented, pythonic fashion.

[![Build Status](https://travis-ci.org/Princeton-CDH/piffle.svg?branch=master)](https://travis-ci.org/Princeton-CDH/piffle)
[![Coverage Status](https://coveralls.io/repos/github/Princeton-CDH/piffle/badge.svg?branch=master)](https://coveralls.io/github/Princeton-CDH/piffle?branch=master)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/cdhdevteam)

Piffle is tested on Python 2.7 and 3.3-3.6.

Piffle was originally developed by Emory University as a part of
[Readux](https://github.com/ecds/readux>) and forked as a separate project
under [emory-lits-labs](https://github.com/emory-lits-labs/).

## Installation and example use:

`pip install piffle`

Example use for generating an IIIF image url:

```
>>> from piffle.iiif import IIIFImageClient
>>> myimg = IIIFImageClient('http://image.server/path/', 'myimgid')
>>> print myimg
http://image.server/path/myimgid/full/full/0/default.jpg
>>> print myimg.info()
http://image.server/path/myimgid/info.json"
>>> print myimg.size(width=120).format('png')
http://image.server/path/myimgid/full/120,/0/default.png
```

Example use for parsing an IIIF image url:

```
>>> from piffle.iiif import IIIFImageClient
>>> myimg = IIIFImageClient.init_from_url('http://www.example.org/image-service/abcd1234/full/full/0/default.jpg')
>>> print myimg
http://www.example.org/image-service/abcd1234/full/full/0/default.jpg
>>> print myimg.info()
http://www.example.org/image-service/abcd1234/info.json
>>> myimg.as_dict()['size']['full']
True
>>> myimg.as_dict()['size']['exact']
False
>>> myimg.as_dict()['rotation']['degrees']
0.0
```

## Development and Testing

This project uses [git-flow](https://github.com/nvie/gitflow) branching conventions.

Install locally for development (the use of virtualenv is recommended):

`pip install -e .`

Install test dependencies:

`pip install -e ".[test]"`

Run unit tests: `py.test` or `python setup.py test`

## Publishing

To upload a tagged release to [PyPI](https://pypi.python.org/pypi) with
a [wheel](http://pythonwheels.com/) package:

  `python setup.py sdist bdist_wheel upload`
