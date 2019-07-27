#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from firebase import firebase
import time
import os
import serial
import SocketServer

firebase = firebase.FirebaseApplication('https://chat-9910d.firebaseio.com/')

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("hi!")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data) # <-- Print post data
#	result = firebase.post('/umidadeM', '31.23333')
	if post_data == '1':
		while post_data == '1':
			post_data = self.rfile.read(content_lenght)
			time.sleep(0.5)
		send = firebase.post('/umidadeM',post_data) 
	elif post_data == '2':
		while post_data == '2':
			post_data = self.rfile.read(content_lenght)
			time.sleep(0.5)
		send = firebase.post('/acidezM', post_data)
 	elif post_data == '3':
		while post_data == '3':
			post_data = self.rfile.read(content_lenght)
			time.sleep(0.5)
		send = firebase.post('/tempM',post_data)
# or post_data == 'acidezM' or post_data == 'umidade' or post_data == 'temp' or post_data == 'pluviometro' or post_data == 'acidez':
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
