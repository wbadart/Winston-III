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
        self._source = Microphone(device_index=0)
        self._backend = _Backend.google

        with self._source as src:
            self._recognizer.adjust_for_ambient_noise(src)

    def listen(self):
        return self._recognize(self._listen())

    def _listen(self):
        '''Get audio sample.'''
        with self._source as src:
            audio = self._recognizer.listen(src)
        return audio

    def _recognize(self, audio):
        '''Use specified backend to recognize audio sample.'''
        return getattr(
            self._recognizer, f'recognize_{self._backend}')(audio)


class _Backend(object):
    google = 'google'
    sphinx = 'sphinx'


if __name__ == '__main__':
    w = WinstonRecognizer()
