#! /usr/bin/python3
"""
/**
 *
 * Date : 29 / 11 / 2017
 *
 * Nom :    Li
 * Prenom : Xiang
 *
 * Email :   xiangfr007@gmail.com
 *
 * Remarques :	
 * 			
 */
"""
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from numpy import median
import sys

resize_wh = 100
decalage = 32
filter_row_col = 0.2
filter_transformation = 40

# return array[resize_wh][resize_wh]
def fill_image_to_resize_wh(image):
	base_img = [[255 for col in range(0,resize_wh)] for row in range(0,resize_wh)]
	base_img = np.array(base_img)
	fill_img = np.array(image)
	for i in range(0,fill_img.shape[0]):
		for j in range(0,fill_img.shape[1]):
			base_img[i][j] = fill_img[i][j]
	return base_img

# return a photo
# zoom the photo to (?,resize_wh) or (resize_wh,?)
def zoom_image(image):
	img_array = np.array(image)
	x = img_array.shape[0]
	y = img_array.shape[1]
	if(x > y):
		rate = resize_wh/x
		y = int(y*rate)
		return image.resize((y,resize_wh))
	else:
		rate = resize_wh/y
		x = int(x*rate)
		return image.resize((resize_wh,x))

# return a photo
def get_image_of_character(image,average):
	img_array = np.array(image)
	x = img_array.shape[0]
	y = img_array.shape[1]
	xx = 0;
	yy = 0;
	#trouver le point noir le plus (haut,gauche) et celui le plus (bas,droite)
	#find two black point that locate (up,left) and (bottom,right)
	for i in range(0,img_array.shape[0]):
		for j in range(0,img_array.shape[1]):
			if(img_array[i][j] < average):
				if(i < x):
					x = i
				if(j < y):
					y = j
				if(i > xx):
					xx = i
				if(j > yy):
					yy = j
	return image.crop((y,x,yy,xx))

#return the average gray of a photo
def get_average(image):
	return median(image) - decalage

#return the list[10] (col = False / True)
def get_row_col_transformation(image,average,col_flag):
	img_array = np.array(image)
	list10 = [ 0 for i in range(10)]
	for i in range(0,img_array.shape[0]):
		flag = 0
		total = 0
		for j in range(0,img_array.shape[1]):
			now = img_array[i][j]
			if(col_flag == True):
				now = img_array[j][i]
			if(now < average):
				if(flag == 0):
					total += 1
					flag = 1
			else:
				if(flag== 1):
					total += 1
					flag = 0
		list10[int(i/10)] += total
	return list10

#return a list[21] and string of ahash
def get_feature_image(image):
	image = image.convert("L")	
	average = get_average(image)
	image_character = get_image_of_character(image,average)
	image_direct_resize = image_character.resize((resize_wh,resize_wh))
	image_filled = fill_image_to_resize_wh(zoom_image(image_character))
	#list[0] = row / col
	list21 = []
	list21.append(round((float(np.array(image_character).shape[0])/np.array(image_character).shape[1]),2))
	#list[1:11] = tranformation of row
	for i in get_row_col_transformation(image_filled,average,False):
		list21.append(i)
	#list[11:20] = tranformation of col
	for i in get_row_col_transformation(image_filled,average,True):
		list21.append(i)
	#ahash retrived from: https://www.cnblogs.com/luolizhi/p/5596171.html
	#hash_2=''.join(map(lambda i: '0' if i<average else '1',image_direct_resize.getdata()))
	hash_2=''.join(map(lambda i: '0' if i<average else '1',image_filled.flatten()))
	hash_16=''.join(map(lambda x:'%x' % int(hash_2[x:x+4],2), range(0,resize_wh*resize_wh,4)))

	return list21,hash_16

def diff_hash_16(hash1,hash2):
	difference = (int(hash1, 16))^(int(hash2, 16))
	return (bin(difference)+"").count("1")

def diff_transformation(list1,list2):
	diff = []
	for i in range(0,len(list1)):
		diff.append(int(list1[i])-int(list2[i]))
	return (sum([i**2 for i in diff])/len(diff))**0.5

def diff_row_col(list1,list2):
	return round(abs(float(list1[0])-float(list2[0])),2)

def load_saved():
	train_labels = []
	train_list21 = []
	train_hashs = []
	for row in open("labels.txt").readlines():
		train_labels.append(row.strip("\n"))
	for row in open("list21s.txt").readlines():
		row = row.strip("\n").replace("[","").replace("]","")
		train_list21.append(list(row.split(",")))
	for row in open("hashs.txt").readlines():
		train_hashs.append(row.strip("\n"))
	return train_labels,train_list21,train_hashs

#return label
def predict(image_path,train_labels,train_list21,train_hashs):
	pre_list,pre_hash = get_feature_image(Image.open(image_path))
	dic_result = {}
	for indice,train_lst in enumerate(train_list21):
		row_col = diff_row_col(pre_list,train_lst)
		if(row_col < filter_row_col):
			diff_trans_row = diff_transformation([i for i in pre_list[1:11]],[i for i in train_lst[1:11]]) 
			diff_trans_col = diff_transformation([i for i in pre_list[11:21]],[i for i in train_lst[11:21]]) 
			diff_transformation_total = diff_trans_row + diff_trans_col
			if(diff_transformation_total < filter_transformation):
				diff_hash = diff_hash_16(pre_hash,train_hashs[indice])
				if(train_labels[indice] not in dic_result or dic_result[train_labels[indice]][1]>diff_transformation_total):
					dic_result[train_labels[indice]] = (row_col,diff_transformation_total,diff_hash)
	
	dic_sorted = sorted(dic_result.items(),key=lambda x:x[1][1])
	#print(dic_sorted)
	#return dic_sorted[0][0]
	if(len(dic_sorted) == 0):
		return "404"
	if(len(dic_sorted) == 1):
		return dic_sorted[0][0]

	#and (abs(dic_sorted[0][1][0] - dic_sorted[1][1][0]) < 0.1)
	if(dic_sorted[1][1][2] < dic_sorted[0][1][2] and (abs(dic_sorted[0][1][1]-dic_sorted[1][1][1])<10)):
		return dic_sorted[1][0]
	else:
		return dic_sorted[0][0]

