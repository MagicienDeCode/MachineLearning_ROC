#! /usr/bin/python3
"""
/**
 * Input : train_set (folder)
 *
 * Output : labels.txt list21s.txt hashs.txt
 *
 * Date : 29 / 11 / 2017
 *
 * Nom :    Li
 * Prenom : Xiang
 *
 * Email :   xiangfr007@gmail.com
 *
 * Remarques :	./training path_of_train_set
 * 				In the folder train_set, each folder's name is a label
 * 			
 */
"""
from common import *



if len(sys.argv) == 2 :
	all_path = sys.argv[1]

all_data = []
total = 0

def reinforce(image,label,all_data):
	height = np.array(image).shape[0]
	weight = np.array(image).shape[1]
	init = 1
	intervalle = 1
	for i in range(init,16,intervalle):
		image_reinforce = image.resize((height,weight+i))
		all_data.append((label,get_feature_image(image_reinforce)))
		image_reinforce = image.resize((height+i,weight))
		all_data.append((label,get_feature_image(image_reinforce)))


for root,dirs,files in os.walk(all_path):
	for d in dirs:
		total +=1
		print("now in "+d+" already treated:"+str(total))
		for root2,dirs2,files2 in os.walk(os.path.join(root,d)):
			for name in files2:
				image_normal = Image.open(os.path.join(root,d,name))
				all_data.append((d,get_feature_image(image_normal)))
				reinforce(image_normal,d,all_data)


labels = list(zip(*all_data))[0]
list21_ahash = list(zip(*all_data))[1]
list21s = list(zip(*list21_ahash))[0]
hashs = list(zip(*list21_ahash))[1]

file_lables = open("labels.txt","w")
file_list21s = open("list21s.txt","w")
file_hashs = open("hashs.txt","w")

for label in labels:
	file_lables.write(label+"\r\n")
for lst in list21s:
	file_list21s.write(str(lst)+"\r\n")
for ah in hashs:
	file_hashs.write(ah+"\r\n")
file_lables.close()
file_list21s.close()
file_hashs.close()
print("total labels :"+str(len(labels)))
print("total lists  :"+str(len(list21s)))
print("total ahashs :"+str(len(hashs)))
