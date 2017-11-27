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
from operator import itemgetter


class Dispatcher(object):
    '''Main Dispatcher implementation.'''
    _RECV_BUFSIZ = 4096
    _SCORE_THRESHOLD = 0.1

    def __init__(self, client_socket, config):
        self._log = getLogger(__name__)
        self._socket = client_socket
        self._services = {}
        for service in config.get('services', ['search']):
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

        scores = list((service, service.score(cmd_str))
                  for service in self._services.values())

        from pprint import pformat
        self._log.debug(pformat(scores))

        if not any(score >= self._SCORE_THRESHOLD for _, score in scores) \
                and 'search' in self._services:
            return self._services['search'].dispatch(cmd_str)

        return max(scores, key=itemgetter(1))[0] \
            .dispatch(cmd_str)
