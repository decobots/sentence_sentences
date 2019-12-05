import re

from preparation.data_base import Books, Lines


def process(book, session):
    with open(book.src, encoding='utf-8') as f:
        text = f.read()
        text = clean(text)
        pattern = r"([\.;?!])"
        sentences = re.split(pattern, text)
        sentences = clay(sentences)
        for s in sentences:
            line = Lines(line=s, books_id=book.id)
            session.add(line)
        session.commit()


def clean(text):
    return re.sub(pattern=r'[\t\n\r]*', repl=r'', string=text, flags=re.IGNORECASE)


def clay(lines):
    # connect ending symbol to the body of line
    result = []
    for i in range(len(lines) - 1):
        if not i % 2:
            result.append(lines[i] + lines[i + 1])
    return result


def import_text_to_db(ss, src):
    book = Books(src=src, title="", author='')

    ss.add(book)
    ss.commit()
    process(book, ss)
