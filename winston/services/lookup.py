#!/usr/bin/env python3

'''
' winston/services/lookup.py
'
' A simple command lookup service, basically for hard-coding
' certain command strings to certain outputs.
' In some cases, apply heuristics to claim command.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

from functools import partial
from string import punctuation
from .util.baseservice import command, ServiceBase


class Service(ServiceBase):
    '''Implements command lookup table.'''

    def dispatch(self, cmd):
        '''Run command from lookup table.'''
        result = max(
            self.commands,
            key=partial(self._match, cmd))(self, cmd)
        return self.send(result)

    def score(self, cmd):
        '''Check for any exact matches, else fallback to defulat impl.'''
        return 2.5 if any(w in self.keywords for w in cmd) \
                   else super().score(cmd)

    @staticmethod
    def _match(cmd_tokens, method):
        '''The real-number score matching a cmd to a mehtod.'''
        keywords = set(getattr(method, 'keywords', []))
        return len(
            keywords.intersection(set(cmd_tokens))) / len(cmd_tokens)

    @command(keywords=['help'])
    def help(self, cmd):
        return 'Just ask me something!'

    @command(keywords=['introduce', 'yourself'])
    def intro(self, cmd):
        return 'Hi, I\'m Winston!'

    @command(keywords=['echo'])
    def echo(self, cmd):
        return str(cmd)

    @command(keywords=['thank', 'you', 'thanks'])
    def manners(self, cmd):
        return "You're welcome!"
