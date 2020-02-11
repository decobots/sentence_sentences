from urllib import parse

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from .environment_variables import get_env

Base = declarative_base()


class DataBase:
    session = None
    Session = None

    def __init__(self, url=None):
        url = url or get_env('DATABASE_URL')
        self.engine = create_engine(url, echo=False)
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    lines_id = Column(Integer, ForeignKey('lines.id'))

    def __repr__(self):
        return self.word


class Lines(Base):
    __tablename__ = 'lines'
    id = Column(Integer, primary_key=True)
    line = Column(String)
    books_id = Column(Integer, ForeignKey('books.id'))
    words = relationship("Words", backref="lines")

    def __repr__(self):
        return self.line


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    lines = relationship(Lines)
    src = Column(String, unique=True)
