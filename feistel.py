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
        elem *= i
        elem <<= k
    return x

P = bytearray('abcdefghijklmno', 'utf8')

P = pkcs7_pad(P)

print(P)

K = 7

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
        if j < 7:
            #Swap the two halfs
            L = R
            R = X
    #Write the ciphertext block back
    P[i * 16 : i * 16 + 16] = L + R

print(P)
