# coding:utf-8

import cv2


def hide(s):
    img = cv2.imread("lena.bmp")

    w, h = img.shape[:2]
    for i in range(w):
        for j in range(h):
            if img[i, j, 2] % 2 != 0:
                img[i, j, 2] = img[i, j, 2] + 1 if img[i, j, 2] < 2 else img[i, j, 2] - 1

    slen = len(s)

    for i in range(h):
        for j in range(w):
            if w * i + j < slen:
                if s[w * i + j] == '1':
                    img[i, j, 2] += 1
            else:
                break

    cv2.imwrite("final.bmp", img)


def show():
    img = cv2.imread("final.bmp")
    a = ''
    w, h = img.shape[:2]
    for i in range(w):
        for j in range(h):
            if img[i, j, 2] % 2 != 0:
                a = a + '1'
            else:
                a = a + '0'
    return a


def encode(s):
    a = ''
    for c in s:
        sCode = bin(ord(c)).replace('0b', '')
        while len(sCode) < 8:
            sCode = '0' + sCode
            # print sCode

        a = a + sCode
    return a


def decode(s):
    slen = len(s)
    a = ''
    for i in range(slen):
        b = s[8 * i:8 * (i + 1)]
        if b == '' or b == '00000000':
            break
        print b
        a = a + chr(int(b, 2))
    return a


def test():
    test = "test"
    for c in test:
        print bin(ord(c)).replace("0b", "")
        print len(bin(ord(c)).replace("0b", ""))


encodeText = raw_input("please input test")
code = encode(encodeText)
print 'encode:' + code
# print decode(code)
hide(code)
showcode = show()
print 'showcode:' + showcode
print "decode:"+decode(showcode)
