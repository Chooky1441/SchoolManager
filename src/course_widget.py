import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
import assignment, course, utils


class Course_Widget:
    
    COLSPAN = 4
    A_COLSPAN = 4
    
    def __init__(self, c: course.Course, schedule_frame: tk.Frame, scroll: tk.Canvas, schedule, root_tracker):
        self._c = c
        self._scroll = scroll
        self._schedule_frame = schedule_frame
        self._schedule = schedule
        self._root_tracker = root_tracker
        self._frame = tk.Frame(self._schedule_frame)
        for i in range(self.COLSPAN):
            self._frame.columnconfigure(i, weight = 1, uniform = 'course')
            
        self._assignments_widgets = dict()
        
        # initializes the name frame and label
        name_frame = tk.Frame(self._frame)
        name_frame.grid(row = 0, column = 0, sticky = tk.EW)
        for i in range(2):
            name_frame.columnconfigure(i, weight = 1, uniform = 'name')
        
        utils.create_label(name_frame, self._c.name, 0, 1, sticky = tk.W)    
        
        # initializes the course info
        self._units = utils.create_label(self._frame, self._c.units, 0, 1, padx = 0)
        self._amt = utils.create_label(self._frame, len(self._c.assignments), 0, 2, padx = 0)
        self._grade = utils.create_label(self._frame, self._c.grade, 0, 3, padx = 0)
        
        # initializes the course drop down
        self._course_frame = tk.Frame(self._frame)
        self._course_frame.grid(row = 1, column = 0, columnspan = self.COLSPAN, sticky = tk.NSEW)
        utils.configure_frame(self._course_frame, rowspan = 2, colspan = 1)
        self._course_frame.grid_remove()
        
        # initializes the options frame
        options_frame = ttk.LabelFrame(self._course_frame, text = 'Options', borderwidth = 15, labelanchor = tk.N)
        options_frame.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 30, pady = 10)
        utils.configure_frame(options_frame, colspan = 3)
        utils.create_button(options_frame, 'Add Assignment', lambda: self._create_assignment(), 0, 0)
        utils.create_button(options_frame, 'Edit Course', lambda: self._edit_course(), 0, 1)
        utils.create_button(options_frame, 'Remove Course', lambda: self._remove_tkcourse(), 0, 2)

        # initializes the assignments frame
        self._assignments_frame = ttk.LabelFrame(self._course_frame, text = 'Assignments', borderwidth = 15, labelanchor = tk.N)
        self._assignments_frame.grid(row = 1, column = 0, sticky = tk.NSEW, padx = 30, pady = 10)
        for i in range(self.A_COLSPAN):
            self._assignments_frame.columnconfigure(i, weight = 1, uniform = 'assignment')    
        
        # initializes the drop down button
        icon = tk.Button(name_frame, command = lambda: self._course_menu(icon), width = 16, height = 16)
        utils.set_widget_image(icon, 'res/arrow.png', 2, 2)
        icon['border'] = '0'
        icon.state = 'hidden'
        icon.grid(row = 0, column = 0)
        
        if len(self._c.assignments) < 1:
            self._clear_assignments_info()
        else:
            self._init_assignments_info()
            for i in range(len(self._c.assignments)):
                self._update_tkassignment(self._c.assignments[i], i + 1)
                
        utils.create_separator(self._frame, 2, 0, self.COLSPAN, 0, 10)
    
        
    def _edit_course(self) -> None:
        print('edit course')
        
    def _remove_tkcourse(self) -> None:
        """Confirms that the user wants to remove the course, then removes it"""
        if tkmsg.askyesno('Warning', f'Are you sure you want to completely remove {self._c.name} and its assignments?'):
            self._schedule.remove_course(self._c)
            self.destroy()
            
    def _course_menu(self, icon) -> None:
        """updates the drop-down arrow and displays/hides a course's assignments"""
        if icon.state == 'shown':
            self._course_frame.grid_remove() 
            icon.state = 'hidden'
            utils.set_widget_image(icon, 'res/arrow.png', 2, 2)
        else:
            self._course_frame.grid()
            icon.state = 'shown'
            utils.set_widget_image(icon, 'res/arrow2.png', 2, 2)
        self._scroll.update_canvas()
        
    def grid(self, row = 0, column = 0) -> None:
        self._frame.grid(row = row, column = column, sticky = tk.NSEW)
        
    def destroy(self) -> None:
        for widget in self._frame.winfo_children():
            widget.destroy()
        self._frame.destroy()
        
        
    # ASSIGNMENT METHODS
            
    def add_tkassignment(self, a: assignment.Assignemnt) -> None:
        self._c.add_assignment(a)
        self._c.calculate_grade()
        self._amt.config(text = len(self._c.assignments))
        self._grade.config(text = self._c.grade)
        self._update_tkassignment(a)
            
    def _create_assignment(self) -> None:
        assignment.TkAssignment(self._c, self, self._root_tracker)
        
    def _edit_assingment(self, a: assignment.Assignemnt, event = None) -> None:
        print('edit assingment')
        
    def _remove_assignment(self, a: assignment.Assignemnt, event = None) -> None:
        """Confirms that the user wants to remove the assignment, then removes it"""
        if tkmsg.askyesno('Warning', f'Are you sure you want to remove {a.name} from {self._c.name}?'):
            self._c.remove_assignment(a)
            if len(self._c.assignments) < 1:
                self._clear_assignments_info()
            for widget in self._assignments_widgets[a.name]:
                self._assignments_widgets[a.name][widget].destroy()
            del self._assignments_widgets[a.name]        
        
    def _init_assignments_info(self) -> None:
        """inits the info bar in the assignments frame"""
        utils.clear_frame(self._assignments_frame)
        tk.Label(self._assignments_frame, text = '{:^20}'.format('Category'), bg = 'dark grey', bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 0, column = 1, sticky = tk.EW)
        tk.Label(self._assignments_frame, text = '{:^20}'.format('Name'), bg = 'dark grey', bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 0, column = 0, sticky = tk.EW)
        tk.Label(self._assignments_frame, text = '{:^20}'.format('Points Received'), bg = 'dark grey', bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 0, column = 2, sticky = tk.EW)
        tk.Label(self._assignments_frame, text = '{:^20}'.format('Total Points'), bg = 'dark grey', bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 0, column = 3, sticky = tk.EW)

    def _clear_assignments_info(self) -> None:
        """clears any widgets in the frame and adds in the no assignments message"""
        utils.clear_frame(self._assignments_frame)
        utils.create_label(self._assignments_frame, 'You currently have no assignments.', 1, 0, colspan = self.A_COLSPAN)
           
    def _update_tkassignment(self, a: assignment.Assignemnt, row = None) -> None:
        """adds an assignment to the given course and updates the status bar"""    
        if row is None:
            row = len(self._c.assignments)
            
        menu = ttk.Menubutton(self._assignments_frame, text = a.name)
        dropdown = tk.Menu(menu, tearoff = False)
        dropdown.add_command(label = 'Edit Assignment', command = lambda: self._edit_assingment(a))
        dropdown.add_command(label = 'Remove Assignment', command = lambda: self._remove_assignment(a))
        menu['menu'] = dropdown
        menu.grid(row = row, column = 0, sticky = tk.EW, padx = 10)
        
        cat = utils.create_label(self._assignments_frame, a.category, row, 1)
        
        if a.points is None:
            points = utils.create_label(self._assignments_frame, 'N/A', row, 2)
        else:
            points = utils.create_label(self._assignments_frame, a.points, row, 2)

        points_total = utils.create_label(self._assignments_frame, a.points_total, row, 3)
        
        self._assignments_widgets.update({a.name: {'name': menu, 'cat': cat, 'points': points, 'points_total': points_total}})
        self._scroll.update_canvas()
    
    
        
    