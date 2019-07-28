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

    def fire(self, data, send):
        if data == 1:
            send = firebase.post('/tasks/umidadeM', send)
        elif data == 2:
            send = firebase.post('/tasks/acidezM', send)
        else:
            print("Sensor invalido")
        
    def do_POST(self):
        # Doesn't do anything with posted data
        global content_length
        global data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #print(post_data) # <-- Print post data
#	result = firebase.post('/umidadeM', '31.23333')
        print(type(post_data))
        print(post_data)
        if post_data == '1.00' or post_data == '2.00':
            print("if")
            post_data = float(post_data)
            post_data = int(post_data)
            print(type(post_data))
            print(post_data)
            data = post_data
        else:
            print("else")
            self.fire(data, post_data)
            #if post_data == 1:
	#	while post_data == 1:
                    #print(type(post_data))
		    #post_data = float(post_data)
                    #post_data = int(post_data)
                    #print(post_data)
        #            content_length = int(self.headers['Content-Length'])
	#	    post_data = self.rfile.read(content_length)
		    #print(post_data)
		    #time.sleep(0.2)
	#	print("sucesso")
	#	content_length = int(self.headers['Content-Length'])
	#	post_data = self.rfile.read(content_length)
	#	print("->")
	#	print(post_data)
	#	send = firebase.post('/tasks/umidadeM',post_data) 
	#elif post_data == 2:
	#	while post_data == '2':
	#	    post_data = self.rfile.read(content_lenght)
	#	    time.sleep(0.5)
	#	send = firebase.post('/tasks/acidezM', post_data)
    
# or post_data == 'acidezM' or post_data == 'umidade' or post_data == 'temp' or post_data == 'pluviometro' or post_data == 'acidez':
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
 #   receive = firebase.get('/tasks/Module/Lksz8VLjXCIM7VYhdSZ/taskM', None)
#    print(receive)
    httpd.serve_forever()
    

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
