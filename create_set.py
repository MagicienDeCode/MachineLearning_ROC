#! /usr/bin/python3

import os
from random import random
import shutil

def resetDirs(name):
    if os.path.exists(name):
        #delete all files
        for root, dirs, files in os.walk(name):
            for f in files:
                os.remove(os.path.join(root,f))
    else:
        os.makedirs(name)


for root, dirs, files in os.walk("all") :
    for d in dirs:
        resetDirs(os.path.join("train_set",d))
        resetDirs(os.path.join("test_set",d))
        for root2, dirs2, files2 in os.walk(os.path.join(root, d)):
            for name in files2:
                if random()>0.2:
                    shutil.copy(os.path.join(root,d,name),os.path.join("train_set",d,name))
                else:
                    #shutil.copy(os.path.join(root,d,name),os.path.join("train_set",d,name))
                    shutil.copy(os.path.join(root,d,name),os.path.join("test_set",d,name))
