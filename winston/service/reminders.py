#!/usr/bin/env python3

'''
' winston/service/reminders.py
'
' Implements a simple reminder service for Winston.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging


class Reminders(object):
    '''Interface to winston reminders API.'''

    def __init__(self):
        self._log = logging.getLogger(__name__)
