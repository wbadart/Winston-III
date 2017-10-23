#!/usr/bin/env python3

'''
' winston/recognition.py
'
' Winston speech to text module.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

from speech_recognition import Microphone, Recognizer


class WinstonRecognizer(object):
    '''
    Winston API to the SpeechRecognition module. Enables swapable
    backends.
    '''

    def __init__(self):
        self._recognizer = Recognizer()
        self._source = Microphone
        self._backend = Backend.google


    def listen(self):
        '''Get audio sample.'''
        with self._source(device_index=0) as src:
            audio = self._recognizer.listen(src)
        return audio

    def recognize(self, audio):
        '''Use specified backend to recognize audio sample.'''
        return getattr(
            self._recognizer, f'recognize_{self._backend}')(audio)


class Backend(object):
    google = 'google'


if __name__ == '__main__':
    w = WinstonRecognizer()
