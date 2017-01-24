# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import os
import re
from PIL import Image
from PIL.ExifTags import TAGS


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
    """Rename an image file with the given name creator. """\

    if not image_name_creator or not callable(image_name_creator):
        print('Lack of valid image name creator.')
        return False
    if not os.path.isfile(image_path):
        print 'Given file is not exist: ', image_path
        return False
    if len(os.path.splitext(image_path)) < 2:
        print ('Given file have not an extension name', image_path)
        return False

    new_name = image_name_creator(image_path)
    new_path = os.path.join(os.path.dirname(image_path), new_name)
    print new_path
    os.rename(image_path, new_path)
    return True


class ImageNameCreator:

    def __init__(self):
        pass

    @staticmethod
    def __name_decorate(name, image_path):
        ext = os.path.splitext(image_path)
        illegal_chars = re.compile('[\\\\/:*?"<>|]')
        name = illegal_chars.sub('_', name)
        if len(ext) == 2 and not name.endswith(ext[1]):
            name += ext[1]
        return name

    @staticmethod
    def __default(image_path):
        return ImageNameCreator.__name_decorate(os.path.basename(image_path), image_path)

    @staticmethod
    def __exif_time(image_path):
        exifinfo = read_exif_info(image_path)
        if not exifinfo or 'DateTimeOriginal' not in exifinfo:
            return ImageNameCreator.__default(image_path)
        timestr = exifinfo['DateTimeOriginal']
        return ImageNameCreator.__name_decorate(timestr, image_path)

    DEFAULT = __default
    EXIF_TIME = __exif_time



if __name__ == '__main__':
    fileName = 'C:\Users\Rock\Desktop\\hello.JPG'
    exif = read_exif_info(fileName)
    # print exif
    print rename_image(fileName, ImageNameCreator.EXIF_TIME)
    print len(os.path.splitext(fileName))


