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

from functools import partialmethod
from nltk import download, pos_tag, word_tokenize
from operator import itemgetter

from ..util import FileStreamMixin, compose, tosentence


class Dispatcher(FileStreamMixin):
    '''Main Dispatcher implementation.'''
    download('averaged_perceptron_tagger')
    download('punkt')

    def __init__(self, client_socket):
        super().__init__(client_socket.makefile())
        self._log = logging.getLogger(__name__)
        self._search = Search()

    def __call__(self, cmd):
        '''Tag the words in the command string to determine the appropriate service.'''
        self._log.info('Dispatching command "%s".', cmd)
        tagged = self._tagtokens(cmd)
        if self._isquestion(tagged[0][1]):
            # self._sendmsg('Thank you for your question.')
            self.send(search(cmd))
        else:
            self.send('Your wish is my command.')

    def _is(self, tag_start, tag):
        return tag.upper().startswith(tag_start.upper())

    _isverb = partialmethod(_is, 'v')
    _isquestion = partialmethod(_is, 'w')

    @staticmethod
    def _tagtokens(string):
        return pos_tag(word_tokenize(tosentence(string)))
