
class lexer:
    def __init__(self, source):
        self.source = source + "\n"
        self.cur_pos = -1
        self.cur_char = ''
        self.next_char()
    def next_char(self):
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0'
        else:
            self.cur_pos += 1
            self.cur_char = self.source[self.cur_pos]
    def peak(self):
        if self.cur_pos >= len(self.source) - 1:
            return '\0'
        return self.source[self.cur_pos + 1]
    def return_error(self):
        pass
    def skip_whitespace(self):
        pass
    def skip_comments(self):
        pass
    def getToken(self): #Will do most of the work, call other methods
        pass

    
    
    