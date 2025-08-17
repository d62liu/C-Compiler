import enum
import sys


import enum
import sys
from typing import Union, Optional


class Token:
    def __init__(self, val: str, type: 'TokenType') -> None:
        self.val = val
        self.type = type


class lexer:
    def __init__(self, source: str) -> None:
        self.source = source + "\n"
        self.cur_pos = -1
        self.cur_char = ''
        self.next_char()
    
    def next_char(self) -> None:
        if self.cur_pos >= len(self.source) - 1:
            self.cur_char = '\0'
        else:
            self.cur_pos += 1
            self.cur_char = self.source[self.cur_pos]
    
    def peak(self) -> str:
        if self.cur_pos >= len(self.source) - 1:
            return '\0'
        return self.source[self.cur_pos + 1]
    
    def return_error(self) -> None:
        pass
    
    def skip_whitespace(self) -> None:
        while (self.cur_char == " " or self.cur_char == "\t" or self.cur_char == "\r") and self.cur_char != '\0':
            self.next_char()
    
    def skip_comments(self) -> None: 
        if self.cur_char == "#":
            while self.cur_char != "\n" and self.cur_char != '\0':
                self.next_char()
        elif self.cur_char == "/" and self.peak() == "*":
            self.next_char()  # Skip the "/"
            self.next_char()  # Skip the "*"
            while not (self.cur_char == "*" and self.peak() == "/") and self.cur_char != '\0':
                self.next_char()
            if self.cur_char == "*":
                self.next_char()  # Skip the "*"
                self.next_char()  # Skip the "/"
        elif self.cur_char == "/" and self.peak() == "/":
            # C++ style single line comments
            while self.cur_char != "\n" and self.cur_char != '\0':
                self.next_char()
    
    def get_token(self) -> Token:
        self.skip_whitespace()
        self.skip_comments()
        token: Optional[Token] = None
        
        if self.cur_char == "*":
            if self.peak() == "=":
                self.next_char()
                token = Token("*=", TokenType.MULEQ)
            else:
                token = Token("*", TokenType.ASTERISK)
        elif self.cur_char == "-":
            if self.peak() == "=":
                self.next_char()
                token = Token("-=", TokenType.MINUSEQ)
            elif self.peak() == "-":
                self.next_char()
                token = Token("--", TokenType.DECR)
            elif self.peak() == ">":
                self.next_char()
                token = Token("->", TokenType.ARROW)
            else:
                token = Token("-", TokenType.MINUS)
        elif self.cur_char == '+':
            if self.peak() == "=":
                self.next_char()
                token = Token("+=", TokenType.PLUSEQ)
            elif self.peak() == "+":
                self.next_char()
                token = Token("++", TokenType.INCR)
            else:
                token = Token("+", TokenType.PLUS)
        elif self.cur_char == '/':
            if self.peak() == '*':
                self.skip_comments()
                return self.get_token()  # Get next token after comment
            elif self.peak() == '/':
                self.skip_comments()
                return self.get_token()  # Get next token after comment
            elif self.peak() == '=':
                self.next_char()
                token = Token("/=", TokenType.DIVEQ)
            else:
                token = Token("/", TokenType.SLASH)
        elif self.cur_char == '%':
            if self.peak() == '=':
                self.next_char()
                token = Token("%=", TokenType.MODEQ)
            else:
                token = Token("%", TokenType.PERCENT)
        elif self.cur_char == '&':
            if self.peak() == '&':
                self.next_char()
                token = Token("&&", TokenType.AND)
            else:
                token = Token("&", TokenType.BITAND)
        elif self.cur_char == '|':
            if self.peak() == '|':
                self.next_char()
                token = Token("||", TokenType.OR)
            else:
                token = Token("|", TokenType.BITOR)
        elif self.cur_char == '^':
            token = Token("^", TokenType.BITXOR)
        elif self.cur_char == '~':
            token = Token("~", TokenType.BITNOT)
        elif self.cur_char == '\n':
            token = Token("NEWLINE", TokenType.NEWLINE)
        elif self.cur_char == '\0':
            token = Token("EOF", TokenType.EOF)
        elif self.cur_char == "=":
            if self.peak() == "=":
                self.next_char()
                token = Token("==", TokenType.EQEQ)
            else:
                token = Token("=", TokenType.EQ)
        elif self.cur_char == ">":
            if self.peak() == "=":
                self.next_char()
                token = Token(">=", TokenType.GTEQ)
            elif self.peak() == ">":
                self.next_char()
                token = Token(">>", TokenType.RSHIFT)
            else:
                token = Token(">", TokenType.GT)
        elif self.cur_char == "<":
            if self.peak() == "=":
                self.next_char()
                token = Token("<=", TokenType.LTEQ)
            elif self.peak() == "<":
                self.next_char()
                token = Token("<<", TokenType.LSHIFT)
            else:
                token = Token("<", TokenType.LT)    
        elif self.cur_char == "!":
            if self.peak() == "=":
                self.next_char()
                token = Token("!=", TokenType.NOTEQ)
            else:
                token = Token("!", TokenType.NOT)
        elif self.cur_char == ';':
            token = Token(";", TokenType.SEMICOLON)
        elif self.cur_char == ',':
            token = Token(",", TokenType.COMMA)
        elif self.cur_char == '(':
            token = Token("(", TokenType.LPAREN)
        elif self.cur_char == ')':
            token = Token(")", TokenType.RPAREN)
        elif self.cur_char == '{':
            token = Token("{", TokenType.LBRACE)
        elif self.cur_char == '}':
            token = Token("}", TokenType.RBRACE)
        elif self.cur_char == '[':
            token = Token("[", TokenType.LBRACKET)
        elif self.cur_char == ']':
            token = Token("]", TokenType.RBRACKET)
        elif self.cur_char == '.':
            token = Token(".", TokenType.DOT)
        elif self.cur_char == '?':
            token = Token("?", TokenType.QUESTION)
        elif self.cur_char == ':':
            token = Token(":", TokenType.COLON)
        elif self.cur_char == '"':
            # String literal
            value = ""
            self.next_char()  # Skip opening quote
            while self.cur_char != '"' and self.cur_char != '\0':
                if self.cur_char == '\\':
                    # Handle escape sequences
                    self.next_char()
                    if self.cur_char == 'n':
                        value += '\n'
                    elif self.cur_char == 't':
                        value += '\t'
                    elif self.cur_char == 'r':
                        value += '\r'
                    elif self.cur_char == '\\':
                        value += '\\'
                    elif self.cur_char == '"':
                        value += '"'
                    else:
                        value += self.cur_char
                else:
                    value += self.cur_char
                self.next_char()
            
            if self.cur_char != '"':
                sys.exit("Unterminated string literal")
            
            token = Token(value, TokenType.STRING)
        elif self.cur_char == "'":
            # Character literal - treat as string for simplicity
            value = ""
            self.next_char()  # Skip opening quote
            while self.cur_char != "'" and self.cur_char != '\0':
                if self.cur_char == '\\':
                    # Handle escape sequences
                    self.next_char()
                    if self.cur_char == 'n':
                        value += '\n'
                    elif self.cur_char == 't':
                        value += '\t'
                    elif self.cur_char == 'r':
                        value += '\r'
                    elif self.cur_char == '\\':
                        value += '\\'
                    elif self.cur_char == "'":
                        value += "'"
                    else:
                        value += self.cur_char
                else:
                    value += self.cur_char
                self.next_char()
            
            if self.cur_char != "'":
                sys.exit("Unterminated character literal")
            
            token = Token(value, TokenType.STRING)  # Treat char as string for simplicity
        elif self.cur_char.isdigit():
            value = ""
            has_decimal = False
            
            # Add current digit
            value += self.cur_char
            
            # Continue while next char is digit or decimal point
            while self.peak().isdigit() or (self.peak() == "." and not has_decimal):
                self.next_char()
                if self.cur_char == ".":
                    if has_decimal:
                        sys.exit("Multiple decimal points found")
                    has_decimal = True
                    if not self.peak().isdigit():
                        sys.exit("Illegal character in number")
                value += self.cur_char
            
            token = Token(value, TokenType.NUMBER)
        elif self.cur_char == "\\" and self.peak() == "0":
            token = Token("EOF", TokenType.EOF)
        elif self.cur_char.isalpha() or self.cur_char == '_':
            word = ""
            word += self.cur_char
            
            while self.peak().isalnum() or self.peak() == '_':      
                self.next_char()
                word += self.cur_char
            
            keyword = self.checkIfKeyword(word)
            if keyword is False:
                token = Token(word, TokenType.IDENT)
            else:
                token = Token(word, keyword)
        else:
            sys.exit(f"Unknown Token: {self.cur_char}")
        
        if token.type != TokenType.EOF:   
            self.next_char()
        
        return token
    
    def checkIfKeyword(self, word: str) -> Union[Token, bool]:
        word_lower = word.lower()
        for token_type in TokenType:
            # Check if it's a keyword (values 101-200)
            if token_type.name.lower() == word_lower and 100 <= token_type.value <= 200:
                return token_type
        return False


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    
    # C Keywords
    AUTO = 101
    BREAK = 102
    CASE = 103
    CHAR = 104
    CONST = 105
    CONTINUE = 106
    DEFAULT = 107
    DO = 108
    DOUBLE = 109
    ELSE = 110
    ENUM = 111
    EXTERN = 112
    FLOAT = 113
    FOR = 114
    GOTO = 115
    IF = 116
    INT = 117
    LONG = 118
    REGISTER = 119
    RETURN = 120
    SHORT = 121
    SIGNED = 122
    SIZEOF = 123
    STATIC = 124
    STRUCT = 125
    SWITCH = 126
    TYPEDEF = 127
    UNION = 128
    UNSIGNED = 129
    VOID = 130
    VOLATILE = 131
    WHILE = 132
    
    # Operators and Punctuation
    EQ = 201          # =
    PLUS = 202        # +
    MINUS = 203       # -
    ASTERISK = 204    # *
    SLASH = 205       # /
    PERCENT = 206     # %
    EQEQ = 207        # ==
    NOTEQ = 208       # !=
    LT = 209          # <
    LTEQ = 210        # <=
    GT = 211          # >
    GTEQ = 212        # >=
    AND = 213         # &&
    OR = 214          # ||
    NOT = 215         # !
    BITAND = 216      # &
    BITOR = 217       # |
    BITXOR = 218      # ^
    BITNOT = 219      # ~
    LSHIFT = 220      # <<
    RSHIFT = 221      # >>
    PLUSEQ = 222      # +=
    MINUSEQ = 223     # -=
    MULEQ = 224       # *=
    DIVEQ = 225       # /=
    MODEQ = 226       # %=
    INCR = 227        # ++
    DECR = 228        # --
    
    # Punctuation
    SEMICOLON = 301   # ;
    COMMA = 302       # ,
    LPAREN = 303      # (
    RPAREN = 304      # )
    LBRACE = 305      # {
    RBRACE = 306      # }
    LBRACKET = 307    # [
    RBRACKET = 308    # ]
    DOT = 309         # .
    ARROW = 310       # ->
    QUESTION = 311    # ?
    COLON = 312       # :
