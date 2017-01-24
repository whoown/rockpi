# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import os
import shutil
import image_libs
from image_libs import ImageNameCreator
import re
from PIL import Image
from PIL.ExifTags import TAGS


def rename_photos(sou, dest):
    print sou, dest
    if dest:
        os.makedirs(dest)
        if not os.path.exists(dest):
            print('Destination directory not exists. ')
            return False


def __rename_photo():
    pass




if __name__ == '__main__':
    fileName = 'C:\Users\Rock\Desktop\\hello.JPG'
    exif = image_libs.read_exif_info(fileName)
    # print exif
    print rename_image(fileName, ImageNameCreator.EXIF_TIME)
    print len(os.path.splitext(fileName))


