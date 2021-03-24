"""
3/23/2021 This is code along for Oleg Molchanov's course on Youtube with some
comments
"""

# This is an imitation of server work to show why do we need async code at all

import socket

# domain:5000 - is a socket that consists of pair (DOMAIN : PORT)

# creating a socket with IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# turning ON reuse of address by switching to 1 param. So aren't timing out
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# configure server to socket info
server_socket.bind(('localhost', 5001))

# start to listen on this port
server_socket.listen()

# .accept() and .send() are block-functions that will stop execution until
#  they're finished handling data - so if we want our server to be able to
#  work with multiple clients we need to implement async methods
while True:
    print('Before .accept()')
    client_socket, addr = server_socket.accept()
    print('Connection from ', addr)

    while True:
        print('Before .recv()')
        # setting message size to 4kB
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            # if we get a message from client response with following(in bytes)
            response = 'Hello world\n'.encode()
            client_socket.send(response)

    client_socket.close()
