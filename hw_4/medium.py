from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import concurrent.futures
import math
import multiprocessing
import time
import datetime


def timed(f, *args, **kwargs):
    start = time.time()
    result = f(*args, **kwargs)
    end = time.time()
    return result, end - start


def job(fn, a, step, from_idx, to_idx, worker_id, fname):
    with open(fname, "a") as f:
        f.write(f"{datetime.datetime.now().isoformat()} worker {worker_id} stared\n")
        result = sum([fn(a + i * step) * step for i in range(from_idx, to_idx)])
        f.write(f"{datetime.datetime.now().isoformat()} worker {worker_id} finished\n")

    return result


def integrate(f, a, b, executor: concurrent.futures.Executor, fname, n_jobs=1, n_iter=1000):
    step = (b - a) / n_iter

    futures = []
    for i in range(n_jobs):
        futures.append(executor.submit(job, f, a, step,  n_iter * i // n_jobs, n_iter * (i + 1) // n_jobs, i, fname))

    return sum([future.result() for future in futures])


if __name__ == "__main__":
    with open("artifacts/medium_logs.txt", "w") as logs, open("artifacts/medium_results.txt", "w") as results:
        def run(exc, name):
            logs.write(f"Run {name} with {i} workers\n")
            result, run_time = timed(lambda: integrate(math.cos, 0, math.pi / 2, exc, "artifacts/medium_logs.txt", n_jobs=i, n_iter=10 ** 7))
            logs.write(f"Result = {result}\nTime = {round(run_time, 2)}\n")

            results.write(f"Run {name} with {i} workers, time = {round(run_time, 2)}\n")

        for i in range(1, multiprocessing.cpu_count() * 2):
            with ThreadPoolExecutor(i) as executor:
                run(executor, "ThreadPoolExecutor")
            with ProcessPoolExecutor(i) as executor:
                run(executor, "ProcessPoolExecutor")
