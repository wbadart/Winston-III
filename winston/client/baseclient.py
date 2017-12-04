#!/usr/bin/env python3.6

'''
' winston/client/_client.py
'
' Abstract client interface for all Winston clients.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

import json
import logging
import os.path
import yaml

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

    def __init__(self, **config):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(config.get('loglevel', logging.DEBUG))

        self._socket = socket()  # default: SOCK_STREAM
        self._config = config
        self._done = False

        addr = config.get('host', 'localhost'), config.get('port', 4000)
        self._log.debug('Connecting to server (%s:%d)', *addr)
        self._socket.connect(addr)

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
            '-c', '--config',
            help='Path to YAML or JSON config file.')

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
        config = {'loglevel': loglevel}

        if args.config and os.path.exists(args.config):
            config_type = (json if args.config.endswith('.json') else yaml)
            with open(args.config, 'r') as config_fs:
                config.update(
                    getattr(config_type, 'load', lambda *_: {})(config_fs))
        config.update(host=args.host, port=args.port)

        client = cls(**config)
        try:
            client.run()
        except KeyboardInterrupt:
            client.putoutput('Goodbye!')
            client.exit()


class NOPClient(Client):
    '''
    A dumb, deaf client. For when you just need a blank slate
    for a client (basically just hijack its connection to server.
    '''

    def putoutput(self, msg):
        '''Ignore the given message.'''
        return msg

    def getinput(self):
        '''Give a blank string.'''
        return ''
