#!/usr/bin/env python3

'''
' winston/service/music.py
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

from functools import partial, partialmethod
from pathlib import Path
from operator import itemgetter
from .util.misc import command, levenshtein
from .util.baseservice import ServiceBase


class Service(ServiceBase):
    '''
    Base implementation of music service
    providers. Plays music from disk.
    '''
    _PLAYER = mx.music

    def __init__(self, socket, config):
        super(Service, self).__init__(socket, config)
        self._lib_root = config.get(
            'music_path',
            library_root=os.path.join(Path.home(), 'Music'))
        self._index_cache = None
        self._songs_cache = None
        self._albums_cache = None
        mx.init()

    def dispatch(self, cmd_str):
        '''Determine appropriate service method and execute.'''

    @command(keywords=['play'])
    def play(self, arg):
        '''Begin playback of front of song queue.'''
        description = ' '.join(arg)
        guess = self._guess(description)
        path = os.path.join(self._lib_root, *guess)

        if self._issong(guess):
            # If song, just play song
            self._PLAYER.load(path)

        elif self._isalbum(guess):
            # If album, queue up all songs on album and play
            self._add_album(guess)

        else:
            # TODO: If artist, queue all songs from all artists
            for album in self._index[guess[0]]:
                self._add_album((guess[0], album))

        self._PLAYER.play()

    @command(keywords=['stop'])
    def stop(self):
        '''Stop current playback.'''
        self._PLAYER.stop()

    @command(keywords=['pause'])
    def pause(self):
        '''Pauses playback of current track.'''
        self._PLAYER.pause()

    @command(keywords=['resume', 'start'])
    def resume(self):
        '''Unpause paused playback.'''
        self._PLAYER.unpause()

    @command(keywords=['add'])
    def add(self, song):
        '''Add a song to the play queue.'''
        path = os.path.join(self._lib_root, *self._guess(song))
        self._PLAYER.queue(path)

    def _add_album(self, album):
        '''Queue all songs on specified album. Load first song.'''
        path = os.path.join(self._lib_root, *album)
        first, *songs = os.listdir(path)
        self._PLAYER.load(os.path.join(path, first))
        for song in os.listdir(path):
            self._PLAYER.queue(os.path.join(path, song))

    def _guess(self, description):
        '''Try to find song in library.'''
        score = partial(levenshtein, description)
        self._log.debug('Guesses for "%s":', description)
        if not self._songs:
            raise RuntimeError('Library is empty')

        best_song = min(
            map(lambda s: (score(s[2]), s), self._songs),
            key=itemgetter(0))
        self._log.debug('\tsong:   %s', best_song[1][2])

        best_album = min(
            map(lambda a: (score(a[1]), a), self._albums),
            key=itemgetter(0))
        self._log.debug('\talbum:  %s', best_album[1][1])

        best_artist = min(
            map(lambda a: (score(a[0]), (a,)), self._index),
            key=itemgetter(0))
        self._log.debug('\tartist: %s', best_artist[1][0])

        guess = min(
            [best_song, best_album, best_artist], key=itemgetter(0))[1]
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

    @property
    def _albums(self):
        if self._albums_cache is None:
            self._albums_cache = set(
                (artist, album)
                for artist, albums in self._index.items()
                for album in albums)
        return self._albums_cache

    def _iswhat(self, tuple_len, description):
        return type(description) is tuple and tuple_len == len(description)

    _issong = partialmethod(_iswhat, 3)
    _isalbum = partialmethod(_iswhat, 2)
    _isartist = partialmethod(_iswhat, 1)
