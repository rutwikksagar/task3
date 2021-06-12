import socket as s
import cv2
import pickle
import struct

# Create Socket
server_s = s.socket(s.AF_INET,s.SOCK_STREAM)
host_name  = s.gethostname()
host_ip = s.gethostbyname(host_name)
print('HOST IP:',host_ip)

# print(host_ip)
port = 1234

s_address = ('192.168.128.1',port)
print("Socket Created Successfully")

#The bind() method of Python's socket class assigns an IP address and a port number to a socket instance.
#The bind() method is used when a socket needs to be made a server socket.
#As server programs listen on published ports, it is required that a port and the IP address to be assigned explicitly to a server socket.
#For client programs, it is not required to bind the socket explicitly to a port.
#The kernel of the operating system takes care of assigning the source IP and a temporary port number.
server_s.bind(s_address)
print("Socket Bind Successfully")

# A server has a listen() method which puts the server into listen mode. This allows the server to listen to incoming connections.
# server_s.listen(backlog) # Maximum no. of quered connections should be at least one.
server_s.listen(5)
print("LISTENING AT:",s_address)

print("Socket Accepted")

while True:
    # The accept() call is used by a server to accept a connection request from a client.
    # When a connection is available, the socket created is ready for use to read data from the process that requested the connection.
    client_s,addr = server_s.accept()
    print('GOT CONNECTION FROM:',addr)
    if client_s:
        vid = cv2.VideoCapture(0)

        while(vid.isOpened()):
            img,frame = vid.read()
            a = pickle.dumps(frame) # Object Serialization (Converting array into a character stream format containing all the information necessary to reconstruct the object later)

            # pack - Return a string containing the values v1, v2, … , that are packed according to the given format
            # (Format strings are the mechanism used to specify the expected layout when packing and unpacking data).
            # The values followed by the format must be as per the format only, else struct.error is raised.
            message = struct.pack("Q",len(a))+a
            client_s.sendall(message)

            cv2.imshow('Server',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_s.close()

print("THANK YOU ALL")
print("Created By TEAM Summer_04_16")a
