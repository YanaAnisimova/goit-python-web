from multiprocessing import Pipe, Process
from sync import factorize
from time import time


def factorize_pipe(number, pipe):
    result = factorize(number)
    pipe.send(result)


if __name__ == '__main__':

    numbers = (128, 255, 99999, 10651060)
    # numbers = (123456780, 123456781, 123456782, 123456783)
    start = time()

    pipes = [Pipe() for number in numbers]
    processes = [Process(target=factorize_pipe, args=(number, pipes[_id][0])) for _id, number in enumerate(numbers)]
    [process.start() for process in processes]

    a, b, c, d = [pipe[1].recv() for pipe in pipes]

    finish = time() - start
    print('Lead time:', round(finish, 3), 's')

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]


# Pipe / numbers = (128, 255, 99999, 10651060)
# Lead time: 1.102 s
# Lead time: 1.17 s
# Lead time: 1.058 s

# Pipe / numbers = (123456780, 123456781, 123456782, 123456783)
# Lead time: 16.029 s
# Lead time: 16.223 s
# Lead time: 15.537 s


