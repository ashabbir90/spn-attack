import Basic_Spn as spn
import Console_Outputs as cout
import random
import time

def pi_s_inv(s_box, input, l=4, m=4):
    """
    Applies inverted S-Box to input
    Param s_box: S-Box parameter
    Param input: Input bit string, l*m bits
    Param l: Bit length per block
    Param m: Block count
    Return: Output bit string, l*m bits
    """
    output = 0
    for i in range(m):
        input_i = input % (2 ** l)
        output_i = s_box.index(input_i)
        output = output + (output_i << (l * i))
        input = input >> l
    return output

def linear_approximation(s_box, l=4):
    Approx = [0] * 16
    for i in range(16):
        Approx[i] = [0] * 16
    # N_L(a,b)
    for a in range(16):
        for b in range(16):
            for x in range(len(s_box)):
                y = s_box[x]
                result = 0
                for i in range(l):
                    result = ( result
                        ^ ((a >> i) % 2 * (x >> i) % 2) 
                        ^ ((b >> i) % 2 * (y >> i) % 2)
                        )
                if result == 0:
                    Approx[a][b] += 1
    # e(a,b)
    for a in range(16):
        for b in range(16):
            Approx[a][b] = (Approx[a][b] - 8)/16    
    return Approx

def linear_attack_1(T_set, pi_s_inv):
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
                v4 =             L1 ^ int(format(y, '016b')[4:8],  2) # v4_<2>
                v4 = (v4 << 8) + L2 ^ int(format(y, '016b')[12:16],2) # v4_<4>
                u4 =             pi_s_inv(spn.S_Box,int(format(v4,'016b')[4:8],  2),4,1) # u4_<2>
                u4 = (u4 << 8) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[12:16],2),4,1) # u4_<4>
                z = ( int(format(x, '016b')[5  - 1],2) # x_5
                    ^ int(format(x, '016b')[7  - 1],2) # x_7
                    ^ int(format(x, '016b')[8  - 1],2) # x_8
                    ^ int(format(u4,'016b')[6  - 1],2) # u4_6
                    ^ int(format(u4,'016b')[8  - 1],2) # u4_8
                    ^ int(format(u4,'016b')[14 - 1],2) # u4_14
                    ^ int(format(u4,'016b')[16 - 1],2) # u4_16
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
    return Count, maxkey

def linear_attack_2(T_set, pi_s_inv):
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
                z = ( int(format(x,'016b')[12-1],2)
                    ^ int(format(u4,'016b')[5-1],2)
                    ^ int(format(u4,'016b')[6-1],2)
                    ^ int(format(u4,'016b')[7-1],2)
                    ^ int(format(u4,'016b')[13-1],2)
                    ^ int(format(u4,'016b')[14-1],2)
                    ^ int(format(u4,'016b')[15-1],2)
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
    
    return Count, maxkey

def linear_attack_3(T_set, pi_s_inv):
    T = len(T_set)
    Count = [0] * 16
    
    for i in range(16):
        Count[i] = [0] * 16
    
    for i in range(16):
        for j in range(16):
            Count[i][j] = [0] * 16
    
    v4 = 0
    u4 = 0
    z = 0

    for (x,y) in T_set:
        for L1 in range(16):
            for L2 in range(16):
                for L3 in range(16):
                    v4 = (L1 ^ int(format(y,'016b')[4:8],2))
                    v4 = (v4 << 4) + L2 ^ int(format(y,'016b')[8:12],2)
                    v4 = (v4 << 4) + L3 ^ int(format(y,'016b')[12:16],2)
                    u4 = (pi_s_inv(spn.S_Box,int(format(v4,'016b')[4:8],2),4,1))
                    u4 = (u4 << 4) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[8:12],2),4,1)
                    u4 = (u4 << 4) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[12:16],2),4,1)
                    z = ( int(format(x,'016b')[1-1],2)
                        ^ int(format(x,'016b')[3-1],2)
                        ^ int(format(x,'016b')[9-1],2)
                        ^ int(format(x,'016b')[11-1],2)
                        ^ int(format(u4,'016b')[6-1],2)
                        ^ int(format(u4,'016b')[10-1],2)
                        ^ int(format(u4,'016b')[14-1],2)
                        )
                    if z == 0:
                        Count[L1][L2][L3] += 1

    MAX = -1
    maxkey = (0,0)
    for L1 in range(16):
        for L2 in range(16):
            for L3 in range(16):
                Count[L1][L2][L3] = abs(Count[L1][L2][L3] - T/2)
                if Count[L1][L2][L3] > MAX:
                    MAX = Count[L1][L2][L3]
                    maxkey = (L1,L2,L3)
    
    return Count, maxkey

def linear_attack_4(T_set, pi_s_inv):
    T = len(T_set)
    Count = [0] * 16
    
    for i in range(16):
        Count[i] = [0] * 16
    
    for i in range(16):
        for j in range(16):
            Count[i][j] = [0] * 16
    
    v4 = 0
    u4 = 0
    z = 0

    for (x,y) in T_set:
        for L1 in range(16):
            for L2 in range(16):
                for L3 in range(16):
                    v4 = (L1 ^ int(format(y,'016b')[0:4],2))
                    v4 = (v4 << 4) + L2 ^ int(format(y,'016b')[4:8],2)
                    v4 = (v4 << 4) + L3 ^ int(format(y,'016b')[8:12],2)
                    v4 = v4 << 4
                    u4 = (pi_s_inv(spn.S_Box,int(format(v4,'016b')[0:4],2),4,1))
                    u4 = (u4 << 4) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[4:8],2),4,1)
                    u4 = (u4 << 4) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[8:12],2),4,1)
                    u4 = u4 << 4
                    z = ( int(format(x,'016b')[1-1],2)
                        ^ int(format(x,'016b')[2-1],2)
                        ^ int(format(x,'016b')[9-1],2)
                        ^ int(format(x,'016b')[10-1],2)
                        ^ int(format(u4,'016b')[2-1],2)
                        ^ int(format(u4,'016b')[6-1],2)
                        ^ int(format(u4,'016b')[10-1],2)
                        )
                    if z == 0:
                        Count[L1][L2][L3] += 1

    MAX = -1
    maxkey = (0,0)
    for L1 in range(16):
        for L2 in range(16):
            for L3 in range(16):
                Count[L1][L2][L3] = abs(Count[L1][L2][L3] - T/2)
                if Count[L1][L2][L3] > MAX:
                    MAX = Count[L1][L2][L3]
                    maxkey = (L1,L2,L3)
    
    return Count, maxkey

def linear_attack_5(T_set, pi_s_inv, xs, ):
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
                v4 = y ^ 0b_1101_0110_0011_1111
                u4 = pi_s_inv(spn.S_Box,v4)
                v3 = spn.pi_p(spn.P_Box, u4)
                v4 =             L1 ^ int(format(y, '016b')[4:8],  2) # v4_<2>
                v4 = (v4 << 8) + L2 ^ int(format(y, '016b')[12:16],2) # v4_<4>
                u4 =             pi_s_inv(spn.S_Box,int(format(v4,'016b')[4:8],  2),4,1) # u4_<2>
                u4 = (u4 << 8) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[12:16],2),4,1) # u4_<4>
                z = ( int(format(x, '016b')[5  - 1],2) # x_5
                    ^ int(format(x, '016b')[7  - 1],2) # x_7
                    ^ int(format(x, '016b')[8  - 1],2) # x_8
                    ^ int(format(u4,'016b')[6  - 1],2) # u4_6
                    ^ int(format(u4,'016b')[8  - 1],2) # u4_8
                    ^ int(format(u4,'016b')[14 - 1],2) # u4_14
                    ^ int(format(u4,'016b')[16 - 1],2) # u4_16
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
    return Count, maxkey

if __name__ == '__main__':
    cout.print_s_box(spn.S_Box)

    approx_table = linear_approximation(spn.S_Box)
    cout.print_linear_approximation_table(approx_table)
    
    K = 0b_0011_1010_1001_0100_1101_0110_0011_1111
    print('\nKey =', cout.bin_str(K,4,8))

    T_set = [(x, spn.encrypt(K, x)) for x in random.sample(range(0, 2**16-1), 20_000)]

    for i in [1]:
        print('=== Starting linear_attack_' + str(i), '==========================')
        start_time = time.time()
        if i == 1:
            tmp_T_set = T_set[0:8000]
            count_table, maxkey = linear_attack_1(tmp_T_set,pi_s_inv)
            cout.print_count_table(count_table, maxkey)
            print('Original key blocks: '
                , format(K,'032b')[20:24]
                , format(K,'032b')[28:32])
        elif i == 2:
            tmp_T_set = T_set[0:16_000]
            count_table, maxkey = linear_attack_2(tmp_T_set,pi_s_inv)
            cout.print_count_table(count_table, maxkey)
            print('Original key blocks: '
                , format(K,'032b')[20:24]
                , format(K,'032b')[28:32])
        elif i == 3:
            tmp_T_set = T_set[0:3000]
            count_table, maxkey = linear_attack_3(tmp_T_set,pi_s_inv)
            print('maxkey =', maxkey)
            print('Original key blocks: '
                , format(K,'032b')[20:24]
                , format(K,'032b')[24:28]
                , format(K,'032b')[28:32])
        elif i == 4:
            tmp_T_set = T_set[0:3000]
            count_table, maxkey = linear_attack_4(tmp_T_set,pi_s_inv)
            print('maxkey =', maxkey)
            print('Original key blocks: '
                , format(K,'032b')[16:20]
                , format(K,'032b')[20:24]
                , format(K,'032b')[24:28])
        print('Estimated key blocks:', end=' ')
        [print(format(x,'04b'),end=' ') for x in maxkey]
        print()
        print('T =', len(tmp_T_set))
        exec_time = time.time() - start_time
        print('Execution time:', f'{exec_time:.2f}', 'seconds')
        print('--- End ----------------------------------------')

# Output - Linear_Attack.py
#
# S-Box:
# input  =  0 2 9 4 D 7 C 3 1 6 B 5 F A E 8
# output =  E 4 D 1 2 F B 8 3 A 6 C 5 9 0 7

# Linear approximation table:
#    |      0      1      2      3      4      5      6      7      8      9      A      B      C      D      E      F
# --------------------------------------------------------------------------------------------------------------------
#  0 |  0.500  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000
#  1 |  0.000  0.000 -0.125 -0.125  0.000  0.000 -0.125  0.375  0.125  0.125  0.000  0.000  0.125  0.125  0.000  0.000
#  2 |  0.000  0.000 -0.125 -0.125  0.000  0.000 -0.125 -0.125  0.000  0.000  0.125  0.125  0.000  0.000 -0.375  0.125
#  3 |  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.125 -0.375 -0.125 -0.125  0.125  0.125 -0.125 -0.125
#  4 |  0.000  0.125  0.000 -0.125 -0.125 -0.250 -0.125  0.000  0.000 -0.125  0.000  0.125  0.125 -0.250  0.125  0.000 
#  5 |  0.000 -0.125 -0.125  0.000 -0.125  0.000  0.250  0.125 -0.125  0.000 -0.250  0.125  0.000 -0.125 -0.125  0.000
#  6 |  0.000  0.125 -0.125  0.250  0.125  0.000  0.000  0.125  0.000 -0.125  0.125  0.250 -0.125  0.000  0.000 -0.125
#  7 |  0.000 -0.125  0.000  0.125  0.125 -0.250  0.125  0.000 -0.125  0.000  0.125  0.000  0.250  0.125  0.000  0.125
#  8 |  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000 -0.125  0.125  0.125 -0.125  0.125 -0.125 -0.125 -0.375 
#  9 |  0.000  0.000 -0.125 -0.125  0.000  0.000 -0.125 -0.125 -0.250  0.000 -0.125  0.125  0.000  0.250  0.125 -0.125
#  A |  0.000  0.250 -0.125  0.125 -0.250  0.000  0.125 -0.125  0.125  0.125  0.000  0.000  0.125  0.125  0.000  0.000
#  B |  0.000  0.250  0.000 -0.250  0.250  0.000  0.250  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000
#  C |  0.000 -0.125  0.250 -0.125 -0.125  0.000  0.125  0.000  0.125  0.000  0.125  0.250  0.000  0.125  0.000 -0.125
#  D |  0.000  0.125  0.125  0.000 -0.125  0.250  0.000  0.125 -0.250 -0.125  0.125  0.000  0.125  0.000  0.000  0.125
#  E |  0.000  0.125  0.125  0.000 -0.125 -0.250  0.000  0.125 -0.125  0.000  0.000 -0.125 -0.250  0.125 -0.125  0.000
#  F |  0.000 -0.125 -0.250 -0.125 -0.125  0.000  0.125  0.000  0.000 -0.125  0.250 -0.125 -0.125  0.000  0.125  0.000
#
# Key = 0011 1010 1001 0100 1101 0110 0011 1111
#
# === Starting attack 1 ==========================
# Count table:
#    |    0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
# ------------------------------------------------------------------------------------
#  0 |   71   51    3   16   13   32   20   44   31    7   19   26   31   18   36   86
#  1 |    1  105   15   44    9   58   48   74    1  121   15   82   51  110   10   96
#  2 |   18   48   34   53   74   83   55  107   84  136  108  117   48   39   53   13
#  3 |   35  103    5   14    5   68   48  114    7   59   39  112   35   44   54   84
#  4 |   13   45    1   80   91   68   88   44   41    3   17    6   13   92   48   80
#  5 |   22   22    6   21   14   99    7   77   38   46   60   53   38   23   39    5
#  6 |   31  147  109  172   39   16   56   32   13   11   29    6  101  164  126  242 
#  7 |    5   17    5   58    9   48   44   44   39   39   43   14   15   78   90   78
#  8 |   46  114   24  101   12    9    7    7   24   24   22   43   12   89    1   67
#  9 |   10   50   90   13   60   41    5   19   28    4   50   51   74    3   37   97
#  A |   19  119   25  180    7   42   58   26   23   61   39    4   11  144   50  150 
#  B |   28   52   18   79  112   11   37    7   56   12   38   63   14   75   41   65
#  C |    6   24    4   23    8    7   15   29   64   50   28   27   30    3   17   13
#  D |   23   79   25   44   71    8   22   22   27   27   41   22   17   86   18   84
#  E |   40   22   24   53   12   17   81   11   58   12   52   57   14   63   61    1
#  F |   30   76   12    7   16   43   13   41   88  116   86  113   34   29   35   11
# maxkey:
# hex    6    F
# bin 0110 1111
# Original key blocks:  0110 1111
# Estimated key blocks: 0110 1111
# T = 8000
# Execution time: 21.46 seconds
# --- End ----------------------------------------
# 
# === Starting attack 2 ==========================
# Count table:
#    |    0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
# ------------------------------------------------------------------------------------
#  0 |   68   31  215   79   89  146  111   23   26  232  143  254   76  128   34  275
#  1 |   25   60   32   70   14  147   22   78   59   45   10    9   67   55   77    2
#  2 |   11   62  180   62   36    1   64  102   47  243   56  271    7  127    7  318 
#  3 |   77  158  122   30   72   79  110  106    3   77   24  115  133   65   55  110
#  4 |    8   87   13   55   49   70   61  101   28   72    3   60   18    2   14    3
#  5 |   25   82   58    2   44   47   92   50   49    1   52   47   97   33   17  116
#  6 |   29   50  250   20  128  119   18   96   63  315  152  205   53   83   17  362 
#  C |   63   14   62   34   42  103   88   26  101   21   24   25   93    5  113  130
#  D |    5   10   20   50   50   83  126   50   57   99   76   23   43   47   17   22
#  E |   39  112  152   66  128   35  176   54   39  101   58  149  159  125   19  238
#  F |   84   41   15   91  103   62  173  129   78  110   11   40   40   48   10   21
# maxkey:
# hex    6    F
# bin 0110 1111
# Original key blocks:  0110 1111
# Estimated key blocks: 0110 1111
# T = 16000
# Execution time: 44.76 seconds
# --- End ----------------------------------------
#
# === Starting attack 3 ==========================
# maxkey = (6, 3, 15)
# Original key blocks:  0110 0011 1111
# Estimated key blocks: 0110 0011 1111 
# T = 3000
# Execution time: 152.40 seconds
# --- End ----------------------------------------
#
# === Starting attack 4 ==========================
# maxkey = (13, 6, 3)
# Original key blocks:  1101 0110 0011 
# Estimated key blocks: 1101 0110 0011 
# T = 3000
# Execution time: 176.82 seconds       
# --- End ----------------------------------------

# K = 0b0011_1010_1001_0100_1101_0110_0011_1111

# K5 = int(format(K,'032b')[16:32])