import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import ttk
from scroll_frame import ScrollingFrame
import assignment, root_tracker, utils
               
class Course:
    
    A, A_MINUS, B_PLUS, B, B_MINUS, C_PLUS, C, C_MINUS, D_PLUS, D, D_MINUS, F = 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'
    
    def __init__(self, name: str, units: int, a: float, a_minus: float, b_plus: float, 
                 b: float, b_minus: float, c_plus: float, c: float, c_minus: float, 
                 d_plus: float, d: float, d_minus: float, categories = {}, assignments = {}, grade = A):
        self.name = name
        self.units = units
        self._a = a
        self._a_minus = a_minus
        self._b_plus = b_plus
        self._b = b
        self._b_minus = b_minus
        self._c_plus = c_plus
        self._c = c
        self._c_minus = c_minus
        self._d_plus = d_plus
        self._d = d
        self._d_minus = d_minus
        self.categories = categories
        self.assignments = []
        for name in assignments:
            points, points_total, category = assignments[name].values()
            self.assignments.append(assignment.Assignemnt(name, points, points_total, category))
        self.grade = grade
    
        
    def __str__(self) -> str:
        return f'\n\tName: {self.name}\n\tUnits: {self.units}\n\tCategories: {self.categories}\n\tAssingments: {self.assignments}\n\tGrade: {self.grade}\n'
        
    def calculate_grade(self) -> None:
        if len(self.assignments) > 0:
            cats_used = []
            total_percent = 0
            for a in self.assignments:
                if a.points is not None:
                    if a.category not in cats_used:
                        cats_used.append(a.category)
                    total_percent += (a.points / a.points_total) * self.categories[a.category]
                    self.set_grade((total_percent / sum((self.categories[c] for c in cats_used))) * 100)
                    
    def set_grade(self, p: float) -> None:
        if p >= self._a:
            self.grade = self.A
        elif p >= self._a_minus:
            self.grade = self.A_MINUS
        elif p >= self._b_plus:
            self.grade = self.B_PLUS
        elif p >= self._b:
            self.grade = self.B
        elif p >= self._b_minus:
            self.grade = self.B_MINUS 
        elif p >= self._c_plus:
            self.grade = self.C_PLUS
        elif p >= self._c:
            self.grade = self.C 
        elif p >= self._c_minus:
            self.grade = self.C_MINUS
        elif p >= self._d_plus:
            self.grade = self.D_PLUS
        elif p >= self._d:
            self.grade = self.D 
        elif p >= self._d_minus:
            self.grade = self.D_MINUS
        else:
            self.grade = self.F
        
    
    def get_dict(self) -> dict:
        assignments_dict = {}
        for a in self.assignments:
            assignments_dict.update(a.get_dict())
        
        return {self.name: {'units': self.units, 'a': self._a, 'a_minus': self._a_minus, 'b_plus': self._b_plus, 'b': self._b, 'b_minus': self._b_minus,
                            'c_plus': self._c_plus, 'c': self._c, 'c_minus': self._c_minus, 'd_plus': self._d_plus, 'd': self._d,
                            'd_minus': self._d_minus, 'categories': self.categories, 'assignments': assignments_dict, 'grade': self.grade}}

    def add_assignment(self, a: assignment.Assignemnt) -> None:
        """Adds the given assignment to the course"""
        self.assignments.append(a)
        
    def remove_assignment(self, a: assignment.Assignemnt) -> None:
        """Removes the given assignment from the course"""
        self.assignments.remove(a)
        
class TkCourse:
    def __init__(self, schedule, tkschedule, root_tracker: root_tracker.Root_Tracker):
        self._schedule = schedule
        self._tkschedule = tkschedule
        self._root_tracker = root_tracker
        
        self._root = tk.Tk()
        ttk.Style(self._root).theme_use('vista')
        self._root.minsize(300, 300)
        self._root.title('Add A Course')
        self._root.protocol('WM_DELETE_WINDOW', self.destroy)
        self._root_tracker.add_root(self._root)
        self._root.columnconfigure(0, weight = 1)
        self._root.rowconfigure(2, weight = 1)
            
        self._total_rows = 17
        self._total_categories = 0
            
        utils.create_title(self._root, 'Add A Course', 1, pady = 1)

        self._scroll = ScrollingFrame(self._root, 2, 0, height_border = 105)
        self._scroll_frame = self._scroll.frame
        utils.configure_frame(self._scroll_frame, colspan = 2)
        
        self._name = utils.create_labeled_entry(self._scroll_frame, 'Name:', 0, 0)
        self._units = utils.create_labeled_entry(self._scroll_frame, 'Units:', 1, 0)
        
        utils.create_separator(self._scroll_frame, 2, 0, colspan = 2)
        
        self._a = utils.create_labeled_entry(self._scroll_frame, 'A  cutoff:', 3, insert = '93.5')
        self._a_minus = utils.create_labeled_entry(self._scroll_frame, 'A- cutoff:', 4, insert = '90.0')
        self._b_plus = utils.create_labeled_entry(self._scroll_frame, 'B+ cutoff:', 5, insert = '86.5')
        self._b = utils.create_labeled_entry(self._scroll_frame, 'B  cutoff:', 6, insert = '83.5')
        self._b_minus = utils.create_labeled_entry(self._scroll_frame, 'B- cutoff:', 7, insert = '80.0')
        self._c_plus = utils.create_labeled_entry(self._scroll_frame, 'C+ cutoff:', 8, insert = '76.5')
        self._c = utils.create_labeled_entry(self._scroll_frame, 'C  cutoff:', 9, insert = '73.5')
        self._c_minus = utils.create_labeled_entry(self._scroll_frame, 'C- cutoff:', 10, insert = '70.0')
        self._d_plus = utils.create_labeled_entry(self._scroll_frame, 'D+ cutoff:', 11, insert = '66.5')
        self._d = utils.create_labeled_entry(self._scroll_frame, 'D  cutoff:', 12, insert = '63.5')
        self._d_minus = utils.create_labeled_entry(self._scroll_frame, 'D- cutoff:', 13, insert = '60.0')
        
        self._grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D-']
        self._grades_values = [self._a, self._a_minus, self._b_plus, self._b, self._b_minus, self._c_plus, self._c, self._c_minus, self._d_plus, self._d, self._d_minus]

        utils.create_separator(self._scroll_frame, 14, 0, colspan = 2)
        
        self._categories = []
        
        utils.create_button(self._scroll_frame, 'Add Category', command = self._add_category, row = 999, column = 0, colspan = 2)
        utils.create_button(self._scroll_frame, 'Remove Category', command = self._remove_category, row = 1000, column = 0, colspan = 2)
        
        utils.create_button(self._root, 'Add Course', command = self._create, row = 3, column = 0, colspan = 2)
        
        self._add_category('General', 100).config(state = 'disabled')
        
        print(self._root.winfo_height())
        self._root.mainloop()
        
    def _add_category(self, name = '', percent = 0) -> None:
        """adds a catatory to the screen, also updating the canvas"""
        category_frame = tk.Frame(self._scroll_frame)
        category_frame.grid(row = self._total_rows, column = 0, columnspan = 2, sticky = tk.NSEW)
        utils.configure_frame(category_frame, colspan = 2)
        
        utils.create_label(category_frame, f'Category {self._total_categories + 1}:', 0)
        name = utils.create_labeled_entry(category_frame, 'Name:', 1, insert = name)
        percent = utils.create_labeled_entry(category_frame, 'Percent of Grade:', 2, insert = percent)
        utils.create_separator(category_frame, 3, 0, colspan = 2)
        self._total_rows += 1
        self._total_categories += 1
        self._categories.append((category_frame, name, percent))
        
        self._scroll.update_canvas()
        return name
       

    def _remove_category(self) -> None:
        """removes the most revent category"""
        if len(self._categories) > 1: 
            self._categories[-1][0].destroy()
            self._total_rows -= 1
            self._total_categories -= 1
            del self._categories[-1]
        self._scroll_frame.update_canvas()
        
                
    def _create(self) -> tuple:
        """tries to add the course to the schedule, checking for any invalid inputs"""
        # check if the name is value
        if self._name.get().replace(' ', '') == '':
            tkmsg.showerror('Warning', '"Name" entry cannot be left blank.')
        else:
            # check if units are valid
            try:
                int(self._units.get())
            except (NameError, ValueError):
                tkmsg.showerror('Warning', '"Units" entry must be an integer.')
            else:
                # check that all grades are valid
                for i in range(10):
                    try:
                        if float(self._grades_values[i].get()) <= float(self._grades_values[i + 1].get()):
                            tkmsg.showerror('Warning', f'A grade of {self._grades[i + 1]} must be less than a grade of {self._grades[i]}')
                            break
                    except ValueError:
                        tkmsg.showerror('Warning', 'All grades must be numbers.')
                else:
                    # check that each category has valid inputs (title, name, pecent, sep)
                    total_percent = 0
                    for i in range(len(self._categories)):
                        if self._categories[i][1].get().replace(' ', '') == '':
                            tkmsg.showerror('Warning', f'"Name" entry on Category {i + 1} cannot be left blank.')
                            break
                        else:
                            try:
                                total_percent += float(self._categories[i][2].get())
                            except (NameError, ValueError):
                                tkmsg.showerror('Warning', f'"Percent" of Category {i + 1} must be a number.')
                                break
                    else:
                        # check that the category percent add up to 100 or more  
                        if len(self._categories) > 1 and total_percent < 100:
                            tkmsg.showerror('Warning', f'The percents of all categories must total to 100% or more.\nIt currently totals to {total_percent}%.')
                        elif total_percent > 100:
                            if tkmsg.askyesno('Warning', f'The percents of all categories total to {total_percent}%, is this okay?'):
                                self._create_course()
                        else:
                            self._create_course()
                            
                            
    def _create_course(self) -> None:
        course = Course(self._name.get(), int(self._units.get()), 
                                          float(self._a.get()), float(self._a_minus.get()), 
                                          float(self._b_plus.get()), float(self._b.get()), float(self._b_minus.get()), 
                                          float(self._c_plus.get()), float(self._c.get()), float(self._c_minus.get()), 
                                          float(self._d_plus.get()), float(self._d.get()), float(self._d_minus.get()), 
                                          {name.get(): float(percent.get()) for _, name, percent in self._categories})
        self.destroy()
        self._schedule.add_course(course)
        self._tkschedule.add_tkcourse(course)  
                    
    def destroy(self) -> None:
        """destoys the root window and removes it from the tkschedule list"""
        self._root_tracker.remove_root(self._root)
        self._root.destroy()                    
