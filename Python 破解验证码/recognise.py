#coding:utf-8

import os
import requests
from PIL import Image
import math

def convert_image(image):  #转换图像
    image=image.convert('L') #转换成 L 型，L为8bit的图像，即黑白图像， 这里是为了防止其他颜色的干扰
    image2=Image.new('L',image.size,255)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if pix<120:
                image2.putpixel((x,y),0)   #过滤不需要的像素
    return image2

def cut_image(image):  #切割图像
    inletter=False
    foundletter=False
    letters=[]
    start=0
    end=0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if(pix==0):
                inletter=True
        if foundletter==False and inletter ==True:
            foundletter=True
            start=x
        if foundletter==True and inletter==False:
            end=x
            letters.append((start,end))
            foundletter=False
        inletter=False
    images=[]
    for letter in letters:
        # 返回当前图像的一个矩形区域。
        # box参数是一个定义了左，上，右，下像素坐标的4元元组。
        img=image.crop((letter[0],0,letter[1],image.size[1]))
        images.append(img)
    return images

def buildvector(image):
    result={}
    count=0
    for i in image.getdata():
        result[count]=i
        count+=1
    return result


class CaptchaRecognize:
    def __init__(self):
        #self 类似于this指针，当self之后跟着变量则为该类的成员变量
        self.letters=['0','1','2','3','4','5','6','7','8','9']
        self.loadSet()

    def loadSet(self):
        self.imgset=[]
        for letter in self.letters:
            temp=[]
            for img in os.listdir('./icon/%s'%(letter)):
                temp.append(buildvector(Image.open('./icon/%s/%s'%(letter,img))))
            self.imgset.append({letter:temp})

    #计算矢量大小
    def magnitude(self,concordance):  #concordance; 一致性
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

    def recognise(self,image):
        image=convert_image(image)
        images=cut_image(image)
        vectors=[]
        for img in images:
            vectors.append(buildvector(img))
        result=[]
        for vector in vectors:
            guess=[]
            for image in self.imgset:
                for letter,temp in image.items():
                    relevance=0  #相关性
                    num=0
                    for img in temp:
                        relevance+=self.relation(vector,img)
                        num+=1
                    relevance=relevance/num
                    guess.append((relevance,letter))
            guess.sort(reverse=True)
            for gus in guess:
                print gus
            print
            result.append(guess[0])
        return result

if __name__=='__main__':
    imageRecognize=CaptchaRecognize()
    image=Image.open('test.jpeg')
    result=imageRecognize.recognise(image)
    string=[''.join(item[1]) for item in result]
    print(string)