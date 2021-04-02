def coroutine(func):
    # creating a wrapper for our func and initializing generator
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


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


def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print('......', message)

    return 'Returned from subgen()'


class BlaBlaException(Exception):
    pass


@coroutine
def delegator(g):
    # all this can be done by simply adding yield from
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except BlaBlaException as e:
    #         g.throw(e)

    result = yield from g
    print(result)
