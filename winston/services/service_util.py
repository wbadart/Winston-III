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


class Service(metaclass=ServiceMeta):
    '''Generic base class for Winston services.'''

    def __init__(self):
        self._log = logging.getLogger(__name__)

    def dispatch(self, cmd_str):
        '''Attempt to run the method that corresponds to cmd verb.'''
        self._log.debug('Attempting to dispatch "%s"', cmd_str)
        cmd, *args = cmd_str.split()
        if cmd in self._verbs:
            return self._dispatch[cmd](*args)
        else:
            pass

    @property
    def verbs(self):
        return self._verbs
