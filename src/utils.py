#cd Desktop/Python/workspace/school_manager
#git add .
#git commit -m ""
#git push origin master

import tkinter as tk
from tkinter import ttk

def create_label(frame, text, row = 0, column = 0, colspan = 1, padx = 5, pady = 5, sticky = tk.NSEW):
    lab = tk.Label(frame, text = text)
    lab.grid(row = row, column = column, columnspan = colspan, padx = padx, pady = pady, sticky = sticky)
    return lab

def create_button(frame, text, command, row = 0, column = 0, sticky = tk.NSEW, padx = 5, pady = 5, colspan = 1) -> ttk.Button:
    button = ttk.Button(frame, text = text, command = command)
    button.grid(row = row, column = column, padx = padx, pady = pady, sticky = sticky, columnspan = colspan)
    return button
    
def create_labeled_entry(frame, label_text, row, column = 0, padx = 5, pady = 5, insert = '') -> tk.Entry:
    tk.Label(frame, text = label_text).grid(row = row , column = column, padx = padx, pady = pady)
    entry = tk.Entry(frame)
    entry.insert(0, insert)
    entry.grid(row = row, column = column + 1, padx = padx, pady = pady)
    return entry

def create_option_menu(frame, str_var, options: [str], row, column, padx = 5, pady = 5) -> ttk.OptionMenu:
    menu = ttk.OptionMenu(frame, str_var, options[0], *options)
    menu.grid(row = row, column = column, padx = padx, pady = pady)
    return menu

def create_title(frame, text, colspan = 0, padx = 5, pady = 5, pack = False) -> None:
    lab = tk.Label(frame, text = text, font = 'Tahoma 18 bold')
    sep = ttk.Separator(frame, orient = tk.HORIZONTAL)
    if pack:
        lab.pack(fill = tk.X, padx = padx, pady = pady)
        sep.pack(fill = tk.X, pady = pady)
    else:
        lab.grid(row = 0, column = 0, columnspan = colspan, sticky = tk.NSEW, padx = padx, pady = pady)
        sep.grid(row = 1, column = 0, columnspan = colspan, sticky = tk.NSEW, pady = pady)
    
def create_separator(frame, row, col, colspan, padx = 5, pady = 5) -> ttk.Separator:
    sep = ttk.Separator(frame, orient = tk.HORIZONTAL)
    sep.grid(row = row, column = col, columnspan = colspan, sticky = tk.NSEW, padx = padx, pady = pady)
    return sep

def raise_frame(frame) -> None:
    frame.tkraise()
    
def clear_frame(frame) -> None:
    for widget in frame.winfo_children():
            widget.destroy()
    
def set_widget_image(widget: 'TkWidget', image: str, x = 1, y = 1) -> None:
    img = tk.PhotoImage(file = image)
    img = img.subsample(x, y)
    widget['image'] = img
    widget.img = img
    
def configure_frame(frame, rowspan = 0, rowoffset = 0, colspan = 0, coloffset = 0) -> None:
    for i in range(rowspan - rowoffset):
        frame.rowconfigure(i + rowspan, weight = 1)
    for i in range(colspan - coloffset):
        frame.columnconfigure(i + coloffset, weight = 1)
        
        
        
