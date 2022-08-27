import socket
from threading import Thread
import sys
import time
import json
from datetime import datetime

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the only server!\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client): 
    name = client.recv(BUFF).decode("utf8")
    welcome = f"Welcome to the server, {name}!\n"
    client.send(bytes(welcome, "utf8"))
    message = f"{name} has joined the chat!\n"
    broadcast(bytes(message, "utf8"))
    time.sleep(0.500)
    clients[client] = name
    usernames.append(name)
    data = json.dumps(usernames).encode("utf8")
    user_broadcast(data)

    while True:
        msg = client.recv(BUFF)
        if msg != bytes("{quit}", "utf8"):
            print(f"<{addresses[client]}><{name}>: {msg}")
            broadcast(msg, f"{name}: ")
        else:
            try:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                usernames.remove(name)
                print(f"<{addresses[client]}><{name}> disconnected 1")
                updated_data = json.dumps(usernames).encode("utf8")
                user_broadcast(updated_data)
                broadcast(bytes(f"{name} has left the chat.", "utf8"))
                break
            except ConnectionResetError:
                client.close()
                del clients[client]
                usernames.remove(name)
                print(f"<{addresses[client]}><{name}> disconnected 2")
                updated_data = json.dumps(usernames).encode("utf8")
                user_broadcast(updated_data)
                broadcast(bytes(f"{name} has left the chat.", "utf8"))
                break

def broadcast(msg, name=""): 
    current_time = datetime.now()
    time_format = current_time.strftime("%I:%M %p")
    for sock in clients:
        sock.send(bytes(f"[{time_format}] {name}","utf8")+msg)

def user_broadcast(json_msg):
    for sock in clients:
        sock.send(json_msg)


usernames = []
clients = {}
addresses = {}

HOST = sys.argv[1]
PORT = int(sys.argv[2])
BUFF = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print(f"[*] Listening as {HOST}:{PORT}")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
