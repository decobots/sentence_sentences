import os

import pytest

from preparation.data_base import DataBase, Books, Lines

src_to_test_text = TEST_DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'test_data/test_text.txt')

src_to_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", 'books.db')  # pragma: no cover
test_title = "test title - + = !@#$%^&*()!№;%:?*()"
test_author = "test author 'd"


def test_db_init():
    DataBase()
    with open(src_to_db):
        pass
    os.remove(src_to_db)
    with pytest.raises(FileNotFoundError):
        open(src_to_db)


def test_db_clean(empty_database):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    test_string = 'test line - + = !@#$%^&*()!№;%:?*()'
    test_line=Lines(line=test_string, books_id=test_book.id)

    empty_database.session.add(test_book)
    empty_database.session.add(test_line)
    empty_database.session.commit()

    empty_database.clean()
    books = empty_database.session.query(Books).all()
    lines = empty_database.session.query(Lines).all()
    assert len(books) == 0
    assert len(lines) == 0


def test_clean_empty_db(empty_database):
    empty_database.clean() #test that there no errors when database clean


def test_books(empty_database):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    empty_database.session.add(test_book)
    empty_database.session.commit()

    all_books = empty_database.session.query(Books).all()
    assert len(all_books) == 1
    assert all_books[0].src == src_to_test_text
    assert all_books[0].title == test_title
    assert all_books[0].author == test_author


def test_lines(empty_database):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    empty_database.session.add(test_book)
    empty_database.session.commit()

    test_string = 'test line - + = !@#$%^&*()!№;%:?*()'
    test_line = Lines(line=test_string, books_id=test_book.id)
    empty_database.session.add(test_line)
    empty_database.session.commit()

    all_lines = empty_database.session.query(Lines).all()
    assert len(all_lines) == 1
    assert all_lines[0].line == test_string
    assert all_lines[0].books_id == test_book.id
    assert str(all_lines[0]) == test_string
    assert repr(all_lines[0]) == test_string
