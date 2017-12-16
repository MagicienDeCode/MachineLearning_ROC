import os
import fnmatch
import cv2
import skimage.data as ski
import numpy as np
import shutil
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../libs/')
from common import *

path_large_folder = '../by_class/'
load_training_dataset = '../training_dataset/'
load_test_dataset = '../test_dataset/'

nb_letter = 26
nb_number = 10
img_size = 40, 40

def rename_dataset():

    init_f = 3
    init_s = "0"

    new_name = "0"

    index_elem = 0

    nb_elem = (nb_letter * 2) + nb_number

    end = False

    while(nb_elem > index_elem) :

        while((not end) and (index_elem <= nb_elem)) :

            index_elem += 1

            if(index_elem > nb_elem):
                break

            print("Folder " + str(init_f) + str(init_s) + " exist ?" + " " + str(os.path.isdir(path_large_folder + str(init_f) + str(init_s))))

            if(str(os.path.isdir(path_large_folder + str(init_f) + str(init_s)))) :
                print(str(init_f) + str(init_s) + " -> " + new_name)
                os.rename(path_large_folder + str(init_f) + str(init_s), path_large_folder + new_name)

            if(ord(new_name) == 57) :
                new_name = "A"
            elif(ord(new_name) == 90) :
                new_name = "a"
            else :
                new_name = chr(ord(new_name) + 1)


            if(index_elem == nb_number) :
                if(init_f == 3 or init_f == 5) :
                    init_s = "1"
                else :
                    init_s = "0"
                end = True
                break

            if(index_elem == (nb_number + nb_letter)) :
                if(init_f == 3 or init_f == 5) :
                    init_s = "1"
                else :
                    init_s = "0"
                end = True
                break

            if(init_s == "9") :
                init_s = "a"

            elif(init_s == "f") :
                if(init_f == 3 or init_f == 5) :
                    init_s = "1"
                else :
                    init_s = "0"
                end = True
                break

            else :
                init_s = chr(ord(init_s) + 1)


        end = False
        init_f += 1


def get_dataset(train_file_nomber, training = True) :
    path = os.path.normpath(path_large_folder)

    path = path.rstrip(os.path.sep)
    assert os.path.isdir(path)
    num_sep = path.count(os.path.sep)

    if training :
        if(os.path.isdir(load_training_dataset)) :
            shutil.rmtree(load_training_dataset)
        os.makedirs(load_training_dataset)
    else :
        if(os.path.isdir(load_test_dataset)) :
            shutil.rmtree(load_test_dataset)
        os.makedirs(load_test_dataset)

    max_to_read = train_file_nomber

    for root, dirs, files in os.walk(path) :
        if training :
            if fnmatch.fnmatch(root, '*train*'):
                print(root)
                os.makedirs(load_training_dataset + root.split(os.path.sep)[-2:][0])
                max_to_read = train_file_nomber
                for name in files :
                    if(max_to_read > 0):
                        img = Image.open(os.path.join(root, name))
                        img.thumbnail(img_size, Image.ANTIALIAS)
                        img.save(load_training_dataset + root.split(os.path.sep)[-2:][0] + os.path.sep + name)
                        max_to_read -= 1
                    else:
                        break
            else:
                continue
        else :
            if not fnmatch.fnmatch(root.split(os.path.sep)[-2:][0], 'by_class') and not fnmatch.fnmatch(root.split(os.path.sep)[-2:][0], '*train*') and not fnmatch.fnmatch(root.split(os.path.sep)[-2:][0], '..') and not fnmatch.fnmatch(root.split(os.path.sep)[-2:][0], '.'):
                print(load_test_dataset + root)
                if(not os.path.isdir(load_test_dataset + root.split(os.path.sep)[-2:][0])) :
                    os.makedirs(load_test_dataset + root.split(os.path.sep)[-2:][0])
                max_to_read = train_file_nomber
                for name in files :
                    if not fnmatch.fnmatch(name, '*.mit') :
                        if(max_to_read > 0):
                            img = Image.open(os.path.join(root, name))
                            img.thumbnail(img_size, Image.ANTIALIAS)
                            img.save(load_test_dataset + root.split(os.path.sep)[-2:][0] + os.path.sep + name)
                            max_to_read -= 1
                        else:
                            break



def load_dataset(path_training_dataset, nb_img_by_char, training = True):

    h, w = img_size

    images = np.zeros((nb_img_by_char*(nb_letter*2+nb_number), h, w, 3), dtype=np.float32)

    labels = []
    im_nb = 0
    for root, dirs, files in os.walk(path_training_dataset) :
        for d in dirs :
            for r, dd, imgs  in os.walk(path_training_dataset + str(d)) :
                for img in imgs :
                    labels += [d]
                    img_content = ski.imread(path_training_dataset + str(d) + os.path.sep + str(img)).astype(np.float32)
                    face = np.asarray(img_content, dtype=np.float32)
                    face /= 255.0
                    images[im_nb, ...] = face
                    im_nb += 1

    return images, labels
