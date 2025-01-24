import os

from kreyol_nlp.corpus.corpus_types import Corpus, TranslationCorpus, WordCorpus
from kreyol_nlp.corpus.utils import parse_group_lines


# TODO: using __file__ is bad practice
KREYÒL_MO_CORPUS = WordCorpus(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mo.txt')))

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

CMU_MEDICAL_TRANSLATION_CORPUS = TranslationCorpus(
    name='Carnegie_Mellon_Haitian_Creole_Medical_translation_text_data',
    src='http://www.speech.cs.cmu.edu/haitian/text/1600_medical_domain_sentences.txt',
    license_src='http://www.speech.cs.cmu.edu/haitian/text/COPYING',
    languages=('English', 'Kreyòl'),
    parse_translations=lambda text: parse_group_lines(text,
                                                      group_size=2,
                                                      group_separator='\n\r',
                                                      line_separator='\r'),
    text_encoding='utf-8-sig'
)