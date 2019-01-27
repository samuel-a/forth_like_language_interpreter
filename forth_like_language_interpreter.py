

class Token:
    def __init__(self, value, type="", body=[], flags=''):
        self.type = type
        self.value = value
        self.flags = flags
        self.body = body # for user defined words, a list of tokens
        
    def __str__(self):
        return '(Token, {value}, {type})'.format(
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
            '+' : Token('+'),
            '-' : Token('-'),
            '*' : Token('*'),
            '/' : Token('/'),
            'print' : Token('print'),
            'branch' : Token('branch'),
            'branch?' : Token('branch?'),
            ':' : Token(':'),
            ';' : Token(';'),
            '(' : Token('('),
            'swap' : Token('swap'),
            'dup' : Token('dup'),
            'rot' : Token('rot'),
            'drop' : Token('drop'),
            'over' : Token('over'),
            'mod' : Token('mod')
        }

        self.tokenized_text = []

    def advance(self):
        self.index += 1
        if self.index > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.index]

    def jump_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def error(self):
        raise Exception('Syntax Error')

    def next_token(self):
        """ Get the next token from the input text and push it onto the tokenized input """

        while self.current_char is not None:

            if self.current_char.isspace():
                self.jump_whitespace()
                continue

            value = ""

            if self.current_char == '(':
                while not self.current_char == ')':
                    value += self.current_char
                    self.advance()
                self.advance()
                return Token(value + ')', 'Comment')
            
            while self.current_char is not None and not self.current_char.isspace():
                value += self.current_char
                self.advance()
            
            if value[0].isdigit():
                return Token(int(value), 'Integer')
            else:
                return Token(value)
            
 
            self.error()
        return Token(None)

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

        self.user_defined_words = []
        
        
        self.execute_mode = True # starts off in execute_mode

   
 
    def process_tokenized_input(self): #TODO compile mode, execute mode
        idx = 0
        
        while idx < len(self.tokenized_input):
            token = self.tokenized_input[idx]
            if token.type == 'Integer':
                self.stack.append(token.value)
            
            elif token.type == 'Comment':
                pass

            

            elif token.value == '+':
                result = 0
                
                if len(self.stack) < 2 : raise Exception('Overflow error')
                result += self.stack.pop()
                result += self.stack.pop()
                self.stack.append(result)

            elif token.value == '-':
                result = 0

                if len(self.stack) < 2 : raise Exception('Overflow error')
                result += self.stack.pop()
                result -= self.stack.pop()
                self.stack.append(result)
            
            elif token.value == '*':
                result = 0
                if len(self.stack) < 2 : raise Exception('Overflow error')
                result += self.stack.pop()
                result *= self.stack.pop()
                self.stack.append(result)

            elif token.value == '/':
                result = 0
                if len(self.stack) < 2 : raise Exception('Overflow error')
                result += self.stack.pop()
                result /= self.stack.pop()
                self.stack.append(int(result))

            elif token.value == 'mod':
                n1 = self.stack.pop()
                n2 = self.stack.pop()

                self.stack.append(int(n2 % n1))
            
            elif token.value == 'print':
                print(str(self.stack) + ' <top')

            elif token.value == 'branch':
                leap_address = self.stack.pop()
                if leap_address-1 < 0: raise Exception("Out of program indexed branch")
                idx = leap_address-1

            elif token.value == 'branch?':
                comparable = self.stack.pop()
                leap_address = self.stack.pop()

                if leap_address-1 < 0: raise Exception("Out of program indexed branch")

                if comparable > 0:
                    idx = leap_address-1
                else: # do nothing
                    pass

            elif token.value == 'swap':
                n2 = self.stack.pop()
                n1 = self.stack.pop()
                self.stack.append(n1)
                self.stack.append(n2)

            elif token.value == 'dup':
                n = self.stack.pop()
                self.stack.append(n)
                self.stack.append(n)
            
            elif token.value == 'rot':
                n3 = self.stack.pop()
                n2 = self.stack.pop()
                n1 = self.stack.pop()

                self.stack.append(n2)
                self.stack.append(n3)
                self.stack.append(n1)

            elif token.value == 'over':
                n2 = self.stack.pop()
                n1 = self.stack.pop()

                self.stack.append(n1)
                self.stack.append(n2)
                self.stack.append(n1)

            elif token.value == 'drop':
                self.stack.pop()

            elif token.value == ':': 
                idx += 1
                body = [] # list of tokens
                name = self.tokenized_input[idx].value
                idx += 1
                while self.tokenized_input[idx].value != ';':
                    body.append(self.tokenized_input[idx])
                    
                    idx += 1
                
                self.user_defined_words.append(Token(name, 'UDW', body))

            elif token.value in [uwd.value for uwd in self.user_defined_words]:
                uwd = [i for i in self.user_defined_words if i.value == token.value]
                l1 = self.tokenized_input[:(idx+1)] + uwd[0].body
                l2 = self.tokenized_input[(idx+1):]

                self.tokenized_input = l1 + l2



                    
            if idx < len(self.tokenized_input): idx += 1

                    


def main():
    print("""This is a partial implementation of an intentionally\nunspecified and possibly non-existent standard for a Forth-like language.\n\nFeature list:\n-Primitives\n-Branch logic\n-User-defined words(macros)\n-Comments""")
    while True:
        try:
            text = input('> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        interpreter.process_tokenized_input()
        
        

if __name__ == "__main__":
    main()