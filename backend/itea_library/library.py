from .library_units.book import Book
from .library_units.reader import Reader
from .library_storage.istorage import IStorage

from .utils import logprint


class Library:
    def __init__(self, storage: IStorage,
                 books: list = None,
                 readers: list = None) -> None:
        self.__storage = storage

        if books:
            self.__storage.add_books(books)

        if readers:
            self.__storage.add_readers(readers)

    # INIT
    ###################################################################################################
    def load_books_from_txt_file(self, filename: str,
                                 sep: str = ',',
                                 encoding: str = 'utf-8') -> bool:
        books = self.__storage.load_books_from_txt_file(filename, sep, encoding)
        if not len(books):
            logprint.print_fail(f'error load books from {filename}')
            return False

        self.__storage.add_books(books)
        return True

    def load_readers_from_txt_file(self, filename: str,
                                   sep: str = ',',
                                   encoding: str = 'utf-8') -> bool:
        readers = self.__storage.load_readers_from_txt_file(filename, sep, encoding)
        if not len(readers):
            logprint.print_fail(f'error load readers from {filename}')
            return False

        self.__storage.add_readers(readers)
        return True

    # GIVE - RETURN
    ###################################################################################################
    def give_book(self, id_book: int, id_reader: int) -> (bool, str):
        return_msg = ''

        book = self.__storage.load_book_by_param(id=id_book)

        if not book:
            return_msg = f'the book with id={id_book} does not exist in the library!'
            logprint.print_fail(return_msg)
            return False, return_msg

        book = book[0]

        if book.get_reader_id():
            return_msg = f'book with id={id_book} is out of stock now!'
            logprint.print_fail(return_msg)
            return False, return_msg

        reader = self.__storage.load_load_reader_by_param(id=id_reader)
        if not reader:
            return_msg = f'reader with id={id_reader} is\'t registered in the library!'
            logprint.print_fail(return_msg)
            return False, return_msg

        reader = reader[0]

        book.set_reader_id(id_reader)
        self.__storage.update_book(book)

        return_msg = f'the book "{book.get_title()}" has been ' \
                     f'successfully issued to the reader by ' \
                     f'{reader.get_name()} {reader.get_surname()}.'
        logprint.print_done(return_msg)
        return True, return_msg

    def give_books(self, id_book_list: list, id_reader: int) -> str:
        return_msg = ''
        return_msg_error = ''

        reader = self.__storage.load_load_reader_by_param(id=id_reader)
        if not reader:
            return_msg = f'reader with id={id_reader} is\'t registered in the library!'
            logprint.print_fail(return_msg)
            return return_msg

        reader = reader[0]

        for id_book in id_book_list:
            book = self.__storage.load_book_by_param(id=id_book)

            if not book:
                return_msg = f'the book with id={id_book} does not exist in the library!'
                return_msg_error += return_msg + '\n'
                logprint.print_fail(return_msg)
                continue

            book = book[0]

            if book.get_reader_id():
                return_msg = f'book with id={id_book} is out of stock now!'
                return_msg_error += return_msg + '\n'
                logprint.print_fail(return_msg)
                continue

            book.set_reader_id(id_reader)
            self.__storage.update_book(book)

            return_msg = f'the book "{book.get_title()}" has been ' \
                         f'successfully issued to the reader by ' \
                         f'{reader.get_name()} {reader.get_surname()}.'
            logprint.print_done(return_msg)

        return return_msg_error

    def return_book(self, id_book: int, id_reader: int) -> bool:
        book = self.__storage.load_book_by_param(id=id_book)
        if not book:
            logprint.print_fail(f'the book with id={id_book} does not exist in the library!')
            return False

        book = book[0]

        if not book.get_reader_id():
            logprint.print_fail(f'a book with id={id_book} is already in the library !')
            return False

        reader = self.__storage.load_load_reader_by_param(id=id_reader)
        if not reader:
            logprint.print_fail(f'reader with id={id_reader} is\'t registered in the library!')
            return False

        reader = reader[0]

        if book.get_reader_id() != reader.get_id():
            logprint.print_fail(f'the book with id={id_book} isn\'t not '
                                f'in the possession of the reader '
                                f'{reader.get_name()} {reader.get_surname()}!')
            return False

        book.set_reader_id(None)
        self.__storage.update_book(book)

        logprint.print_done(f'Reader {reader.get_name()} {reader.get_surname()} '
                            f'returned the book "{book.get_title()}" to the library.')
        return True

    def return_books(self, id_book_list: list, id_reader: int) -> str:
        return_msg_error = ''

        reader = self.__storage.load_load_reader_by_param(id=id_reader)
        if not reader:
            return_msg_error = f'reader with id={id_reader} is\'t registered in the library!'
            logprint.print_fail(return_msg_error)
            return return_msg_error

        reader = reader[0]

        for id_book in id_book_list:
            book = self.__storage.load_book_by_param(id=id_book)
            if not book:
                logprint.print_fail(f'the book with id={id_book} does not exist in the library!')
                return_msg_error += f'the book with id={id_book} does not exist in the library!' + '\n'
                continue

            book = book[0]

            if not book.get_reader_id():
                logprint.print_fail(f'a book with id={id_book} is already in the library !')
                return_msg_error += f'a book with id={id_book} is already in the library !' + '\n'
                continue

            if book.get_reader_id() != reader.get_id():
                msg = f'the book with id={id_book} isn\'t not ' \
                      f'in the possession of the reader ' \
                      f'{reader.get_name()} {reader.get_surname()}!'

                logprint.print_fail(msg)
                return_msg_error += msg + '\n'
                continue

            book.set_reader_id(None)
            self.__storage.update_book(book)
            logprint.print_done(f'Reader {reader.get_name()} {reader.get_surname()} '
                                f'returned the book "{book.get_title()}" to the library.')

        return return_msg_error

    # BOOKS
    ###################################################################################################
    def add_book(self, title: str, author: str, years: int) -> (bool, str):
        book = Book(title, author, years)
        if self.__storage.add_book(book):
            return_msg = f'Book "{book.get_title()}" added to the library.'
            logprint.print_done(return_msg)
            return True, return_msg
        else:
            logprint.print_fail('Error')
            return False, 'Error'

    def remove_book(self, id_: int) -> bool:
        book = self.__storage.load_book_by_param(id=id_)
        if not book:
            logprint.print_fail(f'the book with id={id_} does not exist in the library!')
            return False

        book = book[0]

        self.__storage.remove_book(book)

        logprint.print_done(f'book "{book.get_title()}" removed from library.')
        return True

    def remove_books(self, id_book_list: list) -> str:
        return_msg = ''
        for id_ in id_book_list:
            book = self.__storage.load_book_by_param(id=id_)
            if not book:
                return_msg += f'the book with id={id_} does not exist in the library!' + '\n'
                logprint.print_fail(f'the book with id={id_} does not exist in the library!')

            book = book[0]

            self.__storage.remove_book(book)
            return_msg = f'book "{book.get_title()}" removed from library.'
            logprint.print_done(return_msg)

        return return_msg

    def get_all_books(self) -> list:
        return self.__storage.load_books()

    def get_several_book(self, page: int, page_size: int):
        return self.__storage.load_several_books(page, page_size)

    def get_available_books(self) -> list:
        return [_book for _book in self.__storage.load_books() if not _book.get_reader_id()]

    def get_unavailable_books(self) -> list:
        return [_book for _book in self.__storage.load_books() if _book.get_reader_id()]

    def get_all_book_from_reader(self, id_reader: int) -> list:
        reader = self.__storage.load_load_reader_by_param(id=id_reader)
        if not reader:
            logprint.print_fail(f'reader with id={id_reader} is\'t registered in the library!')
            return []

        reader = reader[0]

        return reader.books

    # READERS
    ###################################################################################################
    def add_reader(self, name: str, surname: str, years: int, email: str, psw: str) -> bool:
        reader = Reader(name, surname, years, email, psw)
        if self.__storage.add_reader(reader):
            logprint.print_done(f'reader "{reader.get_name()}" registered in the library.')
            return True
        else:
            logprint.print_fail('error!')
            return False

    def get_all_readers(self) -> list:
        return self.__storage.load_readers()

    def get_reader_by_id(self, id_: int) -> Reader:
        return self.__storage.load_readers_by_id(id_)

    def get_reader_by_email(self, email: str) -> Reader:
        return self.__storage.load_readers_by_email(email)
