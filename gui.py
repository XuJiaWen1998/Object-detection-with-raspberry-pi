import tkinter as tk
import threading as Thread
from movement_detector import *
from remote_user import *
from remote_monitor import *
from PIL import Image, ImageTk
class Gui():
    def __init__(self, IP='127.0.0.1', PORT=8000):
        self.gui = tk.Tk()
        self.IP = IP
        self.PORT = PORT
        self.set_title()
        self.set_canvas()
        self.status_string = tk.StringVar()
        self.message = tk.StringVar()
        self.status_string.set("Welcome to my smart home!!!")
        self.message.set("")
        self.status = tk.Label(textvariable = self.status_string, width=30, font=('Times', 24)).pack()
        self.message_label = tk.Label(textvariable = self.message, width=40, height=3).pack()
        self.set_button()
        self.currentwork = None
        self.process_list = {'local': False, "monitor": False, "user": False}
        self.done = False
        self.connection_established = False
    
    def set_canvas(self):
        self.w = tk.Canvas(self.gui, width=640, height=480)
        self.image_container = self.w.create_image(0,0, anchor="nw")
        self.w.pack()

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

    def set_done(self):
        self.done = True

    def run_remote_monitor(self):
        if (self.process_list['local'] == False and self.process_list['user'] == False):
            self.process_list['monitor'] = True

    def run_remote_user(self):
        if (self.process_list['local'] == False and self.process_list['monitor'] == False):
            self.process_list['user'] = True
    
    def end_work(self):
        if self.process_list['monitor']:
            self.monitor.client_socket.close()
        if self.process_list['user']:
            self.user.close_socket()
        for process_id in self.process_list:
            self.process_list[process_id] = False
        self.connection_established = False
        self.set_status("Welcome to my smart home!!!")

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
        remote_exit_button = tk.Button(self.gui, 
                                       text='Exit', 
                                       width=25, 
                                       command=self.set_done)
        
        stop_button = tk.Button(self.gui, 
                                text='End Current Work', 
                                width=25, 
                                command=self.end_work)
        start_button.pack()
        remote_user_button.pack()
        remote_monitor_button.pack()
        stop_button.pack()
        remote_exit_button.pack()


    def run(self):
        self.m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])
        while True:
            self.gui.update()
            display = True
            if self.done:
                self.end_work()
                break
            if self.process_list['local']:
                img, message = self.m.run(show=False)
            elif self.process_list['monitor']:
                if not self.connection_established:
                    self.monitor = remote_monitor(self.IP, self.PORT)
                    self.connection_established = True
                img, message = self.monitor.run()
            elif self.process_list['user']:
                if not self.connection_established:
                    self.user = remote_user(self.IP, self.PORT)
                    self.connection_established = True
                img, message = self.user.run()
            else:
                display = False

            if display:
                blue,green,red = cv2.split(img)
                img = cv2.merge((red,green,blue))
                im = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=im)
                self.w.itemconfig(self.image_container,image=imgtk)
                self.display(message)

    
    def display(self, message):
        #Create a Label to display the image
        if (len(message) != 0):
            packet = ''
            for i in message:
                packet += i
                packet += '\n'
            self.message.set(packet)


g = Gui()
g.run()