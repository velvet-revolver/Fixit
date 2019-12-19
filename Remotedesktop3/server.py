import socket
import mss
from zlib import compress, decompress
import json
import autopy

hostname = socket.gethostname()
IPaddr = socket.gethostbyname(hostname)
host = str(IPaddr)
print('host=',host)
port = 50000
WIDTH = 600
HEIGHT = 600
execute = 1
signaltoclient = 1
buffersize = 50240

# datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((host, port))

print('Waiting for incoming connections...........')
msg, address = sock.recvfrom(1024)
#print(msg)
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
while True:
    execute = 1
    while execute == 1:

        errs = 0

        with mss.mss() as sct:
            # The region to capture
            rect = {'top': 0, 'left': 400, 'width': WIDTH, 'height': HEIGHT}
            immage = sct.grab(rect)

        # getting the rgb values of the image and compressing it to level 5
        pixels = compress(immage.rgb, 5)

        # length of the pixels
        size = len(pixels)

        # converting into bytes
        sizebb = size.to_bytes((size.bit_length() + 7) // 8, 'big')
        #print(sizebb)

        lenghtint = int.from_bytes(sizebb, byteorder='big')
        #print(lenghtint)

        # sending the size of the pixels first
        sock.sendto(sizebb, address)
        #print('length sent')

        # error, addresss = sock.recvfrom(1024)
        # err = int.from_bytes(error, byteorder='big')

        # loop for sending the pixels in a buffer size of 100000
        while pixels:
            bytes_sent = sock.sendto(pixels[:buffersize], address)
            pixels = pixels[bytes_sent:]

        error, adrrreesss = sock.recvfrom(1024)
        errs = int.from_bytes(error, byteorder='big')
        #print('sent')
        #print('value of err is', errs)

        # receiving acknowledgement from the client that the image was received fully
        #data, addr = sock.recvfrom(1024)
        #dd = int.from_bytes(data, 'big')
        #print('value=', dd)

        if (errs == 0):

            # recieving the mouse values and automating it
            getmouse, addree = sock.recvfrom(1024)
            getmouse = json.loads(getmouse.decode())
            x = getmouse.get("X")
            y = getmouse.get("Y")
            lb = getmouse.get("lb")
            rb = getmouse.get("rb")
            cb = getmouse.get("cb")
            autopy.mouse.move(x, y)
            if lb == 1:
                autopy.mouse.move(x, y)
                print('left button clicked')
                autopy.mouse.click(autopy.mouse.Button.LEFT)
            elif rb == 1:
                autopy.mouse.move(x, y)
                print('right button')
                autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)
            elif cb == 1:
                print('centre button clicked')
                autopy.mouse.click(autopy.mouse.Button.MIDDLE)

        # execute = int.from_bytes(data, byteorder='big')
        #print('execute=', execute)
