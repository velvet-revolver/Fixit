import socket
from zlib import decompress
import json
from time import monotonic as timer
import numpy as np
import cv2
from PIL import ImageGrab as ig, Image
import time
import ctypes
import config

kk=config.client_keysetter()

k=kk.to_bytes((kk.bit_length() + 7) // 8, 'big')

host = config.ip_setter()
print('host from client=', host)
port = 5000
signal = 0
WIDTH = 1300
HEIGHT = 768
Completed = 1
message = 'handsake'
exist = True
timesup = 0
buffsize = 1024
Error = 1
Noerror = 0
w = 0



user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
send_width = width.to_bytes((width.bit_length() + 7) // 8, 'big')
send_height = height.to_bytes((height.bit_length() + 7) // 8, 'big')

# binding the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# sending the key
sock.sendto(k, (host, port))

# sending the resolution of the viewing computer
# first width
sock.sendto((send_width), (host, port))
# Now height
sock.sendto((send_height), (host, port))

# recieving the resolution of the host

got_width, address2 = sock.recvfrom(1024)
gt_width = int.from_bytes(got_width, byteorder='big')
print('The width is', gt_width)

got_height, address3 = sock.recvfrom(1024)
gt_height = int.from_bytes(got_height, byteorder='big')
print('The height is:', gt_height)

got, addrr = sock.recvfrom(1024)
GOT = int.from_bytes(got, byteorder='big')


# print('The value of got is:', GOT)


def mouseevents(event, x, y, flags, param):
    global LBtn, RB, LB, CB, xi, yi
    if event == cv2.EVENT_RBUTTONDOWN:
        RB = 1
        xi = (x * gt_width) / width
        yi = (y * gt_height) / height
        print(x, y)
        print(xi, yi)
        print(gt_width)

    elif event == cv2.EVENT_LBUTTONDOWN:
        LB = 1
        xi = (x * gt_width) / width
        yi = (y * gt_height) / height
    elif event == cv2.EVENT_MBUTTONDOWN:
        CB = 1
        xi = (x * gt_width) / width
        yi = (y * gt_height) / height


if (GOT == 1):
    signal = 1

else:
    sock.close()
while signal == 1:

    exist = True
    while (exist == True):

        error = Error.to_bytes((Error.bit_length() + 7) // 8, 'big')
        noerror = Noerror.to_bytes((Noerror.bit_length() + 7) // 8, 'big')

        # recieve the length first in a buffer size of 1024
        length, addr = sock.recvfrom(1024)

        # convert into length
        lengthint = int.from_bytes(length, byteorder='big')
        # print('needed=', lengthint)
        data2 = b''
        full = b''

        sock.settimeout(5)
        # reconstruct the data into full
        while (len(full) < lengthint):
            try:
                data2, addr = sock.recvfrom(buffsize)
            except:
                # sock.sendto(error, (host, port))
                socket.timeout()
                # print('loss here')
                exist = False
                break
            else:
                full = full + data2
                # sock.sendto(noerror, (host, port))
        print('recieved=', len(full))

        if lengthint == len(full):

            (xi, yi, LB, CB, RB) = (0, 0, 0, 0, 0)
            (w) = (0)

            sock.sendto(noerror, (host, port))

            fuller = decompress(full)

            # Need to replace it with the resizing amount
            img2 = Image.frombytes('RGB', (1000, 500), fuller)
            img_np = np.array(img2)

            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

            cv2.imshow("test", frame)
            cv2.namedWindow('test')
            cv2.setMouseCallback('test', mouseevents)

            key = cv2.waitKey(25) & 0xFF

            if key == ord('q'):
                exist = False
                signal = 0
                cv2.destroyAllWindows()
            elif key == ord('w'):
                w = 1

        # print(' image constructed')

        # send acknowledgement to the server that the process is complete
        # print('sending ack')

        # sock.sendto(completedbytes, (host, port))

        # sending the values in json structure for simplicity
        # print('LB=', LB)
        mousedata = json.dumps({"X": xi, "Y": yi, "lb": LB, "rb": RB, "cb": CB, "W": w})
        sock.sendto(mousedata.encode(), (host, port))


else:
    sock.sendto(error, (host, port))
