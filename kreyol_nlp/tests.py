import unittest

from kreyol_nlp import process_ng_as_unigraphs_or_digraph

class TextProcessing(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()