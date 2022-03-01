from ..library_storage.sqlstorage.base_class_sqlalchemy import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Reader(Base, UserMixin):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    surname = Column(String, unique=False, nullable=False)
    years = Column(Integer, unique=False, nullable=False)

    # FOR REGISTRATION
    email = Column(String, unique=True, nullable=False)
    psw_hash = Column(String, unique=True, nullable=False)

    def __init__(self, name: str, surname: str, years: int, email: str, psw: str) -> None:
        self.name = name
        self.surname = surname
        self.years = years

        # FOR REGISTRATION
        self.email = email
        self.psw_hash = generate_password_hash(psw)

    def get_name(self) -> str:
        return self.name

    def get_surname(self) -> str:
        return self.surname

    def get_years(self) -> int:
        return self.years

    def get_id(self) -> int:
        return self.id

    # FOR REGISTRATION
    def check_psw(self, psw: str):
        return check_password_hash(self.psw_hash, psw)

    def __str__(self):
        return f'{self.id}) {self.name} {self.surname}, {self.years}.'

    def copy(self, obj_reader):
        self.id = obj_reader.id
        self.name = obj_reader.name
        self.surname = obj_reader.surname
        self.years = obj_reader.years
