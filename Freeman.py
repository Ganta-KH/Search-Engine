import numpy as np
import cv2, sys

sys.setrecursionlimit(99999)


def Naif_Detector(image):
    verticale = abs(image[:, 0: -1] - image[:, 1:])
    horizantal = abs(image[0: -1, :] - image[1:, :])
    contour = np.sqrt(verticale[:-1,:] ** 2 + horizantal[:, :-1] ** 2)
    np.putmask(contour, contour > 255, 255)
    return contour


def ChainCode(img, x, y, chain_code, bitmap):
    #try:
        # right
        if (img[x, y+1] == 255.) and (bitmap[x, y+1] == 0.): 
            chain_code += '0'
            bitmap[x-1, y] == 0.
            bitmap.itemset((x, y+1), 255.)
            y += 1
            return ChainCode(img, x, y, chain_code, bitmap)

        # up
        elif (img[x-1, y] == 255.) and (bitmap[x-1, y] == 0.):
            chain_code += '2'
            bitmap.itemset((x-1, y), 255.)
            x -= 1
            return ChainCode(img, x, y, chain_code, bitmap)

        # left
        elif (img[x, y-1] == 255.) and (bitmap[x, y-1] == 0.):
            chain_code += '4'
            bitmap.itemset((x, y-1), 255.)
            y -= 1
            return ChainCode(img, x, y, chain_code, bitmap)

        # down
        elif (img[x+1, y] == 255.) and (bitmap[x+1, y] == 0.):
            chain_code += '6'
            bitmap.itemset((x+1, y), 255.)
            x += 1
            return ChainCode(img, x, y, chain_code, bitmap)

        # up right
        elif (img[x+1, y+1] == 255.) and (bitmap[x+1, y+1] == 0.):
            chain_code += '1'
            bitmap.itemset((x+1, y+1), 255.)
            x += 1
            y += 1
            return ChainCode(img, x, y, chain_code, bitmap)

        # down right
        elif (img[x-1, y+1] == 255.) and (bitmap[x-1, y+1] == 0.):
            chain_code += '7'
            bitmap.itemset((x-1, y+1), 255.)
            x -= 1
            y += 1
            return ChainCode(img, x, y, chain_code, bitmap)

        # left up
        elif (img[x-1, y-1] == 255.) and (bitmap[x-1, y-1] == 0.):
            chain_code += '3'
            bitmap.itemset((x-1, y-1), 255.)
            x -= 1
            y -= 1
            return ChainCode(img, x, y, chain_code, bitmap)

        # left down
        elif (img[x+1, y-1] == 255.) and (bitmap[x+1, y-1] == 0.):
            chain_code += '5'
            bitmap.itemset((x+1, y-1), 255.)
            x += 1
            y -= 1
            return ChainCode(img, x, y, chain_code, bitmap)

        else: return chain_code
    #except: pass


def Freeman(image): # Freeman chains code 8-connex
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # chage it to gray
    blur = cv2.GaussianBlur(gray, (3, 3), 0) # blur the image
    binary = (blur < 180) * 255. # change it to binary

    img = np.zeros((gray.shape[0]+1, gray.shape[1]+1))
    img[1:-1, 1:-1] = Naif_Detector(binary) # get contour
    Xs, Ys = np.where((img == 255))

    bitmap = np.zeros(img.shape)
    chains_code = []
    for i in range(len(Xs)): # shearch for all tha chain that exit in the image
        startX, startY = Xs[i], Ys[i] # get the starting point
        if bitmap[startX, startY] != 255.: 
            chain_code = ''
            chain_code = ChainCode(img, startX, startY, chain_code, bitmap)
            if chain_code is not None and chain_code != '': chains_code.append(chain_code)


    lengths = np.array(list(map(lambda i: len(i), chains_code)))
    mx = np.argmax(lengths)
    hist = np.array([chains_code[mx].count(c) for c in '01234567'])


    #Image.fromarray(bitmap.astype('uint8')).show()
    return hist #chains_code

