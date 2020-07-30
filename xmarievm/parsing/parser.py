import ply.yacc as yacc

import xmarievm.parsing.ast_types as ast_types
from xmarievm.parsing.lexer import tokens

instructions = []


def _get_ast_obj(token: str) -> type:
    return getattr(ast_types, token)


def p_program(p):
    '''
    program : instructions
    '''
    instructions = []
    labels = set()
    for ast_obj in p[1]:
        if isinstance(ast_obj, ast_types.Label):
            if ast_obj.name in labels:
                raise NameError(f'Redefined label: {ast_obj.name}')
            labels.add(ast_obj.name)
        instructions.append(ast_obj)
    p[0] = p[1]


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


def p_single_instruction(p):
    'single_instruction : action NEWLINE'
    p[0] = p[1]


def p_complex_instruction(p):
    'complex_instruction : command arg NEWLINE'
    p[0] = _get_ast_obj(p[1])(p[2])


def p_label_definition(p):
    'label_definition : LABEL number_definition'
    p[0] = ast_types.Label(name=p[1][:-1], addr=p.lexer.lineno)


def p_number_definition(p):
    '''
    number_definition : HEX HEXNUM NEWLINE
                      | DEC NUM NEWLINE
    '''
    p[0] = _get_ast_obj(p[1])(p[2])


def p_action(p):
    '''
    action : HALT
            | INPUT
    '''
    p[0] = _get_ast_obj(p[1])()


def p_command(p):
    '''
    command : STORE
            | LOAD
    '''
    p[0] = p[1]


def p_arg(p):
    '''
    arg : NUM
        | ID
    '''
    p[0] = p[1]


parser = yacc.yacc(write_tables=False, debug=False)

code = '''\
Load X
Store Y

MyLabel, HEX 0x20
MyAnotherLabel, DEC 20
TurboHex, HEX 0xAA
Load Z
Store THERE
Load 10
Halt
'''
prog = parser.parse(code)
print(prog)
