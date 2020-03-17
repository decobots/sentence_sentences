import json
import re

from sqlalchemy.orm.session import Session  as AlchemySession

from preparation.data_base import Books, Lines
from sqlalchemy.exc import IntegrityError

tabulation_pattern = re.compile(r'[\t\n\r]*')
space_pattern = re.compile(r'\s')
end_of_line_plus_emptyness_after = re.compile(r"([\.;?!])[\t\n\r\s]*")


def process_book(session: AlchemySession, src: str) -> Books:
    with open(src, encoding='utf-8') as f:
        data = json.load(f)
        author = data['author']
        title = data['title']
        lang = data['language']
        book = Books(src=src, title=title, author=author, lang=lang)

        session.add(book)
        session.commit()
    return book


def process_lines(session: AlchemySession, book: Books):
    with open(book.src, encoding='utf-8') as f:
        data = json.load(f)
        text = data['text']

        text = clean_tabulation(text)

        sentences = end_of_line_plus_emptyness_after.split(text)
        new_sentences = []
        for i in range(len(sentences) - 1):
            if i % 2 == 1:
                new_sentences.append(clean_spaces(sentences[i]))
            else:
                new_sentences.append(sentences[i])

        sentences = clay(new_sentences)
        # skip author etc lines
        for s in sentences:
            line = Lines(line=s, books_id=book.id, length=len(s))
            session.add(line)
        session.commit()


def clean_tabulation(text: str) -> str:
    # delete different types of linebreackers.
    return tabulation_pattern.sub(repl=r'', string=text)


def clean_spaces(text: str) -> str:
    return space_pattern.sub(repl=r'', string=text)


def clay(lines: list) -> list:
    # connect ending symbol to the body of line
    result = []
    for i in range(len(lines) - 1):
        if not i % 2:
            result.append(lines[i] + lines[i + 1])
    return result


def import_book_to_db(ss: AlchemySession, src: str):
    try:
        book = process_book(session=ss, src=src)
    except IntegrityError:
        print('Book already added')
        return
    process_lines(book=book, session=ss)
