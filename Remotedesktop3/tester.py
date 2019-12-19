from time import monotonic as timer  # or time.time if it is not available
data=0
ss = b'\x01'
i=1
ii=i.to_bytes(i.bit_length(),'big')
s = int.from_bytes(ss,byteorder='big')

while(data==0):
    print(ii)
    print(s)
    print(ss)
