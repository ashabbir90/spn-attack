from typing import BinaryIO
#import numpy as np

# Ausgabefunktionen
def print_bin(num):
    print(format(num, '#06b')[2:])

def print_hex(num):
    print(hex(num)[2:])

def print_bin_array(bin_array):
    print('[', end = '')
    for i in range(0,len(bin_array)):
        print(format(bin_array[i], '#06b')[2:], end = '')
        if i < len(bin_array) - 1:
            print(', ', end = '')
    print(']')

def print_hex_array(bin_array):
    print('[   ', end = '')
    for i in range(0,len(bin_array)):
        print(hex(bin_array[i])[2:], end = '')
        if i < len(bin_array) - 1:
            print(',    ', end = '')
    print(']')

# Example 4.1 (S. 85 ff.)
l = 4
m = 4
N = 4

# S-Box
S_Box = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
def pi_s(s_box, ur):
    """
    Packet substitution operation

    """
    vr = 0
    for i in range(4):
        uri = ur % (2 ** 4)
        vri = s_box[uri]
        vr = vr + (vri << (4 * i))
        ur = ur >> 4
    return vr

# Permutation
def pi_p(input):
    p = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16]
    return p[input-1]

# Schlüssel K
K = int('00111010100101001101011000111111', 2)

K1 = int(format(K, '#34b')[2:2+16],2)
K2 = int(format(K, '#34b')[6:6+16],2)
K3 = int(format(K, '#34b')[10:10+16],2)
K4 = int(format(K, '#34b')[14:14+16],2)
K5 = int(format(K, '#34b')[18:18+16],2)

print_bin_array([K1,K2,K3,K4,K5])

x = int('0010011010110111', 2)
