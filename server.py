import socket
import ctypes
import json
from zlib import compress
import autopy
from PIL import ImageGrab as ig, Image
from random import randint
import config
import tkinter.messagebox
from tkinter import *

hostname = socket.gethostname()
IPaddr = socket.gethostbyname(hostname)
host = str(IPaddr)
print('host=', host)
port = 5000
execute = 1
signaltoclient = 1
buffersize = 40240
state = ''
user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print('Establishing connection...')

conn, addr = s.accept()
print('Connected by', addr)

msg = conn.recv(1024)
Msg = int.from_bytes(msg, byteorder='big')
print(Msg)

if (Msg == 1234):
    Bypass = True

else:
    Bypass = False
    print('Key is wrong')

print(Bypass)

# getting the clients resolution for resizing
res_fromclient = conn.recv(buffersize)
res_fromclient = json.loads(res_fromclient.decode())
w = res_fromclient.get("W")
h = res_fromclient.get("H")
print(w)
print(h)

# send the resolution from here

res_fromhere = json.dumps({"H": height, "W": width})
conn.send(res_fromhere.encode())

while Bypass == True:
    execute = 1
    while execute == 1:
        (x, y, lb, rb, cb) = (0, 0, 0, 0, 0)
        (W) = (0)

        errs = 0

        image = ig.grab(bbox=(0, 0, 1366, 768))
        # Need to resize it with gt_width
        im_resize = image.resize((w, h))

        imre = im_resize.tobytes()
        pixels = compress(imre, 6)

        # getting the rgb values of the image and compressing it to level 5
        # print(pixels)
        # pixels = compress(immage.rgb, 5)

        # length of the pixels
        size = len(pixels)
        print(size)

        # converting into bytes
        sizebb = size.to_bytes((size.bit_length() + 7) // 8, 'big')
        # print(sizebb)

        lenghtint = int.from_bytes(sizebb, byteorder='big')
        # print(lenghtint)

        # sending the size of the pixels first
        conn.send(sizebb)
        # print('length sent')

        # error, addresss = sock.recvfrom(1024)
        # err = int.from_bytes(error, byteorder='big')

        # loop for sending the pixels in a buffer size of 100000
        while pixels:
            bytes_sent = conn.send(pixels[:buffersize])
            pixels = pixels[bytes_sent:]

        #error = conn.recv(buffersize)

        #errs = int.from_bytes(error, byteorder='big')
        #errs=0
        #print('value is: ',errs)
        # print('sent')
        # print('value of err is', errs)

        # receiving acknowledgement from the client that the image was received fully
        # data, addr = sock.recvfrom(1024)
        # dd = int.from_bytes(data, 'big')
        # print('value=', dd)

        if (errs == 0):

            # recieving the mouse values and automating it
            getmouse = conn.recv(buffersize)
            getmouse = json.loads(getmouse.decode())
            x = getmouse.get("X")
            y = getmouse.get("Y")
            lb = getmouse.get("lb")
            rb = getmouse.get("rb")
            cb = getmouse.get("cb")
            W = getmouse.get("W")

            if lb == 1:
                print(x, y)
                autopy.mouse.move(x, y)
                print('left button clicked')
                autopy.mouse.click(autopy.mouse.Button.LEFT, False)
            elif rb == 1:
                autopy.mouse.move(x, y)
                print('right button')
                autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)
            elif cb == 1:
                autopy.mouse.move(x, y)
                print('centre button clicked')
                autopy.mouse.click(autopy.mouse.Button.MIDDLE)
            elif w == 1:
                autopy.key.tap("w", [autopy.key.Modifier.META])
                print('key pressed')
                # autopy.key.tap(autopy.key.Code.TAB, [autopy.key.Modifier.META])
        # execute = int.from_bytes(data, byteorder='big')
        # print('execute=', execute)
