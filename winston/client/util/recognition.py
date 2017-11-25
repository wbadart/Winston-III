#!/usr/bin/env python3

'''
' winston/recognition.py
'
' Winston speech to text module.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import speech_recognition as sr

from colored import fg, bg, attr
from logging import getLogger
from os import devnull


class WinstonRecognizer(object):
    '''
    Winston API to the SpeechRecognition module. Enables swapable
    backends.
    '''

    def __init__(self, device_index=3):
        self._log = getLogger(__name__)
        self._recognizer = sr.Recognizer()
        self._backend = _Backend.google
        self._source = sr.Microphone(device_index=device_index)

        with self._source as src:
            self._recognizer.adjust_for_ambient_noise(src)

    def listen(self):
        '''Public method for both getting mic input and recognizing.'''
        return self._recognize(self._listen())

    def _listen(self):
        '''Get audio sample.'''
        self._log.info('Listening...')
        with self._source as src:
            audio = self._recognizer.listen(src)
        return audio

    def _recognize(self, audio):
        '''Use specified backend to recognize audio sample.'''
        try:
            return getattr(
                self._recognizer, f'recognize_{self._backend}')(audio)
        except sr.UnknownValueError:
            self._log.error('Could not recognize audio')
        except sr.RequestError:
            self._log.error('Could not contact recognition engine')
        return ''

    def mictest(self):
        microphones = sr.Microphone.list_microphone_names()
        green, blue, gray = map(fg, ('green', 'blue', 'grey_53'))
        bold, reset = map(attr, ('bold', 'reset'))
        for i, micname in enumerate(microphones):
            try:
                sr.Microphone(device_index=i).__enter__()
                msg = f'{green}Mic {blue + bold}#{i}{reset + gray} ' + \
                      f'({micname}) {reset + green}works.{reset}'
                print(msg)
            except OSError as e:
                continue


class _Backend(object):
    google = 'google'
    sphinx = 'sphinx'


if __name__ == '__main__':
    WinstonRecognizer().mictest()
