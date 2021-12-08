import Basic_Spn as spn

def pi_s_inv(s_box, vr, l=4, m=4):
    """
    Inverse packet substitution operation
    Param s_box: S-Box parameter
    Param vr: Input Bit String, 2^l Bits
    Return: Output Bit String, 2^l Bits
    """
    ur = 0
    for i in range(m):
        vri = vr % (2 ** l)
        uri = s_box.index(vri)
        ur = ur + (uri << (l * i))
        vr = vr >> l
    return ur

def print_hex(x, l=4, m=4):
    out = ''
    for i in range(m):
        xi = x % (2 ** l)
        out = (l-1)*' ' + hex(xi)[2:] + ' ' + out
        x = x >> l
    print('hex', out)

def print_bin(x, l=4, m=4):
    out = ''
    for i in range(m):
        xi = x % (2 ** l)
        out = format(xi,f'0{2 + l}b')[2:] + ' ' + out
        x = x >> l
    print('bin', out)

def linear_attack(T_set, pi_s_inv):
    T = len(T_set)
    Count = [0] * 16
    for i in range(16):
        Count[i] = [0] * 16
    
    v4 = 0
    u4 = 0
    z = 0

    for (x,y) in T_set:
        for L1 in range(16):
            for L2 in range(16):
                v4 = L1 ^ int(format(y,'016b')[4:8],2)
                v4 = (v4 << 8) + L2 ^ int(format(y,'016b')[12:16],2)
                u4 = pi_s_inv(spn.S_Box,int(format(v4,'016b')[4:8],2),4,1)
                u4 = (u4 << 8) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[12:16],2),4,1)
                z = ( int(format(x,'016b')[5-1],2)
                    ^ int(format(x,'016b')[7-1],2)
                    ^ int(format(x,'016b')[8-1],2)
                    ^ int(format(u4,'016b')[6-1],2)
                    ^ int(format(u4,'016b')[8-1],2)
                    ^ int(format(u4,'016b')[14-1],2)
                    ^ int(format(u4,'016b')[16-1],2)
                    )
                if z == 0:
                    Count[L1][L2] += 1
    
    MAX = -1
    maxkey = (0,0)
    for L1 in range(16):
        for L2 in range(16):
            Count[L1][L2] = abs(Count[L1][L2] - T/2)
            if Count[L1][L2] > MAX:
                MAX = Count[L1][L2]
                maxkey = (L1,L2)
    
    # print Count Table
    print('  ', '|', end= ' ')
    for h in range(len(Count[0])):
        print(format(h,'4X'), end= ' ')
    print()
    print('-----'*17)
    for i in range(len(Count)):
        print(format(i,'2X'), '|', end= ' ')
        for j in range(len(Count[i])):
            print(format(int(Count[i][j]),'4d'), end= ' ')
        print()

    print('maxkey_bin = (', format(maxkey[0],'04b'), ',', format(maxkey[1],'04b'), ')')
    print('maxkey_hex = (', format(maxkey[0],'4X'), ',', format(maxkey[1],'4X'), ')')

    return maxkey

if __name__ == '__main__':
    K = 0b00111010100101001101011000111111
    T_set = [(x, spn.encrypt(K, x)) for x in range(8000)]
    linear_attack(T_set,pi_s_inv)

# Output:
#    |    0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F 
# -------------------------------------------------------------------------------------
#  0 |  117   57   26   29   52   21   55   15   56   96   62   11   70   73   42   18 
#  1 |   60   42   53   38    9   64   20  124   21   83   39   94    7    8    3   15 
#  2 |   15   11   68    3    2   29   73   45   44   16   60   87   16   81    2    2 
#  3 |   89   15   24   13   22   19   17   19    2    4    2   43   70   33   42   32 
#  4 |    0   34    3   74   51   32   88   44   89   43   13    6   53  124   93  127 
#  5 |   74    8   13   42   73   30   22    8   47   33   85   18    9   64   59   23
#  6 |   29   59   92  131   20   11   67   55   54   68   12   21   84  123  156  244
#  7 |   86   14   37   26   47   30   22   16   19   25   33   50   89   78  101   29 
#  8 |   71    9   40   99   52    7   65   35   54   46   26   71   48   91   42  122
#  9 |   44   36   95    6   25   12   20   36   19    3    5   42   43   46   13   93
#  A |   59   31   10   83   68    7  109   11   82   38   78    3   32  105   84  174
#  B |   15   11    6   51   56    9    1   25   54   28   20   27   12   45   50   24
#  C |   26   72   11   26    5   12   30   58   25    3   21   38   21   36   25   21
#  D |  100   76  103   16   29    2   26   32   67    9   37    6   75   12   15    9
#  E |   55   45   18   25   36   33   27   47    2   76   16   13   84   77   14    4
#  F |    2   30    9   16   25   10    8   62   33  103   85   70   21    4   25    7
# maxkey_bin = ( 0110 , 1111 )
# maxkey_hex = (    6 ,    F )