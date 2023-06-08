import tkinter as tk
import threading as Thread
from movement_detector import *
from remote_user import *
from remote_monitor import *
from PIL import Image, ImageTk
class Gui():
    def __init__(self):
        self.gui = tk.Tk()
        self.set_title()
        self.set_canvas()
        self.status_string = tk.StringVar()
        self.message = tk.StringVar()
        self.status_string.set("Welcome to my smart home!!!")
        self.message.set("")
        self.status = tk.Label(textvariable = self.status_string, width=30, font=('Times', 24)).pack()
        self.message_label = tk.Label(textvariable = self.message, width=40, height=4, background="#34A2FE").pack()
        self.set_button()
        self.currentwork = None
        self.process_list = {'local': False, "monitor": False, "user": False}

        
    
    def set_canvas(self):
        self.mainpage_img = tk.PhotoImage(file = "smart_home.png").subsample(3, 3)
        self.w = tk.Canvas(self.gui, width=640, height=480)
        self.image_container = self.w.create_image(0,0, anchor="nw",image=self.mainpage_img)
        self.w.pack()
        #self.w.itemconfig(self.image_container,image=self.mainpage_img)

    def set_title(self):
        self.gui.title('Smart Home Program')
        title ='SMART HOME PROGRAM'
        title_bar = tk.Message(self.gui, text = title, width=200)
        title_bar.pack()
    
    def run_smart_home(self):
        if (self.process_list['monitor'] == False and self.process_list['user'] == False):
            self.process_list['local'] = True
    
    def set_status(self, status):
        self.status_string.set(status)

    def run_remote_monitor(self):
        if (self.process_list['local'] == False and self.process_list['user'] == False):
            self.process_list['monitor'] = True
        #run_remote_monitor()

    def run_remote_user(self):
        if (self.process_list['local'] == False and self.process_list['monitor'] == False):
            self.process_list['user'] = True
        #run_remote_user()
    
    def end_work(self):
        for process_id in self.process_list:
            self.process_list[process_id] = False
        self.set_status("Welcome to my smart home!!!")
        self.w.itemconfig(self.image_container,image=self.mainpage_img)

    def set_button(self):
        start_button = tk.Button(self.gui, 
                                 text='Start Monitoring (Local)', 
                                 width=25, 
                                 command=lambda: [self.set_status("Running smart home locally"), self.run_smart_home()])
        
        remote_monitor_button = tk.Button(self.gui, 
                                          text='Start Monitoring (Remote Monitor)', 
                                          width=25, 
                                          command=lambda: [self.set_status("Running as remote monitor"), self.run_remote_monitor()])
        remote_user_button = tk.Button(self.gui, 
                                       text='Start Monitoring (Remote User)', 
                                       width=25, 
                                       command=lambda: [self.set_status("Running as remote user"), self.run_remote_user()])
        
        stop_button = tk.Button(self.gui, text='End Current Work', width=25, command=self.end_work)
        start_button.pack()
        remote_user_button.pack()
        remote_monitor_button.pack()
        stop_button.pack()


    def run(self):
        self.m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])
        while True:
            self.gui.update()
            if self.process_list['local']:
                img, message = self.m.run(show=False)
                #Rearrange colors
                blue,green,red = cv2.split(img)
                img = cv2.merge((red,green,blue))
                im = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=im)
                #self.image_container = self.w.create_image(0,0, anchor="CENTER",image=imgtk)
                self.w.itemconfig(self.image_container,image=imgtk)
                #Create a Label to display the image
                if (len(message) != 0):
                    packet = ''
                    for i in message:
                        packet += i
                        packet += '\n'
                    self.message.set(packet)
            elif self.process_list['monitor']:
                run_remote_monitor()
            elif self.process_list['user']:
                run_remote_user()
            

g = Gui()
g.run()