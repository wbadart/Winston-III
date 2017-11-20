#!/usr/bin/env python3

'''
' winston/service/service.py
'
' Generic base class for Winston services.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging
from collections import defaultdict


def command(verbs):
    '''
    Decorator for service subclass _cmd_X methods to specify which
    verbs can trigger the action.
    '''
    def _impl(f):
        f._verbs = verbs
        return f
    return _impl


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


class ServiceMeta(type):
    '''
    Metaclass to automatically register `_cmd_X` methods
    with the class' dispatch method.
    '''
    def __new__(cls, clsname, bases, attrs):
        attrs['_dispatch'] = defaultdict(dict)
        attrs['_verbs'] = set()
        for f in attrs.values():
            for verb in getattr(f, '_verbs', []):
                attrs['_dispatch'][verb] = f
                attrs['_verbs'].add(verb)
        return super(ServiceMeta, cls).__new__(
            cls, clsname, bases, attrs)


class ServiceBase(metaclass=ServiceMeta):
    '''Generic base class for Winston services.'''

    def __init__(self):
        self._log = logging.getLogger(__name__)

    def dispatch(self, cmd_str):
        '''Attempt to run the method that corresponds to cmd verb.'''
        self._log.debug('Attempting to dispatch "%s"', cmd_str)
        cmd, *args = cmd_str.split()
        if cmd in self._verbs:
            return self._dispatch[cmd](self, args)

    @property
    def verbs(self):
        return self._verbs
