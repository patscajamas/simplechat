import time
from chat_gui1 import Login
import socket
from threading import Thread
from tkinter import *
import json


login = Login()
login_info = Login.get_login(login)
HOST = login_info[0]
PORT = int(login_info[1])
BUFFERSIZE = 1024
ADDRESS = (HOST, PORT)
USER = login_info[2]
chat_users = []

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(ADDRESS)
client_socket.send(bytes(USER, "utf8"))

def receive():
    while True:
        try:
            message = client_socket.recv(BUFFERSIZE)
            try:
                chat_users = json.loads(message.decode())
                users_output.delete("1.0", END)
                for user in chat_users:
                    users_output.insert(END, f"# {user}\n")
            except:
                decoded_message = message.decode("utf8")
                chat_output.insert(END, message)
        except OSError:
            break

def send(event=None):
    message = input_field.get()
    if message == "{quit}":
        client_socket.send(bytes(message, "utf8"))
        client_socket.close()
        window.quit()
    else:
        message = text_input.get("1.0", END)
        client_socket.send(bytes(message, "utf8"))
        text_input.delete("1.0", END) 
        return "break"

def on_closing(event=None):
    input_field.set("{quit}")
    send()

window = Tk()
window.title('Dumbscord')
window.geometry('850x800')
window.minsize(450,400)
window.iconbitmap("pngegg1.ico")

# creat main containers
top_frame = Frame(window, bg="#34495e", width=800,height=50)
bottom_frame = Frame(window, bg="white", width=800, height=400)

# layout main containers
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)

top_frame.grid(row=0, sticky="ew")
bottom_frame.grid(row=1, sticky="nsew")

# creat top container widget
title = Label(top_frame, text="Welcome to Dumbscord ",bg="#34495e",fg="#ffffff",font=("times",20))
title.pack(pady=(10,0))

# layout of bottom container
bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1,weight=1)

bottom_left = Frame(bottom_frame, bg="#34495e", width=150,height=400)
bottom_right = Frame(bottom_frame, bg="green", width=650, height=400)

bottom_left.grid(row=0, column=0, sticky="ns")
bottom_right.grid(row=0,column=1, sticky="nsew") 

# layout bottom containers
bottom_left.grid_rowconfigure(1,weight=1)
bottom_right.grid_columnconfigure(0,weight=1)
bottom_right.grid_rowconfigure(0, weight=1)

# creat bottom right containers
bottom_right_top = Frame(bottom_right, bg="#34495e", width=600, height=350)
bottom_right_bottom = Frame(bottom_right, bg="#34495e", width=600, height=50)

bottom_right_top.grid(column=0,row=0,sticky="nsew")
bottom_right_bottom.grid(column=0,row=1,sticky="ew")

# layout bottom right containers
bottom_right_top.grid_columnconfigure(0,weight=1)
bottom_right_top.grid_rowconfigure(1,weight=1)
bottom_right_bottom.grid_columnconfigure(0, weight=1)

# creat bottom left widgets
users_label = Label(bottom_left, text="Users", bg="#34495e",fg="#ffffff",font=("times",15))
users_output = Text(bottom_left,width=20, bg="#5d6d7e", fg="#ffffff",font=("times",15))
users_output.bind("<Key>", lambda e: "break")

users_label.grid(column=0, row=0, sticky="nw",padx=10,pady=(5,0))
users_output.grid(column=0,row=1,sticky="nswe",padx=(10,5),pady=(1,10))

# creat bottom right, top widgets
chat_label = Label(bottom_right_top, text="Chat",bg="#34495e",fg="#ffffff",font=("times",15))
chat_output = Text(bottom_right_top, bg="#5d6d7e", fg="#ffffff",font=("times",15))
chat_output.bind("<Key>", lambda e: "break")

chat_label.grid(column=0, row=0, sticky="nw",padx=5,pady=(5,0))
chat_output.grid(column=0, row=1, sticky="nsew", padx=(5,10),pady=(1,5))

# creat bottom right, bottom widgets
input_field = StringVar()
text_input = Text(bottom_right_bottom, height=2,bg="#5d6d7e",fg="#ffffff",font=("times",12))
text_input.grid(sticky="nsew", padx=(5,10), pady=(5,10))

text_input.bind("<Return>",send)
window.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive)
receive_thread.start()
window.mainloop() 
