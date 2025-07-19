
import enum
import sys

class Token:
    def __init__(self, val, type):
        self.val = val
        self.type = type
 
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
        while self.source[self.cur_pos] == " " or self.source[self.cur_char] == "\n":
            self.next_char()
        self.cur_char = self.source[self.cur_pos]
    def skip_comments(self): #doesn't yet support multi line
        while self.source[self.cur_pos] != "\n":
            self.next_char()
        self.cur_char = self.source[self.cur_pos]
    def get_token(self):
        self.skip_whitespace()
        self.skip_comments()
        token = None
        if self.cur_char == "*":
            token = Token("*", TokenType.ASTERISK)
        elif self.cur_char == "-":
            token = Token("-", TokenType.MINUS)
        elif self.curChar == '+':
            token = Token("+", TokenType.PLUS)
        elif self.curChar == '/':
            token = Token("/", TokenType.SLASH)
        elif self.curChar == '\n':
            token = Token("nl", TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token("EOF", TokenType.EOF)
        elif self.curchar == ">":
            if self.peak() == "=":
                token = Token("GTEQ", TokenType.GTEQ)
            else:
                token = Token("GEQ", TokenType.GT)
        elif self.curchar == ">":
            if self.peak() == "=":
                self.next_char()
                token = Token("GTEQ", TokenType.GTEQ)
            else:
                token = Token("GEQ", TokenType.GT)
        elif self.curchar == "<":
            if self.peak() == "=":
                self.next_char()
                token = Token("LTEQ", TokenType.LTEQ)
            else:
                token = Token("LEQ", TokenType.LT)    
        elif self.curchar == "!":
            if self.peak() == "=":
                self.next_char()
                token = Token("NOTEQ", TokenType.NOTEQ)
            else:
                sys.exit(f"Unknown Token: !")
        else:
            sys.exit(f"Unknown Token:{self.cur_char}")
        self.nextChar()
    
    
        

    
class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	# Keywords
	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	# Operators
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211
    