#! /usr/bin/python3
"""
/**
 *
 * Date : 11 / 12 / 2017
 *
 * Nom :    Li
 * Prenom : Xiang
 *
 * Email :   xiangfr007@gmail.com
 *		
 *
 */
"""
from common import *

from sklearn.metrics import accuracy_score, classification_report


train_labels,train_list21,train_hashs = load_saved()
test_set_answer = ["李","想","一","二","三","四","五","六","七","八","九","十","中","国","你","好","大","小","法","德"]

total_test = 0

print("======KNeighborsClassifier (n_neighbors = 1) ====================")
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors = 1)
model.fit(train_list21,train_labels)

for root,dirs,files in os.walk(test_path):
	test = []
	test_answer = []
	for d in dirs:
		if(d!="FA"):
			for i in range (1,21):
				name = str(i)+".png"
				features = get_feature_image(Image.open(os.path.join(test_path,d,name)))
				test.append(features[0])
				test_answer.append(test_set_answer[i-1])
	if(len(test)==0):
		break
	#print(len(test))
	predictions = model.predict(test)
	print(classification_report(test_answer,predictions))
	accuracy=accuracy_score(test_answer,predictions)
	print("accuracy" + " : " +str(accuracy*100)[0:2]+"%  ")

print("======SVC(kernel='poly')   ====================")
from sklearn.svm import SVC

model = SVC(kernel='poly')
model.fit(train_list21,train_labels)

for root,dirs,files in os.walk(test_path):
	test = []
	test_answer = []
	for d in dirs:
		if(d!="FA"):
			for i in range (1,21):
				name = str(i)+".png"
				features = get_feature_image(Image.open(os.path.join(test_path,d,name)))
				test.append(features[0])
				test_answer.append(test_set_answer[i-1])
	if(len(test)==0):
		break
	#print(len(test))
	predictions = model.predict(test)
	print(classification_report(test_answer,predictions))
	accuracy=accuracy_score(test_answer,predictions)
	print("accuracy" + " : " +str(accuracy*100)[0:2]+"%  ")


print("======RandomForestClassifier (n_estimators = 900)  ====================")
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators = 900)
model.fit(train_list21,train_labels)

for root,dirs,files in os.walk(test_path):
	test = []
	test_answer = []
	for d in dirs:
		if(d!="FA"):
			for i in range (1,21):
				name = str(i)+".png"
				features = get_feature_image(Image.open(os.path.join(test_path,d,name)))
				test.append(features[0])
				test_answer.append(test_set_answer[i-1])
	if(len(test)==0):
		break
	#print(len(test))
	predictions = model.predict(test)
	print(classification_report(test_answer,predictions))
	accuracy=accuracy_score(test_answer,predictions)
	print("accuracy" + " : " +str(accuracy*100)[0:2]+"%  ")