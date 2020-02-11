import os  # pragma: no cover

from preparation.data_base import DataBase  # pragma: no cover
from preparation.import_text_to_db import import_book_to_db  # pragma: no cover

if __name__ == '__main__':  # pragma: no cover
    src = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'src', 'GranatoviyBraslet.txt')  # pragma: no cover
    db = DataBase()  # pragma: no cover
    ss = db.session  # pragma: no cover
    import_book_to_db(ss=ss, src=src)  # pragma: no cover
