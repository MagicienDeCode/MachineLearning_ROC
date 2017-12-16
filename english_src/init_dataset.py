import os
import fnmatch
import cv2
import skimage.data as ski
import numpy as np
import shutil
import matplotlib.pyplot as plt
import sys
from loading_dataset import rename_dataset

rename_dataset()

get_dataset(160)

get_dataset(20, False)
