#Parameters of S box
S_Box = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]

#Parameters of P box
P_Box = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]

def gen_K_list(K):
    """
    Param K: 32-bit secret key
    Return: [k1, k2, k3, k4, k5], five 16-bit subkeys
    """
    Ks = []
    for i in range(5, 0, -1): # 5 4 3 2 1
        ki = K % (2 ** 16)
        Ks.insert(0, ki)
        K = K >> 4
    return Ks

def pi_s(s_box, ur):
    """
    Substitution operation
    Param: Input Bit String, 16 Bits
    Return: Output Bit String, 16 Bits
    """
    vr = 0
    for i in range(4):
        uri = ur % (2 ** 4)
        vri = s_box[uri]
        vr = vr + (vri << (4 * i))
        ur = ur >> 4
    return vr

def pi_p(p_box, vr):
    """
    Permutation operation
    Param vr: input bit string, 16 bits
    Return: Output Bit String, 16 Bits
    """
    wr = 0
    for i in range(15, -1, -1):
        vri = vr % 2
        vr = vr >> 1
        wr = wr + (vri << (16 - p_box[i]))
    return wr

def do_SPN(x, s_box, p_box, Ks):
    """
    Param x: 16 bit input
    Param s_box: S box parameter
    Param p_box: P-box parameter
    Param Ks: [k1, k2, k3, k4, k5], five 16-bit subkeys
    Return: 16 bit output
    """
    WR = x
    for r in range(3):
        Ur = WR ^ Ks [r] #XOR operation
        VR = pi_s (s_box, Ur) # packet substitution
        WR = pi_p (p_box, VR)  #single bit permutation

    ur = WR ^ Ks[3]
    vr = pi_s(s_box, ur)
    y = vr ^ Ks[4]
    return y

def encrypt(K, x):
    """
    Encryption of 16-bit plaintext x based on secret key K
    Param K:32-bit secret key
    Param x: 16 bits plaintext
    Return: 16 bits ciphertext
    """
    Ks = gen_K_list(K)
    return do_SPN(x, S_Box, P_Box, Ks)

if __name__ == '__main__':
    x = 0b0010011010110111
    K = 0b00111010100101001101011000111111
    print ('initial plaintext:', format (x,'016b'))
    print ('encrypted ciphertext:', format (encrypt (K, x),'016b'))


# Output
# initial plaintext: 0010011010110111
# encrypted ciphertext: 1011110011010110
