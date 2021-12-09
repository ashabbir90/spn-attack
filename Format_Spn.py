def hex_str(input, l=4, m=4):
    """
    Generates a formated string of hex numbers from an integer
    Param input: Input integer
    Param l: Bit length per block
    Param m: Block count
    Return: String of hex values
    """
    out = ''
    for i in range(m):
        input_i = input % (2 ** l)
        out = format(input_i,f'{l}X') + ' ' + out
        input = input >> l
    return out

def bin_str(input, l=4, m=4):
    """
    Generates a formated string of bin numbers from an integer
    Param input: Input integer
    Param l: Bit length
    Param m: Block count
    Return: String of bin values
    """
    output = ''
    for i in range(m):
        input_i = input % (2 ** l)
        output = format(input_i, f'0{l}b') + ' ' + output
        input = input >> l
    return output

if __name__ == '__main__':
    x = 0b00111010100101001101011000111111
    print(bin_str(x))
    print(hex_str(x))
    print(bin_str(x,2,8))
    print(hex_str(x,2,8))

# Output:
# 1101 0110 0011 1111 
#    D    6    3    F
# 11 01 01 10 00 11 11 11
#  3  1  1  2  0  3  3  3
