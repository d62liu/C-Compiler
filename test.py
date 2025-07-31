from lexer import *

def main():
    source = "+-123 9.8654*\n\0" 
    Lexer = lexer(source)
    token = Lexer.get_token()
    while token.val != TokenType.EOF:
        print(token.type)
        token = Lexer.get_token()
main()