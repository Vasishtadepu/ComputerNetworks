import socket
import time
import struct 

def unpack_helper(fmt,data):
    size = struct.calcsize(fmt)
    a = struct.unpack(fmt,data[:size])
    final = data[size:]
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
recieving_socket.settimeout(0.10)

#opening the file for reading
file = open("testFile.jpg","rb")

#creating an array of packets we need to send 
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

#sending of the actual packets
no_of_retransmissions = 0
start = time.time()
for x in packets:
    socket_udp.sendto(x,recieverAddressPort)
    acknowledged = False
    c = unpack_helper(fmt,x)
    while not acknowledged:
        try:
            server_resp = recieving_socket.recvfrom(1024)
            if(int(server_resp[0].decode()) == c[1] ):
                acknowledged = True
        except:
            socket_udp.sendto(x,recieverAddressPort)
            no_of_retransmissions = no_of_retransmissions + 1
end = time.time()
file_size = 1100
print(1100/(end-start))
print(no_of_retransmissions)
socket_udp.close()
file.close()