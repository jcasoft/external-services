#!/usr/bin/env python
# Developed by: jcasoft
#               Juan Carlos Argueta
#

from mycroft.configuration import ConfigurationManager
from mycroft.messagebus.service.ws import WebsocketEventHandler
from mycroft.util import validate_param, create_signal

__author__ = 'jcasoft'


from mycroft.messagebus.client.ws import WebsocketClient
from mycroft.messagebus.message import Message
from threading import Thread

ws = None

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
from tornado.options import define, options
import multiprocessing
import json
import time
import os
import socket
from subprocess import check_output

global ip
ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

clients = []

input_queue = multiprocessing.Queue()
output_queue = multiprocessing.Queue()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', ip=ip, port=port)


class StaticFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('js/app.js')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.append(self)
        self.write_message("Welcome to Mycroft")

    def on_message(self, message):
        utterance = json.dumps(message)
        print("*****Utterance : ", utterance)

        if utterance:
            if utterance == '"mic_on"':
                create_signal('startListening')
            else:
                if "|SILENT" in utterance:
                    utterance = utterance.split("|")
                    utterance = utterance[0]
                    data = {
                        "lang": lang,
                        "session": "",
                        "utterances": [utterance],
                        "client": "WebChat"}
                    ws.emit(Message('chat_response', data))
                    ws.emit(Message('recognizer_loop:utterance', data))
                else:
                    data = {
                        "lang": lang,
                        "session": "",
                        "utterances": [utterance]}
                    ws.emit(Message('recognizer_loop:utterance', data))

                t = Thread(target=self.newThread)
                t.start()

    def newThread(self):
        global wait_response
        global skill_response
        timeout = 0
        while wait_response:
            wait_response = True
            time.sleep(1)
            timeout = timeout + 1

        time.sleep(1)


        time.sleep(1)

        if len(skill_response) > 0:
            self.write_message(skill_response)

        skill_response = ""
        wait_response = True

        timeout = 0
        while timeout < 5 or wait_response:
            time.sleep(1)
            timeout = timeout + 1

        if len(skill_response) > 0:
            self.write_message(skill_response)

        wait_response = True
        skill_response = ""

    def on_close(self):
        clients.remove(self)


def connect():
    ws.run_forever()


def handle_speak(event):
    response = event.data['utterance']
    global skill_response, wait_response
    skill_response = ""
    wait_response = False
    skill_response = response


def main():
    global skill_response, wait_response, port, lang
    wait_response = True
    skill_response = ""

    global ws
    ws = WebsocketClient()
    event_thread = Thread(target=connect)
    event_thread.setDaemon(True)
    event_thread.start()

    ws.on('speak', handle_speak)

    import tornado.options

    tornado.options.parse_command_line()
    config = ConfigurationManager.get().get("websocket")
    lang = ConfigurationManager.get().get("lang")

    port = "9090"
    url = ("http://" + str(ip) + ":" + str(port))
    print("*********************************************************")
    print("*   JCASOFT - Mycroft Web Cliento ")
    print("*")
    print("*   Access from web browser " + url)
    print("*********************************************************")

    routes = [
        tornado.web.url(r"/", MainHandler, name="main"),
        tornado.web.url(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': './'}),
        tornado.web.url(r"/ws", WebSocketHandler)
    ]

    settings = {
        "debug": True,
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    application = tornado.web.Application(routes, **settings)
    httpServer = tornado.httpserver.HTTPServer(application)
    tornado.options.parse_command_line()
    httpServer.listen(port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.exception(e)
        event_thread.exit()
        tornado.ioloop.IOLoop.instance().stop()
        sys.exit()


if __name__ == "__main__":
    main()
