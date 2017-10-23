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

from importlib import import_module
from pdb import post_mortem

logging.basicConfig(format='[%(levelname)s]: %(message)s')


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    log = logging.getLogger(__name__)

    parser.add_argument(
        '-m', '--module',
        choices=['baseline', 'main'],
        default='main',
        help='target implementation (default:main)')

    parser.add_argument(
        '-v', '--verbose',
        default=True,
        action='store_true',
        help='enable debugging messages (default:True)')

    args = parser.parse_args()
    loglevel = logging.DEBUG if args.verbose else logging.WARNING
    log.setLevel(loglevel)

    log.debug('Using module "%s"', args.module)
    winston = import_module(f'winston.{args.module}')

    try:
        winston.main(loglevel)
    except EOFError:
        print('\nGoodbye!')
    except KeyboardInterrupt:
        return
    except Exception:
        post_mortem()


if __name__ == '__main__':
    main()
