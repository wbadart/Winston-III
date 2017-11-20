#!/usr/bin/env python3.6

'''
' winston/client/cli.py
'
' Simple command line client for communicating w/ Winston server.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

import logging
from _client import Client


class WinstonCLI(Client):
    '''Allows interaction w/ Winston server via interactive shell.'''
    _PROMPT = 'wcli> '
    _EVENT_LOOP_DEBOUNCE = 0

    def getinput(self):
        '''Grab keyboard input.'''
        try:
            return input(self._PROMPT)
        except EOFError:
            print('\nGoodbye!')
            self.exit()

    def putoutput(self, msg):
        '''Put output to the screen.'''
        print(msg)


if __name__ == '__main__':
    WinstonCLI.main()
