import socket
from _thread import *
import sys
import os
from Crypto.PublicKey import RSA
from Crypto import Random

def generate_keys_and_save():
    # Save to a pem file the public key of the server
    current_folder = os.path.dirname(os.path.abspath(__file__))
    os.path.join(current_folder, 'public_key_medidator.pem')
    file = open("public_key_mediator.pem", "wb")
    file.write(private_key.publickey().exportKey())
    file.close()


# Creates Public and Private key
random = Random.new().read
private_key = RSA.generate(1024, random)
public_key = private_key.publickey().exportKey()

generate_keys_and_save()

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    exit()

port_middle_server = int(sys.argv[1])
port_server = int(sys.argv[2])

sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
middle_server_address = ('localhost', port_middle_server)
sock_client.bind(middle_server_address)

print('Starting up on {} port {}'.format(*middle_server_address))
sock_server.connect(('localhost', port_server))

#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
sock_client.listen(100)
list_of_clients=[]

def clientThread(conn, addr):
    conn.send(b"Welcome to this middle server! :)")
    #sends a message to the client whose user object is conn
    while True:
            try:
                message = conn.recv(2048)
                if message is not None:
                    decrypted_message = private_key.decrypt(message)
                    print("Send to server this message")
                    sock_server.send(decrypted_message)
                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    print(len(list_of_clients))
    for clients in list_of_clients:
        # Sends the message of the 'connection client' to the rest of the clients in the chat room
        if clients != connection:
            try:
                print("Sending the message to client")
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def serverThread():
    while True:
        try:
            message = sock_server.recv(2048) # needs to create a connection with server
            if message is not None:
                print("Got a msg from server")
                message_to_send = "<" + addr[0] + "> " + message.decode("utf-8")
                broadcast(bytes(message_to_send, encoding='utf8'),conn)
            else:
                remove(conn)
        except:
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = sock_client.accept()
    list_of_clients.append(conn)
    print (addr[0] + " Connected")

    # Creates and individual thread for every user that connects
    start_new_thread(clientThread,(conn,addr))
    start_new_thread(serverThread, ())

conn.close()
server.close()