from socket import socket
import ctypes
import json
import cv2
from zlib import compress, decompress
from PIL import Image
import numpy as np
import config

signal = 1
GOT = 1
Error = 1
Noerror = 1
host = config.ip_setter()
port = 5000
buffersize = 40240
user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
print(width, height)

send_width = width.to_bytes((width.bit_length() + 7) // 8, 'big')
send_height = height.to_bytes((height.bit_length() + 7) // 8, 'big')

res = json.dumps({"H": height, "W": width})

kk = config.client_keysetter()
#kk=1234
k = kk.to_bytes((kk.bit_length() + 7) // 8, 'big')
print(kk)

sock = socket()
sock.connect((host, port))

# Sending the security key
sock.send(k)

sock.send(res.encode())

#resolution from server

res_fromserver = sock.recv(buffersize)
res_fromserver = json.loads(res_fromserver.decode())
w = res_fromserver.get("W")
h = res_fromserver.get("H")

print('from server',w)


def mouseevents(event, x, y, flags, param):
    global LBtn, RB, LB, CB, xi, yi
    if event == cv2.EVENT_RBUTTONDOWN:
        RB = 1
        xi = (x * width) / width
        yi = (y * height) / height
        print(x, y)
        print(xi, yi)


    elif event == cv2.EVENT_LBUTTONDOWN:
        LB = 1
        xi = (x * w) / width
        yi = (y * h) / height

    elif event == cv2.EVENT_MBUTTONDOWN:
        CB = 1
        xi = (x * width) / width
        yi = (y * height) / height


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
        length = sock.recv(buffersize)

        # convert into length
        lengthint = int.from_bytes(length, byteorder='big')
        # print('needed=', lengthint)
        data2 = b''
        full = b''

        #sock.settimeout(1)
        # reconstruct the data into full
        while (len(full) < lengthint):
            try:
                data2 = sock.recv(buffersize)
            except:
                # sock.sendto(error, (host, port))
                # socket.timeout()
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

            #sock.send(noerror)

            fuller = decompress(full)

            # Need to replace it with the resizing amount
            img2 = Image.frombytes('RGB', (width,height), fuller)
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
        sock.send(mousedata.encode())


else:
    sock.sendto(error, (host, port))
