import os

import pytest

from preparation.data_base import DataBase, Books, Lines

src_to_test_text = 'test_data/test_text.txt'
test_db_name = 'test_db'
test_title = "test title - + = !@#$%^&*()!№;%:?*()"
test_author = "test author '"
db_name_with_extension = f"{test_db_name}.db"


def test_db_init():
    DataBase(test_db_name)

    try:
        with open(db_name_with_extension):
            pass
    except FileNotFoundError:
        raise

    os.remove(db_name_with_extension)
    with pytest.raises(FileNotFoundError):
        open(db_name_with_extension)


def test_books():
    test_db = DataBase(test_db_name)
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    test_db.session.add(test_book)
    test_db.session.commit()

    all_books = test_db.session.query(Books).all()
    assert len(all_books) == 1
    assert all_books[0].src == src_to_test_text
    assert all_books[0].title == test_title
    assert all_books[0].author == test_author

    test_db.session.close()
    os.remove(db_name_with_extension)


def test_lines():
    test_db = DataBase(test_db_name)
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    test_db.session.add(test_book)
    test_db.session.commit()
    book = test_db.session.query(Books).get(1)

    test_string = 'test line - + = !@#$%^&*()!№;%:?*()'
    test_line = Lines(line=test_string, books_id=book.id)
    test_db.session.add(test_line)
    test_db.session.commit()

    all_lines = test_db.session.query(Lines).all()
    assert len(all_lines) == 1
    assert all_lines[0].line == test_string
    assert all_lines[0].books_id == book.id

    test_db.session.close()
    os.remove(db_name_with_extension)
