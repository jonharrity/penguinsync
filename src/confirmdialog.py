from tkinter import *




class ConfirmDialog():
    
    
    def __init__(self, parent, message, callback):
        
        self.callback_func = callback
        self.top = Toplevel(parent)

        Label(self.top, text=message).grid(row=0)
        
        self.text = Entry(self.top)
        self.text.grid(row=1)

        b = Button(self.top, text="OK", command=self.ok)
        b.grid(row=2, pady=5)
        
        
    def ok(self):
        user_input = self.text.get()
        self.callback_func(user_input)
        self.top.destroy()