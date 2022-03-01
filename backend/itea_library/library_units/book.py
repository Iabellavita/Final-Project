from ..library_storage.sqlstorage.base_class_sqlalchemy import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=True)
    reader = relationship('Reader', backref='books')

    def __init__(self, title: str, author: str, year: int, reader_id: int = None) -> None:
        self.title = title
        self.author = author
        self.year = year

        self.reader_id = reader_id

    def get_title(self) -> str:
        return self.title

    def get_author(self) -> str:
        return self.author

    def get_year(self) -> int:
        return self.year

    def get_id(self) -> int:
        return self.id

    def get_reader_id(self) -> int:
        return self.reader_id

    def set_reader_id(self, _reader_id: int) -> None:
        self.reader_id = _reader_id

    def __str__(self):
        return f'{self.id}) "{self.title}". {self.author}, {self.year}.'

    def copy(self, obj_book):
        self.id = obj_book.id
        self.title = obj_book.title
        self.author = obj_book.author
        self.year = obj_book.year
        self.reader_id = obj_book.reader_id
