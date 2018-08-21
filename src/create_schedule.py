import tkinter as tk
import tkinter.messagebox as tkmsg
import schedule, utils

class TkCreateSchedule:
    COLSPAN = 2
    ROWSPAN = 5
    
    def __init__(self, root, root_frame, start_page):
        
        self._root = root
        self._start_page = start_page
        self._root_frame = root_frame
        
        self._frame = tk.Frame(self._root_frame)
        self._frame.grid(row = 0, column = 0, sticky = tk.NSEW)
        
        # can't use rowspan in the configure_frame for some reason???
        for i in range(self.ROWSPAN - 2):
            self._frame.rowconfigure(i + 2, weight = 1)
        utils.configure_frame(self._frame, colspan = self.COLSPAN)
        
        utils.create_title(self._frame, 'Create a new schedule', self.ROWSPAN)
        
        self._name = utils.create_labeled_entry(self._frame, 'Name:', 2, 0, 10, 10)
        self._units = utils.create_labeled_entry(self._frame, 'Current Units Completed:', 3, 0, 10, 10, '0')
        self._gpa = utils.create_labeled_entry(self._frame, 'Current GPA:', 4, 0, 10, 10, '0.00')
        
        utils.create_button(self._frame, 'Create', self._create, self.ROWSPAN, 0)
        utils.create_button(self._frame, 'Cancel', self._cancel, self.ROWSPAN, 1)
        
        utils.set_menu(self._root, utils.START_MENU)
    
        self.load_schedule()
    
    
    def _create(self) -> None:
        if self._name.get().replace(' ' , '') == '':
            tkmsg.showerror('Warning', '"Name" entry cannot be left blank.')
        else:
            try:
                int(self._units.get())
            except (NameError, ValueError):
                tkmsg.showerror('Warning', '"Units" entry must be an integer.')
            else:
                try:
                    if float(self._gpa.get()) < 0 or float(self._gpa.get()) > 5:
                        raise NameError
                except (NameError, ValueError):
                    tkmsg.showerror('Warning', '"GPA" entry must be a number between 0 and 5.')
                else:
                    schedule.save_schedule(schedule.Schedule(self._name.get(), self._units.get(), self._gpa.get()))
                    schedule.open_schedule(self._root, self._root_frame, open(f'schedules/{self._name.get()}.json'), self._start_page)
        
    def _cancel(self) -> None:
        if tkmsg.askyesno('Warning', 'Are you sure you want to cancel?'):
            self._start_page.load_start()
            
    def is_default(self) -> bool:
        if self._name.get() != '' or self._units.get() != '0' or self._gpa.get() != '0.00':
            return tkmsg.askyesno('Warning', 'You have unsaved work, are you sure you want to continue?')
        return True
            
    def load_schedule(self):
        self._name.delete(0, 'end')
        self._units.delete(0, 'end')
        self._gpa.delete(0, 'end')
        self._frame.tkraise()
        
    
        
      
        