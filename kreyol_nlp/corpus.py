import os
import requests
import unicodedata
from urllib.parse import urlparse


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

class Corpus():
    def __init__(self,
                 name,
                 src,
                 license_src,
                 use_corpus_cache:bool=True,
                 corrected_spellings:dict={}): # corrected_spellings {mispelled => correct spelling}
        self.corpus_text = Corpus.handle_src(src, name, use_corpus_cache, 'txt')
        self.license = Corpus.handle_src(license_src, name, use_corpus_cache, 'LICENSE')
        self.corrected_spellings = corrected_spellings

    @staticmethod
    def handle_src(src, name, use_corpus_cache: bool, copus_cache_file_extension: str):
        corpus_cache_file_path = f'corpuses/{name}.{copus_cache_file_extension}'
        # TODO: using __file__ is bad practice
        corpus_cache_full_file_path = os.path.join(os.path.dirname(__file__), corpus_cache_file_path)

        if use_corpus_cache and os.path.exists(corpus_cache_full_file_path):
            with open(corpus_cache_full_file_path, 'r') as corpus_cache_file:
                return corpus_cache_file.read()

        if type(src) is str and urlparse(src).scheme.lower() in ['http', 'https']:
            response = requests.get(src)
            response.raise_for_status()
            if use_corpus_cache and not os.path.exists(corpus_cache_full_file_path):
                with open(corpus_cache_full_file_path, 'wb+') as corpus_cache_file:
                    corpus_cache_file.write(requests.get(src).content)
            return requests.get(src).content

# TODO: using __file__ is bad practice
KREYÒL_MO_CORPUS = WordCorpus(os.path.join(os.path.dirname(__file__), 'mo.txt'))

CMU_SPEECH_CORPUS = Corpus(
    name='Carnegie_Mellon_Haitian_Creole_Speech_data',
    src='http://www.speech.cs.cmu.edu/haitian/speech/data/cmu_haitian_speech/etc/txt.done.data',
    license_src='http://www.speech.cs.cmu.edu/haitian/speech/data/cmu_haitian_speech/COPYING',
    corrected_spellings = {
        'kontitisyon': 'konstitisyon',
        'kriminèlyo': 'kriminèl yo',
        'lapriyèy': 'lapriyè y',
        'noulo': 'nouvo',
        'pendan': 'pandan'
    }
)

CMU_SPEECH_2_CORPUS = Corpus(
    name='Carnegie_Mellon_Haitian_Creole_Speech_data_2',
    src='http://www.speech.cs.cmu.edu/haitian/speech/data2/cmu_haitian_speech2/etc/txt.done.data',
    license_src='http://www.speech.cs.cmu.edu/haitian/speech/data2/cmu_haitian_speech2/COPYING'
)

CMU_MEDICAL_TEXT_CORPUS = Corpus(
    name='Carnegie_Mellon_Haitian_Creole_Medical_text_data',
    src='http://www.speech.cs.cmu.edu/haitian/text/1600_medical_domain_sentences.ht',
    license_src='http://www.speech.cs.cmu.edu/haitian/text/COPYING'
)

CMU_NEWSWIRE_TEXT_CORPUS = Corpus(
    name='Carnegie_Mellon_Haitian_Creole_Newswire_text_data',
    src='http://www.speech.cs.cmu.edu/haitian/text/newswire-all.ht',
    license_src='http://www.speech.cs.cmu.edu/haitian/text/COPYING'
)

CMU_GLOSSARY_TEXT_CORPUS = Corpus(
    name='Carnegie_Mellon_Haitian_Creole_Newswire_text_data',
    src='http://www.speech.cs.cmu.edu/haitian/text/glossary-all-fix.ht',
    license_src='http://www.speech.cs.cmu.edu/haitian/text/COPYING'
)