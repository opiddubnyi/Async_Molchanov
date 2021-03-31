"""
3/23/2021 This is code along for Oleg Molchanov's course. Video #2
"""

# This is an imitation of server work to show why do we need async code at all

import socket
import selectors


selector = selectors.DefaultSelector()


def server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    # this will define which SOCKET to monitor and what data to look for
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ,
                      data=accept_connection)


def accept_connection(server_socket):

    # to implement async for .accept() we need to wait for connection data
    # in incoming buffer
    client_socket, addr = server_socket.accept()

    selector.register(fileobj=client_socket, events=selectors.EVENT_READ,
                      data=send_message)
    print('Connection from ', addr)


def send_message(client_socket):

    # we need to wait for connection data in incoming buffer from client
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()

        # waiting for send-buffer to clean and be ready to be able to
        # write again
        client_socket.send(response)

    else:
        # we need to unregister before closing connection
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # to get things that are are to be written/read we use .select()
        # returns tuple (key, events). key = SelectorKey <type NamedTuple>
        # which will have same params as our selector, so we can unpack it
        # fileobj
        # events
        # data
        events = selector.select()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)




if __name__ == '__main__':
    server()
    event_loop()
