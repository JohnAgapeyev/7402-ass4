#!/bin/python3

import os
import sys

def pkcs7_pad(x):
    if len(x) % 16 == 0:
        padding = 16
    else:
        padding = 16 - (len(x) % 16)
    return x + bytes([padding]) * padding

def f(i, k, x):
    for elem in x:
        elem *= 3
        elem <<= 1
    return x

if __name__ == '__main__':
    if len(sys.argv[1:]) < 2:
        print("give me mode!")
        sys.exit(1)

    K = 7

    if sys.argv[1] == 'e':
        P = pkcs7_pad(bytearray(open(sys.argv[2], 'rb').read()))
        #i is block num, j is round number
        for i in range(len(P) // 16):
            #Grab the block
            B = P[i * 16 : i * 16 + 16]
            #Split the block
            L, R = B[:8], B[8:]
            for j in range(8):
                # Call f() with round num, key, and input
                X = f(j, K, R)
                #Xor Left half with f() result
                X = [a ^ b for (a,b) in zip(L, X)]
                #Swap the two halfs
                L = R
                R = X
            #Write the ciphertext block back
            P[i * 16 : i * 16 + 16] = R + L
        with open(sys.argv[3], 'wb') as out:
            out.write(P)
    else:
        P = bytearray(open(sys.argv[2], 'rb').read())
        #i is block num, j is round number
        for i in range(len(P) // 16):
            #Grab the block
            B = P[i * 16 : i * 16 + 16]
            #Split the block
            L, R = B[:8], B[8:]
            for j in reversed(range(8)):
                # Call f() with round num, key, and input
                X = f(j, K, R)
                #Xor Left half with f() result
                X = [a ^ b for (a,b) in zip(L, X)]
                #Swap the two halfs
                L = R
                R = X
            #Write the ciphertext block back
            P[i * 16 : i * 16 + 16] = R + L
        print(P)
