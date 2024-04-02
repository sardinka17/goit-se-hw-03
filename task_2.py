from multiprocessing import Process, Queue
from time import time


def measure_elapsed_time(fn):
    def inner(*args):
        t = time()
        result = fn(*args)
        print(f"'{fn.__name__}' elapse time: {time() - t} seconds.")

        return result

    return inner


def factorize_single(number: int, queue: Queue = None):
    result = []

    for num in range(1, number + 1):
        if number % num == 0:
            result.append(num)

    if queue:
        queue.put(result)

    return result


@measure_elapsed_time
def factorize(*numbers):
    result = []

    for num in numbers:
        result.append(factorize_single(num))

    return result


@measure_elapsed_time
def factorize_multiprocess(*numbers):
    queue = Queue()
    processes = []
    result = []

    for num in numbers:
        process = Process(target=factorize_single, args=(num, queue))
        processes.append(process)
        process.start()
        result.append(queue.get())

    [pr.join() for pr in processes]

    return result


if __name__ == "__main__":
    a, b, c, d = factorize_multiprocess(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
