EXEC_FILE : 

load_TrainSet :
	python3 training.py

resultV1 :
	./make_result

resultV2 : 
	python3 resultv2.py > result2.txt
	echo "please run less result2.txt"

resultV3 : 
	python3 resultv3.py > result3.txt
	echo "please run less result3.txt"

.PHONY : clean

clean :
	rm hashs.txt labels.txt list21s.txt result.txt result2.txt result3.txt