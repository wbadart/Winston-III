#!/usr/bin/env python3

'''
' winston/client/builder.py
'
' Spawn a client with the specified inputter and outputter.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

import getinput
import putoutput

from ..baseclient import Client
from inspect import getmembers, isfunction

inputgetters = dict(getmembers(getinput, isfunction))
outputputters = dict(getmembers(putoutput, isfunction))


def mkclientclass(inputter, outputter, name='MyClient'):
    '''Construct a new Client type with the selected I/O methods.'''
    return type(name, (Client,), dict(
        getinput=inputter, putoutput=outputter))


def main():
    '''Command line interface for constructing custom clients.'''
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument(
        'name',
        help='Name of new client type')
    parser.add_argument(
        'inputter', choices=inputgetters,
        help='Input collection method')
    parser.add_argument(
        'outputter', choices=outputputters,
        help='Output reporting method')
    args = parser.parse_args()

    client_t = mkclientclass(
        args.inputter, args.outputter, args.name)

    try:
        client_t()
    except TypeError as e:
        print('You have an error in your class '
              'configuration: "%s"' % e)


if __name__ == '__main__':
    main()
