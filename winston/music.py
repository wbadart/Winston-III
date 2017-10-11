#!/usr/bin/env python3

'''
' winston/music.py
'
' Description of the contract fulfilled by "Music" type services
' leveraged by Winston.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging
import os
import pygame.mixer as mx

from functools import partial
from operator import itemgetter

import winston.util as util


class Music(object):
    '''
    Base implementation of music service
    providers. Plays music from disk.
    '''
    _PLAYER = mx.music

    def __init__(self, library_root='.', verbose=False):
        self._lib_root = library_root
        self._index_cache = None
        self._songs_cache = None
        self._log = logging.getLogger(__name__)
        self._log.setLevel(logging.DEBUG if verbose else logging.WARNING)
        mx.init()

    def dispatch(self, cmd, *args):
        '''Given a user input, execute the appropriate action.'''
        if cmd == _Command.play:
            self.play(' '.join(args))
        elif cmd == _Command.stop:
            self.stop()
        elif cmd == _Command.pause:
            self.pause()
        elif cmd == _Command.resume:
            self.resume()
        elif cmd == _Command.add:
            self.add(' '.join(args))

    def play(self, song):
        '''Begin playback of front of song queue.'''
        path = os.path.join(self._lib_root, *self._guess(song))
        self._PLAYER.load(path)
        self._PLAYER.play()

    def stop(self):
        '''Stop current playback.'''
        self._PLAYER.stop()

    def pause(self):
        '''Pauses playback of current track.'''
        self._PLAYER.pause()

    def resume(self):
        '''Unpause paused playback.'''
        self._PLAYER.unpause()

    def add(self, song):
        '''Add a song to the play queue.'''
        path = os.path.join(self._lib_root, *self._guess(song))
        self._PLAYER.queue(path)

    def _guess(self, description):
        '''Try to find song in library.'''
        guess = min(
            self._songs,
            key=util.compose(
                itemgetter(2),  # (artist, album, *song*)
                partial(util.levenshtein, description)))
        self._log.debug('Guessing "%s" means "%s"', description, guess)
        return guess


    @property
    def _index(self):
        '''
        Load index of music library into memory. Music library must
        be of the following layout: root/artist/album/song. Gives
        map from artists->albums->songs.
        '''
        if self._index_cache is None:
            self._index_cache= {
                artist: {
                    album: os.listdir(os.path.join(self._lib_root, artist, album))
                    for album in os.listdir(os.path.join(self._lib_root, artist))}
                for artist in os.listdir(self._lib_root)}
        return self._index_cache

    @property
    def _songs(self):
        if self._songs_cache is None:
            self._songs_cache = set(
                (artist, album, song)
                for artist, albums in self._index.items()
                for album, songs in albums.items()
                for song in songs)
        return self._songs_cache


class _Command(object):
    '''Label the supported command strings.'''
    play = 'play'
    stop = 'stop'
    pause = 'pause'
    resume = 'resume'
    add = 'add'
    help_ = 'help'
