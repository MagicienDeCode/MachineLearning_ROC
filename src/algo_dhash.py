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

def diff_dhash_img(dh1,dh2):
    difference =  (int(dh1, 16))^(int(dh2, 16))
    return (bin(difference)+"").count("1")

def d_hash(image_path):
    img = Image.open(image_path)
    small_img = img.resize((resize_w,resize_h)).convert('L')
    figure_image = small_img.crop(getFigure(small_img))
    small_img = figure_image.resize((resize_w,resize_h))
    avg = sum(list(small_img.getdata()))/(resize_w*resize_h)
    #avg = 123
    str=''.join(map(lambda i: '0' if i<avg else '1', small_img.getdata()))
    return ''.join(map(lambda x:'%x' % int(str[x:x+4],2), range(0,resize_w*resize_h,4)))



train_labels = []
train_list = []
read_labels = open("labels.txt")
read_list = open("lists.txt")
for row in read_labels.readlines():
	train_labels.append(row.strip("\n"))
for row in read_list.readlines():
	train_list.append(row.strip("\n"))

print("total labels: "+str(len(train_labels)))
print("total list: "+str(len(train_list)))



def predit(img_path):
	prelist = d_hash(img_path)
	k1=(0,10000)
	k2=(0,10001)
	k3=(0,10002)
	for indice,i in enumerate(train_list):
		prediff = diff_dhash_img(prelist,i)
		if(prediff<k3[1]):
			if(prediff<k2[1]):
				if(prediff<k1[1]):
					k1=(indice,prediff)
				else:
					k2=(indice,prediff)
			else:
				k3=(indice,prediff)
	label1=train_labels[k1[0]]
	label2=train_labels[k2[0]]
	label3=train_labels[k3[0]]
	#print(str(k1)+","+str(k2)+","+str(k3))
	#print(str(label1+","+label2+","+label3))
	if(label1 == label2):
		return label1
	if(label1 == label3):
		return label1
	if(label2 == label3):
		return label3
	return "cant not found :("

all_train = []
total = 62
bingo = 0;
error = 0;
for root,dirs,files in os.walk("../test_set"):
	for d in dirs:
		total -=1
		print("now in "+d+" il reste :"+str(total))
		for root2,dirs2,files2 in os.walk(os.path.join(root,d)):
			for name in files2:
				if(d == predit(os.path.join(root,d,name))):
					bingo +=1
				else:
					error +=1
				#all_train.append((d,d_hash(os.path.join(root,d,name))))



print("total : "+str(bingo+error))
print("bingo : "+str(bingo))
print("bingo percentage : "+str(bingo/(bingo+error)))
