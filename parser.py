import sys
from lexer import *
from typing import List, Optional, Union

# AST Node Classes
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self):
        self.declarations: List[ASTNode] = []

class Declaration(ASTNode):
    pass

class FunctionDeclaration(Declaration):
    def __init__(self, return_type: str, name: str, parameters: List, body: 'CompoundStatement'):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

class VariableDeclaration(Declaration):
    def __init__(self, type_name: str, name: str, initializer=None):
        self.type_name = type_name
        self.name = name
        self.initializer = initializer

class Parameter(ASTNode):
    def __init__(self, type_name: str, name: str):
        self.type_name = type_name
        self.name = name

class Statement(ASTNode):
    pass

class CompoundStatement(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

class ExpressionStatement(Statement):
    def __init__(self, expression: Optional['Expression']):
        self.expression = expression

class IfStatement(Statement):
    def __init__(self, condition: 'Expression', then_stmt: Statement, else_stmt: Optional[Statement] = None):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class WhileStatement(Statement):
    def __init__(self, condition: 'Expression', body: Statement):
        self.condition = condition
        self.body = body

class ForStatement(Statement):
    def __init__(self, init: Optional[Statement], condition: Optional['Expression'], 
                 update: Optional['Expression'], body: Statement):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class ReturnStatement(Statement):
    def __init__(self, expression: Optional['Expression'] = None):
        self.expression = expression

class BreakStatement(Statement):
    pass

class ContinueStatement(Statement):
    pass

class Expression(ASTNode):
    pass

class BinaryExpression(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(Expression):
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand

class AssignmentExpression(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

class FunctionCall(Expression):
    def __init__(self, function: Expression, arguments: List[Expression]):
        self.function = function
        self.arguments = arguments

class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name

class Literal(Expression):
    def __init__(self, value: Union[int, float, str]):
        self.value = value

class ArrayAccess(Expression):
    def __init__(self, array: Expression, index: Expression):
        self.array = array
        self.index = index

class MemberAccess(Expression):
    def __init__(self, object_expr: Expression, member: str, is_arrow: bool = False):
        self.object = object_expr
        self.member = member
        self.is_arrow = is_arrow

# C Parser Class
class CParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.advance()
    
    def advance(self):
        try:
            self.current_token = self.lexer.get_token()
        except SystemExit:
            self.current_token = Token("EOF", TokenType.EOF)
    
    def eat(self, expected_type):
        if self.current_token.type == expected_type:
            self.advance()
        else:
            self.abort(f"Expected {expected_type}, got {self.current_token.type}")
    
    def abort(self, message):
        """Abort parsing with error message"""
        sys.exit(f"Parse Error: {message}")
    
    def parse(self) -> Program:
        """Parse the entire C program"""
        program = Program()
        
        while self.current_token.type != TokenType.EOF:
            # Skip newlines at top level
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            
            declaration = self.parse_declaration()
            if declaration:
                program.declarations.append(declaration)
        
        return program
    
    def parse_declaration(self) -> Optional[Declaration]:
        """Parse function or variable declarations"""
        if not self.is_type():
            self.abort(f"Expected type specifier, got {self.current_token.type}")
        
        type_name = self.current_token.val
        self.advance()
        
        if self.current_token.type != TokenType.IDENT:
            self.abort("Expected identifier")
        
        name = self.current_token.val
        self.advance()
        
        if self.current_token.type == TokenType.LPAREN:
            return self.parse_function_declaration(type_name, name)
        else:
            return self.parse_variable_declaration(type_name, name)
    
    def parse_function_declaration(self, return_type: str, name: str) -> FunctionDeclaration:
        """Parse function declaration"""
        self.eat(TokenType.LPAREN)
        parameters = []
        if self.current_token.type != TokenType.RPAREN:
            parameters = self.parse_parameter_list()
        
        self.eat(TokenType.RPAREN)
        
        body = self.parse_compound_statement()
        
        return FunctionDeclaration(return_type, name, parameters, body)
    
    def parse_parameter_list(self) -> List[Parameter]:
        """Parse function parameters"""
        parameters = []
        
        # First parameter
        if self.is_type():
            param_type = self.current_token.val
            self.advance()
            
            if self.current_token.type != TokenType.IDENT:
                self.abort("Expected parameter name")
            
            param_name = self.current_token.val
            self.advance()
            
            parameters.append(Parameter(param_type, param_name))
            
            # Additional parameters
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                
                if not self.is_type():
                    self.abort("Expected parameter type")
                
                param_type = self.current_token.val
                self.advance()
                
                if self.current_token.type != TokenType.IDENT:
                    self.abort("Expected parameter name")
                
                param_name = self.current_token.val
                self.advance()
                
                parameters.append(Parameter(param_type, param_name))
        
        return parameters
    
    def parse_variable_declaration(self, type_name: str, name: str) -> VariableDeclaration:
        """Parse variable declaration"""
        initializer = None
        
        if self.current_token.type == TokenType.EQ:
            self.advance()
            initializer = self.parse_expression()
        
        self.eat(TokenType.SEMICOLON)
        return VariableDeclaration(type_name, name, initializer)
    
    def parse_compound_statement(self) -> CompoundStatement:
        """Parse compound statement { ... }"""
        self.eat(TokenType.LBRACE)
        
        statements = []
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.eat(TokenType.RBRACE)
        return CompoundStatement(statements)
    
    def parse_statement(self) -> Optional[Statement]:
        """Parse individual statements"""
        if self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for_statement()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif self.current_token.type == TokenType.BREAK:
            self.advance()
            self.eat(TokenType.SEMICOLON)
            return BreakStatement()
        elif self.current_token.type == TokenType.CONTINUE:
            self.advance()
            self.eat(TokenType.SEMICOLON)
            return ContinueStatement()
        elif self.current_token.type == TokenType.LBRACE:
            return self.parse_compound_statement()
        elif self.is_type():
            # Variable declaration inside function
            type_name = self.current_token.val
            self.advance()
            name = self.current_token.val
            self.advance()
            return self.parse_variable_declaration(type_name, name)
        else:
            # Expression statement
            expr = self.parse_expression()
            self.eat(TokenType.SEMICOLON)
            return ExpressionStatement(expr)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if statement"""
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        
        then_stmt = self.parse_statement()
        else_stmt = None
        
        if self.current_token.type == TokenType.ELSE:
            self.advance()
            else_stmt = self.parse_statement()
        
        return IfStatement(condition, then_stmt, else_stmt)
    
    def parse_while_statement(self) -> WhileStatement:
        """Parse while statement"""
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        body = self.parse_statement()
        
        return WhileStatement(condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        """Parse for statement"""
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        
        # Init
        init = None
        if self.current_token.type != TokenType.SEMICOLON:
            if self.is_type():
                type_name = self.current_token.val
                self.advance()
                name = self.current_token.val
                self.advance()
                init = self.parse_variable_declaration(type_name, name)
            else:
                expr = self.parse_expression()
                self.eat(TokenType.SEMICOLON)
                init = ExpressionStatement(expr)
        else:
            self.eat(TokenType.SEMICOLON)
        
        # Condition
        condition = None
        if self.current_token.type != TokenType.SEMICOLON:
            condition = self.parse_expression()
        self.eat(TokenType.SEMICOLON)
        
        # Update
        update = None
        if self.current_token.type != TokenType.RPAREN:
            update = self.parse_expression()
        self.eat(TokenType.RPAREN)
        
        body = self.parse_statement()
        
        return ForStatement(init, condition, update, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse return statement"""
        self.eat(TokenType.RETURN)
        
        expr = None
        if self.current_token.type != TokenType.SEMICOLON:
            expr = self.parse_expression()
        
        self.eat(TokenType.SEMICOLON)
        return ReturnStatement(expr)
    
    def parse_expression(self) -> Expression:
        """Parse expressions with proper precedence"""
        return self.parse_assignment()
    
    def parse_assignment(self) -> Expression:
        """Parse assignment expressions"""
        expr = self.parse_ternary()
        
        if self.current_token.type in [TokenType.EQ, TokenType.PLUSEQ, TokenType.MINUSEQ, 
                                      TokenType.MULEQ, TokenType.DIVEQ, TokenType.MODEQ]:
            op = self.current_token.val
            self.advance()
            right = self.parse_assignment()
            return AssignmentExpression(expr, op, right)
        
        return expr
    
    def parse_ternary(self) -> Expression:
        """Parse ternary conditional operator"""
        expr = self.parse_logical_or()
        
        if self.current_token.type == TokenType.QUESTION:
            self.advance()
            then_expr = self.parse_expression()
            self.eat(TokenType.COLON)
            else_expr = self.parse_ternary()
            # Could create TernaryExpression class for this
            return BinaryExpression(BinaryExpression(expr, "?", then_expr), ":", else_expr)
        
        return expr
    
    def parse_logical_or(self) -> Expression:
        """Parse logical OR"""
        expr = self.parse_logical_and()
        
        while self.current_token.type == TokenType.OR:
            op = self.current_token.val
            self.advance()
            right = self.parse_logical_and()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_logical_and(self) -> Expression:
        """Parse logical AND"""
        expr = self.parse_bitwise_or()
        
        while self.current_token.type == TokenType.AND:
            op = self.current_token.val
            self.advance()
            right = self.parse_bitwise_or()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_bitwise_or(self) -> Expression:
        """Parse bitwise OR"""
        expr = self.parse_bitwise_xor()
        
        while self.current_token.type == TokenType.BITOR:
            op = self.current_token.val
            self.advance()
            right = self.parse_bitwise_xor()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_bitwise_xor(self) -> Expression:
        """Parse bitwise XOR"""
        expr = self.parse_bitwise_and()
        
        while self.current_token.type == TokenType.BITXOR:
            op = self.current_token.val
            self.advance()
            right = self.parse_bitwise_and()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_bitwise_and(self) -> Expression:
        expr = self.parse_equality()
        
        while self.current_token.type == TokenType.BITAND:
            op = self.current_token.val
            self.advance()
            right = self.parse_equality()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_equality(self) -> Expression:
        expr = self.parse_relational()
        
        while self.current_token.type in [TokenType.EQEQ, TokenType.NOTEQ]:
            op = self.current_token.val
            self.advance()
            right = self.parse_relational()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_relational(self) -> Expression:
        expr = self.parse_shift()
        
        while self.current_token.type in [TokenType.LT, TokenType.LTEQ, TokenType.GT, TokenType.GTEQ]:
            op = self.current_token.val
            self.advance()
            right = self.parse_shift()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_shift(self) -> Expression:
        expr = self.parse_additive()
        
        while self.current_token.type in [TokenType.LSHIFT, TokenType.RSHIFT]:
            op = self.current_token.val
            self.advance()
            right = self.parse_additive()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_additive(self) -> Expression:
        expr = self.parse_multiplicative()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.val
            self.advance()
            right = self.parse_multiplicative()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_multiplicative(self) -> Expression:
        expr = self.parse_unary()
        
        while self.current_token.type in [TokenType.ASTERISK, TokenType.SLASH, TokenType.PERCENT]:
            op = self.current_token.val
            self.advance()
            right = self.parse_unary()
            expr = BinaryExpression(expr, op, right)
        
        return expr
    
    def parse_unary(self) -> Expression:
        if self.current_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT, 
                                      TokenType.BITNOT, TokenType.INCR, TokenType.DECR]:
            op = self.current_token.val
            self.advance()
            expr = self.parse_unary()
            return UnaryExpression(op, expr)
        else:
            return self.parse_postfix()
    
    def parse_postfix(self) -> Expression:
        expr = self.parse_primary()
        
        while True:
            if self.current_token.type == TokenType.LPAREN:
                # Function call
                self.advance()
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                self.eat(TokenType.RPAREN)
                expr = FunctionCall(expr, args)
            elif self.current_token.type == TokenType.LBRACKET:
                # Array access
                self.advance()
                index = self.parse_expression()
                self.eat(TokenType.RBRACKET)
                expr = ArrayAccess(expr, index)
            elif self.current_token.type == TokenType.DOT:
                # Member access
                self.advance()
                if self.current_token.type != TokenType.IDENT:
                    self.abort("Expected member name")
                member = self.current_token.val
                self.advance()
                expr = MemberAccess(expr, member, False)
            elif self.current_token.type == TokenType.ARROW:
                # Pointer member access
                self.advance()
                if self.current_token.type != TokenType.IDENT:
                    self.abort("Expected member name")
                member = self.current_token.val
                self.advance()
                expr = MemberAccess(expr, member, True)
            elif self.current_token.type in [TokenType.INCR, TokenType.DECR]:
                # Postfix increment/decrement
                op = self.current_token.val
                self.advance()
                expr = UnaryExpression(op + "_post", expr)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> Expression:
        """Parse primary expressions"""
        if self.current_token.type == TokenType.NUMBER:
            value = float(self.current_token.val) if '.' in self.current_token.val else int(self.current_token.val)
            self.advance()
            return Literal(value)
        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.val
            self.advance()
            return Literal(value)
        elif self.current_token.type == TokenType.IDENT:
            name = self.current_token.val
            self.advance()
            return Identifier(name)
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            self.abort(f"Unexpected token in expression: {self.current_token.type}")
    
    def is_type(self) -> bool:
        return self.current_token.type in [
            TokenType.VOID, TokenType.CHAR, TokenType.SHORT, TokenType.INT, 
            TokenType.LONG, TokenType.FLOAT, TokenType.DOUBLE, TokenType.SIGNED, 
            TokenType.UNSIGNED, TokenType.STRUCT, TokenType.UNION, TokenType.ENUM
        ]

# Usage Example
def main():
    source_code = """
    int main() {
        int x = 10;
        int y = 20;
        if (x < y) {
            return x + y;
        }
        return 0;
    }
    """
    
    try:
        lex = lexer(source_code)
        print("Tokenizing successful!")
        
        # Test the lexer
        token_count = 0
        while True:
            token = lex.get_token()
            print(f"Token: '{token.val}' | Type: {token.type}")
            token_count += 1
            
            if token.type == TokenType.EOF:
                break
                
        print(f"Total tokens: {token_count}")
        
    except SystemExit as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()