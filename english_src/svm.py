import os
from shutil import copyfile
from sklearn import datasets, svm
from sklearn.metrics import accuracy_score, classification_report
from sklearn.externals import joblib
import fnmatch
import cv2
import skimage.data as ski
import numpy as np
import shutil
import matplotlib.pyplot as plt
from loading_dataset import *
import sys
from random import shuffle


print('Number of arguments: ' + str(len(sys.argv)) + ' arguments.')
print('Argument List: ' + str(sys.argv))

if len(sys.argv) != 2 :
    print("agument necessaire: poly ou linear")
    sys.exit(0)

if((sys.argv[1] != "linear") and (sys.argv[1] != "poly")) :
        print("agument necessaire: poly ou linear")
        sys.exit(0)

images, labels = load_dataset("../training_dataset/", 160)

data = images.reshape(len(images), -1)

if sys.argv[1] == "poly" :
    classifier = svm.SVC(kernel='poly', gamma=0.001)
else :
    classifier = svm.SVC(kernel='linear', gamma=0.001)

print("classifier set\n")

classifier.fit(data, labels)

print("fitted\n")

print("process prediction")

images_test, labels_test = load_dataset("../test_dataset/", 160, False)

data_test = images_test.reshape(len(images_test), -1)

expected = labels_test
predicted = classifier.predict(data_test)

accuracy = accuracy_score(expected,predicted)

print("****************** average_score : " + str(accuracy))

images_and_predictions = list(zip(images_test, predicted))
shuffle(images_and_predictions)

for index, (image, prediction) in enumerate(images_and_predictions[80:120]):
    plt.subplot(2, 20, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title(str(prediction))

plt.show()
