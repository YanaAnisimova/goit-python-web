from time import time


def factorize(number):
    return [j for j in range(1, number+1) if number % j == 0]


def collects_result(*numbers):
    return [factorize(number) for number in numbers]


if __name__ == '__main__':

    start = time()
    a, b, c, d = collects_result(128, 255, 99999, 10651060)
    # a, b, c, d = collects_result(123456780, 123456781, 123456782, 123456783)
    finish = time() - start
    print('Lead time:', round(finish, 5), 's')

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]


# numbers =(128, 255, 99999, 10651060)
# Lead time: 0.75001 s
# Lead time: 0.77031 s
# Lead time: 0.77401 s

# numbers = (123456780, 123456781, 123456782, 123456783)
# Lead time: 38.84525 s
# Lead time: 35.75336 s


