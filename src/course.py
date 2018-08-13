import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import ttk
from scroll_frame import ScrollingFrame
import assignment, root_tracker, utils
               
class Course:
    
    A, A_MINUS, B_PLUS, B, B_MINUS, C_PLUS, C, C_MINUS, D_PLUS, D, F = 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F'
    
    def __init__(self, name: str, units: int, a: float, a_minus: float, b_plus: float, 
                 b: float, b_minus: float, c_plus: float, c: float, c_minus: float, 
                 d_plus: float, d: float, categories = {}, assignments = {}, grade = A):
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
        else:
            self.grade = self.F
    
    def update(self, name: str, units: int, a: float, a_minus: float, b_plus: float, 
                 b: float, b_minus: float, c_plus: float, c: float, c_minus: float, 
                 d_plus: float, d: float, categories = {}):
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
        self.categories = categories
        
    
    def get_dict(self) -> dict:
        assignments_dict = {}
        for a in self.assignments:
            assignments_dict.update(a.get_dict())
        
        return {self.name: {'units': self.units, 'a': self._a, 'a_minus': self._a_minus, 'b_plus': self._b_plus, 'b': self._b, 'b_minus': self._b_minus,
                            'c_plus': self._c_plus, 'c': self._c, 'c_minus': self._c_minus, 'd_plus': self._d_plus, 'd': self._d,
                             'categories': self.categories, 'assignments': assignments_dict, 'grade': self.grade}}

    def add_assignment(self, a: assignment.Assignemnt) -> None:
        """Adds the given assignment to the course"""
        self.assignments.append(a)
        
    def remove_assignment(self, a: assignment.Assignemnt) -> None:
        """Removes the given assignment from the course"""
        self.assignments.remove(a)
        self.calculate_grade()
        
class Category:
    
    def __init__(self, frame, name, percent):
        self.frame = frame
        self.name = name
        self.percent = percent
        
class TkCourse:
    
    def __init__(self, schedule, root_tracker: root_tracker.Root_Tracker, c: Course = None):
        self._schedule = schedule
        self._root_tracker = root_tracker
        self._c = c
        
        self._root = tk.Tk()
        utils.init_root_options(self._root)
        utils.init_theme()
        self._root.minsize(300, 300)
        self._root.protocol('WM_DELETE_WINDOW', self.destroy)
        self._root_tracker.add_root(self._root)
        self._root.columnconfigure(0, weight = 1)
        self._root.rowconfigure(2, weight = 1)

        self._scroll = ScrollingFrame(self._root, 2, 0, height_border = 105)
        self._scroll_frame = self._scroll.frame
        utils.configure_frame(self._scroll_frame, rowspan = 100, colspan = 2)
        
        self._grade_cutoffs_frame = utils.create_labelframe(self._scroll_frame, 'Grade Cutoff Percentages', row = 2, column = 0, colspan = 2)
        utils.configure_frame(self._grade_cutoffs_frame, rowspan = 11, colspan = 2)
        
        self._category_frame = utils.create_labelframe(self._scroll_frame, 'Categories', row = 3, column = 0, colspan = 2)
        
        utils.configure_frame(self._category_frame, rowspan = 1, colspan = 1)
        
        self._grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+']
        
        self._categories = dict()
        
        utils.create_button(self._category_frame, 'Add Category', command = self._add_category, row = 0, column = 0, colspan = 2)
        
        self._buttons_frame = tk.Frame(self._root)
        self._buttons_frame.grid(row = 4, column = 0, sticky = tk.NSEW)
        utils.configure_frame(self._buttons_frame, colspan = 2)
        utils.create_button(self._buttons_frame, 'Cancel', command = self._cancel, column = 1)
        
    def _cancel(self) -> None:
        if tkmsg.askyesno('Warning', 'Are you sure you want to cancel?'):
            self._destroy()
        
    def _add_category(self, name = '', percent = 0, is_gen = False) -> None:
        """adds a catatory to the screen, also updating the canvas"""
        category_frame = tk.Frame(self._category_frame)
        category_frame.grid(row = len(self._categories) + 1, column = 0, columnspan = 2, sticky = tk.NSEW)
        utils.configure_frame(category_frame, rowspan = 4, colspan = 2)
        
        if not is_gen:
            utils.create_separator(category_frame, 0, 0, colspan = 2, pady = 10)
        name = utils.create_labeled_entry(category_frame, 'Name:', 1, insert = name)
        percent = utils.create_labeled_entry(category_frame, 'Percent of Grade:', 2, insert = percent)
        
        cat = Category(category_frame, name, percent)
        
        if not is_gen:
            utils.create_button(category_frame, 'Remove', lambda: self._remove_category(id(cat)), 3, 0, sticky = tk.NS)
    
        self._categories.update({id(cat): cat})
        
        self._scroll.update_canvas()
        
        return name
       
       
    def _remove_category(self, cat: int) -> None:
        """removes the most revent category"""
        self._categories[cat].frame.destroy()
        del self._categories[cat]
        self._scroll.update_canvas()
        
        
    def _check_valid_inputs(self) -> bool:
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
                    for _, cat in self._categories.items():
                        if cat.name.get().replace(' ', '') == '':
                            tkmsg.showerror('Warning', f'"Name" entry on cannot be left blank on any categories.')
                            break
                        else:
                            try:
                                total_percent += float(cat.percent.get())
                            except (NameError, ValueError):
                                tkmsg.showerror('Warning', f'"Percent" of Category {cat.name} must be a number.')
                                break
                    else:
                        # check that the category percent add up to 100 or more  
                        if len(self._categories) > 1 and total_percent < 100:
                            tkmsg.showerror('Warning', f'The percents of all categories must total to 100% or more.\nIt currently totals to {total_percent}%.')
                        elif total_percent > 100:
                            if tkmsg.askyesno('Warning', f'The percents of all categories total to {total_percent}%, is this okay?'):
                                return True
                        else:
                            return True
        return False
                    
    def destroy(self) -> None:
        """destroys the root window and removes it from the tkschedule list"""
        self._root_tracker.remove_root(self._root)
        self._root.destroy()   
        
    
class NewTkCourse(TkCourse):
    
    def __init__(self, schedule, tkschedule, root_tracker: root_tracker.Root_Tracker):
        TkCourse.__init__(self, schedule, root_tracker)
        self._tkschedule = tkschedule
        self._root.title('Add A Course')
        
        utils.create_title(self._root, 'Add A Course', 1, pady = 1)
        self._name = utils.create_labeled_entry(self._scroll_frame, 'Name:', 0, 0)
        self._units = utils.create_labeled_entry(self._scroll_frame, 'Units:', 1, 0)
        
        self._a = utils.create_labeled_entry(self._grade_cutoffs_frame, 'A  :', 0, insert = '93.5')
        self._a_minus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'A- :', 1, insert = '90.0')
        self._b_plus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'B+ :', 2, insert = '86.5')
        self._b = utils.create_labeled_entry(self._grade_cutoffs_frame, 'B  :', 3, insert = '83.5')
        self._b_minus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'B- :', 4, insert = '80.0')
        self._c_plus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'C+ :', 5, insert = '76.5')
        self._c = utils.create_labeled_entry(self._grade_cutoffs_frame, 'C  :', 6, insert = '73.5')
        self._c_minus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'C- :', 7, insert = '70.0')
        self._d_plus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'D+ :', 8, insert = '66.5')
        self._d = utils.create_labeled_entry(self._grade_cutoffs_frame, 'D  :', 9, insert = '63.5')
        
        self._grades_values = [self._a, self._a_minus, self._b_plus, self._b, self._b_minus, self._c_plus, self._c, self._c_minus, self._d_plus, self._d]
        
        utils.create_button(self._buttons_frame, 'Add Course', command = self._create, column = 0)
        
        self._add_category('General', 100, True).config(state = 'disabled')
        
        self._root.mainloop()
        
    def _create(self) -> tuple:
        """Adds the course to the schedule"""
        if self._check_valid_inputs():
            course = Course(self._name.get(), int(self._units.get()), 
                                              float(self._a.get()), float(self._a_minus.get()), 
                                              float(self._b_plus.get()), float(self._b.get()), float(self._b_minus.get()), 
                                              float(self._c_plus.get()), float(self._c.get()), float(self._c_minus.get()), 
                                              float(self._d_plus.get()), float(self._d.get()), 
                                              {cat.name.get(): float(cat.percent.get()) for _, cat in self._categories.items()})
            self.destroy()
            self._schedule.add_course(course)
            self._tkschedule.add_tkcourse(course)  
             

class EditTkCourse(TkCourse):
    
    def __init__(self, schedule, root_tracker: root_tracker.Root_Tracker, c: Course, course_widget, tkschedule):
        TkCourse.__init__(self, schedule, root_tracker)   
        self._c = c
        self._root.title('Edit Course')
        self._course_widget = course_widget
        self._tkschedule = tkschedule
        
        utils.create_title(self._root, f'Edit Course', 1, pady = 1)
        
        self._name = utils.create_labeled_entry(self._scroll_frame, 'Name:', 0, 0, insert = self._c.name)
        self._units = utils.create_labeled_entry(self._scroll_frame, 'Units:', 1, 0, insert = self._c.units)
        
         
        
        self._a = utils.create_labeled_entry(self._grade_cutoffs_frame, 'A  :', 3, insert = self._c._a)
        self._a_minus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'A- :', 4, insert = self._c._a_minus)
        self._b_plus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'B+ :', 5, insert = self._c._b_plus)
        self._b = utils.create_labeled_entry(self._grade_cutoffs_frame, 'B  :', 6, insert = self._c._b)
        self._b_minus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'B- :', 7, insert = self._c._b_minus)
        self._c_plus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'C+ :', 8, insert = self._c._c_plus)
        self._c_grade = utils.create_labeled_entry(self._grade_cutoffs_frame, 'C  :', 9, insert = self._c._c)
        self._c_minus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'C- :', 10, insert = self._c._c_minus)
        self._d_plus = utils.create_labeled_entry(self._grade_cutoffs_frame, 'D+ :', 11, insert = self._c._d_plus)
        self._d = utils.create_labeled_entry(self._grade_cutoffs_frame, 'D  :', 12, insert = self._c._d)
        
        self._grades_values = [self._a, self._a_minus, self._b_plus, self._b, self._b_minus, self._c_plus, self._c_grade, self._c_minus, self._d_plus, self._d]
        
        utils.create_button(self._buttons_frame, 'Update Course', command = self._update_course, column = 0)
        
        for cat, percent in self._c.categories.items():
            if cat == 'General':
                self._add_category(cat, percent, True)
            else:
                self._add_category(cat, percent)
        
        self._root.mainloop()
        
        
    def _update_course(self) -> None:
        if self._check_valid_inputs():
            for a in self._c.assignments:
                if a.category not in self._c.categories:
                    if tkmsg.askyesno('Warning', 'You have assignments whose category no longer exists, would like like to proceed?  All assignments who no longer have a category will be put in the "General" category.'):
                        self._run_update_course()
                    break
            else:   
                self._run_update_course()
                
    def _run_update_course(self) -> None:
        self._c.update(self._name.get(), int(self._units.get()), 
                                                  float(self._a.get()), float(self._a_minus.get()), 
                                                  float(self._b_plus.get()), float(self._b.get()), float(self._b_minus.get()), 
                                                  float(self._c_plus.get()), float(self._c_grade.get()), float(self._c_minus.get()), 
                                                  float(self._d_plus.get()), float(self._d.get()), 
                                                  {cat.name.get(): float(cat.percent.get()) for _, cat in self._categories.items()})
        self._c.calculate_grade()
        self._tkschedule.update_projected_gpa()
        self._course_widget.update_course()
        self.destroy()
                 
        
        
        
                     
