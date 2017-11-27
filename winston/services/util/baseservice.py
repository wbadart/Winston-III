#!/usr/bin/env python3

'''
' winston/services/util/baseservice.py
'
' Provides the base class to be used by all Winston services.
'
' Will Badart <wbadart@live.com>
' created: OCT 2017
'''

from abc import ABCMeta, abstractmethod


class ServiceMeta(ABCMeta):
    '''Registers service methods with provided keywords.'''

    def __new__(cls, clsname, bases, attrs):
        registry = {}
        for f in attrs.values():
            for keyword in getattr(f, 'keywords', []):
                registry[keyword] = f
        attrs['registry'] = registry
        attrs['keywords'] = set(registry)
        return super(ServiceMeta, cls).__new__(
            cls, clsname, bases, attrs)


class ServiceBase(metaclass=ServiceMeta):
    '''Generic base class for Winston services.'''

    def __init__(self, socket, config):
        self._socket = socket
        self._config = config

    @abstractmethod
    def dispatch(self, cmd_str):
        '''Attempt to run the method that corresponds to cmd verb.'''

    def score(self, cmd_str):
        '''
        Report how likely it is that a command string was meant
        for this service. Should return float in [0, 1].
        '''
        cmd_tokens = map(str.lower, word_tokenize(cmd_string))
        return (
            len(t for t in cmd_tokens if t in self.keywords)
          / len(cmd_tokens))

    def send(self, msg):
        '''Relay control information back to the client.'''
        if msg:
            self._socket.send(msg.encode())


def command(verbs):
    '''
    Decorator for service subclass _cmd_X methods to specify which
    verbs can trigger the action.
    '''
    def _impl(f):
        f.keywords = keywords
        return f
    return _impl
