##### GOALPOST:
##### MORE PRIMITIVES (Mod, swap, dup, over, rot, drop // loop)
##### COMPILE MODE(user defined words(body is a list of tokens))
### test programs, while and if, fibonacci

#TODO: diffrentiate Lexer from interpreter


class Token:
    def __init__(self, type, value, body=[], flags=''):
        self.type = type
        self.value = value
        self.flags = flags
        self.body = body # for user defined words, a list of tokens
        
    def __str__(self):
        return '(Token, {type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.current_char = self.text[self.index]
        self.operands = { # used to keep track for documentation purposes, not necessarily ever referenced
            '+' : Token('Plus', '+'),
            '-' : Token('Minus', '-'), #TODO more primites (especially stack ones)
            '*' : Token('Multiply', '*'),
            '/' : Token('Divide', '/'),
            'print' : Token('Print', 'print'),
            'branch' : Token('Branch', 'branch'),
            'branch?' : Token('Branch?', 'branch'),
            ':' : Token('Compile-flag', ':'),
            ';' : Token('Execute-flag', ';'),
            '(' : Token('Comment', '('),
            'swap' : Token('Swap', 'swap'),
            'dup' : Token('Dup', 'dup'),
            'rot' : Token('Rot', 'rot'),
            'drop' : Token('Drop', 'drop'),
            'over' : Token('Over', 'over'),
            'mod' : Token('Mod', 'mod')
        }

        self.tokenized_text = []

    def advance(self, word_length=1): #TODO: take length of command word as optional argument
        self.index += word_length
        if self.index > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.index]

    def jump_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def error(self):
        raise Exception('Syntax Error')

    def integer(self):
        """ return a multidigit integer from input text """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def next_token(self):
        """ Get the next token from the input text and push it onto the tokenized input """

        while self.current_char is not None:

            if self.current_char.isspace():
                self.jump_whitespace()
                continue

            if self.current_char.isdigit():
                return Token('Integer', self.integer())

            if self.current_char == ':' :
                self.advance()
                self.execute_mode = False
                self.compile_mode = True


            
            if self.current_char == '+':
                self.advance()
                return Token('Plus', '+')

            if self.current_char == '-':
                self.advance()
                return Token('Minus', '-')

            if self.current_char == '*':
                self.advance()
                return Token('Multiply', '*')

            if self.current_char == '/':
                self.advance()
                return Token('Divide', '/')

            if self.current_char == '(':
                self.advance()
                comment_body = ""

                idx = 0
                while self.text[self.index+idx] != ')':
                    comment_body += self.text[self.index+idx]
                    idx += 1
                
                self.advance(idx+1)
                return Token('Comment', comment_body)

  
            # whole word commands
            if 'print' in self.text[self.index : self.index+5]:
                self.advance(5)
                return Token('Print', 'print')

            if 'branch?' == self.text[self.index : self.index+7]:
                self.advance(7)
                return Token('Branch?', 'branch?')

            if 'branch' == self.text[self.index : self.index+6]:
                self.advance(6)
                return Token('Branch', 'branch')

            if 'swap' == self.text[self.index : self.index+4]:
                self.advance(4)
                return Token('Swap', 'swap')
            
            if 'over' == self.text[self.index : self.index+4]:
                self.advance(4)
                return Token('Over', 'over')

            if 'drop' == self.text[self.index : self.index+4]:
                self.advance(4)
                return Token('Drop', 'drop')

            if 'rot' == self.text[self.index : self.index+3]:
                self.advance(3)
                return Token('Rot', 'rot')
            
            if 'dup' == self.text[self.index : self.index+3]:
                self.advance(3)
                return Token('Dup', 'dup')

            if 'mod' == self.text[self.index : self.index+3]:
                self.advance(3)
                return Token('Mod', 'mod')
 
            self.error()
            
        return Token('EOF', None)
        
    def tokenize_input(self):
        """ turn the input into a array of Tokens"""
        self.current_token = self.next_token()

        while self.current_token.value != None:
            
            self.tokenized_text.append(self.current_token)
            self.current_token = self.next_token()



class Interpreter:
    def __init__(self, text):
        
        self.lexer = Lexer(text)
        self.lexer.tokenize_input()
        self.tokenized_input = self.lexer.tokenized_text
        self.current_token = None
        self.stack = [] # has integers/objects(perhaps in future, TODO), python's callstack used as the callstack (out of convenience)

        
        
        self.execute_mode = True # starts off in execute_mode
        self.compile_mode = False

   
    def eat_integer(self, token):
        if token.type == 'Integer':
            self.stack.append(token.value)
        else:
            raise Exception("eat_integer has received a non-integer Token")      
 
    def process_tokenized_input(self): #TODO compile mode, execute mode, comment mode
        idx = 0
        
        while idx < len(self.tokenized_input):
            token = self.tokenized_input[idx]
            if self.execute_mode:
                if token.type == 'Integer':
                    self.eat_integer(token)
                
                elif token.type == 'Comment':
                    pass

                

                elif token.type == 'Plus':
                    result = 0
                    
                    if len(self.stack) < 2 : raise Exception('Overflow error')
                    result += self.stack.pop()
                    result += self.stack.pop()
                    self.stack.append(result)

                elif token.type == 'Minus':
                    result = 0

                    if len(self.stack) < 2 : raise Exception('Overflow error')
                    result += self.stack.pop()
                    result -= self.stack.pop()
                    self.stack.append(result)
                
                elif token.type == 'Multiply':
                    result = 0
                    if len(self.stack) < 2 : raise Exception('Overflow error')
                    result += self.stack.pop()
                    result *= self.stack.pop()
                    self.stack.append(result)

                elif token.type == 'Divide':
                    result = 0
                    if len(self.stack) < 2 : raise Exception('Overflow error')
                    result += self.stack.pop()
                    result /= self.stack.pop()
                    self.stack.append(int(result))

                elif token.type == 'Mod':
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()

                    self.stack.append(int(n2 % n1))
                
                elif token.type == 'Print':
                    print(self.stack)

                elif token.type == 'Branch':
                    leap_address = self.stack.pop()
                    if leap_address-1 < 0: raise Exception("Out of program indexed branch")
                    idx = leap_address-1

                elif token.type == 'Branch?':
                    comparable = self.stack.pop()
                    leap_address = self.stack.pop()

                    if leap_address-1 < 0: raise Exception("Out of program indexed branch")

                    if comparable > 0:
                        idx = leap_address-1
                    else: # do nothing
                        pass

                elif token.type == 'Swap':
                    n2 = self.stack.pop()
                    n1 = self.stack.pop()
                    self.stack.append(n1)
                    self.stack.append(n2)

                elif token.type == 'Dup':
                    n = self.stack.pop()
                    self.stack.append(n)
                    self.stack.append(n)
                
                elif token.type == 'Rot':
                    n3 = self.stack.pop()
                    n2 = self.stack.pop()
                    n1 = self.stack.pop()

                    self.stack.append(n2)
                    self.stack.append(n3)
                    self.stack.append(n1)

                elif token.type == 'Over':
                    n2 = self.stack.pop()
                    n1 = self.stack.pop()

                    self.stack.append(n1)
                    self.stack.append(n2)
                    self.stack.append(n1)

                elif token.type == 'Drop':
                    self.stack.pop()
                    
            
            if self.compile_mode:
                pass


            idx += 1

                    


def main():
    print("""This is a partial implementation of an intentionally\nunspecified and possibly non-existent standard for a Forth-like language.\n\nFeature list:\n-Primitives\n-Branch logic\n-User-defined words\n-Comments""")
    while True:
        try:
            text = input('> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        #print(interpreter.tokenized_input)
        interpreter.process_tokenized_input()

if __name__ == "__main__":
    main()