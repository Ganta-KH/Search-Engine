import cv2
import numpy as np
from math import sqrt, pi

n = 8

Q = np.array([
    [16, 11, 10, 16,  24,  40,  51,  61],
    [12, 12, 14, 19,  26,  58,  60,  55],
    [14, 13, 16, 24,  40,  57,  69,  56],
    [14, 17, 22, 29,  51,  87,  80,  62],
    [18, 22, 37, 56,  68, 109, 103,  77],
    [24, 35, 55, 64,  81, 104, 113,  92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103,  99]
], dtype=np.float16)

def alpha(q, M): 
    return 1 / sqrt(M) if q == 0 else sqrt(2 / M)


def zigzag_scan(block, n):
    return np.concatenate([np.diagonal(block[::-1, :], i)[::(2 * (i % 2) - 1)] for i in range(1 - n, n)])


def DCT(image):
    global Q
    global n

    W, H = image.shape[:2]
    # DCT-I
    dW, dH = W // n, H // n
    M, N = dW * n, dH * n
    nbrPixel = dW * dH

    # DCT_II
    DCT_I = np.zeros((M, N, 3))

    for i in range(n):
        pos_i_1, pos_i_2 = i * dW, (i+1) * dW
        for j in range(n):
            pos_j_1, pos_j_2 = j * dH, (j+1) * dH
            DCT_I[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2, 0] = image[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2, 0].sum() / nbrPixel
            DCT_I[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2, 1] = image[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2, 1].sum() / nbrPixel
            DCT_I[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2, 2] = image[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2, 2].sum() / nbrPixel

    # DCT_III

    YCbCr = cv2.cvtColor(DCT_I.astype('uint8'), cv2.COLOR_RGB2YCrCb)

    # DCT_IV

    Y = YCbCr[..., 0]
    Cb = YCbCr[..., 1]
    Cr = YCbCr[..., 2]

    Xs, Ys = np.where(Y >= 0)

    Xs = Xs.reshape(Y.shape[0], Y.shape[1])
    Ys = Ys.reshape(Y.shape[0], Y.shape[1])

    dctY = np.zeros((n, n))
    dctCb = np.zeros((n, n))
    dctCr = np.zeros((n, n))

    Y -= 128
    Cb -= 128
    Cr -= 128

    for p, u in enumerate(range(0, M, dW)):
        pos_i_1, pos_i_2 = u , u + dW
        for q, v in enumerate(range(0, N, dH)):
            pos_j_1, pos_j_2 = v, v + dH

            sum_Y = Y[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2]
            sum_Cb = Cb[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2]
            sum_Cr = Cr[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2]

            cosx = np.cos(((2 * Xs[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2] + 1) * pi * p) / (2 * M))
            cosy = np.cos(((2 * Ys[pos_i_1 : pos_i_2, pos_j_1 : pos_j_2] + 1) * pi * q) / (2 * N))

            dctY[p, q] = alpha(p, M) * alpha(q, N) * np.sum(sum_Y * cosx * cosy)
            dctCb[p, q] = alpha(p, M) * alpha(q, N) * np.sum(sum_Cb * cosx * cosy)
            dctCr[p, q] = alpha(p, M) * alpha(q, N) * np.sum(sum_Cr * cosx * cosy)

    # DCT_V and DCT_VI

    dY = zigzag_scan(dctY / Q, n)
    dCb = zigzag_scan(dctCb / Q, n)
    dCr = zigzag_scan(dctCr / Q, n)

    return dY, dCb, dCr
