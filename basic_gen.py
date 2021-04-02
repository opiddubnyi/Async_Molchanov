import time

queue = []


def counter():
    counter = 0
    while True:
        print(counter)
        counter += 1
        yield


def printer():
    counter = 0
    while True:
        if not counter % 3:
            print('Bang!')
        counter += 1
        yield


def main():
    while True:
        g = queue.pop(0)
        next(g)
        queue.append(g)
        time.sleep(0.3)


if __name__ == '__main__':
    g1 = counter()
    queue.append(g1)
    g2 = printer()
    queue.append(g2)
    main()
