from preparation.import_text_to_db import process, clean, clay, import_text_to_db
from preparation.data_base import Books, Lines

src_to_test_text = 'test_data/test_text.txt'
test_db_name = 'test_db'
test_title = "test title - + = !@#$%^&*()!№;%:?*()"
test_author = "test author '"
db_name_with_extension = f"{test_db_name}.db"


def test_clean():
    # mix of spaces, tabs, eols
    text = ''' я помню чудное мгновение передо мной '''
    assert clean(text) == text

    text2 = ''' я помню чудное мгновение 	передо мной \r'''
    assert clean(text2) == ' я помню чудное мгновение передо мной '


def test_clay():
    lines = ["sentence 1", '.', ' sentence 2', '[', 'sentence 3', '!']
    assert clay(lines) == ['sentence 1.', ' sentence 2[', 'sentence 3!']


def test_process(empty_table):
    test_book = Books(src=src_to_test_text, title=test_title, author=test_author)
    empty_table.session.add(test_book)
    empty_table.session.commit()
    book = empty_table.session.query(Books).get(1)
    process(book, empty_table.session)
    all_lines = empty_table.session.query(Lines).all()
    assert len(all_lines) == 17
    assert all_lines[0].line == "В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные погоды, какие так свойственны северному побережью Черного моря."
    # assert all_lines[16] == "И теперь она очень радовалась наступившим прелестным дням, тишине, уединению, чистому воздуху, щебетанью на телеграфных проволоках ласточек, стаившихся к отлету, и ласковому соленому ветерку, слабо тянувшему с моря."
    assert len(empty_table.session.query(Lines).filter(Lines.books_id == 1).all()) == 17


def iesi_import_text_to_database(empty_table):
    import_text_to_db(ss=empty_table.session, src=src_to_test_text)

    all_books = empty_table.session.query(Books).all()
    assert len(all_books) == 1

    all_lines = empty_table.session.query(Lines).all()
    assert len(all_lines) == 17
    assert all_lines[0].line == "В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные погоды, какие так свойственны северному побережью Черного моря."
    assert len(empty_table.session.query(Lines).filter(Lines.books_id == 1).all()) == 17
