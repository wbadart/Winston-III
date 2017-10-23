#!/usr/bin/env python3

'''
' winston/baseline.py
'
' Skeletal implementation of core features. Essentially maps
' specifically structured commands to service calls and outputs.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging
import winston.util as util

from functools import partial
from pdb import post_mortem

from winston.music import Music

PROMPT = '>> '
get_input = util.compose(input, str.lower)


def main(loglevel=loggin.DEBUG):
    '''Main execution/ event loop.'''
    log = logging.getLogger(__name__)
    log.setLevel(loglevel)
    MusicService = Music(library_root='./music_lib', verbose=True)

    usr_in = get_input(PROMPT)
    while usr_in:
        MusicService.dispatch(usr_in)

        #=====================
        usr_in = get_input(PROMPT)


if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass
    except Exception:
        post_mortem()
