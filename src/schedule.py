import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
from scroll_frame import ScrollingFrame
import course, course_widget, json, pathlib, root_tracker, utils

class Schedule:
    
    def __init__(self, name: str, units: int, gpa: float, courses = {}):
        self.name = name
        self.units = units
        self.gpa = gpa
        self.courses = []
        for name in courses:
            units, a, a_minus, b_plus, b, b_minus, c_plus, c, c_mins, d_plus, d, d_minus, categories, assignments, grade = courses[name].values()
            self.courses.append(course.Course(name, units, float(a), float(a_minus), float(b_plus), float(b), float(b_minus), float(c_plus), float(c), float(c_mins), float(d_plus), float(d), float(d_minus), categories, assignments, grade))
    
    def __str__(self) -> str:
        c = '\n'.join([str(c) for c in self.courses])
        return f'Name: {self.name}\nUnits: {self.units}\nGPA: {self.gpa}\nCourses: {c}'
        
    def __len__(self) -> int:
        return len(self.courses)
    
    def add_course(self, course: course.Course) -> None:
        """adds a course to the schedule and sorts the courses by name"""
        self.courses.append(course)
    
    def remove_course(self, course: course.Course) -> None:
        """removes a course from the schedule"""
        self.courses.remove(course)
        
    def get_dict(self) -> dict:
        """returns a dictionary of the schedule, used in saving"""
        courses_dict = dict()
        for c in self.courses:
            courses_dict.update(c.get_dict())
        return {'name': self.name, 'units': self.units, 'gpa': self.gpa, 'courses': courses_dict}
 
def open_schedule(root, root_frame, open_file, start_page) -> None:
    """opens a schedule from a json file"""
    s = get_schedule_dict(open_file)
    open(pathlib.Path('schedules/recent.txt'), 'w').write(s['name'] + '.json')
    TkSchedule(root, root_frame, Schedule(s['name'], int(s['units']), float(s['gpa']), s['courses']), start_page)
    
def get_schedule_dict(open_file) -> dict:
    """returns a dict of the json file containing the schedule info"""
    with open_file as f:
        s = json.load(f)
    open_file.close()
    return s
        
def save_schedule(schedule: Schedule) -> None:
    """saves the schedule as a json file"""
    file = open(pathlib.Path(f'schedules/{schedule.name}.json'), 'w')
    with file as f:
        json.dump(schedule.get_dict(), f)
    file.close()
    
class TkSchedule:
    COLSPAN = 4
    ROWSPAN = 100
    A_COLSPAN = 4
    
    def __init__(self, root, root_frame, schedule: Schedule, start_page):
        # initialize the root frame
        self._root = root
        self._root.protocol('WM_DELETE_WINDOW', self._destroy)
        self._root_frame = root_frame
        self._schedule = schedule
        self._start_page = start_page
        
        # initialize the new menu bar
        self._menu = tk.Menu(self._root)
        file_menu = tk.Menu(self._menu, tearoff = 0)
        file_menu.add_command(label = 'New Schedule', accelerator = 'Ctrl+N', command = self._new_schedule)
        file_menu.add_command(label = 'Open Schedule', accelerator = 'Ctrl+O', command = self._open_schedule)
        file_menu.add_command(label = 'Open Most Recent', accelerator = 'Ctrl+R', command = self._open_recent)
        file_menu.add_command(label = 'Save Schedule', accelerator = 'Ctrl+S', command = self._save )
        file_menu.add_command(label = 'Quit', accelerator = 'Ctrl+Q', command = self._quit)
        self._menu.add_cascade(label = 'File', menu = file_menu)
        
        edit_menu = tk.Menu(self._menu, tearoff = 0)
        edit_menu.add_command(label = 'Edit Schedule', accelerator = 'Ctrl+E', command = self._edit)
        self._menu.add_cascade(label = 'Edit', menu = edit_menu)
        self._root.config(menu = self._menu)
        
        # bind accelerators (same options as menu bar)
        self._root.bind('<Control-n>', self._new_schedule)
        self._root.bind('<Control-o>', self._open_schedule)
        self._root.bind('<Control-r>', self._open_recent)
        self._root.bind('<Control-s>', self._save)
        self._root.bind('<Control-e>', self._edit)
        self._root.bind('<Control-q>', self._quit)
        
        # initialize status bar (top)
        self._frame = tk.Frame(self._root_frame)
        self._frame.grid(row = 0, column = 0, sticky = tk.NSEW)
        self._frame.rowconfigure(2, weight = 1)
        utils.configure_frame(self._frame, colspan = 4)
        
        self._status_color = 'dark grey'
        self._status_frame = tk.Frame(self._frame, bg = self._status_color)
        self._status_frame.grid(row = 0, column = 0, columnspan = 4, sticky = tk.NSEW)
        utils.configure_frame(self._status_frame, colspan = 6)
        
        self._project_name = tk.Label(self._status_frame, bg = self._status_color, text = self._schedule.name)
        self._project_name.grid()
        self._total_units = tk.Label(self._status_frame, bg = self._status_color, text = f'Total Units Completed: {self._schedule.units}')
        self._total_units.grid(row = 0, column = 1)
        self._enrolled_units = tk.Label(self._status_frame, bg = self._status_color, text = f'Units Enrolled In: {sum([c.units for c in self._schedule.courses])}')
        self._enrolled_units.grid(row = 0, column = 2)
        self._total_courses = tk.Label(self._status_frame, bg = self._status_color, text = f'Total Courses: {len(self._schedule)}')
        self._total_courses.grid(row = 0, column = 3)
        self._gpa = tk.Label(self._status_frame, bg = self._status_color, text = f'GPA: {self._schedule.gpa}')
        self._gpa.grid(row = 0, column = 4)
        self._gpa_projected = tk.Label(self._status_frame, bg = self._status_color, text = f'Projected GPA: {self._schedule.gpa}')
        self._gpa_projected.grid(row = 0, column = 5)
        
        
        # initialize course labels
        self._info_color = 'light grey'
        self._info_frame = tk.Frame(self._frame, padx = 16, bg = self._status_color)
        self._info_frame.grid(row = 1, column = 0, columnspan = 4, sticky = tk.NSEW)
        
        for i in range(4):
            self._info_frame.columnconfigure(i, weight = 1, uniform = 'info')
        
        tk.Label(self._info_frame, text = '{:^25}'.format('Course'), bg = self._info_color, bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 3, column = 0, sticky = tk.EW)
        tk.Label(self._info_frame, text = '{:^25}'.format('Units'), bg = self._info_color, bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 3, column = 1, sticky = tk.EW)
        tk.Label(self._info_frame, text = '{:^25}'.format('Total Assignments'), bg = self._info_color, bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 3, column = 2, sticky = tk.EW)
        tk.Label(self._info_frame, text = '{:^25}'.format('Grade'), bg = self._info_color, bd = 1, relief = tk.SUNKEN, padx = 8, pady = 5).grid(row = 3, column = 3, sticky = tk.EW)
        
        # initialize courses frame
        self._course_scroll = ScrollingFrame(self._frame, 2, 1, 4, height_border = 91, w_cutoff = 30, h_cuttoff = 30, scroll_size = 15)
        self._courses_frame = self._course_scroll.frame
        utils.configure_frame(self._courses_frame, colspan = 1)
        
        # other
        ttk.Button(self._frame, text = 'Add Course', command = self._create_tkcourse).grid(row = 3, column = 0, columnspan = 4, sticky = tk.NSEW, padx = 5, pady = 5)
        self._root_tracker = root_tracker.Root_Tracker()
        self._root_tracker.add_root(self._root)
        self._total_rows = 0
        self._init_courses()
        self.load_tkschedule()
        
    # SCHEDULE METHODS
    
    def _new_schedule(self, event = None) -> None:
        self._check_safe_to_run(self._start_page.new_schedule)
        
    def _open_recent(self, event = None) -> None:
        self._check_safe_to_run(self._start_page.open_recent)
    
    def _open_schedule(self, event = None) -> None:
        self._check_safe_to_run(self._start_page.open_schedule)
        
    def _check_for_changes(self) -> None:
        return self._schedule.get_dict() == get_schedule_dict(open(f'schedules/{self._schedule.name}.json'))
    
    def _check_safe_to_run(self, func) -> None:
        """checks if there are unsaved changes, if so the user is prompted, if not then the function is executed"""
        if self._check_for_changes():
            func()
        else:
            if tkmsg.askyesno('Warning', 'You have unsaved changes, would you like to proceed?'):
                func()
    def _save(self, event = None) -> None:
        save_schedule(self._schedule)
        
    def _edit(self, event = None) -> None:
        print('edit_schedule')
    
    def _destroy(self) -> None:
        """destroys all open course windows as well as the roots and assignments"""
        self._root_tracker.destroy()
        
    def _quit(self, event = None) -> None:
        """Checks if there are any changes made to the schedule, if so it warns the user first before quitting"""
        if not self._check_for_changes():
            if tkmsg.askyesno('Warning', 'You have unsaved changes, continue to quit?'):
                self._destroy()
        else:
            self._destroy()
    
    def load_tkschedule(self):
        self._frame.tkraise()
        
    # COURSE METHODS
    
    def add_tkcourse(self, c: course.Course) -> None:
        """adds a course to the display"""
        course_widget.Course_Widget(c, self._courses_frame, self._course_scroll, self._schedule, self._root_tracker).grid(row = self._total_rows)
        self._total_rows += 1
        self._total_courses.config(text = f'Total Courses: {len(self._schedule)}')
        self._course_scroll.update_canvas()
        
    def _init_courses(self) -> None:
        """adds the courses read from the json file to the screen"""
        for c in self._schedule.courses:
            self.add_tkcourse(c)
        
    def _create_tkcourse(self) -> None:
        course.NewTkCourse(self._schedule, self, self._root_tracker)
        