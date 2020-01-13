from preparation.data_base import DataBase
from preparation.import_text_to_db import import_book_to_db

if __name__ == '__main__':
    src = 'src/GranatoviyBraslet.txt'
    db = DataBase('books')
    ss = db.session
    import_book_to_db(ss=ss, src=src)
