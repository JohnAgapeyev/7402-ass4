#!/bin/python3

import os
import sys

def f(i, k, x):
    return bytes(((2 * i * k)**int.from_bytes(x, byteorder='big')) % 15)

P = bytearray('Foobar', 'utf8')
K = 7

#i is block num, j is round number
for i in range(len(P) // 16 + 1):
    #Grab the block
    B = P[i * 16 : i * 16 + 16]
    print(B)
    print(i)
    for j in range(8):
        print(j)
        #Split the block
        L, R = B[:8], B[8:]
        # Call f() with round num, key, and input
        X = f(j, K, R)
        #Xor Left half with f() result
        #X = L ^ X
        X = [a ^ b for (a,b) in zip(L, X)]
        if j < 7:
            #Swap the two halfs
            L = R
            R = X
    #Write the ciphertext block back
    P[i * 16 : i * 16 + 16] = B
    print(B)

print(P)
