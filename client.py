import socket
import threading
import random
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

PORT = int(sys.argv[1])

name = input("Nickname?: ")


def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass


t = threading.Thread(target=receive)
t.start()

#when signup happens, print the singed username on the server
client.sendto(f"SIGNUP_TAG: {name}".encode(), ("localhost", PORT))

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost", PORT))