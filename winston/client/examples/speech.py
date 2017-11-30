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
import os

from ..baseclient import Client
from ..util.recognition import WinstonRecognizer


class MicrophoneClient(Client):
    '''Use speech recogniztion to collect commands.'''
    _EVENT_LOOP_DEBOUNCE = 0.3

    def __init__(self, **config):
        super().__init__(**config)
        self._recognizer = WinstonRecognizer(config.get('mic_index', 3))

    def getinput(self):
        '''Get input from the microphone.'''
        return self._recognizer.listen()

    def putoutput(self, msg):
        '''Speak output back to user.'''
        print(msg)
        os.system('espeak "%s" &' % msg)


if __name__ == '__main__':
    MicrophoneClient.main()
