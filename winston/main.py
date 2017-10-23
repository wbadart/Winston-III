#!/usr/bin/env python3

'''
' winston/main.py
'
' Main event loop for target implementation.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging
import speech_recognition as sr

from time import sleep
from winston.music import Music
from winston.recognition import WinstonRecognizer


def main(loglevel=logging.DEBUG):
    '''Main execution/ event loop.'''
    log = logging.getLogger(__name__)
    log.setLevel(loglevel)
    recognizer = WinstonRecognizer()
    music = Music(library_root='./music_lib', verbose=True)

    while True:
        log.info('Listening...')

        try:
            usr_in = recognizer.listen()
        except sr.UnknownValueError:
            log.error('Couldn\'t understand')
            continue
        except sr.RequestError as e:
            log.error(
                'Couln\'t reach backend {0}: {1}',
                recognizer._backend,
                e)
            continue

        log.info('Heard "%s"', usr_in)

        music.dispatch(usr_in.lower())


        sleep(0.2)
