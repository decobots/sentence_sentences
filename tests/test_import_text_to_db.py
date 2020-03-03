import os

from preparation.data_base import Books, Lines
from preparation.import_text_to_db import process_lines, clean_tabulation, clay, clean_spaces, import_book_to_db, \
    process_book

src_to_test_text = TEST_DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'test_data/test_text.json')

test_db_name = 'test_db'
test_title = "test title - + = !@#$%^&*()!№;%:?*()"
test_author = "test author '"
db_name_with_extension = f"{test_db_name}.db"


def test_clean_tabulation():
    # mix of spaces, tabs, eols
    text = ''' я помню чудное мгновение передо мной.   ты '''
    assert clean_tabulation(text) == ' я помню чудное мгновение передо мной.   ты '

    text2 = ''' я помню чудное мгновение 	передо мной \r'''
    assert clean_tabulation(text2) == ' я помню чудное мгновение передо мной '
    text3 = '''\n
     я помню чудное мгновение 
	передо мной \r'''
    assert clean_tabulation(text3) == '''     я помню чудное мгновение передо мной '''


def test_clean_spaces():
    text = '''12ddgsdg'''
    assert clean_spaces(text) == text

    text2 = ''' '''
    assert clean_spaces(text2) == ''
    text3 = 'lksgdrahg safjoisjg 452n .rgasg\n dfdfs dfg'
    assert clean_spaces(text3) == 'lksgdrahgsafjoisjg452n.rgasgdfdfsdfg'


def test_clay():
    lines = ["sentence 1", '.', ' sentence 2', '[', 'sentence 3', '!']
    assert clay(lines) == ['sentence 1.', ' sentence 2[', 'sentence 3!']


def test_process_book(empty_database):
    process_book(session=empty_database.session, src=src_to_test_text)
    all_books = empty_database.session.query(Books).all()
    assert len(all_books) == 1
    assert all_books[0].src == src_to_test_text
    assert all_books[0].author == 'Александр Иванович Куприн.'
    assert all_books[0].title == 'Гранатовый Браслет.'
    assert all_books[0].lang == 'RU'


def test_process_lines(empty_database):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    empty_database.session.add(test_book)
    empty_database.session.commit()
    process_lines(book=test_book, session=empty_database.session)
    all_lines = empty_database.session.query(Lines).all()
    assert len(all_lines) == 17
    assert all_lines[0].line == "В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные " \
                                "погоды, какие так свойственны северному побережью Черного моря."
    assert all_lines[0].length == len(all_lines[0].line)
    assert len(empty_database.session.query(Lines).filter(Lines.books_id == 1).all()) == 17


def test_import_book_to_database(empty_database):
    import_book_to_db(ss=empty_database.session, src=src_to_test_text)

    all_books = empty_database.session.query(Books).all()
    assert len(all_books) == 1

    all_lines = empty_database.session.query(Lines).all()
    assert len(all_lines) == 17
    assert all_lines[0].line == "В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные " \
                                "погоды, какие так свойственны северному побережью Черного моря."
    assert len(empty_database.session.query(Lines).filter(Lines.books_id == 1).all()) == 17


def test_import_dblicate_of_book_to_database(empty_database, capfd):
    import_book_to_db(ss=empty_database.session, src=src_to_test_text)
    import_book_to_db(ss=empty_database.session, src=src_to_test_text)
    out, err = capfd.readouterr()
    assert out == 'Book already added\n'
