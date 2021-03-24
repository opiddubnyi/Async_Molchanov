"""
3/23/2021 This is code along for Oleg Molchanov's course. Video #2
"""

# This is an imitation of server work to show why do we need async code at all

import socket
from select import select

# select - system function for tracking state changes in file objects from
# sockets. In unix systems everything that has .fileno() method is
# considered to be a file.

to_monitor = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()


def accept_connection(server_socket):

    # to implement async for .accept() we need to wait for connection data
    # in incoming buffer
    client_socket, addr = server_socket.accept()
    print('Connection from ', addr)

    to_monitor.append(client_socket)


def send_message(client_socket):

    # we need to wait for connection data in incoming buffer from client
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()

        # waiting for send-buffer to clean and be ready to be able to
        # write again
        client_socket.send(response)

    else:
        to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    while True:

        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        for sock in ready_to_read:

            # if socket is server - append to list for monitoring
            if sock is server_socket:
                accept_connection(sock)

            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
