import tkinter
from tkinter import ttk
import clientIPy as client
import serverIPy as server
import threading

class app():

    def __init__(self):
        self.create_window = tkinter.Tk("IPyChat")
        self.create_window.geometry("250x220")
        self.mode_window()
        self.create_window.mainloop()

    def chat_window_join(self):
        if self.ip_entry.get() and self.port_entry.get():

            self.row_msg = 1

            self.clear_message = tkinter.StringVar()
            self.chat_window = tkinter.Tk("IPyChat")
            self.chat_window.geometry("300x500")
 
            self.messages_frame = ttk.Frame(master=self.chat_window,height=450, width=290)

            self.messages_frame.grid(column=0,row=0,columnspan=2)
            self.messages = []

            self.chat_entry = ttk.Entry(self.chat_window, width=30, textvariable=self.clear_message)
            self.send_button = ttk.Button(self.chat_window, text="Enviar", command=lambda: self.send_msg_join())

            self.chat_entry.grid(column=0, row=1, padx=10)
            self.send_button.grid(column=1, row=1, padx=10)
            
            self.out_messages = ttk.Treeview(height=22,master=self.messages_frame,column=["in","out"],show="headings")

            self.out_messages.column(0,width=137)
            self.out_messages.heading(0,text=self.ip_entry.get(),anchor="center")
            self.out_messages.column(1,width=137)
            self.out_messages.heading(1,text="YOU",anchor="center")

            self.as_client = client.Client()

            self.out_messages.grid(column=1, row=0, padx=3)

            self.as_client.setHost(self.ip_entry.get())
            self.as_client.setPort(self.port_entry.get())
            
            self.as_client.connect()
            print("connectando")
            self.create_window.destroy()
            self.chat_entry.bind("<Return>", self.send_msg_join)
            
            listening = threading.Thread(target=self.recieving_join)
            listening.start()
            self.chat_window.mainloop()

    def chat_window_create(self):
        if self.port_entry_c.get():
            self.row_msg = 1

            self.clear_message = tkinter.StringVar()
            self.chat_window = tkinter.Tk("IPyChat")
            self.chat_window.geometry("300x500")
 
            self.messages_frame = ttk.Frame(master=self.chat_window,height=450, width=290)

            self.messages_frame.grid(column=0,row=0,columnspan=2)
            self.messages = []

            self.chat_entry = ttk.Entry(self.chat_window, width=30, textvariable=self.clear_message)
            self.send_button = ttk.Button(self.chat_window, text="Enviar", command=lambda: self.send_msg_create())

            self.chat_entry.grid(column=0, row=1, padx=10)
            self.send_button.grid(column=1, row=1, padx=10)
            
            self.out_messages = ttk.Treeview(height=22,master=self.messages_frame,column=["in","out"],show="headings")
            self.as_server = server.Server()
            self.as_server.start()

            self.out_messages.column(0,width=137)
            self.out_messages.heading(0,text=self.as_server.addrclient[0],anchor="center")
            self.out_messages.column(1,width=137)
            self.out_messages.heading(1,text="YOU",anchor="center")


            self.out_messages.grid(column=1, row=0, padx=3)

            listening = threading.Thread(target=self.recieving_create)
            listening.start()
            
            self.create_window.destroy()
            self.chat_entry.bind("<Return>", self.send_msg_create)
            

            self.chat_window.mainloop()

    def recieving_create(self):
        while True:
            listening = threading.Thread(target=self.as_server.client_get)
            listening.start()
            listening.join()
            self.msg = self.as_server.MSGglobal if self.as_server.MSGglobal != None else ""
            print(f"msg:{self.msg}")
            self.out_messages.insert("",index="end",values=(self.msg,""))

    def recieving_join(self):
        while True:
            listening = threading.Thread(target=self.as_client.recive)
            listening.start()
            listening.join()
            self.msg = self.as_client.MSGglobal if self.as_client.MSGglobal != None else ""
            print(f"msg:{self.msg}")
            self.out_messages.insert("",index="end",values=(self.msg,""))

    def send_msg_create(self, *args):
        self.out_messages.insert("",index="end",values=("",self.chat_entry.get()))
        self.as_server.send2(self.chat_entry.get())
        self.chat_entry.delete(0,"end")

    def send_msg_join(self,*args):
        self.out_messages.insert("",index="end",values=("",self.chat_entry.get()))
        self.as_client.send(self.chat_entry.get())
        self.chat_entry.delete(0,"end")

    def server_join(self):
        self.aserver = False
        self.server_mode.destroy()
        self.client_mode.destroy()

        self.info_label2 = ttk.Label(text="Join server:",font="Arial 12")

        self.ip_label = ttk.Label(text="IP:")
        self.ip_entry = ttk.Entry()

        self.port_label = ttk.Label(text="Port:")
        self.port_entry = ttk.Entry()


        self.start = ttk.Button(text="Join",command=lambda: self.chat_window_join())

        #griding
        self.info_label2.grid(column=0,row=3,pady=4)
        
        self.ip_label.grid(column=0,row=4,pady=4)

        self.ip_entry.grid(column=1,row=4,pady=4)

        self.port_label.grid(column=0,row=5,pady=4)

        self.port_entry.grid(column=1,row=5,pady=4)

        self.start.grid(column=0,row=6,pady=10,columnspan=2)
    
    def server_create(self):
        self.aserver = True
        self.server_mode.destroy()
        self.client_mode.destroy()

        self.info_label1 = ttk.Label(text="Create server:",font="Arial 12")

        self.port_label = ttk.Label(text="Port:")
        self.port_entry_c = ttk.Entry()

        self.start_c = ttk.Button(text="Create",command=lambda: self.chat_window_create())
        
        #Griding:

        self.info_label1.grid(column=0,row=0,pady=4)

        self.port_label.grid(column=0,row=2,pady=4)

        self.port_entry_c.grid(column=1,row=2,pady=4)

        self.start_c.grid(column=0,row=6,pady=10,columnspan=2)

    def mode_window(self):
        self.server_mode  = ttk.Button(self.create_window,text="Server",command=lambda: self.server_create())
        self.client_mode = ttk.Button(self.create_window,text="Client",command=lambda: self.server_join())

        self.server_mode.grid(column=0,row=0,pady=70,padx=10)
        self.client_mode.grid(column=1,row=0,pady=70,padx=60)

if __name__ == "__main__":
    app()