#!/usr/bin/env python3

'''
' winston/test/music.py
'
' Benchmark different techniques for extracting song
' designation from command strings.
'
' Will Badart <wbadart@live.com>
' created: DEC 2017
'''

from io import StringIO
from itertools import starmap
from unittest import main as runtests, TestCase
from ..server.util import Command
from ..services.music import Service as Music, Song


class DummySocket(StringIO):
    '''A StringIO buffer pretending to be a socket.'''

    def send(self, data):
        '''Alias for StringIO.write.'''
        return self.write(str(data))

    def recv(self):
        '''Alias for StringIO.read.'''
        return self.read()


class TestSongMatching(TestCase):
    '''
    Takes a list of (cmd_str, [expected_path|None]) tuples and
    see how accurate a given indexing method (mainly Levenshtein
    and syntax-based). Method should return None if it doesn't
    think it has that song.
    '''
    _SERVER_STREAM = DummySocket()
    _SERVICE = Music(_SERVER_STREAM, {})

    _CASES = starmap(Song, map(reversed, [
        ('Green Day', '21st Century Breakdown', 'Jesus of Suburbia'),
        ('Green Day', 'American Idiot', 'Boulevard of Broken Dreams'),
        ('Green Day', 'American Idiot', 'Extraordinary Girl'),
        ('Green Day', 'American Idiot', 'Holiday'),
        ('Green Day', 'American Idiot', 'Wake Me Up When September Ends'),
        ('Green Day', 'Dookie', 'Burnout'),
        ('Green Day', 'Dookie', 'Chump'),
        ('Green Day', 'Dookie', 'Having A Blast'),
    ]))

    def test_basic(self):
        '''An easy case to make sure things are working.'''
        cmd = Command(
            'play holiday by green day on american idiot')
        expected_song = Song(
            title='Holiday', album='American Idiot', artist='Green Day')
        self.assertEqual(expected_song, self._SERVICE._guess(cmd))

    def test_cases(self):
        '''Test the cases defined on the class.'''
        commands = map(
            Command, starmap('play {} by {} on {}'.format, self._CASES))
        guesses = list(map(self._SERVICE._guess, commands))
        self.assertSequenceEqual(self._CASES, guesses)


if __name__ == '__main__':
    runtests()
