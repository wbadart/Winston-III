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


def tosentence(string):
    '''Capitalize starting character and append period. Helps POS tagging.'''
    return (
        string[0].upper() + string[1:] + ('.' if not string.endswith('.') else '')
        if len(string) > 1 else string)



class FileStreamMixin(object):
    '''Provides methods for automatically flushing streams after sending messages.'''

    def __init__(self, fs):
        self._fs = fs

    def send(self, msg):
        self._fs.write(msg)
        self._fs.flush()

    def recv(self):
        msg = self._fs.readline().strip()
        self._fs.flush()
        return msg


def levenshtein(s, t):
    """
    http://en.wikipedia.org/wiki/Levenshtein_distance
    Implementation by David Chiang
    """
    s, t = s.lower(), t.lower()
    m, n = len(s), len(t)
    # d[i][j] says how to get t[:j] from s[:i]
    d = [[None for j in range(n+1)] for i in range(m+1)]
    d[0][0] = 0
    for i in range(m+1):
        for j in range(n+1):
            if i == j == 0: continue

            cands = []

            if i > 0 and j > 0 and  d[i-1][j-1] is not None:
                antcost = d[i-1][j-1]
                if s[i-1] == t[j-1]:
                    cands.append(antcost+0)
                else:
                    cands.append(antcost+1)

            if i > 0 and d[i-1][j] is not None:
                # deletion
                antcost = d[i-1][j]
                cands.append(antcost+1)

            if j > 0 and d[i][j-1] is not None:
                # insertion
                antcost = d[i][j-1]
                cands.append(antcost+1)

            d[i][j] = min(cands)
    return float(d[m][n])
