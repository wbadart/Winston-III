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

import os
import pygame.mixer as mx

from collections import namedtuple
from functools import partial
from logging import getLogger
from pathlib import Path
from .util.baseservice import command, ServiceBase
from .util.misc import levenshtein

Song = namedtuple('Song', 'title artist album')


class Service(ServiceBase):
    '''
    Base implementation of music service
    providers. Plays music from disk.
    '''
    _PLAYER = mx.music
    _GMUSIC_CRED_PATH = '.gmusic.creds'

    def __init__(self, socket, config):
        super(Service, self).__init__(socket, config)
        self._log = getLogger(__name__)
        self._lib_root = config.get(
            'music_path',
            os.path.join(Path.home(), 'Music'))
        self.artists = self.load_artists()
        self.albums = self.load_albums()
        self.songs = self.load_songs()
        mx.init()

    def score(self, cmd):
        '''Try to determine if cmd fits "play X by Y on Z" structure.'''
        return float(any(cmd.tokens[0] == kw for kw in self.keywords))

    def dispatch(self, cmd):
        '''Determine appropriate service method and execute.'''
        return self.play(cmd)

    @command(keywords=['play'])
    def play(self, cmd):
        '''Begin playback of front of song queue.'''
        guess = self._guess(cmd)
        self._log.debug('Guess: %s', guess)
        if not self._hassong(guess):
            return self.send('I couldn\'t find that song.')
        # path = self._getpath(guess)
        # self._PLAYER.load(path)
        # self._PLAYER.play()
        return self.send('Playing %s by %s on %s.' % guess)

    @command(keywords=['pause'])
    def pause(self):
        '''Pauses playback of current track.'''
        self._PLAYER.pause()

    @command(keywords=['resume', 'start'])
    def resume(self):
        '''Unpause paused playback.'''
        self._PLAYER.unpause()

    def _guess(self, cmd):
        '''Use syntactic information to help ID the song.'''
        song = [tuple()] * 3
        state = 0
        for word, tag in cmd.tagged:
            if word.casefold() == 'play':
                continue
            elif tag == 'IN':
                if word.casefold() == 'by':
                    state = 1
                elif word.casefold() == 'on':
                    state = 2
            else:
                song[state] += (
                    word  # .capitalize()
                    if word not in {'in', 'the'} or not song[state]
                    else word,)
        return Song(*map(' '.join, song))

    def _guess_old(self, cmd):
        '''
        Levenshtein method for command to song matching,
        adapted to new method interface.
        '''
        song_strs = {
            'play {} by {} on {}'.format(*s): s for s in self.gen_index()}
        return song_strs[
            max(song_strs, key=partial(levenshtein, cmd))]

    def _getpath(self, song):
        '''
        Load index of music library into memory. Music library must
        be of the following layout: root/artist/album/song. Gives
        map from artists->albums->songs.
        '''
        # TODO: handle cases when only given title is album
        # or artist name, not just song
        album = self.songs[song.title]
        artist = self.albums[album]
        return self.libpath(artist, album, song.title)

    def _hassong(self, song):
        '''Check if a song is present in the library.'''
        return song.title in self.songs or os.path.isfile(self.libpath(*song))

    def load_artists(self):
        '''Read the list of album names from lib root dir listing.'''
        return set(
            artist for artist in os.listdir(self._lib_root)
            if os.path.isdir(self.libpath(artist)))

    def load_albums(self):
        '''The set of all album names. (Mapped to artists)'''
        return {
            album: artist
            for artist in self.artists
            for album in os.listdir(self.libpath(artist))
            if os.path.isdir(self.libpath(artist, album))}

    def load_songs(self):
        '''The set of all song names. (Mapped to album)'''
        songs = {}
        for album, artist in self.albums.items():
            if not os.path.isdir(self.libpath(artist, album)):
                continue
            for song in os.listdir(self.libpath(artist, album)):
                if not os.path.isfile(self.libpath(artist, album, song)):
                    continue
                songs[song[len('01. '):-len('.mp3')]] = album
        return songs

    def libpath(self, *path):
        '''Return the path starting at the library root.'''
        return os.path.join(self._lib_root, *path)

    def gen_index(self):
        '''Flat listing of all songs.'''
        for song, album in self.songs.items():
            artist = self.albums[album]
            yield Song(song.lower(), artist.lower(), album.lower())
