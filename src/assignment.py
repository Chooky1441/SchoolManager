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
        
    def update(self, name, points, points_total, category) -> None:
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
        utils.init_root_options(self._root)
        
        self._root.protocol('WM_DELETE_WINDOW', self.destroy)
        self._root_tracker.add_root(self._root)
        
        utils.init_theme()
        utils.configure_frame(self._root, colspan = self.COLSPAN)
        for i in range(5):
            self._root.rowconfigure(i + 2, weight = 1)
            
        self._use_points = tk.IntVar(self._root)
        
        ttk.Checkbutton(self._root, text = 'Not Yet Graded', variable = self._use_points, command = self._disable_points_entry).grid(row = 4)
        self._cat_name = utils.create_label(self._root, 'Category: ', 6, 0)
        self._cat = tk.StringVar(self._root)
        utils.create_option_menu(self._root, self._cat, [cat for cat in self._c.categories], 6, 1)
        
        self._points_entry = None
        
    def _disable_points_entry(self, event = None) -> None:
        if self._use_points.get() == 0:
            self._points.config(state = 'normal')
        else:
            self._points.config(state = 'disabled')
            
    def _check_valid_inputs(self) -> bool:
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
                    if self._use_points.get() == 0:
                        self._points_entry = float(self._points.get())
                    return True
        return False
        
        
    def destroy(self) -> None:
        """destroys the root window and removes it from the tkschedule list"""
        self._root_tracker.remove_root(self._root)
        self._root.destroy() 
        
        
class NewTkAssignment(TkAssignment):
   
    def __init__(self, c: 'Course', course_widget: 'Course Widget', root_tracker: root_tracker.Root_Tracker):
        TkAssignment.__init__(self, c, course_widget, root_tracker)
        self._root.title('Add An Assignment')
        
        utils.create_title(self._root, 'Add An Assignment', self.COLSPAN)
        self._name = utils.create_labeled_entry(self._root, 'Name:', 2, 0)
        self._points = utils.create_labeled_entry(self._root, 'Points Received:', 3, 0)
        self._points_total = utils.create_labeled_entry(self._root, 'Total Points:', 5, 0)
        
        utils.create_button(self._root, 'Add Assignment', self._create, 7, 0, sticky = tk.EW + tk.S, colspan = 2)
        
        self._root.mainloop()
        
    def _create(self) -> None:
        """Adds the assignments to the course"""
        if self._check_valid_inputs():
            self._course_widget.add_tkassignment(Assignemnt(self._name.get(), self._points_entry, float(self._points_total.get()), self._cat.get()))
            self.destroy()
        
        
        
class EditTkAssignment(TkAssignment):
    
    def __init__(self, c: 'Course', course_widget: 'Course Widget', root_tracker: root_tracker.Root_Tracker, a: Assignemnt):
        TkAssignment.__init__(self, c, course_widget, root_tracker)
        self._a = a
        self._root.title('Edit Assignment')
        self._points = a.points
        
        utils.create_title(self._root, f'Edit Assignment', self.COLSPAN)
        self._name = utils.create_labeled_entry(self._root, 'Name:', 2, 0, insert = a.name)
        p = '' if a.points is None else a.points
        self._points = utils.create_labeled_entry(self._root, 'Points Received:', 3, 0, insert = p)
        self._points_total = utils.create_labeled_entry(self._root, 'Total Points:', 5, 0, insert = a.points_total)
        self._cat.set(a.category)
        
        utils.create_button(self._root, 'Update Assignment', self._update_assignment, 7, 0, sticky = tk.EW + tk.S, colspan = 2)
        
        if self._a.points is None:
            self._disable_points_entry()
            
        self._root.mainloop()
        
    def _update_assignment(self) -> None:
        """Updates the assignment"""
        if self._check_valid_inputs():
            #UPDATE THE ASSIGNMENT
            p = None if self._use_points.get() == 1 else float(self._points.get())
            self._a.update(self._name.get(), p, float(self._points_total.get()), self._cat.get())
            self._course_widget.update_assignment(self._a)
            self.destroy()
        