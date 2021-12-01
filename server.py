import socket
from _thread import *
import sys
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.219.100'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except:
    print(str(socket.error))
s.listen(3)
print("Waiting...")

score = {}


# def acceptC():
#     global client, server, addr
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server = '192.168.219.100'
#     port = 5555
#     s.bind((server, port))
#     s.listen()
#     client, addr = s.accept()


def threaded_client(conn, addr):
    score[addr[1]] = 0
    conn.send(str.encode("Connected"))
    reply = ""

    while True:
        try:

            data = conn.recv(2048)
            data = data.decode('utf-8')
            print("data: ", data)
            score[addr[1]] = int(data)

            v_max = max(score.values())
            for k in score.keys():
                if v_max == score[k]:
                    reply = k

            if not data:
                print("Disconnected")
                break

            else:
                print("score: ", score)
                print("Received:", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, addr))
