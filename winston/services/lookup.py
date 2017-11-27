#!/usr/bin/env python3

'''
' winston/services/lookup.py
'
' A simple command lookup service, basically for hard-coding
' certain command strings to certain outputs.
' TODO: levenshtein threshold rather than exact equality
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

from service_util import ServiceBase


class Service(ServiceBase):
    '''Implements command lookup table.'''
