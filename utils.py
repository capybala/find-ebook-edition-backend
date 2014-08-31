#coding: utf-8
from __future__ import unicode_literals


def to_bytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('utf-8')


def to_str(b):
    # Convert to the py3 str
    if isinstance(b, unicode):
        return b
    return b.decode('utf-8')


if __name__ == '__main__':
    from pprint import pprint
    pprint(to_bytes(b'Should be bytes だよ'))
    pprint(to_bytes('Should be bytes だよ'))
    pprint(to_str(b'Should be (Python 3) str だよ'))
    pprint(to_str('Should be (Python 3) str だよ'))
