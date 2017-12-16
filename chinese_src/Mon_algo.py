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

"""
if len(sys.argv) != 2 :
    print("The arg1 must be a path of test_set:")
    print("./test_set path")
    exit(-1)
"""

train_labels,train_list21,train_hashs = load_saved()
test_set_answer = ["李","想","一","二","三","四","五","六","七","八","九","十","中","国","你","好","大","小","法","德"]

print("===========Algo XiangLI==================")
dic_error = {}
nom = []
average_accuracy = []
for root,dirs,files in os.walk(test_path):
    for d in dirs:
        success = 0
        error=[]
        #print("================="+d+"====================")
        for i in range (1,21):
            name = str(i)+".png"
            predict_label = predict(os.path.join(test_path,d,name),train_labels,train_list21,train_hashs)
            if(predict_label == test_set_answer[i-1]):
                success += 1
            else:
                if(test_set_answer[i-1] not in dic_error):
                    dic_error[test_set_answer[i-1]] = str(predict_label+" ")
                else:
                    dic_error[test_set_answer[i-1]] += str(predict_label+" ")
                error_mes = name + " : " + predict_label+" , but it's "+test_set_answer[i-1]
                error.append(error_mes)
        #print("accuracy : "+str(success/20*100)[0:2]+"% "+str(success)+"/"+str(20))
        nom.append(d)
        average_accuracy.append(success/20)
        """
        for i in error:
            print(i)
		"""
#print("========== Report ========================")

for i in range(0,len(nom)):
    print("%10s"%nom[i] +" :  "+str(average_accuracy[i]*100)[0:2]+"%")

print("************* average_accuracy : "+str(sum(average_accuracy)/len(average_accuracy)*100)[0:2]+"%")
"""
print(">>>>>>>>>>>>> Error <<<<<<<<<<<<<<<")
dic_sorted = sorted(dic_error.items(),key=lambda x:len(x[1]),reverse=True)
for i in dic_sorted:
    print(i)
"""