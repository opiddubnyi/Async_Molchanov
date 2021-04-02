def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


def subgen():
    x = 'Ready to accept message:'
    message = yield x
    print('Received :', message)


class BlaBlaException(Exception):
    pass


@coroutine
def average():
    count = 0
    summa = 0
    average = None

    while True:
        try:
            x = yield average

        except StopIteration:
            print('Something useful might be here:')

        except BlaBlaException:
            print('Also we van add custom error handling as well')

        else:
            count += 1
            summa += x
            average = round(summa / count, 2)


