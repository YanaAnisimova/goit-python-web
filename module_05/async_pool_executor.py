from concurrent.futures import ProcessPoolExecutor
from sync import factorize
from time import time


if __name__ == '__main__':

    numbers = (128, 255, 99999, 10651060)
    # numbers = (123456780, 123456781, 123456782, 123456783)
    start = time()
    with ProcessPoolExecutor(4) as executor:
        a, b, c, d = executor.map(factorize, numbers)
    finish = time() - start
    print('Lead time:', round(finish, 3), 's')

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]


# ProcessPoolExecutor / numbers =(128, 255, 99999, 10651060)
# 4 proc
# Lead time: 1.0 s
# Lead time: 1.05 s
# Lead time: 1.06 s

# 3 proc
# Lead time: 1.1 s
# Lead time: 1.14 s
# Lead time: 1.12 s

# 2 proc
# Lead time: 0.97 s
# Lead time: 0.96 s
# Lead time: 1.25 s

# ProcessPoolExecutor / numbers = (123456780, 123456781, 123456782, 123456783)
# 4 proc
# Lead time: 17.434 s
# Lead time: 16.439 s
# Lead time: 17.74 s

# 3 proc
# Lead time: 21.059 s
# Lead time: 22.356 s

# 2 proc
# Lead time: 21.5 s
# Lead time: 24.29 s
