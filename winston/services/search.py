#!/usr/bin/env python3

'''
' winston/server_utils/service/search.py
'
' Perform a web search on some query.
' See: duckduckgo.com/api
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging

from .service_util import command, Service


class Search(Service):
    '''Do a web search.'''
    _API_URI = 'https://https://api.duckduckgo.com/?q={q}&format=json'

    def __init__(self):
        pass

    def __call__(self, query):
        return get(self._API_URI.format(q=query)).json()['Abstract']
