import threading
import multiprocessing
import socket
from playsound import playsound

PCName = socket.gethostname()
IPAddr = socket.gethostbyname(PCName)
print(PCName, "@", IPAddr)

host = input("IP address: ")
host = [host, "127.0.0.1"][host == "local"]
host = [host, IPAddr][host == "this"]
port = 5454

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
currentSong = []

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode("UTF-8")
            msg = message.split(": ")[1]

            if msg == "song":
                playsound("1.mp3")
            elif msg == "ping":
                client.send("ping".encode("UTF-8"))
            elif msg[0:4] == "song":
                # global currentSong
                # if len(currentSong) == 1:
                #     currentSong[0].terminate()
                #     del currentSong[0]
                # currentSong.append(multiprocessing.Process(target=playsound, args=(msg[5:] + ".mp3")))
                # currentSong[0].start()
                threading.Thread(target=music, args=(msg[5:])).start()
            else:
                print(message)
                broadcast(message.encode("UTF-8"))
        except:
            index = clients.index(client)
            clients.remove(index)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat".encode("UTF-8"))
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")
        
        client.send("NICK".encode("UTF-8"))
        nickname = client.recv(1024).decode("UTF-8")
        print(f"Nickname: {nickname}")
        clients.append(client)
        nicknames.append(nickname)

        broadcast(f"{nickname} joined the chat!".encode("UTF-8"))
        client.send("Connected to the server!".encode("UTF-8"))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

def music(i):
    playsound(str(i) + ".mp3")

print("Server is listening...")
receive()