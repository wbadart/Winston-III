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
from nltk import pos_tag, sent_tokenize
from pprint import pformat
from requests import get
from .util.baseservice import ServiceBase


class Service(ServiceBase):
    '''Do a web search.'''
    _API_URI = 'https://api.duckduckgo.com/?q={q}&format=json'

    def __init__(self, socket, config):
        super().__init__(socket, config)
        self._log = getLogger(__name__)

    def score(self, cmd_tokens):
        '''Claim command if it is a quesiton.'''
        tagged = pos_tag(cmd_tokens)
        print(tagged)
        self._log.debug(tagged)
        return float(tagged[0][1].startswith('W'))

    def dispatch(self, cmd_tokens):
        cmd_str = self.detokenize(cmd_tokens)
        return self.send(self(cmd_str))

    def __call__(self, query):
        response = get(self._API_URI.format(q=query)).json()
        try:
            info = response['Abstract'] or response['RelatedTopics'][0]['Text']
        except IndexError:
            info = 'I couldn\'t find anything for "%s".' % query
        return ' '.join(sent_tokenize(info)[:2])
