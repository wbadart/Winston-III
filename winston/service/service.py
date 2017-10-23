#!/usr/bin/env python3

'''
' winston/service/service.py
'
' Generic base class for Winston services.
'
' Will Badart <wbadart@nd.edu>
' created: OCT 2017
'''

import logging


class Service(object):
    '''Generic base class for Winston services.'''

    def dispatch(self, cmd_str):
        cmd, *args = cmd_str.split()
        try:
            getattr(self, f'_cmd_{cmd}')(*args)
        except AttributeError:
            log.warning(
                'Attempted to dispatch unsupported command "%s"',
                cmd)
