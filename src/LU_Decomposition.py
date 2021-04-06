from math import log10
from threading import Thread
from random import randint
from time import time
from pprint import pprint


def threadCompare(A, B, i, j, maxi):
    if maxi[0] < A[i][j]: maxi[0] = A[i][j]
    if maxi[0] < B[i][j]: maxi[0] = B[i][j]


def threadOne_New(A, C, i, j, P):
    C[i] = C[i] * 10 ** (P) + A[i][j]


def threadTwo_New(B, D, i, j, P, N):
    D[j] = D[j] * 10 ** (P) + B[N - 1 - i][j]


def threadThree_New(E, C, D, i, j, P, N):
    E[i][j] = int(C[i] * D[j] / (10 ** (P * (N - 1)))) % (10 ** P)


def new_matrix_multiply(A, B):
    N = len(A)
    maxi = [0]
    threadSeries = [[Thread(target=threadCompare, args=(A, B, i, j, maxi,)) for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N): threadSeries[i][j].start()
    for i in range(N):
        for j in range(N): threadSeries[i][j].join()
    M = int(log10(maxi[0])) + 1
    P = int(log10((10 ** (2 * M) - 1) * N)) + 1
    C, D, E = [0 for i in range(N)], [0 for i in range(N)], [[0 for i in range(N)] for j in range(N)]
    threadSeriesOne = [[Thread(target=threadOne_New, args=(A, C, i, j, P,)) for j in range(N)] for i in range(N)]
    threadSeriesTwo = [[Thread(target=threadTwo_New, args=(B, D, i, j, P, N,)) for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N): threadSeriesOne[i][j].start()
    for i in range(N):
        for j in range(N): threadSeriesOne[i][j].join()
    for i in range(N):
        for j in range(N): threadSeriesTwo[i][j].start()
    for i in range(N):
        for j in range(N): threadSeriesTwo[i][j].join()
    threadSeriesThree = [[Thread(target=threadThree_New, args=(E, C, D, i, j, P, N,)) for j in range(N)] for i in
                         range(N)]
    for i in range(N):
        for j in range(N): threadSeriesThree[i][j].start()
    for i in range(N):
        for j in range(N): threadSeriesThree[i][j].join()
    return E


for size in range(1, 21):
    A = [[randint(1, 15) for j in range(size)] for i in range(size)]
    B = [[randint(1, 15) for j in range(size)] for i in range(size)]
    start = time()
    new_matrix_multiply(A, B)
    end = time()
    print('Size', size, 'Expected time consumed', int((end - start) * 10 ** 6 / size / size), ' microseconds')
