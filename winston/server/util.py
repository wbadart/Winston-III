#!/usr/bin/env python3

'''
' winston/server/util.py
'
' Shared utilities for server module.
'
' Will Badart <wbadart@nd.edu>
' created: NOV 2017
'''


class FileStreamMixin(object):
    '''
    Provides methods for automatically flushing streams
    after sending messages.
    '''

    def __init__(self, fs):
        self._fs = fs

    def send(self, msg):
        '''Write a message to the stream.'''
        self._fs.write(msg)
        self._fs.flush()

    def recv(self):
        '''Grab a line from the stream.'''
        msg = self._fs.readline().strip()
        self._fs.flush()
        return msg
