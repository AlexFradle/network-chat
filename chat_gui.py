from tkinter import *
from chat_client import Client
import threading


class ChatWindow(Frame):
    def __init__(self, master, client):
        super().__init__(master)
        self.master = master
        self.pack()
        self.text = StringVar()
        self.client = client
        self.create_widgets()
        self.listen_thread = threading.Thread(target=self.listen, args=(self.client.received,), daemon=True)
        self.listen_thread.start()

    def send_text(self, _):
        temp = self.text.get()
        self.text.set("")
        self.client.send(temp)

    def listen(self, msgs):
        while True:
            if msgs:
                for msg in msgs:
                    self.main_text_area.configure(state=NORMAL)
                    self.main_text_area.insert(END, f"{msg}\n")
                    self.main_text_area.configure(state=DISABLED)
                    self.main_text_area.see(END)
                    self.client.received.remove(msg)

    def create_widgets(self):
        self.main_text_area = Text(self, width=100, height=20, wrap=WORD)
        self.main_text_area.pack()
        text_in_area = Entry(self, width=100, textvariable=self.text)
        text_in_area.bind("<Return>", self.send_text)
        text_in_area.pack()
        quit_ = Button(self, text="QUIT", fg="red", command=self.master.destroy)
        quit_.pack(side="bottom")


if __name__ == '__main__':
    c = Client("192.168.1.16", 51123)
    c.connect()
    root = Tk()
    root.title("Client")
    app = ChatWindow(root, c)
    app.mainloop()
