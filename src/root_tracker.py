class Root_Tracker:
    
    def __init__(self):
        self._roots = []
        
    def add_root(self, frame: 'tk root') -> None:
        self._roots.append(frame)
        
    def remove_root(self, frame: 'tk root') -> None:
        self._roots.remove(frame)
        
    def destroy(self) -> None:
        for root in self._roots:
            root.destroy()