#!/usr/bin/env

'''
' winston/server/config.py
'
' Defines the shape of the server config object.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

from typing import NamedTuple, List


class ServerConfig(NamedTuple):
    '''
    Defines the expected properties of a server configuration
    object. Probably store as dict and instantiate as kwargs.
    '''
    # IP address for server bind call
    host: str = 'localhost'

    # Port on which to listen for incoming connections
    port: int = 4000

    # Path to service package, relative to runtime WD
    services_root: str = 'winston.services'

    # List of services to support. Give the names of the target
    # modules from the services package.
    services: List[str] = ['music', 'reminders', 'search']
