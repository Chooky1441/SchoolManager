import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
from scroll_frame import ScrollingFrame
import course, course_widget, edit_schedule, json, pathlib, root_tracker, utils

class Schedule:
    
    def __init__(self, name: str, units: int, gpa: float, projected_gpa: float, courses = {}):
        self.name = name
        self.units = units
        self.gpa = gpa
        self.projected_gpa = projected_gpa
        self.courses = []
        for name in courses:
            units, a, a_minus, b_plus, b, b_minus, c_plus, c, c_mins, d_plus, d, categories, assignments, grade = courses[name].values()
            self.courses.append(course.Course(name, units, float(a), float(a_minus), float(b_plus), float(b), float(b_minus), float(c_plus), float(c), float(c_mins), float(d_plus), float(d), categories, assignments, grade))
    
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
        return {'name': self.name, 'units': self.units, 'gpa': self.gpa, 'projected_gpa': self.projected_gpa, 'courses': courses_dict}
    
    
    def calculate_projected_gpa(self) -> None:
        """calculates the projected gpa based on the schedule's courses"""
        course_gpa = sum({self.convert_grade_to_gpa(course.grade) for course in self.courses})/len(self)
        course_units = sum({course.units for course in self.courses})
        total_units = self.units + course_units
        self.projected_gpa = self.gpa * (self.units / total_units) + course_gpa * (course_units / total_units)
        
    def update_gpa_and_units(self, units: int, grade: str) -> None:
        total_units = self.units + units
        self.gpa = self.gpa * (self.units / total_units) + self.convert_grade_to_gpa(grade) * (units / total_units)
        self.units += units
        
    def convert_grade_to_gpa(self, grade: str) -> None:
        return {'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C+': 2.3, 'C': 2, 'C-': 1.7, 'D+': 1.3, 'D': 1, 'F': 0}[grade]
        
 
def open_schedule(root, root_frame, open_file, start_page) -> None:
    """opens a schedule from a json file"""
    s = get_schedule_dict(open_file)
    open(pathlib.Path('schedules/recent.txt'), 'w').write(s['name'] + '.json')
    TkSchedule(root, root_frame, Schedule(s['name'], int(s['units']), float(s['gpa']), float(s['projected_gpa']), s['courses']), start_page)
    
def get_schedule_dict(open_file) -> dict:
    """returns a dict of the json file containing the schedule info"""
    with open_file as f:
        s = json.load(f)
    open_file.close()
    return s
        
def save_schedule(schedule: Schedule, name = None) -> None:
    """saves the schedule as a json file"""
    if name is None:
        name = schedule.name
    file = open(pathlib.Path(f'schedules/{name}.json'), 'w')
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
        self._mode = 0
        
        # initialize the new menu bar
        if utils.SCHEDULE_MENU is None:
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
            
            mode_menu = tk.Menu(self._menu, tearoff = 0)
            mode_menu.add_command(label = 'Normal', command = lambda: self._switch_mode(0))
            mode_menu.add_command(label = 'Experimental', command = lambda: self._switch_mode(1))
            mode_menu.add_command(label = 'What is Mode?', command = lambda: tkmsg.showinfo('Help', 'Changing modes allows you to easily calculate grades without permanently making changes to your schedule.\n\nIn Normal Mode any changes you make will be saved when saving the schedule.\n\nIn Experimental Mode any changes you make will be discarded when saving or when switching back to Normal Mode.'))
            self._menu.add_cascade(label = 'Mode', menu = mode_menu)
            
            utils.SCHEDULE_MENU = self._menu
        utils.set_menu(self._root, utils.SCHEDULE_MENU)
        
        # bind accelerators (same options as menu bar)
        self._root.bind('<Control-n>', self._new_schedule)
        self._root.bind('<Control-o>', self._open_schedule)
        self._root.bind('<Control-r>', self._open_recent)
        self._root.bind('<Control-q>', self._quit)
        
        self._root.bind('<Control-s>', self._save)
        self._root.bind('<Control-e>', self._edit)
        
        
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
        self._gpa = tk.Label(self._status_frame, bg = self._status_color, text = f'GPA: {round(self._schedule.gpa, 2)}')
        self._gpa.grid(row = 0, column = 4)
        self._gpa_projected = tk.Label(self._status_frame, bg = self._status_color, text = f'Projected GPA: {round(self._schedule.projected_gpa, 2)}')
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
        ttk.Button(self._frame, text = 'Add Course', command = self._create_tkcourse).grid(row = 3, column = 0, columnspan = 4, sticky = tk.NSEW, padx = 5, pady = 0)
        
        bottom_bar = tk.Frame(self._frame)
        bottom_bar.grid(row = 4, column = 1, sticky = tk.NSEW)
        self._mode_label = utils.create_label(bottom_bar, 'Mode: Normal', padx = 0, pady = 0)
        
        self._root_tracker = root_tracker.Root_Tracker()
        self._root_tracker.add_root(self._root)
        self._total_rows = 0
        self._init_courses()
        
        self._temp_file = None
        
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
            if tkmsg.askyesno('Warning', 'You have unsaved changes, would you like to proceed?\nAny changes made will not be saved.'):
                func()
                
    def _save(self, event = None) -> None:
        save_schedule(self._schedule)
        
    def _edit(self, event = None) -> None:
        edit_schedule.EditTkSchedule(self)
    
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
            
    def _switch_mode(self, mode: int, event = None) -> None:
        if mode == 0 and self._mode != 0:
            open_schedule(self._root, self._root_frame, open(pathlib.Path(f'schedules/{self._schedule.name}-temp.json')), self._start_page)
            #pathlib.Path(f'schedules/{self._schedule.name}-temp.json').unlink()
            
        elif mode == 1 and self._mode != 1:
            self._mode = 1
            self._mode_label['text'] = 'Mode: Experimental'
            self._temp_file = open(pathlib.Path(f'schedules/{self._schedule.name}-temp.json'), 'w')
            save_schedule(self._schedule, f'{self._schedule.name}-temp')
            
            
            
    def update_info_bar(self) -> None:
        self._gpa['text'] =  f'GPA: {round(self._schedule.gpa, 2)}'
        self._total_units['text'] = f'Total Units Completed: {self._schedule.units}'
        self._enrolled_units['text'] = f'Units Enrolled In: {sum([c.units for c in self._schedule.courses])}'
        self._total_courses['text'] = f'Total Courses: {len(self._schedule)}'
            
    def update_projected_gpa(self) -> None:
        """calculates and then displays the projected gpa"""
        self._schedule.calculate_projected_gpa()
        self._gpa_projected['text'] = f'Projected GPA: {round(self._schedule.projected_gpa, 2)}'
    
    def load_tkschedule(self):
        self._frame.tkraise()
        
    # COURSE METHODS
    
    def add_tkcourse(self, c: course.Course) -> None:
        """adds a course to the display"""
        course_widget.Course_Widget(c, self._courses_frame, self._course_scroll, self._schedule, self._root_tracker, self).grid(row = self._total_rows)
        self._total_rows += 1
        self._total_courses.config(text = f'Total Courses: {len(self._schedule)}')
        
    def _init_courses(self) -> None:
        """adds the courses read from the json file to the screen"""
        for c in self._schedule.courses:
            self.add_tkcourse(c)
        
    def _create_tkcourse(self) -> None:
        """opens the new course dialog"""
        course.NewTkCourse(self._schedule, self, self._root_tracker)
