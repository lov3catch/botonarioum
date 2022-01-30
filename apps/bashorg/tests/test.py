import unittest
from pprint import pprint

from apps.bashorg.app import LastPageParser, QuoteParser
import os


class TestBashorgParser(unittest.TestCase):

    def test_quote(self):
        filename = os.path.dirname(__file__) + '/../index.html'

        quote_parser = QuoteParser()
        with open(filename, 'r') as f:
            quote_parser.feed(f.read())

        text_should_be = '*Новость об обнаружении китайским луноходом камня, названного "нефритовым кроликом"*vanya sidorov > Да какие ещё кролики. Ясно же, что там секретный лаз в пусковую шахту, подлунной нацистской базы. И всё время пока этот китайский ровер подъезжал, они изо всех сил его закапывали и маскировали. А потом сидят такие запыхавшиеся с лопатами, и один говорит «Ганс, пометь сверху камнем, а то сами потом не найдём».'

        self.assertTrue(text_should_be == quote_parser.selected(7))

    def test_last_page(self):
        filename = os.path.dirname(__file__) + '/../index.html'

        last_page_parser = LastPageParser()
        with open(filename, 'r') as f:
            last_page_parser.feed(f.read())

        self.assertTrue(3459 == last_page_parser.last_page())