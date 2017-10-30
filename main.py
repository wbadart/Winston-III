#!/usr/bin/env python3

'''
' main.py
'
' Entry point for Winston III implementations.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging

from pdb import post_mortem
from winston.server import Server


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    log = logging.getLogger(__name__)

    parser.add_argument(
        '-v', '--verbose',
        default=True,
        action='store_true',
        help='enable debugging messages (default:True)')

    args = parser.parse_args()
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        format='[%(levelname)s]: %(message)s', level=loglevel)

    try:
        Server().run()
    except EOFError:
        print('\nGoodbye!')
    except KeyboardInterrupt:
        return
    except Exception:
        post_mortem()


if __name__ == '__main__':
    main()
