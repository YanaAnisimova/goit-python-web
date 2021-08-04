from multiprocessing import Pool
from sync import factorize
from time import time


if __name__ == '__main__':

    numbers = (128, 255, 99999, 10651060)
    # numbers = (123456780, 123456781, 123456782, 123456783)
    start = time()
    with Pool(processes=4) as pool:
        a, b, c, d = pool.map(factorize, numbers)
    finish = time() - start
    print('Lead time:', round(finish, 2), 's')

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]


# Pool / numbers =(128, 255, 99999, 10651060)
# 4 proc
# Lead time: 1.112 s
# Lead time: 1.227 s
# Lead time: 1.036 s

# 3 proc
# Lead time: 0.982 s
# Lead time: 1.035 s
# Lead time: 1.12 s

# 2 proc
# Lead time: 1.105 s
# Lead time: 1.03 s
# Lead time: 1.006 s

# Pool / numbers = (123456780, 123456781, 123456782, 123456783)
# 4 proc
# Lead time: 17.386 s
# Lead time: 14.44 s
# Lead time: 18.616 s

# 3 proc
# Lead time: 23.182 s
# Lead time: 20.611 s

# 2 proc
# Lead time: 21.33 s
# Lead time: 21.24 s
