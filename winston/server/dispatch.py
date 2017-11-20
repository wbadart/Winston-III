#!/usr/bin/env python3

'''
' winston/server_utils/dispatch.py
'
' Receives a command string and forwards to the
' best-guess service.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import sys

from functools import partialmethod
from importlib import import_module
from logging import getLogger
from nltk import download, pos_tag, word_tokenize
from operator import itemgetter

from config import ServerConfig

# from services.music import Music
# from services.search import Search


class Dispatcher(object):
    '''Main Dispatcher implementation.'''
    _RECV_BUFSIZ = 4096

    # Get NLTK data if not yet cached
    download('averaged_perceptron_tagger')
    download('punkt')

    def __init__(self, client_socket, server_conf):
        self._log = getLogger(__name__)
        self._socket = client_socket
        sys.path.append(server_conf.services_path)
        self._services = {}
        for service in server_conf.services:
            try:
                self._services[service] = import_module(service)
                self._log.debug('Loaded service "%s"', service)
            except ImportError as e:
                self._log.error('Couldn\'t import service "%s": %s', service, e)

        self._search = self._services['search'].Service()
        self._music = self._services['music'].Service()


    def __call__(self, cmd):
        '''
        Tag the words in the command string to determine the
        appropriate service.
        '''
        self._log.info('Dispatching command "%s".', cmd)
        if not cmd:
            return
        tagged = self._tagtokens(cmd)
        self._log.debug(tagged)
        if self._isquestion(tagged[0][1]):
            # self._send('Thank you for your question.')
            self._send(self._search(cmd))
        elif tagged[0][0].casefold() == 'play'.casefold():
            self._music.dispatch(cmd)
            self._send('Playing...')
        else:
            self._send('Your wish is my command.')

    def _is(self, tag_start, tag):
        '''See if a POS tag is descendant of a higher level POS.'''
        return tag.upper().startswith(tag_start.upper())

    _isverb = partialmethod(_is, 'v')
    _isquestion = partialmethod(_is, 'w')

    @classmethod
    def _tagtokens(cls, string):
        '''Wrap the tokenization and tagging of a string.'''
        return pos_tag(word_tokenize(cls.tosentence(string)))

    @staticmethod
    def tosentence(string):
        '''Capitalize starting character and append period. Helps POS tagging.'''
        return (
            string[0].upper() + string[1:] + ('.' if not string.endswith('.') else '')
            if len(string) > 1 else string)

    def _send(self, msg):
        '''Give a message to the client.'''
        if msg:
            self._log.debug('Sending message "%s"', msg)
            self._socket.send(msg.encode())
