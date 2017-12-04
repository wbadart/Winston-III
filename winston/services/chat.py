#!/usr/bin/env python3

'''
' winston/services/chat.py
'
' Interface with Chatterbot chat bot.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from .util.baseservice import ServiceBase


class Service(ServiceBase):
    '''Wrapper to ChatBot.'''

    def __init__(self, socket, config):
        super().__init__(socket, config)
        self._bot = ChatBot('winston')
        self._bot.set_trainer(ChatterBotCorpusTrainer)
        self._bot.train('chatterbot.corpus.english')

    def score(self, cmd_tokens):
        '''Try to identify if a command is conversational.'''
        return float('inf')

    def dispatch(self, cmd_tokens):
        cmd_str = self.detokenize(cmd_tokens)
        return self.send(self(cmd_str))

    def __call__(self, msg):
        '''Get the conversational response to a message.'''
        return self._bot.get_response(msg)
