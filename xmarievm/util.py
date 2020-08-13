def int_from_2c(arg: int, bitsize: int) -> int:
    arg &= 2 ** bitsize - 1
    sign = arg >> (bitsize - 1)
    return arg - ((1 << bitsize) if sign else 0)
