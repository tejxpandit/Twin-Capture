# File      : Data Stream Class for Multiprocessing in Python
# Author    : Tej Pandit
# Date      : Oct 2024

import time
import queue
import multiprocessing as mp

class DataStream:
    def __init__(self):
        self.func = self.data_loop
        self.initfunc = self.idle
        self.datafunc = self.idle
        self.enabled = mp.Event()
        self.buffer = mp.Queue()
        self.process = None
        self.time_interval = 1
        self.logging = False

    def idle(self):
        time.sleep(1)

    def setInitFunction(self, func):
        self.initfunc = func

    def setDataFunction(self, func):
        self.datafunc = func
    
    def setBufferFunction(self, func):
        self.func = func

    def setBuffersize(self, buffer_size):
        self.buffer = mp.Queue(maxsize=buffer_size)

    def setTimeInterval(self, time_interval):
        self.time_interval = time_interval

    def enableLogging(self):
        self.logging = True

    def disableLogging(self):
        self.logging = False

    def begin(self):
        self.enabled.set()
        self.process = mp.Process(target=self.func, args=(self.enabled, self.buffer, self.initfunc, self.datafunc, self.time_interval, self.logging, ))
        self.process.start()

    def pause(self):
        self.enabled.clear()

    def unpause(self):
        self.enabled.set()
    
    def end(self):
        self.enabled.clear()
        self.process.terminate()
        self.process.join()

    def getData(self):
        try:
            data = self.buffer.get_nowait()
        except:
            data = None
        return data

    def data_loop(self, enabled, buffer, initfunc, datafunc, time_interval, logging):
        initfunc()
        while True:
            if enabled.is_set():
                data = datafunc()
                try:
                    buffer.put_nowait(data)
                except queue.Full:
                    try:
                        buffer.get_nowait()
                        buffer.put_nowait(data)
                    except queue.Empty:
                        pass
                if logging:
                    print(data)
                time.sleep(time_interval)

    #-----------------
    # EXAMPLE FUNCTION
    # def livedata(self, enabled, buffer):
    #     while True:
    #         if enabled.is_set():
    #             t = time.time()
    #             # Try to add data to the queue without blocking
    #             try:
    #                 buffer.put_nowait(t)
    #             except queue.Full:
    #                 try:
    #                     # Get and discard the oldest item from the queue
    #                     buffer.get_nowait()
    #                     # Add the new data
    #                     buffer.put_nowait(t)
    #                 except queue.Empty:
    #                     pass
    #             time.sleep(0.2)

#----------------
# EXAMPLE : USAGE
if __name__ == '__main__': 
    ds = DataStream()
    ds.setDataFunction(time.time)
    ds.setTimeInterval(1)
    # ds.enableLogging()
    # ds.setBuffersize(2)
    ds.begin()

    while True:
        data = ds.getData()
        print(data)
        time.sleep(0.2)

    # print("run")
    # time.sleep(3)
    # ds.pause()
    # print("pause")
    # time.sleep(3)
    # ds.unpause()
    # print("run again")
    # time.sleep(1)
    # ds.end()
    # print("end")
