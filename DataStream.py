# File      : Data Stream Class
# Project   : Twin Capture
# Author    : Tej Pandit
# Date      : Oct 2024

import time
import queue
import multiprocessing as mp
import dearpygui.dearpygui as dpg

class DataStream:
    def __init__(self):
        self.func = self.idle
        self.enabled = mp.Value('i', 0) # 0=False, 1=True
        self.buffer = mp.Queue()
        self.process = None

    def idle(self):
        time.sleep(1)

    def setFunction(self, func):
        self.func = func

    def setBuffersize(self, buffer_size):
        self.buffer = mp.Queue(maxsize=buffer_size)

    def begin(self):
        self.enabled = 1
        self.process = mp.Process(target=self.func, args=(self.enabled, self.buffer,))
        self.process.start()

    def pause(self):
        self.enabled = 0

    def unpause(self):
        self.enabled = 1
    
    def end(self):
        self.process.join()

    #-----------------
    # EXAMPLE FUNCTION
    def livedata(self, enabled, buffer):
        while True:
            if enabled:
                t = time.time()
                # Try to add data to the queue without blocking
                try:
                    buffer.put_nowait(t)
                except queue.Full:
                    try:
                        # Get and discard the oldest item from the queue
                        buffer.get_nowait()
                        # Add the new data
                        buffer.put_nowait(t)
                    except queue.Empty:
                        pass
                time.sleep(0.2)

#----------------
# EXAMPLE : USAGE
if __name__ == '__main__': 
    ds = DataStream()
    ds.setFunction(ds.livedata)
    # ds.setBuffersize(1)
    ds.begin()

    while True:
        t = ds.buffer.get()
        print(t)
        print(ds.buffer.qsize())
        time.sleep(1)
