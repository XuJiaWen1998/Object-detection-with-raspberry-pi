import tkinter as tk
from movement_detector import *

class Gui():
    def __init__(self):
        self.gui = tk.Tk()
        self.set_title()
        self.set_canvas()
        self.set_checklist()
    
    def set_canvas(self):
        w = tk.Canvas(self.gui, width=40, height=60)
        w.pack()
    def set_title(self):
        self.gui.title('Smart Home Program')
        title ='SMART HOME PROGRAM'
        title_bar = tk.Message(self.gui, text = title, width=200)
        title_bar.pack()
    
    def run_smart_home(self):
        m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])
        while True:
            m.run()
    
    def run(self):
        self.gui.mainloop()
    

    def set_checklist(self):
        self.monitor = ['person', 'bottle', 'cup', 'chair', 'door', 'everything']
        self.result = {}
        self.object_list = []
        for item in self.monitor:
            self.result[item] = tk.IntVar()
            self.object_list.append(self.result[item])
            item_button = tk.Checkbutton(self.gui, text=item, variable=self.result[item])
            item_button.pack(anchor="w")
        start_button = tk.Button(self.gui, text='Start Monitoring', width=25, command=self.run_smart_home)
        stop_button = tk.Button(self.gui, text='Stop Program', width=25, command=self.gui.destroy)
        start_button.pack()
        stop_button.pack()

g = Gui()
g.run()