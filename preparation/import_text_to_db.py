import re

from preparation.data_base import Books, Lines, Words


def process_lines(session, book: Books):
    with open(book.src, encoding='utf-8') as f:
        text = f.read()

        text = clean_tabulation(text)
        pattern = r"([\.;?!])[\t\n\r\s]*"
        sentences = re.split(pattern, text)
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
    # delete empty symbols between lines. Doesn't delete leading line space.
    return re.sub(pattern=r'[\t\n\r]*', repl=r'', string=text, flags=re.IGNORECASE)


def clean_spaces(text):
    return re.sub(pattern=r'\s', repl=r'', string=text, flags=re.IGNORECASE)


def clay(lines):
    # connect ending symbol to the body of line
    result = []
    for i in range(len(lines) - 1):
        if not i % 2:
            result.append(lines[i] + lines[i + 1])
    return result


def import_book_to_db(ss, src):
    book = Books(src=src, title="", author='')

    ss.add(book)
    ss.commit()
    process_lines(book=book, session=ss)
    process_words(book=book, session=ss)
