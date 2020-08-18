def int_from_2c(arg: int, bitsize: int) -> int:
    arg &= 2 ** bitsize - 1
    sign = arg >> (bitsize - 1)
    return arg - ((1 << bitsize) if sign else 0)


def int_in_2c_to_hex(arg: int, bitsize: int) -> str:
    if arg < 0:
        arg += 1 << bitsize
    return f'0x{arg:X}'
