import socket
import struct

def unpack_helper(fmt,data):
    size = struct.calcsize(fmt)
    a = struct.unpack(fmt,data[:size])
    final = data[size:]
    b = (final,)
    c = a+b
    return c


clientIP = "10.0.0.1"
clientPort = 20001
clientAddressPort = (clientIP,clientPort)
recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
file = open("server.jpg","wb")

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))
print("UDP socket created successfully....." )

#server side recieving code
seq = 0
fmt = 'iii'
image_data = socket_udp.recvfrom(bufferSize)
while True:
    a = unpack_helper(fmt,image_data[0])
    if(a[1] == seq):
        file.write(a[3])
        seq = seq + 1
    socket_udp.sendto(str(a[1]).encode(),clientAddressPort)
    if(not a[2]):
        image_data = socket_udp.recvfrom(bufferSize)
    else:
        print("It came here")
        break
print("file close")
file.close()
socket_udp.close()