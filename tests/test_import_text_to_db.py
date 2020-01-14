import os

from preparation.data_base import Books, Lines, Words
from preparation.import_text_to_db import process_lines, clean_tabulation, clay, clean_spaces, \
    process_words

src_to_test_text = TEST_DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'test_data/test_text.txt')

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


def test_process_lines(empty_table):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    empty_table.session.add(test_book)
    empty_table.session.commit()
    process_lines(book=test_book, session=empty_table.session)
    all_lines = empty_table.session.query(Lines).all()
    assert len(all_lines) == 17
    assert all_lines[
               0].line == "В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные погоды, какие так свойственны северному побережью Черного моря."
    # assert all_lines[16] == "И теперь она очень радовалась наступившим прелестным дням, тишине, уединению, чистому воздуху, щебетанью на телеграфных проволоках ласточек, стаившихся к отлету, и ласковому соленому ветерку, слабо тянувшему с моря."
    assert len(empty_table.session.query(Lines).filter(Lines.books_id == 1).all()) == 17


def test_process_words(empty_table):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    empty_table.session.add(test_book)
    empty_table.session.commit()

    process_lines(book=test_book, session=empty_table.session)
    process_words(book=test_book, session=empty_table.session)
    all_words = empty_table.session.query(Words).all()
    assert len(all_words) == 377
    assert all_words[376].word == "моря."
    assert len(empty_table.session.query(Words).filter(Words.lines_id == 1).all()) == 18

# def iesi_import_book_to_database(empty_table):
#     import_book_to_db(ss=empty_table.session, src=src_to_test_text)
#
#     all_books = empty_table.session.query(Books).all()
#     assert len(all_books) == 1
#
#     all_lines = empty_table.session.query(Lines).all()
#     assert len(all_lines) == 17
#     assert all_lines[
#                0].line == "В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные погоды, какие так свойственны северному побережью Черного моря."
#     assert len(empty_table.session.query(Lines).filter(Lines.books_id == 1).all()) == 17
