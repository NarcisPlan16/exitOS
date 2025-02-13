import threading
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor


def update():
    time.sleep(5)
    print("HI!")


def update2():
    print("començco")
    time.sleep(10)
    print("HOLA!")


if __name__ == "__main__":

    executor = ProcessPoolExecutor(max_workers=2)

    # Submit tasks to the thread pool executor
    executor.submit(update)
    executor.submit(update2)

    executor.shutdown(wait=True)
