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

from flask import Flask, render_template, send_file
from ...baseclient import Client


class WinstonWeb(Client):
    '''Provdes a web interface to Winston server.'''
    app = Flask(__name__)

    @app.route('/')
    def index(name='world'):
        return send_file('templates/index.html')

    def getinput(self):
        return ''

    def putoutput(self, msg):
        print(msg)

    def run(self):
        self.app.run()


if __name__ == '__main__':
    WinstonWeb().main()
