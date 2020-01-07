import socket
from zlib import compress, decompress
import json
import autopy
import ctypes
import numpy as np
import json
import mss
import pickle
from PIL import ImageGrab as ig, Image
from random import randint
import config

Bypass = True

# security = config.key_setter()
# print(security)

security = 1234

hostname = socket.gethostname()
IPaddr = socket.gethostbyname(hostname)
host = str(IPaddr)
print('host=', host)
port = 5000
WIDTH = 1300
HEIGHT = 768
execute = 1
signaltoclient = 1
buffersize = 1024

user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
send_width = width.to_bytes((width.bit_length() + 7) // 8, 'big')
send_height = height.to_bytes((height.bit_length() + 7) // 8, 'big')

# datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

print('Waiting for incoming connections...........')

# recieving the key
msg, address = sock.recvfrom(1024)
Msg = int.from_bytes(msg, byteorder='big')

if (Msg == 1234):
    Bypass = True
else:
    Bypass = True

# recieving the other computer's resolution
got_width, address2 = sock.recvfrom(1024)
gt_width = int.from_bytes(got_width, byteorder='big')
print('The width is', gt_width)

got_height, address3 = sock.recvfrom(1024)
gt_height = int.from_bytes(got_height, byteorder='big')
print('The height is:', gt_height)

# sending the Host's resolution
sock.sendto(send_width, address)
sock.sendto(send_height, address)

print('Conection incoming from:', address)

state = input('Press A for Accept and R for Reject')

if (state == 'A'):
    STC = signaltoclient.to_bytes((signaltoclient.bit_length() + 7) // 8, 'big')
    sock.sendto(STC, address)

else:
    print('You rejected the proposal')
    sock.close()
    execute = 0

# capturing image and sending it the client
while Bypass == True:
    execute = 1
    while execute == 1:
        (x, y, lb, rb, cb) = (0, 0, 0, 0, 0)
        (w) = (0)

        errs = 0

        image = ig.grab(bbox=(0, 0, 1366, 768))
        # Need to resize it with gt_width
        im_resize = image.resize((1000, 500))

        imre = im_resize.tobytes()
        pixels = compress(imre, 5)

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
        sock.sendto(sizebb, address)
        # print('length sent')

        # error, addresss = sock.recvfrom(1024)
        # err = int.from_bytes(error, byteorder='big')

        # loop for sending the pixels in a buffer size of 100000
        while pixels:
            bytes_sent = sock.sendto(pixels[:buffersize], address)
            pixels = pixels[bytes_sent:]

        error, adrrreesss = sock.recvfrom(1024)
        errs = int.from_bytes(error, byteorder='big')
        # print('sent')
        # print('value of err is', errs)

        # receiving acknowledgement from the client that the image was received fully
        # data, addr = sock.recvfrom(1024)
        # dd = int.from_bytes(data, 'big')
        # print('value=', dd)

        if (errs == 0):

            # recieving the mouse values and automating it
            getmouse, addree = sock.recvfrom(1024)
            getmouse = json.loads(getmouse.decode())
            x = getmouse.get("X")
            y = getmouse.get("Y")
            lb = getmouse.get("lb")
            rb = getmouse.get("rb")
            cb = getmouse.get("cb")
            w = getmouse.get("W")

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
