from pyparsing import *


integer = Word(nums)
integer.Name = "integer"
integer.ParseAction = lambda t: int(t[0])
integer = Word(nums).setName("integer").setParseAction(lambda t:int(t[0]))

decimal = (Word(nums)+Optional("."+Optional(Word(nums)))).setParseAction(lambda t: int(t[0]))


number = integer | decimal


LPAREN = Suppress("(")
RPAREN = Suppress(")")

expression = forward()
expression << (variable | number | Group(LPAREN+expression+RPAREN))

def parseTree(atoms, ops):
	"""
	"""

def evalTree(atoms, ops):
	"""
	"""