import numpy as np
import Basic_Spn as spn
import Console_Outputs as cout
import Linear_Attack as la
import random
import time

def delta(x_prime, l=4):
    return [[i,i ^ x_prime] for i in range(2 ** l)]

def N_D(x_prime, y_prime, sbox=spn.S_Box):
    delta_x_prime = delta(x_prime)
    count = 0 # number of pairs where pi_s(x) xor pi_s(x_star) == y_prime
    for dxp in delta_x_prime:
        if sbox[dxp[0]] ^ sbox[dxp[1]] == y_prime:
            count += 1
    return count

def difference_distribution_table():
    Count = np.zeros((16,16))
    for a_prime in range(16):
        for b_prime in range(16):
            Count[a_prime][b_prime] = N_D(a_prime, b_prime)
    return Count

def R_p(a_prime, b_prime, m=4, sbox=spn.S_Box):
    return N_D(a_prime, b_prime, sbox) / (2 ** m)


def differential_attack(T_set, pi_s_inv):
    T = len(T_set)
    Count = np.zeros((16,16))

    right_pairs_count = 0
    for (x,y,x_star,y_star) in T_set:
        if  ( int(format(y, '016b')[0:4],2)  == int(format(y_star, '016b')[0:4],2)
            & int(format(y, '016b')[8:12],2) == int(format(y_star, '016b')[8:12],2)):
            right_pairs_count += 1
            for L1 in range(16):
                for L2 in range(16):
                    v4 =             L1 ^ int(format(y, '016b')[4:8],  2) # v4_<2>
                    v4 = (v4 << 8) + L2 ^ int(format(y, '016b')[12:16],2) # v4_<4>
                    
                    u4 =             pi_s_inv(spn.S_Box,int(format(v4,'016b')[4:8],  2),4,1) # u4_<2>
                    u4 = (u4 << 8) + pi_s_inv(spn.S_Box,int(format(v4,'016b')[12:16],2),4,1) # u4_<4>

                    v4_star =                  L1 ^ int(format(y_star, '016b')[4:8],  2) # v4_star_<2>
                    v4_star = (v4_star << 8) + L2 ^ int(format(y_star, '016b')[12:16],2) # v4_star_<4>
                    
                    u4_star =                  pi_s_inv(spn.S_Box,int(format(v4_star,'016b')[4:8],  2),4,1) # u4_star_<2>
                    u4_star = (u4_star << 8) + pi_s_inv(spn.S_Box,int(format(v4_star,'016b')[12:16],2),4,1) # u4_star_<4>
                    
                    u4_prime = int(format(u4,'016b')[4:8],  2) ^ int(format(u4_star,'016b')[4:8],  2) # u4_strich_<2>
                    u4_prime = (u4_prime << 8) + ( int(format(u4,'016b')[12:16],  2) 
                                                 ^ int(format(u4_star,'016b')[12:16],  2)
                                                 ) # u4_strich_<4>

                    if  ( int(format(u4_prime, '016b')[4:8],2)   == 0b_0110 
                        & int(format(u4_prime, '016b')[12:16],2) == 0b_0110):
                        Count[L1][L2] += 1
    
    MAX = -1
    maxkey = (0,0)
    for L1 in range(16):
        for L2 in range(16):
            if Count[L1][L2] > MAX:
                MAX = Count[L1][L2]
                maxkey = (L1,L2)

    return Count, maxkey, right_pairs_count

if __name__ == '__main__':
    cout.print_s_box(spn.S_Box)
    
    K = 0b_0011_1010_1001_0100_1101_0110_0011_1111
    print('\nKey =', cout.bin_str(K,4,8))

    cout.print_R_p(0b_1011,0b_0010)
    cout.print_R_p(0b_0100,0b_0110)
    cout.print_R_p(0b_0010,0b_0101)
    cout.print_R_p(0b_0010,0b_0101)

    cout.print_difference_distribution_table(difference_distribution_table())

    x_prime = 0b_0000_1011_0000_0000
    T_set = [(x, spn.encrypt(K, x), (x ^ x_prime) % (2 ** 16), spn.encrypt(K, (x ^ x_prime) % (2 ** 16))) for x in random.sample(range(0, 2**16), 20_000)]

    tmp_T_set = T_set[0:4000]
    print('\n=== Starting differential_attack', '==========================')
    start_time = time.time()
    count_table, maxkey, right_pairs_count = differential_attack(tmp_T_set,la.pi_s_inv)
    print('T =', len(tmp_T_set))
    print('right pairs found:',right_pairs_count)
    print('pairs filtered out:',len(tmp_T_set) - right_pairs_count)
    cout.print_count_table(count_table, maxkey)
    print('Original key blocks: '
        , format(K,'032b')[20:24]
        , format(K,'032b')[28:32])
    exec_time = time.time() - start_time
    print('Execution time:', f'{exec_time:.2f}', 'seconds')
    print('--- End ----------------------------------------\n')

# Output

# S-Box:
# input  =  0 2 9 4 D 7 C 3 1 6 B 5 F A E 8
# output =  E 4 D 1 2 F B 8 3 A 6 C 5 9 0 7

# Key = 0011 1010 1001 0100 1101 0110 0011 1111

# Difference distribution table:
#    |                        b'
#  a'|  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
# ----------------------------------------------------
#  0 | 16  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
#  1 |  0  0  0  2  0  0  0  2  0  2  4  0  4  2  0  0 
#  2 |  0  0  0  2  0  6  2  2  0  2  0  0  0  0  2  0
#  3 |  0  0  2  0  2  0  0  0  0  4  2  0  2  0  0  4
#  4 |  0  0  0  2  0  0  6  0  0  2  0  4  2  0  0  0
#  5 |  0  4  0  0  0  2  2  0  0  0  4  0  2  0  0  2
#  6 |  0  0  0  4  0  4  0  0  0  0  0  0  2  2  2  2
#  7 |  0  0  2  2  2  0  2  0  0  2  2  0  0  0  0  4
#  8 |  0  0  0  0  0  0  2  2  0  0  0  4  0  4  2  2
#  9 |  0  2  0  0  2  0  0  4  2  0  2  2  2  0  0  0
#  A |  0  2  2  0  0  0  0  0  6  0  0  2  0  0  4  0
#  B |  0  0  8  0  0  2  0  2  0  0  0  0  0  2  0  2
#  C |  0  2  0  0  2  2  2  0  0  0  0  2  0  6  0  0
#  D |  0  4  0  0  0  0  0  4  2  0  2  0  2  0  2  0
#  E |  0  0  2  4  2  0  0  0  6  0  0  0  0  0  2  0
#  F |  0  2  0  0  6  0  0  0  0  4  0  2  0  0  2  0

# === Starting differential_attack ==========================
# right pairs found: 35

# Count table:
#    |    0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
# ------------------------------------------------------------------------------------
#  0 |    0    0    0    0    0    2    1    0    2    1    1    1    1    1    1    1
#  1 |    2    1    1    0    1    0    1    0    0    1    0    1    1    0    1    2
#  2 |    0    0    0    0    0    1    0    0    1    0    0    0    0    0    0    0
#  3 |    3    2    1    1    2    1    2    0    1    3    1    1    2    1    1    4
#  4 |    2    1    1    0    1    0    1    0    0    1    0    1    1    0    1    2 
#  5 |    0    0    0    0    0    1    0    0    1    0    0    0    0    0    0    0
#  6 |    4    1    2    1    1    2    2    1    3    3    3    3    3    3    3    5 
#  7 |    0    0    1    0    1    1    1    0    1    1    0    1    0    1    0    0
#  8 |    2    0    1    2    0    0    0    0    2    1    2    1    2    3    2    2
#  9 |    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0 
#  A |    1    0    1    1    0    1    1    0    1    1    1    1    2    2    2    1
#  B |    1    0    2    0    1    1    1    1    0    1    0    1    0    1    0    0
#  C |    0    0    0    0    0    1    1    0    1    1    1    1    1    1    1    1
#  D |    1    0    1    1    0    0    0    0    0    0    0    0    1    1    1    0
#  E |    0    0    0    0    1    1    1    0    0    0    0    0    1    1    0    1
#  F |    2    1    1    2    0    0    0    0    1    2    1    0    1    1    1    1
# maxkey:
# hex    6    F
# bin 0110 1111
# Original key blocks:  0110 1111
# T = 4000
# Execution time: 0.30 seconds
# --- End ----------------------------------------