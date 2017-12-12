#!/usr/bin/env python3

'''
' winston/test/__main__.py
'
' Run ALL the tests.
'
' Will Badart <wbadart@live.com>
' created: DEC 2017
'''

from unittest import main as runtests
from .music import TestSongMatching


if __name__ == '__main__':
    runtests()
