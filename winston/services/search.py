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

from logging import getLogger
from pprint import pformat
from requests import get
from service_util import command, ServiceBase


class Service(ServiceBase):
    '''Do a web search.'''
    _API_URI = 'https://api.duckduckgo.com/?q={q}&format=json'

    def __init__(self):
        # super(Service, self).__init_()
        self._log = getLogger(__name__)

    def __call__(self, query):
        response = get(self._API_URI.format(q=query)).json()
        self._log.debug(pformat(response))
        if response['Abstract']:
            return response['Abstract']
        else:
            return response['RelatedTopics'][0]['Text']
