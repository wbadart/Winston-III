#!/usr/bin/env python3

'''
' winston/util.py
'
' General utilities for Winston III.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

from functools import reduce, wraps


def compose(*funcs):
    '''Feed the result of once function into another, left to right.'''
    return lambda x: reduce(lambda acc, f: f(acc), funcs, x)
