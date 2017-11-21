#!/usr/bin/env python3

'''
' winston/client/putoutput.py
'
' Library of functions for returning output to a user. Each
' function should take one argument, the message to report,
' execute the side-effect for reporting the output, and
' return None.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

import os


def stdout(client, msg, **kwags):
    '''Print the designated message to screen.'''
    print(msg)


def speak(client, msg, **kwargs):
    '''Play the message via espeak TTS.'''
    os.system('espeak "%s" &' % msg)
