# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 08:16:12 2018

@author: 14flash
"""

import threading

class Plugin():
    
    def __init__(self, time_to_loop, **kwargs):
        self.time_to_loop = time_to_loop
        self.t_args = tuple()
        self.t_kwargs= dict()
        self.thread = None
        self.stop_event = threading.Event()
    
    def start(self):
        self.thread = threading.Thread(
            target=self._action,
            args=self.t_args,
            kwargs=self.t_kwargs
        )
        self.thread.start()
    
    def stop(self):
        if not self.thread:
            # Thread can't be joined (and is already stopped).
            return
        self.thread.join()
    
    def _action(self, *args, **kwargs):
        while True:
            # Wait for stop event.
            signal = self.stop_event.wait(self.time_to_loop)
            # Break the loop (and thus end the thread) if the stop event was
            # triggered.
            if signal:
                self.stop_event.clear()
                break
            # Otherwise, do the desired action.
            self.action(*args, **kwargs)
            pass
    
    def action(self, *args, **kwargs):
        pass