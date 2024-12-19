import os
import unicodedata


class WordCorpus():
    def __init__(self, corpus_file_path: str):
        self.words = set()
        with open(corpus_file_path) as corpus_file:
            for word in corpus_file.readlines():
                word = word.strip() # remove new line char
                if word in self.words:
                    raise ValueError(f'{word} is found multiple times in corpus')
                else:
                    self.words.add(word)
    
    def add_word(self, word: str):
        self.words.add(word)
    
    def save_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            file.write('\n'.join(sorted(self.words, key=lambda word: unicodedata.normalize('NFKD', word))))

# TODO: using __file__ is bad practice
KREYÒL_MO_CORPUS = WordCorpus(os.path.join(os.path.dirname(__file__), 'mo.txt'))