import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import ttk
import utils
from utils import create_labeled_entry


class EditTkSchedule:
    
    def __init__(self, tkschedule):
        self._tkschedule = tkschedule
        self._root = tk.Tk()
        self._root.protocol('WM_DELETE_WINDOW', self._destroy)
        self._root.minsize(300, 300)
        utils.init_root_options(self._root)
        utils.init_theme()
        self._tkschedule._root_tracker.add_root(self._root)
        
        self._frame = tk.Frame(self._root)
        utils.configure_frame(self._root, colspan = 1)
        self._root.rowconfigure(0, weight = 1)
        self._frame.grid(row = 0, column = 0, sticky = tk.NSEW)
        utils.configure_frame(self._frame, colspan = 2)
        for i in range(3):
            self._frame.rowconfigure(i + 2, weight = 1)
        
        utils.create_title(self._frame, 'Edit Schedule', colspan = 2)
        
        name = utils.create_labeled_entry(self._frame, 'Name: ', 2, insert = tkschedule._schedule.name)
        units = utils.create_labeled_entry(self._frame, 'Units: ', 3, insert = tkschedule._schedule.units)
        gpa = utils.create_labeled_entry(self._frame, 'GPA: ', 4, insert = tkschedule._schedule.gpa)
        
        buttons_frame = tk.Frame(self._frame)
        buttons_frame.grid(row = 5, column = 0, columnspan = 2, sticky = tk.NSEW)
        for i in range(2):
            buttons_frame.columnconfigure(i, weight = 1, uniform = 'button')
            
        utils.create_button(buttons_frame, 'Update Schedule', self._update, 5, 0)
        utils.create_button(buttons_frame, 'Cancel', self._cancel, 5, 1)
        
        self._root.mainloop()
        
    def _update(self) -> None:
        pass
    
    def _cancel(self) -> None:
        if tkmsg.askyesno('Warning', 'Are you sure you want to cancel?'):
            self._destroy()
        
        
    def _destroy(self) -> None:
        self._tkschedule._root_tracker.remove_root(self._root)
        self._root.destroy()
        
        