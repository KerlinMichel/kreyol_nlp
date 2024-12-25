import unittest

from kreyol_nlp import process_ng_as_unigraphs_or_digraph, process_numbers
from kreyol_nlp import int_to_words

class TextProcessingTest(unittest.TestCase):
    def test_process_ng_as_unigraphs_or_digraph(self):
        text_and_processed_text_target_pairs = [
            ("bilding", "bildi<ng>"),
            (" King ", " Ki<ng> "),
            (" angajman m", " angajman m"),
            ("bilding, bilding sa", "bildi<ng>, bildi<ng> sa")
        ]
        for text, processed_text_target in text_and_processed_text_target_pairs:
            processed_text = process_ng_as_unigraphs_or_digraph(text)
            self.assertEqual(processed_text, processed_text_target)

    def test_process_numbers(self):
        numbers_text_and_processed_numbers_text_target_pairs = [
            ('12 ', '12 '),
            ('gen 100,', 'gen 100'),
            (' 456.', ' 456'),
            ('33.000', '33000'),
            ('189,123', '189123')
        ]
        for numbers_text, processed_numbers_text_target in numbers_text_and_processed_numbers_text_target_pairs:
            processed_numbers_text = process_numbers(numbers_text)
            self.assertEqual(processed_numbers_text, processed_numbers_text_target)


class NumToWordsTest(unittest.TestCase):
    def test_int_to_words(self):
        integer_and_words_target_pairs = [
            (0, 'zewo'),
            (99, 'katreven-diznèf'),
            (100, 'san'),
            (1804, 'mil uit san kat'),
            (9999, 'nèf mil nèf san katreven-diznèf'),
            (555_555, 'senk san senkannsenk mil senk san senkannsenk'),
            (999_999, 'nèf san katreven-diznèf mil nèf san katreven-diznèf'),
            (1_000_000, 'en milyon'),
        ]

        for integer, words_target in integer_and_words_target_pairs:
            words = int_to_words(integer)
            self.assertEqual(words, words_target)



if __name__ == '__main__':
    unittest.main()