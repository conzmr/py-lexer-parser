import sys
import re

class Error:
	def __init__(self, type, line_num, char_num, ch, line):
		self.type = type
		self.line_num = line_num
		self.char_num = char_num
		self.ch = ch
		self.line = line
	def __repr__(self):
		return '{}: Invalid {} in {} \nLine {}, character {}.'.format(self.type, repr(self.ch), repr(self.line), repr(self.line_num), repr(self.char_num))

class Token:
	def __init__(self, type, value, line, ch):
		self.value = value
		self.type = type
		self.ch = ch
		self.line = line
	def __repr__(self):
		return '{}({}, {}, {}, {})'.format(self.__class__.__name__, repr(self.type), repr(self.value), repr(self.line), repr(self.ch))


class Lexer:
	def __init__(self):
		self.tokens = []
		self.errors = []
		self.current = ''
		self.symbol_table = {
		'keywords': {
		'principal': 'KEYWORD',
		'entero': 'KEYWORD',
		'real': 'KEYWORD',
				'logico': 'KEYWORD',
				'si': 'KEYWORD',
				'mientras': 'KEYWORD',
				'regresa': 'KEYWORD',
				'verdadero': 'KEYWORD',
				'falso': 'KEYWORD'
			}
		}

	def add_token(self, type, val, line, char):
		self.tokens.append(Token(type, val, line, char))
		self.current = None

	def add_token_instance(self, token):
		self.tokens.append(token)
		self.current = None

	def get_tokens(self, source_code):
		self.tokens = []
		self.current = None
		self.errors = []
		line_num = 0
		ch_num = 0
		for line in source_code:
			line_num += 1
			for ch in line:
				ch_num += 1
				if ch and ch.strip():
					if not (self.current is None):
						if self.current.type == 'ASSIGNATION_OP':
							if ch in "=":
								self.add_token('RELATIONAL_OP', "==", self.current.line, self.current.ch)
								continue
							else:
								self.add_token_instance(self.current)
						elif self.current.type == 'INTEGER':
							if ch in ".":
								self.current.type = 'REAL'
								self.current.value += ch
								continue
							elif re.match("[ 0-9 ]", ch):
								self.current.value += ch
								continue
							else:
								self.add_token_instance(self.current)
						elif self.current.type == 'REAL':
							if re.match("[ 0-9 ]", ch):
								self.current.value += ch
								continue
							else:
								if re.match("[ 0-9 ]*.[ 0-9 ]*", self.current.value):
									self.add_token_instance(self.current)
								else:
									self.errors.append(Error("LexicalError", line_num, ch_num, ch, line))
						elif self.current.type == 'IDENTIFIER':
							if re.match("[a-zA-Z0-9]", ch):
								self.current.value += ch
								continue
							else:
								self.add_token_instance(self.current)
					if ch in "+-*/^":
						self.add_token('ARITHMETIC_OP', ch, line_num, ch_num)
					elif ch in "&|!":
						self.add_token('LOGICAL_OP', ch, line_num, ch_num)
					elif ch in "<>":
						self.add_token('RELATIONAL_OP', ch, line_num, ch_num)
					elif ch in "{":
						self.add_token('LEFT_KEY', ch, line_num, ch_num)
					elif ch in "}":
						self.add_token('RIGHT_KEY', ch, line_num, ch_num)
					elif ch in "(":
						self.add_token('LEFT_PARENTHESIS', ch, line_num, ch_num)
					elif ch in ")":
						self.add_token('RIGHT_PARENTHESIS', ch, line_num, ch_num)
					elif ch in ";":
						self.add_token('SEMICOLON', ch, line_num, ch_num)
					elif ch in ",":
						self.add_token('COLON', ch, line_num, ch_num)
					elif ch in "=":
						self.current = Token('ASSIGNATION_OP', ch, line_num, ch_num)
					elif re.match("[ a-z ]", ch):
						self.current = Token('IDENTIFIER', ch, line_num, ch_num)
					elif re.match("[ 0-9 ]", ch):
						self.current = Token('INTEGER', ch, line_num, ch_num)
					else:
						self.errors.append(Error("LexicalError", line_num, ch_num, ch, line))
		print(self.tokens)
		print(self.errors)

def main():
	file = sys.argv[1]
	with open(file,'r') as source_code:
		lexer = Lexer()
		lexer.get_tokens(source_code)

if __name__ == "__main__":
    main()
