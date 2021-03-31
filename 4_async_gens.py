import socket
from select import select


tasks = []

# creating dicts to contain pairs of SOCKET:GENERATOR
to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    while True:
        # returning control until we know that .accept() is ready to read
        yield ('read', server_socket)

        # resume after we know its ready
        client_socket, addr = server_socket.accept()
        print('Connection from ', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield ('read', client_socket)
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = 'Hello world\n'.encode()

            yield ('write', client_socket)
            # send response after buffer is ready
            client_socket.send(response)

    client_socket.close()


def event_loop():
    # while one of these lists/dicts not empty
    while any([tasks, to_read, to_write]):

        while not tasks:
            # select ready sockets if there's nothing in the tasks
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                # retrieving generator from our dict by KEY(socket) and add
                # to tasks
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            # get first generator from tasks which will return state & socket
            task = tasks.pop(0)
            ready, sock = next(task)

            if ready == 'read':
                #  adding generator for ready to read SOCKET
                to_read[sock] = task

            if ready == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done!')


tasks.append(server())
event_loop()


