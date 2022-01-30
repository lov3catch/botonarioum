from __future__ import annotations
from html.parser import HTMLParser

import random


class QuoteParser(HTMLParser):
    container: list[str] = []
    acc = ''
    detect = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if 'div' == tag:
            if ('class', 'quote__body') in attrs:
                self.detect = 1

    def handle_data(self, data: str) -> None:
        if self.detect == 1:
            self.acc += data
        if self.acc and self.detect == 0:
            self.container.append(self.acc)
            self.acc = ''

    def handle_endtag(self, tag: str) -> None:
        if 'div' == tag:
            self.detect = 0

    def random(self) -> str:
        return random.choice(self.container[1:25])

    def selected(self, index: int) -> str:
        if 1 <= index <= 25:
            return self.container[index].strip()
        raise Exception('Min is 1, Max is 25')


class LastPageParser(HTMLParser):
    attrs: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if 'input' == tag:
            if ('class', 'pager__input') in attrs:
                self.attrs = attrs

    def last_page(self) -> int:
        for attr in self.attrs:
            [name, value] = attr
            if 'value' == name:
                return int(value)
        raise Exception('Last page not found')


if __name__ == '__main__':
    file = open('index.html', 'r')
    lines = file.read()

    quote_parser = QuoteParser()
    quote_parser.feed(lines)
    text_should_be = '*Новость об обнаружении китайским луноходом камня, названного "нефритовым кроликом"*vanya sidorov > Да какие ещё кролики. Ясно же, что там секретный лаз в пусковую шахту, подлунной нацистской базы. И всё время пока этот китайский ровер подъезжал, они изо всех сил его закапывали и маскировали. А потом сидят такие запыхавшиеся с лопатами, и один говорит «Ганс, пометь сверху камнем, а то сами потом не найдём».'
    assert quote_parser.selected(7) == text_should_be

    last_page_parser = LastPageParser()
    last_page_parser.feed(lines)
    last_page_should_be = 3459
    assert last_page_parser.last_page() == last_page_should_be

