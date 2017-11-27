#!/usr/bin/env python3

'''
' winston/services/lookup.py
'
' A simple command lookup service, basically for hard-coding
' certain command strings to certain outputs.
' TODO: levenshtein threshold rather than exact equality
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

from nltk import word_tokenize
from .util.baseservice import command, ServiceBase


class Service(ServiceBase):
    '''Implements command lookup table.'''

    def dispatch(self, cmd_str):
        '''Run command from lookup table.'''
        cmd_tokens = word_tokenize(cmd_str)
        result = max(dir(self), key=lambda m: len(set(getattr(m, 'keywords', [])).intersection(set(cmd_tokens))))(self)
        return self.send(result)

    @command(keywords=['help'])
    def help(self):
        return 'Just ask me something!'

    @command(keywords=['winston', 'introduce', 'yourself'])
    def intro(self):
        return 'Hi, I\'m Winston!'
