import re
from itertools import cycle
from typing import Match, List

from bs4 import BeautifulSoup, Tag, NavigableString


class PageContentFilter:
    def __init__(self, *, emojis: List[str], word_length: int) -> None:
        self._emoji_adder = EmojiAdder(emojis=emojis, word_length=word_length)

    def add_emojis_to_article(self, content: bytes) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        article = soup.find('article')
        if article is None:
            return str(soup)
        for child in article.contents:
            if child.string is None:
                self._recursively_add_emoji(child)
            else:
                child.string = self._emoji_adder.add_emoji(child.string)
        return str(soup)

    def _recursively_add_emoji(self, element: Tag) -> None:
        for i, item in enumerate(element.contents):
            if isinstance(item, NavigableString):
                item.replace_with(self._emoji_adder.add_emoji(item))
            else:
                self._recursively_add_emoji(item)


class EmojiAdder:
    def __init__(self, *, emojis: List[str], word_length: int) -> None:
        self._emojis = cycle(emojis)
        self._word_length = word_length
        self._word_re = re.compile(r'\b(\w{%s})\b' % self._word_length)

    def add_emoji(self, text: str) -> str:
        return self._word_re.sub(self._replace, text)

    def _replace(self, m: Match) -> str:
        word = m.group(0)
        return f'{word}{self._emoji}'

    @property
    def _emoji(self):
        return next(self._emojis)
