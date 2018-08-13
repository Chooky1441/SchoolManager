import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
import assignment, course, utils


class Course_Widget:
    
    COLSPAN = 4
    A_COLSPAN = 4
    
    def __init__(self, c: course.Course, schedule_frame: tk.Frame, scroll: tk.Canvas, schedule, root_tracker, tkschedule):
        self._c = c
        self._scroll = scroll
        self._schedule_frame = schedule_frame
        self._schedule = schedule
        self._root_tracker = root_tracker
        self._tkschedule = tkschedule
        self._frame = tk.Frame(self._schedule_frame)
        for i in range(self.COLSPAN):
            self._frame.columnconfigure(i, weight = 1, uniform = 'course')
            
        self._assignments_widgets = dict()
        
        # initializes the name frame and label
        name_frame = tk.Frame(self._frame)
        name_frame.grid(row = 0, column = 0, sticky = tk.EW)
        for i in range(2):
            name_frame.columnconfigure(i, weight = 1, uniform = 'name')
        
        self._name = utils.create_label(name_frame, self._c.name, 0, 1, sticky = tk.W)    
    
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
        options_frame = utils.create_labelframe(self._course_frame, 'Options', 0, 0)
        utils.configure_frame(options_frame, colspan = 3)
        utils.create_button(options_frame, 'Add Assignment', lambda: self._create_assignment(), 0, 0)
        utils.create_button(options_frame, 'Edit Course', lambda: self._edit_course(), 0, 1)
        utils.create_button(options_frame, 'Remove Course', lambda: self._remove_tkcourse(), 0, 2)

        # initializes the assignments frame
        self._assignments_frame = utils.create_labelframe(self._course_frame, 'Assignments', 1, 0)
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
                
        utils.create_separator(self._frame, 2, 0, self.COLSPAN, 0, 5)
    
        
    def _edit_course(self) -> None:
        """opens the edit course dialog"""
        course.EditTkCourse(self._schedule, self._root_tracker, self._c, self, self._tkschedule)
        
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
        """is used to grid the widget onto the root frame"""
        self._frame.grid(row = row, column = column, sticky = tk.NSEW)
        
    def update_course(self) -> None:
        """updates the name, units, and grade in the course view"""
        self._name['text'] = self._c.name
        self._units['text'] = self._c.units
        self._grade['text'] = self._c.grade
        
    def destroy(self) -> None:
        """removes the course widget from the display"""
        for widget in self._frame.winfo_children():
            widget.destroy()
        self._frame.destroy()
        
        
    # ASSIGNMENT METHODS
            
    def add_tkassignment(self, a: assignment.Assignemnt) -> None:
        """adds the assignment to the course and displays it to the screen"""
        self._c.add_assignment(a)
        self._c.calculate_grade()
        self._tkschedule.update_projected_gpa()
        self._amt.config(text = len(self._c.assignments))
        self._grade.config(text = self._c.grade)
        self._update_tkassignment(a)
            
    def _create_assignment(self) -> None:
        """opens the add assignment dialog"""
        assignment.NewTkAssignment(self._c, self, self._root_tracker)
        
    def _edit_assingment(self, a: assignment.Assignemnt, event = None) -> None:
        """opens the edit assignment dialog"""
        assignment.EditTkAssignment(self._c, self, self._root_tracker, a)
        
    def _remove_assignment(self, a: assignment.Assignemnt, event = None) -> None:
        """Confirms that the user wants to remove the assignment, then removes it"""
        if tkmsg.askyesno('Warning', f'Are you sure you want to remove {a.name} from {self._c.name}?'):
            self._c.remove_assignment(a)
            if len(self._c.assignments) < 1:
                self._clear_assignments_info()
            for widget in self._assignments_widgets[a]:
                self._assignments_widgets[a][widget].destroy()
            del self._assignments_widgets[a] 
        
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
        utils.create_label(self._assignments_frame, 'You currently have no assignments.', 0, 0, colspan = self.A_COLSPAN)
           
    def _update_tkassignment(self, a: assignment.Assignemnt, row = None) -> None:
        """adds an assignment to the given course and updates the status bar"""    
        if len(self._c.assignments) - 1 < 1: # -1 because the new assignment has already been added to the list
            self._init_assignments_info()
        if row is None:
            row = len(self._c.assignments)
            
        s = ttk.Style()
        s.configure('TMenubutton', font = utils.FONT)
        menu = ttk.Menubutton(self._assignments_frame, text = a.name, style = 'TMenubutton')
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
        
        self._assignments_widgets.update({a: {'name': menu, 'cat': cat, 'points': points, 'points_total': points_total}})
        self._scroll.update_canvas()
        
    def update_assignment(self, a: assignment.Assignemnt) -> None:
        """Updates the given assignment on the screen"""
        self._assignments_widgets[a]['name']['text'] = a.name
        self._assignments_widgets[a]['cat']['text'] = a.category
        if a.points is None:
            self._assignments_widgets[a]['points']['text'] = 'N/A'
        else:
            self._assignments_widgets[a]['points']['text'] = a.points
        self._assignments_widgets[a]['points_total']['text'] = a.points_total
        
        self._c.calculate_grade()
        self._tkschedule.update_projected_gpa()
        self.update_course()
        
    
    
        
    