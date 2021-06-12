```python
import socket as s
import cv2
import pickle
import struct

client_s = s.socket(s.AF_INET,s.SOCK_STREAM)
host_ip = '192.168.128.1'
port = 1234
print("Socket Created Successfully")

# Connecting to the server
# The client socket can use the connect() method, after the socket creation is complete to contact the server socket.
client_s.connect((host_ip,port))
data = b"" # Empty string of defined 1 byte size.

# Return the size of the struct (and hence of the string) corresponding to the given format.
# calcsize() is important function, and is required for function such as struct.pack_into() and
# struct.unpack_from(), which require offset value and buffer as well.
payload_size = struct.calcsize("Q")
print(payload_size)
print("Socket Accepted")

while True:
    while len(data) < payload_size: # 1 byte < 8 bytes
        packet = client_s.recv(2160)
        if not packet: break
        data+=packet # Appending serialized data coming from server (stored in loc var message on in Server.ipynb)
    dynamicSerializedMsg = data[:payload_size] # Data of first 8 bytes.
    data = data[payload_size:] #

    # Unpacks (string to int (of size 8 bytes)) only 8 bytes of data dynamically stored in packed message.
    # [0] refers to element at first index
    msg_size = struct.unpack("Q",dynamicSerializedMsg)[0]

    # len(data) - (One of them: 2152 (max); Defined by strlen passed as an arguement in .recv function)
    # msg_size (One of them:  9044780001777646981; Type - int)
    while len(data) < msg_size:
        data += client_s.recv(2160)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data) # Object Deserialization
    cv2.imshow("Client",frame)
    key = cv2.waitKey(1) & 0xFF

    # In Python, the ord () function accepts a string of unit length as an argument and returns the Unicode equivalence of the passed argument.
    if key  == ord('q'): # 113
        break
client_s.close()
```
