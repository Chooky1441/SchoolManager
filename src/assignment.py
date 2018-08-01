import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
import root_tracker, utils

class Assignemnt:
    def __init__(self, name: str, points: float, points_total: float, category = 'General'):
        self.name = name
        self.points = points
        self.points_total = points_total
        self.category = category
        
    def get_dict(self) -> dict:
        return {self.name: {'points': self.points, 'points_total': self.points_total, 'category': self.category}}
        
class TkAssignment:
    
    COLSPAN = 2
    
    def __init__(self, c: 'Course', course_widget: 'Course Widget', root_tracker: root_tracker.Root_Tracker):
        self._c = c
        self._course_widget = course_widget
        self._root_tracker = root_tracker
        
        self._root = tk.Tk()
        self._root.minsize(300, 300)
        self._root.title('Add An Assignment')
        self._root.protocol('WM_DELETE_WINDOW', self.destroy)
        self._root_tracker.add_root(self._root)
        
        ttk.Style(self._root).theme_use('vista')
        utils.configure_frame(self._root, rowspan = 6, colspan = self.COLSPAN)
        
        utils.create_title(self._root, 'Add An Assignment', self.COLSPAN)
        self._name = utils.create_labeled_entry(self._root, 'Name: ', 2, 0)
        self._points = utils.create_labeled_entry(self._root, 'Points Received: ', 3, 0)
        self._use_points = tk.IntVar(self._root)
        ttk.Checkbutton(self._root, text = 'Not Yet Graded', variable = self._use_points, command = self._disable_points_entry).grid(row = 4)
        self._points_total = utils.create_labeled_entry(self._root, 'Total Points: ', 5, 0)
        self._cat_name = utils.create_label(self._root, 'Category: ', 6, 0)
        self._cat = tk.StringVar(self._root)
        utils.create_option_menu(self._root, self._cat, [cat for cat in self._c.categories], 6, 1)
            
        utils.create_button(self._root, 'Add Assignment', self._create, 7, 0, sticky = tk.EW + tk.S, colspan = 2)
        self._root.mainloop()
        
    def _disable_points_entry(self, event = None) -> None:
        if self._use_points.get() == 0:
            self._points.config(state = 'normal')
        else:
            self._points.config(state = 'disabled')
        
    def _create(self) -> None:
        """Checks that all entries are valid and adds the assignments to the course"""
        if self._name.get().replace(' ', '') == '':
            tkmsg.showerror('Warning', '"Name" entry cannot be left blank.')
        else:
            try:
                if self._use_points.get() == 0:
                    float(self._points.get())
            except (NameError, ValueError):
                tkmsg.showerror('Warning', '"Points Received" entry must be a number.')
            else:
                try:
                    float(self._points_total.get())
                except (NameError, ValueError):
                    tkmsg.showerror('Warning', '"Total Points" entry must be a number.')
                else:
                    if self._use_points.get() == 1:
                        points = None
                    else:
                        points = float(self._points.get())
                    self._course_widget.add_tkassignment(Assignemnt(self._name.get(), points, float(self._points_total.get()), self._cat.get()))
                    self.destroy()
        
    def destroy(self) -> None:
        """destroys the root window and removes it from the tkschedule list"""
        self._root_tracker.remove_root(self._root)
        self._root.destroy() 