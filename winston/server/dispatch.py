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

from functools import partial
from importlib import import_module
from logging import getLogger
from nltk import download
from operator import itemgetter
from pprint import pformat
from string import punctuation
from threading import Lock, Thread


class Dispatcher(object):
    '''Main Dispatcher implementation.'''
    _RECV_BUFSIZ = 4096
    _SCORE_THRESHOLD = 0.1
    _SERVICE_PATH = 'winston.services'

    # Get NLTK data if not yet cached
    download('averaged_perceptron_tagger')
    download('maxent_ne_chunker')
    download('punkt')
    download('words')

    def __init__(self, client_socket, config):
        self._log = getLogger(__name__)
        self._config = config
        self._socket = client_socket
        self._services = {}
        self._service_lock = Lock()
        for name in config.get('services', ['search', 'lookup']):
            Thread(
                target=self._register_service,
                args=(name,)).start()

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

        cmd = Command(cmd_str)

        scores = list(
            (service, service.score(cmd))
            for service in self._services.values())
        self._log.debug(pformat(scores))

        if not any(score >= self._SCORE_THRESHOLD for _, score in scores) \
                and 'search' in self._services:
            return self._services['search'].dispatch(cmd)

        return max(scores, key=itemgetter(1))[0] \
            .dispatch(cmd_tokens)

    def _register_service(self, name):
        '''Add a service to the registry.'''
        try:
            module = import_module(
                '{path}.{name}'.format(path=self._SERVICE_PATH, name=name))
        except ImportError as e:
            return self._log.error(
                'Couldn\'t import service "%s": %s', name, e)
        service = module.Service(self._socket, self._config)
        with self._service_lock:
            self._services[name] = service
