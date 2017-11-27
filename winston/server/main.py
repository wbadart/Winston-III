#!/usr/bin/env python3.6

'''
' main.py
'
' Entry point for Winston III implementations.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import json
import logging
import os
import yaml

from pdb import post_mortem
from ._server import Server


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    log = logging.getLogger(__name__)

    parser.add_argument(
        '-c', '--config',
        help='specify path to server config file')

    parser.add_argument(
        '-v', '--verbose',
        default=True,
        action='store_true',
        help='enable debugging messages (default:True)')

    args = parser.parse_args()
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        format='[%(module)s][%(levelname)s]: %(message)s', level=loglevel)
    config = {}

    if args.config and os.path.exists(args.config):
        config_type = (json if args.config.endswith('.json') else yaml)
        with open(args.config) as config_fs:
            config = getattr(config_type, 'load', lambda *_: {})(config_fs)

    try:
        Server(**config).run()
    except (EOFError, KeyboardInterrupt):
        print('\nGoodbye!')
    except Exception:
        post_mortem()


if __name__ == '__main__':
    main()
