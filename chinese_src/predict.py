#! /usr/bin/python3
"""
/**
 * Input : image_path
 *
 * Output : label predicted
 *
 * Date : 29 / 11 / 2017
 *
 * Nom :    Li
 * Prenom : Xiang
 *
 * Email :   xiangfr007@gmail.com
 *
 * Remarques :	./predictK1 image_path
 *				
 * 			
 *
 */
"""
from common import *

train_labels,train_list21,train_hashs = load_saved()

for i in sys.argv[1:]:
	print(predict(i,train_labels,train_list21,train_hashs))

