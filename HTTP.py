#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
from firebase import firebase
import time
import os
import serial
import SocketServer
import json

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(37,GPIO.IN)

firebase = firebase.FirebaseApplication('https://chat-9910d.firebaseio.com/')
Receive_serial = serial.Serial('/dev/ttyACM0', 9600)

class S(BaseHTTPRequestHandler):
    #def __init__(self, args):
    #    pass
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("Flavio Bergamini")

    def do_HEAD(self):
        self._set_headers()

    def fire(self, data, send):
        if data == 1:
            firebase.delete('/tasks/umidadeM', None)
            send = firebase.post('/tasks/umidadeM', send)
        elif data == 2:
            firebase.delete('/tasks/acidezM', None)
            send = firebase.post('/tasks/acidezM', send)
        else:
            print("Sensor invalido")
        
    def do_POST(self):
        global content_length
        global data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        
        print(type(post_data))
        print(post_data)
        if post_data == '1.00' or post_data == '2.00':
            post_data = float(post_data)
            post_data = int(post_data)
            print(type(post_data))
            print(post_data)
            data = post_data
            print("entrou")
        else:
            try:
                self.fire(data, post_data)
            except:
                print("Mensagem invalida para ser enviada ao Firebase")
    
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        serialAT()
        
def serialAT():
    print('serial')
    Receive_serial.write('1')
    send = Receive_serial.readline()
    print(send)
    send = send.replace('\r\n','')
    firebase.delete('/tasks/umidade', None)
    send = firebase.post('/tasks/umidade', send)
    
    data = Receive_serial.write('2')
    send = Receive_serial.readline()
    print(send)
    send = send.replace('\r\n','')
    firebase.delete('/tasks/acidez', None)
    send = firebase.post('/tasks/acidez', send)

    Receive_serial.write('3')
    send = Receive_serial.readline()
    print(send)
    send = send.replace('\r\n','')
    firebase.delete('/tasks/temp', None)
    send = firebase.post('/tasks/temp', send)
    
    data = Receive_serial.write('4')
    send = Receive_serial.readline()
    print(send)
    send = send.replace('\r\n','')
    firebase.delete('/tasks/pluv', None)
    send = firebase.post('/tasks/pluv', send)

    if GPIO.RISING:
        firebase.delete('/tasks/bateria', None)
        send = firebase.post('/tasks/bateria', 'Bateia fraca')


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    
    #receive = firebase.get('/tasks/Station', None)
    #receive = str(receive)
    #print(type(receive))
    #print(receive)
    #size = int(len(receive))
    #print(size)
    #receive_process = receive[(size-6):(size-3)]
    #print(receive_process)

    #receiveM = firebase.get('/tasks/Module', None)
    #receiveM = str(receiveM)
    #print(type(receiveM))
    #print(receiveM)
    #size = int(len(receiveM))
    #print(size)
    #receiveM_process = receiveM[(size-6):(size-3)]
    #print(receiveM_process)
    #--parce = json.loads(receive)
    #--print(parce["taskS"])

    #Receive_serial.flushInput()
    #Receive_serial.flushOutput()
    
    #Receive_serial.write('t')
    #ser = Receive_serial.readline()
    #print('---------------------------')
    #print(ser)
    #size = int(len(ser))
    #ser = ser[0:(size-2)]
    #firebase.delete('/tasks/temp', None)
    #send = firebase.post('/tasks/temp', ser)
    #print('---------------------------')

    #Receive_serial.write('a')
    #ser = Receive_serial.readline()
    #print('---------------------------')
    #print(ser)
    #size = int(len(ser))
    #ser = ser[0:(size-2)]
    #firebase.delete('/tasks/acidez', None)
    #send = firebase.post('/tasks/acidez', ser)
    #print('---------------------------')

    #Receive_serial.write('u')
    #ser = Receive_serial.readline()
    #print('---------------------------')
    #print(ser)
    #size = int(len(ser))
    #ser = ser[0:(size-2)]
    #firebase.delete('/tasks/umidade', None)
    #send = firebase.post('/tasks/umidade', ser)
    #print('---------------------------')
    httpd.serve_forever()
    GPIO.add_event_detect(37, GPIO.RISING, callback=serialAT, bouncetime=50)
    
    

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
