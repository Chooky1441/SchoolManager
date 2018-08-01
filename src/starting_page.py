import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as tkmsg
import create_schedule, pathlib, schedule, utils


class StartingPage:
    
    def __init__(self, root: tk.Tk, root_frame: tk.Frame):
        self._root = root
        self._root_frame = root_frame
        
        ttk.Style().theme_use('vista')
        
        self._frame = tk.Frame(self._root_frame)
        self._frame.grid(row = 0, column = 0, sticky = tk.NSEW)
        self._frame.columnconfigure(0, weight = 10)
        self._frame.columnconfigure(2, weight = 10)
        self._frame.rowconfigure(2, weight = 1)
        
        self._root.bind('<Control-n>', self.new_schedule)
        self._root.bind('<Control-o>', self.open_schedule)
        self._root.bind('<Control-r>', self.open_recent)
        
        
        self._menu = tk.Menu(self._root)
        file_menu = tk.Menu(self._menu, tearoff = 0)
        file_menu.add_command(label = 'New Schedule', accelerator = 'Ctrl+N', command = self.new_schedule)
        file_menu.add_command(label = 'Open Schedule', accelerator = 'Ctrl+O', command = self.open_schedule)
        file_menu.add_command(label = 'Open Most Recent', accelerator = 'Ctrl+R', command = self.open_recent)
        file_menu.add_command(label = 'Quit', accelerator = 'Ctrl+Q', command = lambda: self._root.destroy())
        self._menu.add_cascade(label = 'File', menu = file_menu)
        self._root.config(menu = self._menu)
        
        utils.create_title(self._frame, 'School Manager', 3)
        ttk.Button(self._frame, text = 'Create New Schedule', command = self.new_schedule).grid(row = 2, column = 0, padx = 10, sticky = tk.E)
        ttk.Button(self._frame, text = 'Open Existing Schedule', command = self.open_schedule).grid(row = 2, column = 1, padx = 10)
        ttk.Button(self._frame, text = 'Open Recent Schedule', command = self.open_recent).grid(row = 2, column = 2, padx = 10, sticky = tk.W)
        tk.Label(self._frame, text = 'By Anthony Navarrette', font = 'Tahoma 10 bold').grid(row = 3, column = 0, pady = 10, sticky = tk.NSEW, columnspan = 3)
    
        self.load_start()
        
        self._schedule = None
        self._courses = None
        
    def open_schedule(self, event = None) -> None:
        schedule_dir = None
        file = None
        try:
            schedule_dir = filedialog.askopenfilename(initialdir = f'schedules/', filetypes =(('JSON Files', "*.json"),), title = 'Open File')
            file = open(schedule_dir)
        except FileNotFoundError:
            if schedule_dir != '':
                tkmsg.showinfo('Error', f'File cannot be opened at the given path.\n{schedule_dir}')
        else: 
            file.close()
            recent = open('schedules/recent.txt', 'w')
            recent.write(pathlib.Path(schedule_dir).parts[-1].replace('.track', ''))
            recent.close()
            schedule.open_schedule(self._root, self._root_frame, open(schedule_dir), self)
            
    def new_schedule(self, event = None) -> None:
        reset = True
        if self._schedule is not None:
            reset = self._schedule.is_default()
            
        if reset:
            if self._schedule is None:
                self._schedule = create_schedule.TkCreateSchedule(self._root, self._root_frame, self)
            else:
                self._schedule.load_schedule()
                
    def open_recent(self, event = None) -> None:
        recent = open('schedules/recent.txt', 'r')
            
        recent_name = recent.readline().rstrip()
        if recent_name != '':
            file = None
            try:
                file = open(f'schedules/{recent_name}')
            except FileNotFoundError:
                tkmsg.showinfo('Warning', f'{recent_name} cannot be found.')
            
            if file is not None:
                file.close()
            schedule.open_schedule(self._root, self._root_frame, open(f'schedules/{recent_name}'), self)
        else:
            tkmsg.showinfo('Warning', f'You have no recently opened schedules.')
            
    def load_start(self) -> None:
        self._schedule = None
        self._frame.tkraise()
        self._root.config(menu = self._menu)
                
        
        
        
        