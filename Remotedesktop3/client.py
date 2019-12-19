import socket
from zlib import decompress
import pygame
import json
import config
from time import monotonic as timer

host = config.setter()
#host = 'localhost'
print('host from client=', host)
port = 50000
signal = 0
WIDTH = 600
HEIGHT = 600
Completed = 1
message = 'handsake'
exist = True
timesup = 0
buffsize = 50240
Error = 1
Noerror = 0

# binding the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(str.encode(message), (host, port))

got, addrr = sock.recvfrom(1024)
GOT = int.from_bytes(got, byteorder='big')
#print('The value of got is:', GOT)

if (GOT == 1):
    signal = 1
else:
    sock.close()
while signal == 1:
    exist = True
    Completed = 1
    completedbytes = Completed.to_bytes((Completed.bit_length() + 7) // 8, byteorder='big')
    while (exist == True):
        error = Error.to_bytes((Error.bit_length() + 7) // 8, 'big')
        noerror = Noerror.to_bytes((Noerror.bit_length() + 7) // 8, 'big')

        # recieve the length first in a buffer size of 1024
        length, addr = sock.recvfrom(1024)

        # convert into length
        lengthint = int.from_bytes(length, byteorder='big')
        #print('needed=', lengthint)
        data2 = b''
        full = b''

        sock.settimeout(0.5)
        # reconstruct the data into full
        while (len(full) < lengthint):
            try:
                data2, addr = sock.recvfrom(buffsize)
            except:
                # sock.sendto(error, (host, port))
                socket.timeout()
                #print('loss here')
                exist = False
                break
            else:
                full = full + data2
                # sock.sendto(noerror, (host, port))
        #print('recieved=', len(full))

        if lengthint == len(full):

            sock.sendto(noerror, (host, port))

            # decompress the compressed data
            #print('The image is complete')
            data3 = decompress(full)
            #print('decompressed')

            # initialize pygame
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            clock = pygame.time.Clock()

            # construct image from rgb values
            img1 = pygame.image.fromstring(data3, (WIDTH, HEIGHT), 'RGB')
            # Display the picture
            screen.blit(img1, (0, 0))
            pygame.display.flip()
            clock.tick(1000)

            #print(' image constructed')

            # send acknowledgement to the server that the process is complete
            #print('sending ack')

            # sock.sendto(completedbytes, (host, port))

            (x, y, LB, CB, RB) = (0, 0, 0, 0, 0)
            # recording the events in pygame
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exist = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exist = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = pygame.mouse.get_pos()
                    if event.button == pygame.BUTTON_LEFT:
                        LB = 1
                    elif event.button == pygame.BUTTON_RIGHT:
                        RB = 1
                    elif event.button == pygame.BUTTON_MIDDLE:
                        CB = 1
                    break

                # sending the values in json structure for simplicity
            #print('LB=', LB)
            mousedata = json.dumps({"X": x, "Y": y, "lb": LB, "rb": RB, "cb": CB, })
            sock.sendto(mousedata.encode(), (host, port))

        else:
            sock.sendto(error, (host, port))
