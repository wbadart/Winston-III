#!/usr/bin/env python3

'''
test/util.py

Utility functions shared by tests.

Will Badart <wbadart@live.com>
created: DEC 2017
'''

from io import StringIO


class DummySocket(StringIO):
    '''A StringIO buffer pretending to be a socket.'''

    def send(self, data):
        '''Alias for StringIO.write.'''
        return self.write(str(data))

    def recv(self):
        '''Alias for StringIO.read.'''
        return self.read()
