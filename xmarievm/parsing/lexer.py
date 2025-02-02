import ply.lex as lex

tokens = (
    'ID',
    'NUM',
    'HEXNUM',
    'JNS',
    'LOAD',
    'STORE',
    'ADD',
    'SUBT',
    'SUBTI',
    'INPUT',
    'OUTPUT',
    'HALT',
    'SKIPCOND',
    'JUMP',
    'CLEAR',
    'ADDI',
    'JUMPI',
    'LOADI',
    'STOREI',
    'PUSH',
    'POP',
    'INCR',
    'DECR',
    'SHIFTL',
    'SHIFTR',
    'STOREX',
    'LOADX',
    'STOREY',
    'LOADY',
    'NEWLINE',
    'DEC',
    'HEX',
    'LABEL',
)

reserved = {
    'JnS': 'JNS',
    'Load': 'LOAD',
    'LoadI': 'LOADI',
    'Store': 'STORE',
    'StoreI': 'STOREI',
    'Add': 'ADD',
    'AddI': 'ADDI',
    'Subt': 'SUBT',
    'SubtI': 'SUBTI',
    'Input': 'INPUT',
    'Output': 'OUTPUT',
    'Skipcond': 'SKIPCOND',
    'Jump': 'JUMP',
    'JumpI': 'JUMPI',
    'Clear': 'CLEAR',
    'Halt': 'HALT',
    'DEC': 'DEC',
    'HEX': 'HEX',
    'StoreX': 'STOREX',
    'StoreY': 'STOREY',
    'LoadX': 'LOADX',
    'LoadY': 'LOADY',
    'Push': 'PUSH',
    'Pop': 'POP',
    'ShiftL': 'SHIFTL',
    'ShiftR': 'SHIFTR',
    'Incr': 'INCR',
    'Decr': 'DECR',
}

t_JNS = r'JnS'
t_LOAD = r'Load'
t_LOADI = r'LoadI'
t_STORE = r'Store'
t_STOREI = r'StoreI'
t_ADD = r'Add'
t_ADDI = r'AddI'
t_SUBT = r'Subt'
t_INPUT = r'Input'
t_OUTPUT = r'Output'
t_SKIPCOND = r'Skipcond'
t_JUMP = r'Jump'
t_JUMPI = r'JumpI'
t_CLEAR = r'Clear'
t_HALT = r'Halt'
t_PUSH = r'Push'
t_POP = r'Pop'
t_SHIFTL = r'ShiftL'
t_SHIFTR = r'ShiftR'
t_STOREX = r'StoreX'
t_STOREY = r'StoreY'
t_DEC = r'DEC'
t_HEX = r'HEX'
t_ignore = ' \t'


def t_NEWLINE(t):
    r'\n\s*'
    t.lexer.lineno += 1  # lineno represents memory address
    if not hasattr(t.lexer, 'line_number'):
        t.lexer.line_number = 2
    else:
        t.lexer.line_number += t.value.count('\n')
    return t


def t_LABEL(t):
    r'[A-Za-z_]+,'
    return t


def t_ID(t):
    r'[A-Za-z_]+'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_HEXNUM(t):
    r'0x[0-9A-F]+'
    t.value = int(t.value, 16)
    return t


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


lexer = lex.lex()
