from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class DataBase:
    session = None

    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}.db', echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


class Lines(Base):
    __tablename__ = 'lines'
    id = Column(Integer, primary_key=True)
    line = Column(String)
    books_id = Column(Integer, ForeignKey('books.id'))

    def __repr__(self):
        return self.line


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    lines = relationship(Lines)
    src = Column(String, unique=True)
