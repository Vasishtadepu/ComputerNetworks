import socket
import struct
import base64

def unpack_helper(fmt,data):
    size = struct.calcsize(fmt)
    a = struct.unpack(fmt,data[:size])
    final = data[size:]
    # print(type(final))
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


seq = 0
fmt = 'iii'
Flag = 1

#Server Side Code
while Flag:
    image_data = socket_udp.recvfrom(bufferSize)
    a = unpack_helper(fmt,image_data[0])
    expected_seq = seq
    while not a[2]:
        if expected_seq == a[1]:
            file.write(a[3])
            expected_seq = expected_seq + 1
        socket_udp.sendto(str(expected_seq-1).encode(),clientAddressPort)
        image_data = socket_udp.recvfrom(bufferSize)
        a = unpack_helper(fmt,image_data[0])
        if a[2]:
            if expected_seq == a[1]:
                file.write(a[3])
                socket_udp.sendto(str(expected_seq).encode(),clientAddressPort)
                seq = 0
                print("File transfer Complete")
                Flag = 0
            else:
                seq = expected_seq
                socket_udp.sendto(str(expected_seq-1).encode(),clientAddressPort)
file.close()
socket_udp.close()
