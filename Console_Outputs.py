from colorama import Fore, Back, Style

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

def print_count_table(Count, maxkey):
    print('\nCount table:')
    print('  ', '|', end= ' ')
    for h in range(len(Count[0])):
        print(format(h,'4X'), end= ' ')
    print()
    print('----' + '-----'*16)
    for i in range(len(Count)):
        print(format(i,'2X'), '|', end= ' ')
        for j in range(len(Count[i])):
            if i == maxkey[0] and j == maxkey[1]: # print maxkey with red color
                print(Fore.RED, end= '')
                print(format(int(Count[i][j]),'4d'), end= ' ')
                print(Style.RESET_ALL, end= '')
            else:
                print(format(int(Count[i][j]),'4d'), end= ' ')  
        print()
    print('maxkey:')
    print('hex ' + hex_str(maxkey[0],4,1) + hex_str(maxkey[1],4,1))
    print('bin ' + bin_str(maxkey[0],4,1) + bin_str(maxkey[1],4,1))

def print_linear_approximation_table(Approx):
    print('\nLinear approximation table:')
    print('   |' + '       '*8 + 'b')
    print(' a ' + '|', end= ' ')
    for h in range(len(Approx[0])):
        print(format(h,'6X'), end= ' ')
    print()
    print('----' + '-------'*16)
    for i in range(len(Approx)):
        print(format(i,'2X'), '|', end= ' ')
        for j in range(len(Approx[i])):
            if Approx[i][j] >= 1/4 or Approx[i][j] <= -1/4:
                print(Fore.RED, end= '')
                print(format(Approx[i][j],' .3f'), end= ' ')
                print(Style.RESET_ALL, end= '')
            else:
                print(format(Approx[i][j],' .3f'), end= ' ')
        print()

def print_difference_distribution_table(N_D_values):
    print('\nDifference distribution table:')
    print('   |' + '   '*8 + 'b\'')
    print(' a\'' + '|', end= ' ')
    for h in range(len(N_D_values[0])):
        print(format(h,'2X'), end= ' ')
    print()
    print('----' + '---'*16)
    for i in range(len(N_D_values)):
        print(format(i,'2X'), '|', end= ' ')
        for j in range(len(N_D_values[i])):
            print(format(N_D_values[i][j],'2d'), end= ' ')
        print()

def print_s_box(s_box):
    print('\nS-Box:')
    s_box_in_str = 'input  = '
    s_box_out_str = 'output = '
    for i in s_box:
        s_box_in_str += format(s_box[i],'2X')
        s_box_out_str += format(i,'2X')
    print(s_box_in_str + '\n' + s_box_out_str)

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
