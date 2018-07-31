import tkinter as tk
from tkinter import ttk

class ScrollingFrame:
    def __init__(self, frame: tk.Frame, row = 0, column = 0, columnspan = 1, height_border = 0):
        self._height_border = height_border
        self._parent_frame = frame
        self._frame_canvas = tk.Frame(frame)
        self._frame_canvas.grid(row = row, column = column, columnspan = columnspan, sticky = tk.NSEW)
        self._frame_canvas.rowconfigure(0, weight = 1)
        self._frame_canvas.columnconfigure(0, weight = 1)
        
        self._canvas = tk.Canvas(self._frame_canvas, highlightthickness = 0)
        self._canvas.grid(row = 0, column = 0)
        
        def _on_mousewheel(event):
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), tk.UNITS)
           
        self._canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self._scroll = ttk.Scrollbar(self._frame_canvas, orient = tk.VERTICAL, command = self._canvas.yview)
        self._scroll.grid(row = 0, column = 1, sticky = tk.NS)
        self._canvas.configure(yscrollcommand = self._scroll.set)
        
        self.frame = tk.Frame(self._canvas)
        self._window = self._canvas.create_window((0, 0), window = self.frame, anchor = tk.NW, tags = 'self.frame')
                
        self.frame.bind("<Configure>", self.update_frame)
        self._canvas.bind("<Configure>", self.update_canvas)
        self._previous_width = 0
        self._previous_height = 0
        
        self.update_canvas()
    
    def update_canvas(self, event = None) -> None:
        self.frame.update_idletasks()
        h = self._parent_frame.winfo_height() - self._height_border
        if h < self.frame.winfo_reqheight():
            h = self.frame.winfo_reqheight()
        
        w = self._parent_frame.winfo_width()
        if w < self.frame.winfo_reqwidth():
            w = self.frame.winfo_reqwidth()

        self._canvas.itemconfig(self._window, width = w, height = h)
        
    def update_frame(self, event = None) -> None:
        delta_w, delta_h = abs(self._previous_width - self.frame.winfo_width()), abs(self._previous_height - self.frame.winfo_height())
        if delta_w > 30 or delta_h > 30: 
            self._previous_width = self.frame.winfo_width()
            self._previous_height = self.frame.winfo_height()
            self._canvas.configure(scrollregion = self._canvas.bbox(tk.ALL), width = self.frame.winfo_width(), height = self.frame.winfo_height())
        
        