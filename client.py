import socket
import select
import sys
from Crypto.PublicKey import RSA

server_public_key = RSA.importKey(open('public_key_server.pem', 'rb').read())
mixnet_public_key = RSA.importKey(open('public_key_mediator.pem', 'rb').read())
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 2:
    exit()

port_middle_server = int(sys.argv[1])

server.connect( ('localhost', port_middle_server))

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print (message)
        else:
            message = sys.stdin.readline()
            encrypted_message = server_public_key.encrypt(bytes(message, encoding='utf8'), 32)
            encrypted_message_middle_server = mixnet_public_key.encrypt(encrypted_message[0], 32)
            server.send(encrypted_message_middle_server[0])
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()