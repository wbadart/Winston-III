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
        default='baseline',
        help='target implementation (default:baseline)')

    parser.add_argument(
        '-v', '--verbose',
        default=False,
        action='store_true',
        help='enable debugging messages (default:False)')

    args = parser.parse_args()
    log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

    log.debug('Using module "%s"', args.module)
    winston = import_module(f'winston.{args.module}')

    try:
        winston.main()
    except EOFError:
        print('\nGoodbye!')
    except Exception:
        post_mortem()


if __name__ == '__main__':
    main()
