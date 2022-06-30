# source >> https://www.youtube.com/watch?v=3UOyky9sEQY
# chats don't come through. not sure why

import socket
import threading
import queue
import sys

messages = queue.Queue()
clients = []  # list for client addresses
PORT = int(sys.argv[1])

#create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", PORT))  # bind it to port 9009


# function that receives the messages and stores in queue structure
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass


#takes messages from the queue
def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                print(type(client), f"{client}")
                try:  #if message has "signup_tag" it means that its a new paticipant, chat should be notified
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":") +
                                                1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    else:  # if not new joiner, then just broadcast the message
                        server.sendto(message.encode(), client)
                except:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
print(f"Server started at {PORT}")