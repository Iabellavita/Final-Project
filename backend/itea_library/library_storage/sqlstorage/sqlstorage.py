from abc import ABC

from .base_class_sqlalchemy import Base
from ..istorage import IStorage

from ...library_units.book import Book
from ...library_units.reader import Reader

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import os
from ...utils import logprint


class SQLStorage(IStorage, ABC):
    def __init__(self, db_user, db_password, db_name,
                 db_address='localhost', db_port=5432, dialect='postgresql'):

        self.__engine = create_engine(f'{dialect}://{db_user}:{db_password}@'
                                      f'{db_address}:{db_port}/{db_name}')

        # create table
        Base.metadata.create_all(self.__engine)

        # create session
        self.__session = Session(self.__engine)

    def add_book(self, obj_book: Book) -> bool:
        self.__session.add(obj_book)
        try:
            self.__session.commit()
        except:
            return False
        return True

    def remove_book(self, obj_book: Book) -> bool:
        self.__session.delete(obj_book)
        try:
            self.__session.commit()
        except:
            return False
        return True

    def update_book(self, obj_book: Book) -> bool:
        book = self.__session.query(Book).filter(Book.id == obj_book.id).first()

        if not book:
            return False

        book.copy(obj_book)

        try:
            self.__session.commit()
        except:
            return False
        return True

    def load_books(self) -> list:
        return self.__session.query(Book).all()

    def load_several_books(self, page: int, page_size: int) -> list:
        query = self.__session.query(Book).order_by(Book.id).limit(page_size).offset(page * page_size).all()

    def load_book_by_param(self, **kwargs):
        for k, _ in kwargs.items():
            if k not in dir(Book):
                return None

        return self.__session.query(Book).filter_by(**kwargs).all()

    @staticmethod
    def load_books_from_txt_file(filename: str,
                                 sep: str = ',',
                                 encoding: str = 'utf-8') -> list:
        _res_books_list = []

        if not os.path.exists(filename):
            logprint.print_fail(f'file \'{filename}\' not found!')
            return _res_books_list

        with open(filename, encoding=encoding) as _file:
            for _line in _file:
                _line_list = _line.strip().split(sep)
                _res_books_list.append(Book(
                    _line_list[0],  # title
                    _line_list[1],  # author
                    int(_line_list[2])  # years
                ))

        return _res_books_list

    def add_reader(self, obj_reader: Reader) -> bool:
        self.__session.add(obj_reader)
        try:
            self.__session.commit()
        except:
            return False
        return True

    def remove_reader(self, obj_reader: Reader) -> bool:
        self.__session.delete(obj_reader)
        try:
            self.__session.commit()
        except:
            return False
        return True

    def update_reader(self, obj_reader: Reader) -> bool:
        reader = self.__session.query(Reader).filter(Reader.id == obj_reader.id).first()

        if not reader:
            return False

        reader.copy(obj_reader)

        try:
            self.__session.commit()
        except:
            return False
        return True

    def load_readers(self) -> list:
        return self.__session.query(Reader).all()

    def load_readers_by_email(self, email: str) -> Reader:
        return self.__session.query(Reader).filter_by(email=email).first()

    def load_readers_by_id(self, id_: int) -> Reader:
        return self.__session.query(Reader).filter_by(id=id_).first()

    def load_load_reader_by_param(self, **kwargs):
        for k, _ in kwargs.items():
            if k not in dir(Reader):
                return None

        return self.__session.query(Reader).filter_by(**kwargs)

    @staticmethod
    def load_readers_from_txt_file(filename: str,
                                   sep: str = ',',
                                   encoding: str = 'utf-8') -> list:
        _res_readers_list = []

        if not os.path.exists(filename):
            logprint.print_fail(f'file \'{filename}\' not found!')
            return _res_readers_list

        with open(filename, encoding=encoding) as _file:
            for _line in _file:
                _line_list = _line.strip().split(sep)
                _res_readers_list.append(Reader(
                    _line_list[0],  # name
                    _line_list[1],  # surname
                    int(_line_list[2])  # years
                ))

        return _res_readers_list

    def add_books(self, _obj_books: list):
        self.__session.add_all(_obj_books)
        try:
            self.__session.commit()
        except:
            return False
        return True

    def add_readers(self, _obj_readers: list):
        self.__session.add_all(_obj_readers)
        try:
            self.__session.commit()
        except:
            return False
        return True
