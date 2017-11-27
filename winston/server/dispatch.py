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

from importlib import import_module
from logging import getLogger
from nltk import download, word_tokenize
from operator import itemgetter
from pprint import pformat
from string import punctuation


class Dispatcher(object):
    '''Main Dispatcher implementation.'''
    _RECV_BUFSIZ = 4096
    _SCORE_THRESHOLD = 0.1

    # Get NLTK data if not yet cached
    download('averaged_perceptron_tagger')
    download('punkt')

    def __init__(self, client_socket, config):
        self._log = getLogger(__name__)
        self._socket = client_socket
        self._services = {}
        for service in config.get('services', ['search', 'lookup']):
            try:
                self._services[service] = \
                    import_module('winston.services.' + service) \
                    .Service(client_socket, config)
                self._log.debug('Loaded service "%s"', service)
            except ImportError as e:
                self._log.error(
                    'Couldn\'t import service "%s": %s', service, e)

    def __call__(self, cmd_str):
        '''
        Tag the words in the command string to determine the
        appropriate service.
        '''
        self._log.info('Dispatching command "%s".', cmd_str)
        if not self._services:
            raise RuntimeError('This server has no services.')
        if not cmd_str:
            return

        cmd_tokens = word_tokenize(cmd_str)
        while cmd_tokens[0].casefold() == 'winston' \
                or cmd_tokens[0] in punctuation:
            cmd_tokens.pop(0)

        scores = list(
            (service, service.score(cmd_tokens))
            for service in self._services.values())
        self._log.debug(pformat(scores))

        if not any(score >= self._SCORE_THRESHOLD for _, score in scores) \
                and 'search' in self._services:
            return self._services['search'].dispatch(cmd_tokens)

        return max(scores, key=itemgetter(1))[0] \
            .dispatch(cmd_tokens)
