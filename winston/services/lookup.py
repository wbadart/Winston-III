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

    def dispatch(self, cmd_tokens):
        '''Run command from lookup table.'''
        result = max(
            self.commands,
            key=partial(self._match, cmd_tokens))(self, cmd_tokens)
        return self.send(result)

    def score(self, cmd_tokens):
        '''Check for any exact matches, else fallback to defulat impl.'''
        for cmd in self.commands:
            if cmd_tokens[0] in self.keywords:
                return 2.5
        return super().score(cmd_tokens)

    @staticmethod
    def _match(cmd_tokens, method):
        '''The real-number score matching a cmd to a mehtod.'''
        keywords = set(getattr(method, 'keywords', []))
        return len(
            keywords.intersection(set(cmd_tokens))) / len(cmd_tokens)

    @staticmethod
    def _detokenize(tokens):
        '''Join a list of tokens back into sentences.'''
        result = tokens[0]
        for token in tokens[1:]:
            if token not in punctuation:
                result += ' '
            result += token
        return result

    @command(keywords=['help'])
    def help(self, cmd_tokens):
        return 'Just ask me something!'

    @command(keywords=['introduce', 'yourself'])
    def intro(self, cmd_tokens):
        return 'Hi, I\'m Winston!'

    @command(keywords=['echo'])
    def echo(self, cmd_tokens):
        if cmd_tokens[0].casefold() == 'echo':
            cmd_tokens.pop(0)
        return self._detokenize(cmd_tokens)

    @command(keywords=['thank', 'you', 'thanks'])
    def manners(self, cmd_tokens):
        return "You're welcome!"
