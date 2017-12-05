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
from .util.baseservice import command, ServiceBase


class Service(ServiceBase):
    '''Wrapper to ChatBot.'''
    _BOT = ChatBot('winston')
    _CHAT_SENTINEL = 'done'
    _TRAINED = False

    def __init__(self, socket, config):
        super().__init__(socket, config)
        if not self._TRAINED:
            self._BOT.set_trainer(ChatterBotCorpusTrainer)
            self._BOT.train('chatterbot.corpus.english')
            self._TRAINED = True

    def score(self, cmd):
        '''Try to identify if a command is conversational.'''
        return float('inf')

    def dispatch(self, cmd):
        cmd_str = self.detokenize(cmd_tokens)
        return self.send(self(str(cmd)))

    def __call__(self, msg):
        '''Get the conversational response to a message.'''
        return self._BOT.get_response(msg)

    @command(keywords=['let\'s', 'chat'])
    def chat(self, msg):
        while msg.casefold() != self._CHAT_SENTINEL:
            self.send(self(msg))
            msg = self.recv()
