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
from logging import getLogger


class WinstonRecognizer(object):
    '''
    Winston API to the SpeechRecognition module. Enables swapable
    backends.
    '''

    def __init__(self):
        self._log = getLogger(__name__)
        self._recognizer = sr.Recognizer()
        self._source = sr.Microphone(device_index=3)
        self._backend = _Backend.google

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


class _Backend(object):
    google = 'google'
    sphinx = 'sphinx'


if __name__ == '__main__':
    w = WinstonRecognizer()
