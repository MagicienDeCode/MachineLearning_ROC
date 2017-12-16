#! /usr/bin/python3
"""
/**
 * Input : test_set (folder)
 *
 * Output : accurecy and error
 *
 * Date : 29 / 11 / 2017
 *
 * Nom :    Li
 * Prenom : Xiang
 *
 * Email :   xiangfr007@gmail.com
 *
 * Remarques :	./test_set folder_path
 *				
 * 			
 *
 */
"""
from common import *
from sklearn.metrics import accuracy_score, classification_report


"""
if len(sys.argv) != 2 :
	print("The arg1 must be a path of test_set:")
	print("./test_set path")
	exit(-1)
"""

train_labels,train_list21,train_hashs = load_saved()
test_set_answer = ["李","想","一","二","三","四","五","六","七","八","九","十","中","国","你","好","大","小","法","德"]

from sklearn.tree import DecisionTreeClassifier


model = DecisionTreeClassifier()
model.fit(train_list21,train_labels)

print("======DecisionTreeClassifier     ====================")
total_accuracy=[]
for root,dirs,files in os.walk(test_path):
    for d in dirs:
        test = []
        for i in range (1,21):
            name = str(i)+".png"
            features = get_feature_image(Image.open(os.path.join(test_path,d,name)))
            test.append(features[0])
        predictions = model.predict(test)
        #print(predictions)
        accuracy=accuracy_score(test_set_answer,predictions)
        total_accuracy.append(accuracy)
        print("%10s"%d + " : " +str(accuracy*100)[0:2]+"%    "+str(int(accuracy*20))+"/20")
        #print(classificat=ion_report(test_set_answer,predictions))

print("****************** average_score : "+str(sum(total_accuracy)/len(total_accuracy)*100)[0:2]+"%")