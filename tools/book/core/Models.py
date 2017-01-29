# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import os

from tools.file import file_libs


class Series:
    series_name = None
    author = None
    info = None
    books = None

    def __init__(self, _series_name='', _author=''):
        self.series_name = _series_name.strip()
        self.author = _author.strip()
        self.books = []

    def add_book(self, new_book):
        self.books.append(new_book)

    def save_to_txt(self, dir_path):
        # If there're multiple books in this series. Save them in one folder.
        if self.series_name and len(self.books) > 1:
            dir_path = os.path.join(dir_path, self.series_name)
        if not file_libs.make_sure_dir(dir_path):
            raise Exception('Can not save books since destination directory can not be created. %s.' % dir)
        for book in self.books:
            try:
                book.save_to_txt(dir_path, self.series_name)
            except Exception, e:
                print e


class Book:
    __SEPARATOR__ = '=' * 20
    title = None
    author = None
    info = None
    chapters = None

    def __init__(self, book_title='', book_author=''):
        self.title = book_title
        self.author = book_author
        self.chapters = []

    def add_chapter(self, new_chapter):
        self.chapters.append(new_chapter)

    def build(self):
        if not self.title:
            raise Exception('This book has no title.')
        book = "%s\n%s\n" % (self.title, Book.__SEPARATOR__)
        if self.author:
            book += u"作者: %s\n" % self.author
        if self.info:
            book += u"信息：%s\n" % self.info
        book += "%s\n" % Book.__SEPARATOR__

        chapter_index = 0
        for cpt in self.chapters:
            chapter_index += 1
            book += u"Chapter%d：%s\n" % (chapter_index, cpt.title)
        book += Book.__SEPARATOR__ + "\n\n"

        for cpt in self.chapters:
            book += u"%s\n\n" % cpt.build()
        return book

    def save_to_txt(self, txt_path, series_name=''):
        if txt_path.endswith('.txt'):
            dir_path = os.path.dirname()
        else:  # There's no specific file name
            if not self.title:
                raise Exception('Failed to save book since lack of book name.')
            if series_name:
                filename = "[%s]%s.txt" % (series_name, self.title)
            else:
                filename = self.title + ".txt"
            dir_path = txt_path
            txt_path = os.path.join(dir_path, file_libs.correct_file_name(filename))

        if not file_libs.make_sure_dir(dir_path):
            raise Exception('Can not save books since destination directory can not be created. %s.' % dir_path)

        content = self.build()
        try:
            fout = open(txt_path, "w")
            fout.write(content.encode("utf-8"))
            fout.flush()
            fout.close()
        except Exception, e:
            print 'Failed to save book since %s' % str(e)
            return False
        return True


class Chapter:
    title = None
    content = None

    def __init__(self, chapter_title='', chapter_content=''):
        self.title = chapter_title
        self.content = chapter_content

    def append_line(self, new_line):
        self.content = self.content + "\n" + new_line

    def append_content(self, new_content):
        self.content = self.content + new_content

    def build(self):
        return ("**** %s ****\n" % self.title) + self.content
