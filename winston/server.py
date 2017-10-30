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
from socket import socket
from threading import Thread
from .server_utils.dispatch import Dispatcher


class Server(object):
    '''Main server implementation.'''
    # Only allow one instance of the mic and one of the cli
    _SOCKET_BACKLOG = 2
    _CMD_SENTINEL = 'done'

    def __init__(self, host='localhost', port=4000):
        self._log = logging.getLogger(__name__)
        self._addr = self._host, self._port = host, port
        self._listen_socket = socket()  # default: SOCK_STREAM
        self._listen_socket.bind((host, port))

    def run(self):
        '''Begin listening for incoming connections.'''
        self._listen_socket.listen(self._SOCKET_BACKLOG)
        self._log.info('Server listening on %s:%d', self._host, self._port)
        while True:
            client_info = self._listen_socket.accept()  # -> (sock_obj, addr)
            Thread(target=self._handle_connection, args=client_info).start()

    def _handle_connection(self, client_socket, client_addr):
        '''Dispatch the incoming command.'''
        self._log.debug('Dispatched new connection (%s:%d) to thread.', *client_addr)
        dispatch = Dispatcher(client_socket)
        with closing(client_socket):
            client_fs = client_socket.makefile()
            cmd = 'anything truthy; immediately reassigned'
            while cmd and cmd != self._CMD_SENTINEL:
                cmd = client_fs.readline().strip()
                client_fs.flush()
                dispatch(cmd)
        self._log.debug('Handler terminated')


if __name__ == '__main__':
    Server().run()
