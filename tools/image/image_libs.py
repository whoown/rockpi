# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import os
import re
from tools.file import file_libs
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime


def read_exif_info(image_path):
    """ Get embedded EXIF data from image file. """
    ret = {}
    try:
        img = Image.open(image_path)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOError ' + image_path
    return ret


def rename_image(image_path, image_name_creator):
    """Rename an image file with the given name creator. """
    if not image_name_creator or not callable(image_name_creator):
        print('Lack of valid image name creator.')
        return False
    if not os.path.isfile(image_path):
        print 'Given file is not exist: ', image_path
        return False
    if len(os.path.splitext(image_path)) < 2:
        print ('Given file have not an extension name', image_path)
        return False
    if "." not in os.path.basename(image_path):
        return False
    image_path = fix_image_file(image_path)
    new_name = image_name_creator(image_path)
    if not new_name:
        return False
    if new_name == image_path:
        return True
    new_path = os.path.join(os.path.dirname(image_path), new_name)
    os.rename(image_path, new_path)
    print image_path, "===>", new_path
    return True


def fix_image_file(image_path):
    ext = os.path.splitext(image_path)
    if len(ext) != 2:
        return image_path
    ext_name = ext[1]
    ext_name = re.sub("\(\d+\)", "", ext_name)
    new_path = ext[0] + ext_name
    os.rename(image_path, new_path)
    return new_path.lower()


class ImageNameCreator:
    def __init__(self):
        pass

    @staticmethod
    def __name_decorate(name, image_path):
        ext = os.path.splitext(image_path)
        name = file_libs.correct_file_name(name)
        dir_name = os.path.dirname(image_path)
        ext_name = ''
        if len(ext) == 2 and not name.endswith(ext[1]):
            ext_name = ext[1]
        target_path = os.path.join(dir_name, name + ext_name)
        if target_path == image_path:
            return image_path
        if os.path.exists(os.path.join(dir_name, name + ext_name)):
            for i in range(2, 10000):
                if not os.path.exists(os.path.join(dir_name, name + "(%d)" % i + ext_name)):
                    return name + ("(%d)" % i) + ext_name
        return name + ext_name

    @staticmethod
    def __default(image_path):
        image = os.path.splitext(image_path)[0]
        return ImageNameCreator.__name_decorate(os.path.basename(image), image_path)

    @staticmethod
    def __exif_time(image_path):
        exifinfo = read_exif_info(image_path)
        if not exifinfo or 'DateTimeOriginal' not in exifinfo:
            return None
        timestr = exifinfo['DateTimeOriginal']
        return ImageNameCreator.__name_decorate(timestr, image_path)

    @staticmethod
    def __modified_time(image_path):
        try:
            date = datetime.fromtimestamp(os.path.getmtime(image_path))
            return ImageNameCreator.__name_decorate(date.strftime("%Y_%m_%d %H_%M_%S"), image_path)
        except Exception:
            return None

    DEFAULT = __default
    EXIF_TIME = __exif_time
    MODIFIED_TIME = __modified_time


if __name__ == '__main__':
    fileName = 'C:\Users\Rock\Desktop\\hello.JPG'
    exif = read_exif_info(fileName)
    # print exif
    # print rename_image(fileName, ImageNameCreator.EXIF_TIME)
    # print len(os.path.splitext(fileName))
    # print ImageNameCreator.MODIFIED_TIME("/Users/zhangyan/Desktop/Images/IMG_0827.m4v")
