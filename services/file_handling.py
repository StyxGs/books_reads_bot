BOOK_PATH = r'book\book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    signs = (',', '.', '!', ':', ';', '?',)
    end = start + size
    if len(text) > end:
        for i in range(end, -1, -1):
            if text[i] in signs and len(text[start:i + 1]) <= size:
                if text[i - 1] not in signs and text[i + 1] not in signs:
                    return text[start:i + 1], len(text[start:i + 1])
    else:
        return text[start:], len(text[start:])


def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf8') as text:
        start = 0
        page_number = 1
        text_all_book = text.read()
        size_book = len(text_all_book)
        while start < size_book:
            page_text, page_size = _get_part_text(text_all_book, start, PAGE_SIZE)
            book[page_number] = page_text.strip()
            page_number += 1
            start += page_size


prepare_book(BOOK_PATH)
