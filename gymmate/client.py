import cv2
import io
import socket
import struct
import time
import pickle
import zlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

start=time.time()

while (time.time()-start) <= 180:

    ret, frame = cam.read()  #ret=True is frame is read correctly
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    #data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)
    print(time.time()-start)
    print("{}: {}".format(img_counter, size))
    cv2.imshow('Sending Video',frame)
    client_socket.sendall(struct.pack(">L", size) + data)

cam.release()
cv2.destroyAllWindows()