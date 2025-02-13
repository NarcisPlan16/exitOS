import multiprocessing
import threading
import time

import OptimalScheduler as optimalscheduler
from Application import Application


def backgroundSimulation(gui, os):

    read_pipe, write_pipe = multiprocessing.Pipe()

    t2 = multiprocessing.Process(target=os.startOptimization, args=(write_pipe,))
    t2.start()

    gui.updateProgress(read_pipe)


def checkloop(event: threading.Event):

    while True:

        event.wait()
        backgroundSimulation(app, scheduler)

        time.sleep(2)


if __name__ == "__main__":

    event = threading.Event()
    scheduler = optimalscheduler.OptimalScheduler()
    app = Application(scheduler, event)

    check_loop = threading.Thread(target=checkloop, args=(event,))
    check_loop.start()

    app.mainloop()






