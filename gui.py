import tkinter as tk
import threading as Thread
from movement_detector import *
from remote_user import *
from remote_monitor import *
class Gui():
    def __init__(self):
        self.gui = tk.Tk()
        self.set_title()
        self.set_canvas()
        self.set_button()
    
    def set_canvas(self):
        w = tk.Canvas(self.gui, width=40, height=60)
        w.pack()

    def set_title(self):
        self.gui.title('Smart Home Program')
        title ='SMART HOME PROGRAM'
        title_bar = tk.Message(self.gui, text = title, width=200)
        title_bar.pack()
    
    def run_smart_home(self):
        self.gui.destroy()
        m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])
        while True:
            m.run()

    def run(self):
        self.gui.mainloop()
    
    def run_remote_monitor(self):
        self.gui.destroy()
        run_remote_monitor()

    def run_remote_user(self):
        self.gui.destroy()
        run_remote_user()

    def set_button(self):
        start_button = tk.Button(self.gui, text='Start Monitoring (Local)', width=25, command=self.run_smart_home)
        remote_monitor_button = tk.Button(self.gui, text='Start Monitoring (Remote Monitor)', width=25, command=self.run_remote_monitor)
        remote_user_button = tk.Button(self.gui, text='Start Monitoring (Remote User)', width=25, command=self.run_remote_user)
        stop_button = tk.Button(self.gui, text='Stop Program', width=25, command=self.gui.destroy)
        start_button.pack()
        remote_user_button.pack()
        remote_monitor_button.pack()
        stop_button.pack()

g = Gui()
g.run()