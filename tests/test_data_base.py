import os

import pytest

from preparation.data_base import DataBase, Books, Lines, Words

src_to_test_text = TEST_DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'test_data/test_text.txt')

test_title = "test title - + = !@#$%^&*()!№;%:?*()"
test_author = "test author '"


def test_db_init():
    test_db_name = 'test_db'
    db_name_with_extension = f"{test_db_name}.db"
    DataBase(test_db_name)

    with open(db_name_with_extension):
        pass

    os.remove(db_name_with_extension)
    with pytest.raises(FileNotFoundError):
        open(db_name_with_extension)


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


def test_words_class(empty_database):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    empty_database.session.add(test_book)
    empty_database.session.commit()

    test_string = 'В'
    test_line = Lines(line=test_string, books_id=test_book.id)
    empty_database.session.add(test_line)
    empty_database.session.commit()

    test_words = ['В', 'середине', 'августа,', 'перед', 'рождением', 'молодого', 'месяца']
    for word in test_words:
        test_line = Words(word=word, lines_id=1)
        empty_database.session.add(test_line)
    empty_database.session.commit()
    all_words = empty_database.session.query(Words).all()
    assert len(all_words) == 7
    assert all_words[0].word == 'В'
    assert all_words[6].word == 'месяца'
    assert str(all_words[6]) == 'месяца'
