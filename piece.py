class Piece:
    captured = False
    white = False
    
    def __init__(self, white):
        self.set_white(white)
        
    def is_white(self) -> bool:
        return self.white
    
    def set_white(self, white):
        self.white = white
        
    def is_captured(self) -> bool:
        return self.captured
    
    def set_captured(self, captured):
        self.captured = captured
    
    def can_move(self, board, start, end) -> bool: _abstract()
    
    def __str__(self):
        if self.white:
            return f"White {type(self).__name__}"
        else :
            return f"Black {type(self).__name__}"
    
def _abstract():
    raise NotImplementedError
    
def override(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider
