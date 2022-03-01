from abc import ABCMeta, abstractmethod
from ..library_units.book import Book
from ..library_units.reader import Reader

import os
from ..utils import logprint


class IStorage(metaclass=ABCMeta):
    @abstractmethod
    def add_book(self, obj_book: Book) -> bool:
        pass

    @abstractmethod
    def remove_book(self, obj_book: Book) -> bool:
        pass

    @abstractmethod
    def update_book(self, obj_book: Book) -> bool:
        pass

    @abstractmethod
    def load_books(self) -> list:
        pass

    @abstractmethod
    def load_several_books(self, page: int, page_size: int) -> list:
        pass

    @abstractmethod
    def load_book_by_param(self, **kwargs):
        pass

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

    @abstractmethod
    def add_reader(self, obj_reader: Reader) -> bool:
        pass

    @abstractmethod
    def remove_reader(self, obj_reader: Reader) -> bool:
        pass

    @abstractmethod
    def update_reader(self, obj_reader: Reader) -> bool:
        pass

    @abstractmethod
    def load_readers(self) -> list:
        pass

    @abstractmethod
    def load_readers_by_email(self, email: str) -> Reader:
        pass

    @abstractmethod
    def load_readers_by_id(self, id_: int) -> Reader:
        pass

    @abstractmethod
    def load_load_reader_by_param(self, **kwargs):
        pass

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

    @abstractmethod
    def add_books(self, _obj_books: list):
        pass

    @abstractmethod
    def add_readers(self, _obj_readers: list):
        pass
