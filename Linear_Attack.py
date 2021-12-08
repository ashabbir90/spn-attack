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