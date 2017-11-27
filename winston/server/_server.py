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

from collections import namedtuple
from contextlib import closing
from socket import socket, SO_REUSEADDR, SOL_SOCKET
from threading import Thread

from .dispatch import Dispatcher

ClientSockets = namedtuple('ClientSockets', 'control data')


class Server(object):
    '''Main server implementation.'''
    # Only allow one instance of the mic and one of the cli
    _CMD_SENTINEL = 'done'
    _RECV_BUFSIZ = 4096
    _SOCKET_BACKLOG = 2

    def __init__(self, **config):
        self._log = logging.getLogger(__name__)
        self._config = config

        addr = config.get('host', '0.0.0.0'), config.get('port', 4000)
        self._host, self._port = addr
        self._listen_socket = socket()  # default: SOCK_STREAM
        self._listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, int(True))
        self._listen_socket.bind(addr)
        self._log.info('Server bound to %s:%d', *addr)

    def run(self):
        '''Begin listening for incoming connections.'''
        self._listen_socket.listen(self._SOCKET_BACKLOG)
        with closing(self._listen_socket):
            while True:
                client_info = self._listen_socket.accept()  # -> (sock_obj, addr)
                Thread(target=self._handle_connection, args=client_info).start()

    def _handle_connection(self, control_socket, client_addr):
        '''Dispatch the incoming command.'''
        self._log.debug('Dispatched new connection (%s:%d) to thread.', *client_addr)
        data_socket = self._mkdatasocket(control_socket)
        client = ClientSockets(control_socket, data_socket)
        dispatch = Dispatcher(client, self._config)
        with closing(client_socket):
            cmd = 'anything truthy; immediately reassigned'
            while cmd and cmd != self._CMD_SENTINEL:
                cmd = control_socket.recv(self._RECV_BUFSIZ).decode()
                try:
                    dispatch(cmd)
                except RuntimeError as e:
                    control_socket.send('Something went wrong: {}'.format(e).encode())
        self._log.debug('Handler terminated')

    def _mkdatasocket(self, client_control_socket):
        data_socket = socket()
        data_socket.bind((self._host, 0))
        data_socket.listen(1)
        _, port = data_socket.getsockname()
        client_control_socket.send(str(port).encode())
        client_data_socket = data_socket.accept()
        data_socket.close()
        return client_data_socket


if __name__ == '__main__':
    Server().run()
