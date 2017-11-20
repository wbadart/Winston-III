#!/usr/bin/env python3

'''
' winston/server.py
'
' Main Winston server implementation. Can listen to
' and dispatch commands for multiple clients.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging

from contextlib import closing
from socket import socket, SO_REUSEADDR, SOL_SOCKET
from threading import Thread

from config import ServerConfig
from dispatch import Dispatcher


class Server(object):
    '''Main server implementation.'''
    # Only allow one instance of the mic and one of the cli
    _CMD_SENTINEL = 'done'
    _RECV_BUFSIZ = 4096
    _SOCKET_BACKLOG = 2

    def __init__(self, **kwargs):
        self._log = logging.getLogger(__name__)
        try:
            self._config = ServerConfig(**kwargs)
        except TypeError as e:
            self._log.warn('Invalid server config. Using defaults.')
            self._config = ServerConfig()

        self._host, self._port = self._config.host, self._config.port
        self._listen_socket = socket()  # default: SOCK_STREAM
        self._listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, int(True))
        self._listen_socket.bind((self._host, self._port))

    def run(self):
        '''Begin listening for incoming connections.'''
        self._listen_socket.listen(self._SOCKET_BACKLOG)
        self._log.info('Server listening on %s:%d', self._host, self._port)
        with closing(self._listen_socket):
            while True:
                client_info = self._listen_socket.accept()  # -> (sock_obj, addr)
                Thread(target=self._handle_connection, args=client_info).start()

    def _handle_connection(self, client_socket, client_addr):
        '''Dispatch the incoming command.'''
        self._log.debug('Dispatched new connection (%s:%d) to thread.', *client_addr)
        dispatch = Dispatcher(client_socket, self._config)
        with closing(client_socket):
            cmd = 'anything truthy; immediately reassigned'
            while cmd and cmd != self._CMD_SENTINEL:
                cmd = client_socket.recv(self._RECV_BUFSIZ).decode()
                try:
                    dispatch(cmd)
                except RuntimeError as e:
                    client_socket.send('Something went wrong: {}'.format(e).encode())
        self._log.debug('Handler terminated')


if __name__ == '__main__':
    Server().run()
