import unicodedata

from kreyol_nlp.corpus.utils import handle_corpus_src


class Corpus():
    def __init__(self,
                 name,
                 src,
                 license_src,
                 use_corpus_cache:bool=True,
                 corrected_spellings:dict={},
                 text_encoding='utf-8'): # corrected_spellings {mispelled => correct spelling}
        self.corpus_text = handle_corpus_src(src, name, use_corpus_cache, 'txt', text_encoding=text_encoding)
        self.license = handle_corpus_src(license_src, name, use_corpus_cache, 'LICENSE', text_encoding=text_encoding)
        self.corrected_spellings = corrected_spellings

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

class TranslationCorpus(Corpus):
    def __init__(self,
                 name,
                 src,
                 license_src,
                 languages:tuple,
                 parse_translations,
                 use_corpus_cache:bool=True,
                 corrected_spellings:dict={},
                 text_encoding='utf-8'):
        super().__init__(name, src, license_src, use_corpus_cache, corrected_spellings, text_encoding=text_encoding)
        self.languages = languages
        self.translations: tuple = parse_translations(self.corpus_text)