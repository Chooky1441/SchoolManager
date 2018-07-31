import tkinter as tk
from starting_page import StartingPage

class ClassManager:
    
    def __init__(self):
        self._root = tk.Tk()
        self._root.minsize(700, 350)
        self._root.title('School Buddy')
        
        self._root.bind('<Control-q>', self._quit)
        
        self._root_frame = tk.Frame(self._root)
        self._root_frame.pack(fill = tk.BOTH, expand = True)
        self._root_frame.rowconfigure(0, weight = 1)
        self._root_frame.columnconfigure(0, weight = 1)
        
        self._start_page = StartingPage(self._root, self._root_frame)

        self._root.mainloop()
    
    def _quit(self, event = None) -> None:
        self._root.destroy()
        
    def reset(self) -> None:
        for widget in self._root_frame.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    ClassManager()
