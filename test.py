from lexer import *

def main():
    source = "+-\0"
    Lexer = lexer(source)
    token = Lexer.get_token()
    while token.val != TokenType.EOF:
        print(token.type)
        token = Lexer.get_token()
main()