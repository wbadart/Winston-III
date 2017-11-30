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

from flask import Flask, redirect, request, send_file, url_for
from ...baseclient import Client


class WinstonWeb(Client):
    '''Provdes a web interface to Winston server.'''
    # app = Flask(__name__)

    # @app.route('/', methods=['GET'])
    def index(name='world'):
        return send_file('templates/index.html')

    # @app.route('/', methods=['POST'])
    def putmsg(self):
        msg = request.form['usr_in']
        self.send(msg)
        return self.recv()

    def getinput(self):
        return ''

    def putoutput(self, msg):
        print(msg)

    # def run(self):
    #     self.app.run()

    @classmethod
    def main(cls):




# if __name__ == '__main__':
        client = cls()

        app = Flask(__name__)

        @app.route('/', methods=['GET'])
        def index():
            return send_file('templates/index.html')

        @app.route('/', methods=['POST'])
        def handle_usrin():
            msg = request.form['usr_in']
            client.send(msg)
            return client.recv()

        app.run()
