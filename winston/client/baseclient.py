#!/usr/bin/env python3.6

'''
' winston/client/_client.py
'
' Abstract client interface for all Winston clients.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

import logging
from abc import ABC, abstractmethod
from contextlib import closing
from socket import socket, timeout
from time import sleep


class Client(ABC):
    '''
    Provide the interface and some common methods for
    Winston clients.
    '''
    _EVENT_LOOP_DEBOUNCE = 0.1
    _SOCKET_TIMEOUT = 5
    _RECV_BUFSIZ = 4096

    def __init__(self, server_host, server_port):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(logging.DEBUG)
        addr = self._host, self._port = server_host, server_port
        self._socket = socket()  # default: SOCK_STREAM
        self._log.debug('Connecting to server (%s:%d)', *addr)
        self._socket.connect(addr)
        self._done = False

    def run(self):
        '''Spawn client's main event loop.'''
        self._log.info('Running main event loop...')
        with closing(self._socket):
            self._socket.settimeout(self._SOCKET_TIMEOUT)
            while not self._done:
                sleep(self._EVENT_LOOP_DEBOUNCE)
                usrin = self.getinput()
                if not usrin:
                    continue
                self.send(usrin)
                try:
                    self.putoutput(self.recv())
                except timeout:
                    self.putoutput('Timeout')

    def exit(self):
        self._done = True

    def send(self, msg):
        '''Give a command to the server.'''
        self._log.debug('Sending message "%s"', msg)
        self._socket.send(msg.encode())

    def recv(self):
        '''Get a message from the server.'''
        res = self._socket.recv(self._RECV_BUFSIZ).decode()
        self._log.debug('Got server response "%s"', res)
        return res

    @abstractmethod
    def getinput(self):
        '''Defines how the client collects commands from the user.'''

    @abstractmethod
    def putoutput(self, msg):
        '''Defines how the client reports back to the user.'''

    @classmethod
    def main(cls):
        '''Run via command line invocation.'''
        from argparse import ArgumentParser
        parser = ArgumentParser()

        parser.add_argument(
            '-H', '--host', default='localhost',
            help='Hostname of remote Winston server (default:localhost)')

        parser.add_argument(
            '-p', '--port', default=4000, type=int,
            help='Winston server port to connect to (default:4000)')

        parser.add_argument(
            '-v', '--verbose', default=False, action='store_true',
            help='Display debugging output (default:False)')

        args = parser.parse_args()

        log = logging.getLogger(__name__)
        loglevel = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(
            format='[%(module)s][%(levelname)s]: %(message)s', level=loglevel)

        client = cls(args.host, args.port)
        try:
            client.run()
        except KeyboardInterrupt:
            client.putoutput('Goodbye!')
            client.exit()
