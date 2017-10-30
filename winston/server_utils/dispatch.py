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

import logging

# from functools import partialmethod
from nltk import download, pos_tag, word_tokenize
from operator import itemgetter
from .service.search import Search
from ..util import compose, tosentence


class Dispatcher(object):
    '''Main Dispatcher implementation.'''
    download('averaged_perceptron_tagger')
    download('punkt')

    def __init__(self, client_socket):
        self._log = logging.getLogger(__name__)
        self._fs = client_socket.makefile()
        self._search = Search()

    def __call__(self, cmd):
        '''Tag the words in the command string to determine the appropriate service.'''
        self._log.info('Dispatching command "%s".', cmd)
        tagged = self._tagtokens(cmd)
        if self._isquestion(tagged[0][1]):
            # self._sendmsg('Thank you for your question.')
            self._sendmsg(search(cmd))
        else:
            self._sendmsg('Your wish is my command.')

    def _sendmsg(self, s):
        self._fs.write(s + '\n')
        self._fs.flush()

    def _is(self, tag_start, tag):
        return tag.upper().startswith(tag_start.upper())

    # _isverb = partial(_is, 'v')
    # _isquestion = partial(_is, 'w')
    def _isquestion(self, tag):
        return tag.startswith('W')

    @staticmethod
    def _tagtokens(string):
        return pos_tag(word_tokenize(tosentence(string)))
