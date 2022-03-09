import threading
import multiprocessing
import time


def fib(n):
    result = [0, 1]
    for _ in range(n - 2):
        result.append(result[-1] + result[-2])


def timed(f, *args, **kwargs):
    start = time.time()
    f(*args, **kwargs)
    end = time.time()
    return end - start


def run_sync(f, *args, n=10):
    for _ in range(n):
        f(*args)


def run_threading(func, *args, n=10):
    threads = []
    for _ in range(n):
        t = threading.Thread(target=func, args=args)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def run_multiprocess(func, *args, n=10):
    processes = []
    for _ in range(n):
        p = multiprocessing.Process(target=func, args=args)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    args = (100000,)

    with open("artifacts/easy.txt", "w") as f:
        f.write(f'cpu count: {multiprocessing.cpu_count()}\n\n')
        sync_time = timed(run_sync, fib, *args, n=10)
        f.write(f'Single process run time: {round(sync_time, 2)} n={10}\n')

        threading_time = timed(run_threading, fib, *args, n=10)
        f.write(f'Multithreading time: {round(threading_time, 2)} n={10}\n')

        multiprocessing_time = timed(run_multiprocess, fib, *args, n=10)
        f.write(f'Multiprocessing time: {round(multiprocessing_time, 2)} n={10}\n\n')
