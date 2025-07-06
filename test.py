from lexer import *

def main():
    source = "let Foobar = 123"
    Lexer = lexer(source)
    
    while Lexer.peak() != "\0":
        print(Lexer.cur_char)
        Lexer.next_char()

main()