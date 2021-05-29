import socket
import os

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!CLOSE"
SERVER = "192.168.1.78"
ADDR = (SERVER, PORT)
PREFIX = "% "

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    s.send(send_length)
    s.send(message)

def recv(server):
    msg_len = server.recv(HEADER).decode(FORMAT)
    msg = ""
    if msg_len:
        msg_len = int(msg_len)
        msg = server.recv(msg_len).decode(FORMAT)
    return msg

def cls():
    os.system("cls")

print("UnsecureClient v1.0") #refactor all, wrap in own class.
connected = False
while True:
    inp = input(PREFIX)
    inps = inp.split()
    if inps[0] == "connect":
        if connected:
            print("Allready connected")
        else:
            if len(inps) < 3:
                print("missing args")
            else:
                ADDR = inps[1], int(inps[2])
                if not s.connect(ADDR):
                    print(f"Connecting to {ADDR}")
                    rec = recv(s)
                    if rec == "conn" :
                        print("Connected successfully")
                        connected = True
                    else:
                        print("Connection Refused")
                else:
                    print("Server not found")
    print("test")

    if inps[0] == "send":
        if len(inps) < 1:
            print("missing args")
            break
        if connected:
            msg = ""
            for i in range(len(inps) - 1):
                msg += inps[i + 1]
                msg += " "
            send(msg)
        else:
            print("Not connected to server")

    if inps[0] == "exit":
        if connected:
            send(DISCONNECT_MESSAGE)
            connected = False
            print("Disconnected")
            s.close()
            exit()
        else:
            print("Cant close connection, not connected to any server.")


    if connected:
        rec = recv(s)
        if rec == "":
            print("Server did not respond, Closing connection")
            exit()
        print(f"SERVER: {rec}")