#!/usr/bin/env python3

'''
' winston/client/microphone.py
'
' Speech recognition Winston client.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

import logging
from _client import Client
from recognition import WinstonRecognizer


class MicrophoneClient(Client):
    '''Use speech recogniztion to collect commands.'''
    _EVENT_LOOP_DEBOUNCE = 0.3

    def __init__(self, server_host, server_port):
        super().__init__(server_host, server_port)
        self._recognizer = WinstonRecognizer()

    def getinput(self):
        '''Get input from the microphone.'''
        return self._recognizer.listen()

    def putoutput(self, msg):
        '''Report output back to user. TODO: tts'''
        # print(msg)
        os.system('espeak "%s" &' & msg)


if __name__ == '__main__':
    MicrophoneClient.main()
