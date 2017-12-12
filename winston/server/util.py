#!/usr/bin/env python3

'''
' winston/server/util.py
'
' Shared utilities for server module.
'
' Will Badart <wbadart@nd.edu>
' created: NOV 2017
'''

from nltk.parse.bllip import RerankingParser
from nltk.tree import Tree


class FileStreamMixin(object):
    '''
    Provides methods for automatically flushing streams
    after sending messages.
    '''

    def __init__(self, fs):
        self._fs = fs

    def send(self, msg):
        '''Write a message to the stream.'''
        self._fs.write(msg)
        self._fs.flush()

    def recv(self):
        '''Grab a line from the stream.'''
        msg = self._fs.readline().strip()
        self._fs.flush()
        return msg


class Command(list):
    '''Hold all representations of a command string.'''
    _PARSER = RerankingParser.fetch_and_load('WSJ-PTB3')

    def __init__(self, cmd_str):
        self._str = cmd_str
        self.parse = self._PARSER.simple_parse(cmd_str)
        self.tree = Tree.fromstring(self.parse)
        self.tagged = self.tree.pos()
        self.tokens = self.tree.leaves()

    def __str__(self):
        return self._str

    def __repr__(self):
        return (
            'Command: "%s"\n'
            '   tokens: %s\n'
            '   tags:   %s\n'
            '   parse:  %s\n'
            '   tree:   \n%s\n'
        ) % (self._str, self.tokens, self.tagged, self.parse, self.tree.pformat())

    def __iter__(self):
        return iter(self.tokens)

    def __len__(self):
        return len(self.tokens)
