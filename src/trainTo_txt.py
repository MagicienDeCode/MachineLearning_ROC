#! /usr/bin/python3

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

resize_w = 90
resize_h = 120

def getFigure(image):
    img = np.array(image.convert("L"))
    x = img.shape[0];
    y = img.shape[1];
    xx = 0;
    yy = 0;
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            if(img[i][j] < 123):
                if(i<x):
                    x = i
                if(j<y):
                    y = j
                if(i>xx):
                    xx = i
                if(j>yy):
                    yy = j
    #return (x,y,xx,yy)
    return (y,x,yy,xx)

def d_hash(image_path):
    img = Image.open(image_path)
    small_img = img.resize((resize_w,resize_h)).convert('L')
    figure_image = small_img.crop(getFigure(small_img))
    small_img = figure_image.resize((resize_w,resize_h))
    #avg = sum(list(small_img.getdata()))/(resize_w*resize_h)
    avg = 123
    str=''.join(map(lambda i: '0' if i<avg else '1', small_img.getdata()))
    return ''.join(map(lambda x:'%x' % int(str[x:x+4],2), range(0,resize_w*resize_h,4)))



all_train = []
total = 62

for root,dirs,files in os.walk("../train_set"):
#for root,dirs,files in os.walk("../all"):
	for d in dirs:
		total -=1
		print("now in "+d+" il reste :"+str(total))
		for root2,dirs2,files2 in os.walk(os.path.join(root,d)):
			for name in files2:
				all_train.append((d,d_hash(os.path.join(root,d,name))))

labels = list(zip(*all_train))[0]
lists = list(zip(*all_train))[1]
file_labels = open("labels.txt","w")
file_lists = open("lists.txt","w")
for lst in lists:
	file_lists.write(lst+"\r\n")
for la in labels:
	file_labels.write(la+"\r\n")
file_lists.close()
file_labels.close()
print("total labels: "+str(len(labels)))
print("total list: "+str(len(lists)))
