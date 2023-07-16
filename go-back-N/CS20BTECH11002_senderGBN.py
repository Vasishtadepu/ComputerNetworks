import socket
import time
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




senderIP = "10.0.0.1"
senderPort   = 20001
senderAddressPort = (senderIP,senderPort)
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 800 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
recieving_socket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
recieving_socket.bind(senderAddressPort)

#Opening the image to be sent
file = open("testFile.jpg","rb")

#Creating an array of packets which are to sent
image_chunk = file.read(bufferSize)
fmt = 'iii'
seq = 0
file_end = 0
packets = []
test = image_chunk
while image_chunk:
    test = image_chunk
    image_chunk = file.read(bufferSize)
    if(not image_chunk):
        file_end = 1
    packet = struct.pack(fmt,len(test),seq,file_end) + test
    packets.append(packet) 
    seq = seq+1



#Actual Go Back N Protocol and sending of packets takes place here
seq = 0
base = 0
window_size = 256
start = time.time()
while seq < len(packets):
    while seq < len(packets) and seq < base + window_size:
        socket_udp.sendto(packets[seq],recieverAddressPort)
        if base == seq:
            recieving_socket.settimeout(0.01)
        seq = seq+1
    while base < seq:
        try:
            recieving_socket.settimeout(0.01)
            server_resp = recieving_socket.recvfrom(1024)
            if base == int(server_resp[0].decode()):
                base = base + 1
            if base < int(server_resp[0].decode()):
                base = int(server_resp[0].decode()) + 1
                if seq < base:
                    seq = base
        except:
            seq = base
            break
end = time.time()
file_size = 1100
print(file_size/(end-start))
socket_udp.close()
file.close()