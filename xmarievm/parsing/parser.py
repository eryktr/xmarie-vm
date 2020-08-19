import ply.yacc as yacc

import xmarievm.parsing.ast_types as ast_types
from xmarievm.parsing import translator
from xmarievm.parsing.ast_types import Program
from xmarievm.const import MAX_DEC, MEM_BITSIZE, MAX_HEX
from xmarievm.parsing.lexer import tokens, lexer

instructions = []


def _get_ast_obj(token: str) -> type:
    return getattr(ast_types, token)


def p_program(p):
    '''
    program : instructions
    '''
    instructions = []
    labels = {}
    for ast_obj in p[1]:
        if isinstance(ast_obj, ast_types.Label):
            if ast_obj.name in labels:
                raise NameError(f'Redefined label: {ast_obj.name}')
            labels[ast_obj.name] = ast_obj.addr
            instructions.append(ast_obj.val)
        else:
            instructions.append(ast_obj)
    encoded_instructons = translator.translate(instructions, labels)
    p[0] = Program(encoded_instructons, labels)


def p_instructions_instruction(p):
    '''
    instructions : instruction
    '''
    p[0] = [p[1]]


def p_instructions_instructions(p):
    '''
    instructions : instructions instruction
    '''
    p[0] = p[1] + [p[2]]


def p_instruction(p):
    '''
    instruction : single_instruction
                | complex_instruction
                | label_definition
    '''
    p[0] = p[1]


def p_strict_instruction(p):
    '''
    strict_instruction : single_instruction
                       | complex_instruction
    '''
    p[0] = p[1]


def p_single_instruction(p):
    'single_instruction : action NEWLINE'
    p[0] = p[1]


def p_complex_instruction(p):
    'complex_instruction : command arg NEWLINE'
    p[0] = _get_ast_obj(p[1])(p[2])


def p_label_definition(p):
    '''
    label_definition : LABEL number_definition
                    | LABEL strict_instruction
    '''

    p[0] = ast_types.Label(name=p[1][:-1], addr=p.lexer.lineno - 1, val=p[2])


def p_number_definition(p):
    '''
    number_definition : HEX HEXNUM NEWLINE
                      | DEC NUM NEWLINE
    '''
    if p[1] == 'DEC' and p[2] > MAX_DEC:
        raise ValueError(f'Maximum integer value: {MAX_DEC} exceeded.')
    if p[1] == 'HEX' and p[2] > MAX_HEX:
        raise ValueError(f'Maximum variable length: {MEM_BITSIZE} exceeded')
    p[0] = _get_ast_obj(p[1])(p[2])


def p_action(p):
    '''
    action : HALT
            | INPUT
            | OUTPUT
            | CLEAR
            | INCR
            | DECR
            | PUSH
            | POP
    '''
    p[0] = _get_ast_obj(p[1])()


def p_command(p):
    '''
    command : STORE
            | STOREI
            | LOAD
            | ADD
            | SUBT
            | SKIPCOND
            | ADDI
            | SUBTI
            | JUMP
            | JUMPI
            | SHIFTL
            | SHIFTR
    '''
    p[0] = p[1]


def p_arg(p):
    '''
    arg : NUM
        | ID
    '''
    p[0] = p[1]


_parser = yacc.yacc(write_tables=False, debug=False)


def parse(code):
    lexer.lineno = 0
    return _parser.parse(code.lstrip())

# code = '''\
# Load 20
# Store Y
#
# MyLabel, HEX 0x20
# MyAnotherLabel, DEC 20
# TurboHex, HEX 0xAA
# Load Z
# Store THERE
# Load 10
# Halt
# '''
# prog = parser.parse(code)
# print(prog)
