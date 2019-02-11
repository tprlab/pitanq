import cv2 as cv
import numpy as np
import sys
import os
import math

gray_EPS = 25
rgb_EPS = 25
gray_blur = 7

resize_blur = 15
resize_size = 64

white_threshold = 10



def blur_resize(path, outpath, blur, size):
    img = cv.imread(path)
    if img is None:
        return None, None
    h, w = img.shape[:2]

    blur = cv.medianBlur(img, blur)
    blur = blur[0:h, w - h:w]
    cut = cv.resize(blur, (size, size))
    if not outpath is None:
        cv.imwrite(outpath, cut)
    return img, cut


def get_clr_weight(bgr):
    x = np.argmax(bgr)
    n = np.argmin(bgr)
    if x == n:
        return 0        
    m = 3 - x - n
    d1 = int(bgr[x]) - int(bgr[m])
    d2 = int(bgr[n]) - int(bgr[m])
    return math.sqrt(d1 *d1 + d2 *d2)


def get_gray_avg(img, Q, r):
    avg = 0
    avg_n = 0
    h, w = img.shape[:2]
    for x in range(0, r):
        for y in range(h - r, h):
            bgr = img[y,x]
            D = get_clr_weight(bgr)
            #print bgr, D
            if D < Q:
                avg += (int(bgr[0]) + int(bgr[1]) + int(bgr[2]))
                avg_n += 3

    A = avg / avg_n if avg_n != 0 else 0;
    return A



def filter_gray(img, Q, avg, A, blur, outfile = None):
    h, w = img.shape[:2]
    gray = np.zeros((h,w,1), np.uint8)
    hblack = h / 3

    for x in range(0, w):
        for y in range(hblack, h):
            bgr = img[y,x]
            D = get_clr_weight(bgr)
            if D < Q:
                c = (int(bgr[0]) + int(bgr[1]) + int(bgr[2])) / 3;
                R = abs(c - avg)
                #print D, R
                if R < A:
                    gray[y,x] = 255
    gray = cv.medianBlur(gray, blur)
    if outfile is not None:
        cv.imwrite(outfile, gray)
    return gray

def prepare_gray(path, out_path, Q, avg, A):
    img = cv.imread(path)
    gray = filter_gray(img, Q, avg, A)
    cv.imwrite(out_path + ".jpg", gray)
    return gray
    


def get_white_percent(g):
    nwh = cv.countNonZero(g)
    h, w = g.shape[:2]
    d = 100 * nwh / h / w
    return d

def write_word(img, word, clr):
    cv.putText(img, word,(20,30), cv.FONT_HERSHEY_SIMPLEX, 1, clr, 2, cv.LINE_AA)

def apply_mask_word(cpath, gpath, outpath, clr, word, clrw):
    img = apply_mask(cpath, gpath, None, clr)
    if img is None:
        return False
    write_word(img, word, clrw)
    if outpath is not None:
        cv.imwrite(outpath, img)
    return True

def apply_mask(cpath, gpath, outpath, clr):
    cimg = cv.imread(cpath)
    g = cv.imread(gpath, cv.IMREAD_GRAYSCALE)
    if cimg is None or g is None:
        return None

    h, w = cimg.shape[:2]
    for x in range(0, w):
        for y in range(0, h):
            if g[y, x] != 0:
                cimg[y,x] = clr
    if outpath is not None:
        cv.imwrite(outpath, cimg)

    return cimg


def to_hsv(img):    
    return cv.cvtColor(img, cv.COLOR_BGR2HSV)

def get_bright(img):
    return np.mean(img[:,:,2])

def get_avg_rgb(img, q):
    h, w = img.shape[:2]
    
    b = 0 
    g = 0
    r = 0

    for x in range(0, q):
        for y in range(h - q, h):
            bgr = img[y,x]
            b += bgr[0]
            g += bgr[1]
            r += bgr[2]

    qq = q * q
    b /= qq
    g /= qq
    r /= qq
    return r, g, b



if __name__ == '__main__':
    img = cv.imread("all/ctrain/l/16012019142446-349856.jpg")
    #avg = get_gray_avg(img, 15, 10)
    #print "Avg", avg
    avg = 110
    gray = filter_gray(img, 12, avg, 25)


    