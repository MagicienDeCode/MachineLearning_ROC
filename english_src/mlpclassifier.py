import os
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from loading_dataset import load_dataset
import matplotlib.pyplot as plt
from random import shuffle

images_test, labels_test = load_dataset("../training_dataset/", 160)

data = images_test.reshape(len(images_test), -1)

classifier = MLPClassifier(solver="sgd")

classifier.activation = "relu"
classifier.learning_rate_init = 0.001
classifier.learning_rate = "adaptive"

print(classifier)

classifier.fit(data, labels_test)

images_test, labels_test = load_dataset("../test_dataset/", 160, False)

data_test = images_test.reshape(len(images_test), -1)

expected = labels_test
predicted = classifier.predict(data_test)

accuracy = accuracy_score(expected,predicted)

print("****************** average_score : " + str(accuracy))

images_and_predictions = list(zip(images_test, predicted))
shuffle(images_and_predictions)

for index, (image, prediction) in enumerate(images_and_predictions[0:40]):
    plt.subplot(2, 20, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title(str(prediction))

plt.show()
