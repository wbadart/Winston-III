#!/usr/bin/env python3

'''
' winston/client/getinput.py
'
' Library for input gathering functions. All module functions
' should accept a client object, and configuration as kwargs,
' gather text input from the target source, and return it as a string.
'
' Will Badart <wbadart@nd.edu>
' created: NOV 2017
'''

# from winston.client.util.recognition import WinstonRecognizer
from ..util import recognition

_RECOGNIZER = recognition.WinstonRecognizer()


def stdin(client, **kwargs):
    '''Get input from the keyboard.'''
    try:
        return input(kwargs.get('prompt', '>> '))
    except EOFError:
        client.exit()


def microphone(client, **kwargs):
    '''Collect and recognize mic input.'''
    return _RECOGNIZER.listen()
