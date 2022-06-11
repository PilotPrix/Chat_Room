import threading
import socket
from playsound import playsound
import time

PCName = socket.gethostname()
IPAddr = socket.gethostbyname(PCName)
print(PCName, "@", IPAddr)

address = input("IP address: ")
address = [address, "127.0.0.1"][address == "local"]  # if address is "this", replace with "127.0.0.1"
address = [address, IPAddr][address == "this"]

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 5454))


startTime = 0

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            elif message == "ping":
                print(f"{round((time.time() - startTime) / 1000, 10)}ms")
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        i = input()
        message = f"{nickname}: {i}"
        client.send(message.encode("ascii"))

        if i == "ping":
            global startTime
            startTime = time.time()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()