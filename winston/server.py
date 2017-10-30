#!/usr/bin/env python

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

from socket import socket
from threading import Thread


class Server(object):
    '''Main server implementation.'''
    # Only allow one instance of the mic and one of the cli
    _BACKLOG = 2

    def __init__(self, host='0.0.0.0', port=4000):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(logging.DEBUG)
        self._host = host
        self._port = port
        self._listen_socket = socket()
        self._listen_socket.bind((host, port))

    def run(self):
        '''Begin listening for incoming connections.'''
        self._listen_socket.listen(self._BACKLOG)
        self._log.info('Server listening on %s:%d', self._host, self._port)
        while True:
            client_info = self._listen_socket.accept()  # -> (sock_obj, addr)
            Thread(target=self._handle_connection, args=client_info).run()

    def _handle_connection(self, client_socket, client_addr):
        '''Dispatch the incoming command.'''
        self._log.debug('Dispatched new connection (%s:%d) to thread.', *client_addr)
        client_fs = client_socket.makefile()
        cmd = client_fs.getline()
        print('COMMAND:', cmd)


if __name__ == '__main__':
    Server().run()
