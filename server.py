import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.219.100'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

# currentId = "0"
# pos = ["0:50,50", "1:100,100"]


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(0, 0), (150, 150)]


def threaded_client(conn, player):
    # global currentId, pos
    conn.send(str.encode(make_pos(pos[player])))
    # currentId = "1"
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            # reply = data.decode('utf-8')

            # if not data:
            #     conn.send(str.encode("Goodbye"))
            #     break
            # else:
            #     print("Recieved: " + reply)
            #     arr = reply.split(":")
            #     id = int(arr[0])
            #     pos[id] = reply

            #     if id == 0:
            #         nid = 1
            #     if id == 1:
            #         nid = 0

            #     reply = pos[nid][:]
            #     print("Sending: " + reply)

            # conn.sendall(str.encode(reply))

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Connection Closed")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
