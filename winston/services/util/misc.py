#!/usr/bin/env python3

'''
' winston/services/util/misc.py
'
' Utility functions used by Winston service implementations.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging
from collections import defaultdict


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
