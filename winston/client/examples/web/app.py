#!/usr/bin/env python3

'''
' winston/client/examples/web.py
'
' Web interface to Winston server. Interestingly, this client
' is a server.
'
' Will Badart <wbadart@live.com>
' created: NOV 2017
'''

from contextlib import closing
from flask import Flask, g, render_template, request
from ...baseclient import NOPClient


class WinstonWeb(NOPClient):
    '''Provdes a web interface to Winston server.'''
    _USR_MSG_FIELD = 'usr_in'
    _app = Flask(__name__)

    def run(self):
        '''Configure and run the Flask app.'''
        @self._app.route('/', methods=['GET'])
        def index():
            return render_template(
                'index.html', msg_field=self._USR_MSG_FIELD)

        @self._app.route('/', methods=['POST'])
        def handle_usrin():
            '''Exract user message from field, send to server.'''
            msg = request.form[self._USR_MSG_FIELD]
            self.send(msg)
            return self.recv()

        with closing(self._socket), self._app.app_context():
            g._escape = self._escape
            self._app.run()

    @staticmethod
    def _escape(s):
        '''
        Put curly braces around a string
        so they don't get eatean by Jinja.
        '''
        return '{{' + str(s) + '}}'
