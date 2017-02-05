# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import os
import shutil

import image_libs
from image_libs import ImageNameCreator
from tools.file import file_libs


def rename_photos(src, dst):
    photodir = src
    if dst:
        if not os.path.isdir(dst):
            pass
        else:
            files = os.listdir(dst)
            is_empty = True
            for f in files:
                if os.path.isdir(f):
                    is_empty = False
                    break
                elif os.path.islink(f):
                    pass
                elif os.path.isfile(f):
                    if not os.path.basename(f).startswith("."):
                        is_empty = False
                        break
            if not is_empty:
                print 'Destination directory is not empty. Failed!'
                return False
            shutil.rmtree(dst)
        photodir = dst
        shutil.copytree(src, dst, False)
    if not photodir:
        print('Photo directory is illegal. ')
        return False

    def rename_photo(image):
        image_libs.rename_image(image, ImageNameCreator.EXIF_TIME)

    file_libs.iterate(photodir, rename_photo, None)
    return True


def __test_rename_photos():
    src = '/Users/zhangyan/Desktop/test'
    dst = '/Users/zhangyan/Desktop/res'
    print rename_photos(src, dst)


if __name__ == '__main__':
    # __test_rename_photos()
    src = '/Users/zhangyan/Desktop/2016.05.08-2016.05.23 日常'
    src = '/Users/zhangyan/Records'
    print rename_photos(src, None)
