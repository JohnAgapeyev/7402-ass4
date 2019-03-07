#!/bin/python3

import sys

#ensure data is the correct length
def pkcs7_pad(x):
    padding = 16 - ((len(x) % 16 != 0) * (len(x) % 16))
    return x + bytes([padding]) * padding

#remove and check the padding
def pkcs7_strip(x):
    for i in range(x[-1]):
        if x[-(i + 1)] != x[-1]:
            raise ValueError('Input is not padded or padding is corrupt')
    return x[:-x[-1]]

#This is completely arbitrary, and bad
#dont use this f
def f(i, k, x):
    for elem in x:
        elem *= i
        elem <<= k
    return x

def round(i, k, L, R):
    return R, [a ^ b for (a,b) in zip(L, f(i, k, R))]

def process_block(B, rounds, subkeys):
    #Split the block
    L, R = B[:8], B[8:]
    for j in rounds:
        L, R = round(j, subkeys[j], L, R)
    return R + L

# Args are [mode] [input filename] [output filename]
# mode is 'e' for encrypt, else decrypt
if __name__ == '__main__':
    if len(sys.argv[1:]) != 3:
        print("usage: ./feistel.py {e, d} /path/to/input /path/to/output")
        sys.exit(1)

    round_count = 6

    #Master secret key
    K = 7

    #Subkey generation, not really lol
    k = [K] * round_count

    if sys.argv[1] == 'e':
        P = pkcs7_pad(bytearray(open(sys.argv[2], 'rb').read()))
        #i is block num
        for i in range(len(P) // 16):
            start_block = i * 16
            end_block = start_block + 16
            #Grab the block
            B = P[start_block : end_block]
            B = process_block(B, range(round_count), k)
            #Write the block back
            P[start_block : end_block] = B
        with open(sys.argv[3], 'wb') as out:
            out.write(P)
    elif sys.argv[1] == 'd':
        P = bytearray(open(sys.argv[2], 'rb').read())
        if len(P) % 16 != 0:
            raise ValueError('Ciphertext is not a valid length, it must be corrupted')
        #i is block num
        for i in range(len(P) // 16):
            start_block = i * 16
            end_block = start_block + 16
            #Grab the block
            B = P[start_block : end_block]
            B = process_block(B, reversed(range(round_count)), k)
            #Write the block back
            P[start_block : end_block] = B
        P = pkcs7_strip(P)
        with open(sys.argv[3], 'wb') as out:
            out.write(P)
    else:
        print("unknown directive {}".format(sys.argv[1]))
