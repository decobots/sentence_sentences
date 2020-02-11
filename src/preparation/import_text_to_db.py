import re

from preparation.data_base import Books, Lines, Words
from sqlalchemy.exc import IntegrityError

tabulation_pattern = re.compile(r'[\t\n\r]*')
space_pattern = re.compile(r'\s')
end_of_line_plus_emptyness_after = re.compile(r"([\.;?!])[\t\n\r\s]*")


def process_book(session, src, author='', title=''):
    book = Books(src=src, title=title, author=author)

    session.add(book)
    session.commit()
    return book


def process_lines(session, book: Books):
    with open(book.src, encoding='utf-8') as f:
        text = f.read()

        text = clean_tabulation(text)

        sentences = end_of_line_plus_emptyness_after.split(text)
        new_sentences = []
        for i in range(len(sentences) - 1):
            if i % 2 == 1:
                new_sentences.append(clean_spaces(sentences[i]))
            else:
                new_sentences.append(sentences[i])

        sentences = clay(new_sentences)
        for s in sentences:
            line = Lines(line=s, books_id=book.id)
            session.add(line)
        session.commit()


def process_words(session, book: Books):
    lines = session.query(Lines).filter(Lines.books_id == book.id).all()
    for line in lines:
        pattern = r"\s"
        words = re.split(pattern, line.line)

        for word in words:
            w = Words(word=word, lines_id=line.id)
            session.add(w)
        session.commit()


def clean_tabulation(text):
    # delete different types of linebreackers.
    return tabulation_pattern.sub(repl=r'', string=text)


def clean_spaces(text):
    return space_pattern.sub(repl=r'', string=text)


def clay(lines):
    # connect ending symbol to the body of line
    result = []
    for i in range(len(lines) - 1):
        if not i % 2:
            result.append(lines[i] + lines[i + 1])
    return result


def import_book_to_db(ss, src):
    try:
        book = process_book(session=ss, src=src)
    except IntegrityError:
        print('Book already added')
        return
    process_lines(book=book, session=ss)
    process_words(book=book, session=ss)
