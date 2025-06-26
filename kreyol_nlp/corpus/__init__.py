import os
from collections import defaultdict

from kreyol_nlp.corpus.corpus_types import Corpus, TranslationCorpus, WordCorpus
from kreyol_nlp.corpus.utils import handle_corpus_src, parse_group_lines, _CORPUS_CACHE_DIR
from kreyol_nlp.pos import SINGULAR_DEFINITE_ARTICLES


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

def load_Jean_Raphael_HaitianCreole_English_dictionary():
    from pypdf import PdfReader
    import re

    pdf_url = "https://hopeforhaitischildren.org/wp-content/uploads/Haitian_Creole_English_Dictionary_2nd_printing.pdf"
    try:
        handle_corpus_src(
            pdf_url,
            "Jean_Raphael_HaitianCreole_English_dictionary",
            True,
            "pdf",
        )
    except UnicodeDecodeError:
        # ignore parsing error, just need to download the pdf file and cache it
        pass

    _HAITIAN_CREOLE_DICTIONARY_START_PAGE = 11
    _HAITIAN_CREOLE_DICTIONARY_END_PAGE = 218

    KREYÒL_TO_ENGLISH_DICTIONARY = defaultdict(list)

    pdf_file_path = os.path.join(_CORPUS_CACHE_DIR, "Jean_Raphael_HaitianCreole_English_dictionary.pdf")

    POS_ABVS_MAP_IN_DICTIONARY = {
        "n": "noun",
        "v marker": "verb_marker",
        "def art": "definite_article",
        "prep": "preposition",
        "conj": "conjunction",
        "interj": "interjection",
        "vt": "transitive_verb",
        "attrib": "attributive",
        "adv": "adverb",
        "vi": "intransitive_verb",
        "vpr": "pronominal_verb",
        "indef pron": "indefinite_pronoun",
        "indef adj": "indefinite_adjective",
        "num": "numeral",
        "aux v": "auxiliary_verb",
        "pers pron": "personal_pronoun",
        "interrog adj": "interrogative_adjective",
        "adj": "adjective",
        "v": "verb",
        "indef art": "indefinite_article",
        "rel pron": "relative_pronoun",
        "demons pron": "demonstrative_pronoun",
        "demons adj": "demonstrative_adjective",
    }

    MALFORMED_POS_ABVS_MAP = {
        "prep  ’": "preposition",
        "attrib.": "attributive",
        "Interj": "interjection",
        "interrog pron": "interrogative_pronoun",
        "v i": "intransitive_verb",
        "v t": "transitive_verb",
        "adv.": "adverb",
        "prep  ’": "preposition",
        "poss adj": "possessive_adjective",
        "Adj": "adjective",
        "(adv)": "adverb",
        "(onom)": "onomatopoeia",
        "(vpr)": "pronominal_verb",
    }

    # these are inferred and not well described in the dictionary
    POS_ABVS_MAP_NOT_IN_DICTIONARY_ABVS_LIST = {
        "prep phr": "preposition_phrase",
        "pron": "pronoun",
        "conj phr": "conjunction_phrase",
        "interrog adv": "interrogative_adverb",
        "def  art plur": "definite_article_plural",
        "impers v": "impersonal_verb",
        "def art sing": "definite_article_singular",
        "demons adj sing": "demonstrative_adjective_singular",
        "demons pron sing": "demonstrative_pronoun_singular",
        "demons adj plur": "demonstrative_adjective_plural",
        "demons pron plur": "demonstrative_pronoun_plural",
        "def art plur": "definite_article_plural",
        "refl v": "reflexive_verb",
        "refl": "reflexive_verb",
    }

    POS_ABVS_MAP = {**POS_ABVS_MAP_IN_DICTIONARY, **MALFORMED_POS_ABVS_MAP, **POS_ABVS_MAP_NOT_IN_DICTIONARY_ABVS_LIST}

    global dictionary_entries_pdf_text_parts
    # [[{"text": str, "font": str}, ...], ...]
    dictionary_entries_pdf_text_parts = []

    def _load_haitian_creole_english_translation():
        reader = PdfReader(pdf_file_path)

        def visitor_body(text: str, cm, tm, font_dict, font_size):
            global dictionary_entries_pdf_text_parts

            # Kreyòl dictionary word entries are bolded
            if font_dict and font_dict['/BaseFont'] == "/GGEPPD+NewBaskerville-Bold":
                # Kreyòl dictionary word entries are aligned at 72.0, 315.0
                if tm[4] in [72.0, 315.0]:
                   dictionary_entries_pdf_text_parts.append([{
                        "text": text,
                        "font": font_dict['/BaseFont'],
                    }])
            else:
                if dictionary_entries_pdf_text_parts:
                    dictionary_entries_pdf_text_parts[-1].append({
                        "text": text,
                        "font": font_dict['/BaseFont'] if font_dict != None else None,
                    })

        for page_i in range(_HAITIAN_CREOLE_DICTIONARY_START_PAGE, _HAITIAN_CREOLE_DICTIONARY_END_PAGE+1):
            page = reader.pages[page_i]
            page.extract_text(visitor_text=visitor_body)

    _load_haitian_creole_english_translation()

    # [{"words": [str], "pos": str?, "alt_pos": str?, "definition_text": str?, "examples": [str], "words_dialects": ["north" | "south" | None]}, "phrase_usage": str?]
    dictionary_entries = []
    for dictionary_entry_pdf_text_parts in dictionary_entries_pdf_text_parts:
        assert dictionary_entry_pdf_text_parts[0]["font"] == "/GGEPPD+NewBaskerville-Bold"
        dictionary_entry = {
            "words": [],
            "pos": None,
            "definition_text": "",
            "examples": [],
            "words_dialects": [],
            "phrase_usage": None,
        }

        text_entry_parts = dictionary_entry_pdf_text_parts[0]["text"].split(",")
        text_entry_parts = list(map(str.strip, text_entry_parts))

        dictionary_entry["words_dialects"] = [None] * len(text_entry_parts)

        for i in range(len(text_entry_parts)):
            # TODO: handle parsing all dialect cases. Some dialect info is all stored in the defintion
            if "(North)" in text_entry_parts[i]:
                text_entry_parts[i].replace("(North)", "")
                dictionary_entry["words_dialects"][i] = "north"

        dictionary_entry["words"] = text_entry_parts

        # Dictionary entry words and then...
        # 0: pos tag | ' V ' see other entry marker | definition text | used in phrase
        # 1: pos tag | definition text | used in phrase
        # 2: definition text | used in phrase | alt pos tag
        # n: TODO handle collecting rest of definition text

        # remove text parts that is just whitespace
        dictionary_entry_pdf_text_parts = list(filter(lambda tp: not tp["text"].isspace(), dictionary_entry_pdf_text_parts))
        # remove text parts that are empty strings
        dictionary_entry_pdf_text_parts = list(filter(lambda tp: tp["text"], dictionary_entry_pdf_text_parts))
        # remove header text which uses "/GGEPMO+Optima" font
        dictionary_entry_pdf_text_parts = list(filter(lambda tp: not tp["font"] == "/GGEPMO+Optima", dictionary_entry_pdf_text_parts))
        # remove text that is just a period
        dictionary_entry_pdf_text_parts = list(filter(lambda tp: not tp["text"] == ".", dictionary_entry_pdf_text_parts))
        # remove homograph index
        if (len(dictionary_entry_pdf_text_parts) > 1 and dictionary_entry_pdf_text_parts[1]["text"].strip().isdigit()):
                del dictionary_entry_pdf_text_parts[1]
                # merge the text that was between the homograph index if they have the same font
                # TODO: look into this. seems like the merge code never runs
                if dictionary_entry_pdf_text_parts[0]["font"] == dictionary_entry_pdf_text_parts[1]["font"]:
                    dictionary_entry_pdf_text_parts[0]["text"] += dictionary_entry_pdf_text_parts[1]["text"]
                    del dictionary_entry_pdf_text_parts[1]

        for i, dictionary_entry_pdf_text_part in enumerate(dictionary_entry_pdf_text_parts[1:]):
            if i == 0:
                # pos tag
                if dictionary_entry_pdf_text_part["text"].strip() in POS_ABVS_MAP:
                    dictionary_entry["pos"] = POS_ABVS_MAP[dictionary_entry_pdf_text_part["text"].strip()]
                elif all(text.strip() in POS_ABVS_MAP for text in dictionary_entry_pdf_text_part["text"].strip().split("&")):
                    pos_s = dictionary_entry_pdf_text_part["text"].strip().split("&")
                    dictionary_entry["pos"] = POS_ABVS_MAP[pos_s[0].strip()]
                    dictionary_entry["alt_pos"] = POS_ABVS_MAP[pos_s[1].strip()]
                elif all(text.strip() in POS_ABVS_MAP for text in dictionary_entry_pdf_text_part["text"].strip().split(",")):
                    pos_s = dictionary_entry_pdf_text_part["text"].strip().split(",")
                    dictionary_entry["pos"] = POS_ABVS_MAP[pos_s[0].strip()]
                    dictionary_entry["alt_pos"] = POS_ABVS_MAP[pos_s[1].strip()]

                # ' V ' see other entry marker
                elif re.match(r"^\s*V\s*$", dictionary_entry_pdf_text_part["text"]):
                    pass # TODO: handle see other entry entries

                # definition text
                elif dictionary_entry_pdf_text_part["font"] == "/GGEPPB+NewBaskerville-Roman":
                    dictionary_entry["definition_text"] += dictionary_entry_pdf_text_part["text"]
                elif dictionary_entry_pdf_text_part['text'] == "n  Excitement, agitation":
                    # the english translation of "ajitasyon an" is malformed by using wrong font
                    dictionary_entry["pos"] = POS_ABVS_MAP["n"]
                    dictionary_entry["definition_text"] += "Excitement, agitation*."
                    # TODO: mark as same word origin as English translation
                elif dictionary_entry_pdf_text_part['text'] == "n  Hula hoop":
                    # the english translation of "woulawoup la" is malformed by using wrong font
                    dictionary_entry["pos"] = POS_ABVS_MAP["n"]
                    dictionary_entry["definition_text"] += "Hula hoop"
                    # TODO: mark as same word origin as English translation

                # used in phrase
                elif dictionary_entry_pdf_text_part["font"] == "/GGFAAI+NewBaskerville-BoldItalic" :
                    dictionary_entry["phrase_usage"] = dictionary_entry_pdf_text_part["text"].strip()
                else:
                    raise NameError(f"{dictionary_entry_pdf_text_parts}")

            elif i == 1:
                # pos tag
                if dictionary_entry_pdf_text_part["text"].strip() in POS_ABVS_MAP:
                    dictionary_entry["pos"] = POS_ABVS_MAP[dictionary_entry_pdf_text_part["text"].strip()]
                elif all(text.strip() in POS_ABVS_MAP for text in dictionary_entry_pdf_text_part["text"].strip().split("&")):
                    pos_s = dictionary_entry_pdf_text_part["text"].strip().split("&")
                    dictionary_entry["pos"] = POS_ABVS_MAP[pos_s[0].strip()]
                    dictionary_entry["alt_pos"] = POS_ABVS_MAP[pos_s[1].strip()]
                elif all(text.strip() in POS_ABVS_MAP for text in dictionary_entry_pdf_text_part["text"].strip().split(",")):
                    pos_s = dictionary_entry_pdf_text_part["text"].strip().split(",")
                    dictionary_entry["pos"] = POS_ABVS_MAP[pos_s[0].strip()]
                    dictionary_entry["alt_pos"] = POS_ABVS_MAP[pos_s[1].strip()]

                # definition text
                elif dictionary_entry_pdf_text_part["font"] == "/GGEPPB+NewBaskerville-Roman":
                    dictionary_entry["definition_text"] += dictionary_entry_pdf_text_part["text"]
                elif dictionary_entry["phrase_usage"] and dictionary_entry_pdf_text_part["font"] == "/GGEPPF+NewBaskerville-Italic":
                    # for "phrasal" words the english definition in sometimes or always in italics after the phrase
                    dictionary_entry["definition_text"] += dictionary_entry_pdf_text_part["text"]
                elif dictionary_entry_pdf_text_part["text"] == "the hell!’":
                    # special case
                    # TODO: mark as having same word origin as English translation
                    dictionary_entry["definition_text"] += dictionary_entry_pdf_text_part["text"]

                # used in phrase
                elif dictionary_entry_pdf_text_part["font"] == "/GGFAAI+NewBaskerville-BoldItalic":
                    dictionary_entry["phrase_usage"] = dictionary_entry_pdf_text_part["text"].strip()

            elif i == 2:
                # definition text
                if dictionary_entry_pdf_text_part["font"] == "/GGEPPB+NewBaskerville-Roman":
                    dictionary_entry["definition_text"] += dictionary_entry_pdf_text_part["text"]
                elif dictionary_entry_pdf_text_part["font"] == "/GGFAAI+NewBaskerville-BoldItalic":
                    dictionary_entry["phrase_usage"] = dictionary_entry_pdf_text_part["text"].strip()
                elif dictionary_entry["phrase_usage"] != None and dictionary_entry_pdf_text_part["font"] == "/GGEPPF+NewBaskerville-Italic":
                    # "phrasal" words' definitions are in italics
                    dictionary_entry["definition_text"] += dictionary_entry_pdf_text_part["text"]
                elif dictionary_entry_pdf_text_part["text"] == "To speak in parables.":
                    dictionary_entry["definition_text"] += dictionary_entry_pdf_text_part["text"]

                # alt pos
                elif dictionary_entry_pdf_text_part["text"].strip() in POS_ABVS_MAP:
                    dictionary_entry["alt_pos"] = POS_ABVS_MAP[dictionary_entry_pdf_text_part["text"].strip()]

        dictionary_entries.append(dictionary_entry)

    # parse definition text
    definition_delimiters = r"[;,]"
    for dictionary_entry in dictionary_entries:
        dictionary_entry["defintions"] = re.split(definition_delimiters, dictionary_entry["definition_text"])

    for dictionary_entry in dictionary_entries:
        for word_or_phrase in dictionary_entry["words"]:
            word_or_phrase = word_or_phrase.split()

            definitions = dictionary_entry["defintions"]

            # clean definition text
            for def_i in range(len(definitions)):
                definitions[def_i] = "".join(char for char in definitions[def_i] if char.isalpha() or char.isspace())
                definitions[def_i] = definitions[def_i].replace("\n", " ")
                definitions[def_i] = definitions[def_i].strip()

            if len(word_or_phrase) == 1:
                KREYÒL_TO_ENGLISH_DICTIONARY[word_or_phrase[0]] += definitions
            elif len(word_or_phrase) == 2 and word_or_phrase[1] in SINGULAR_DEFINITE_ARTICLES:
                KREYÒL_TO_ENGLISH_DICTIONARY[word_or_phrase[0]] += definitions
            else: # TODO: handle all dictionary_entries cases
                pass

    return {
        "dictionary_entries": dictionary_entries,
        "english_translations": KREYÒL_TO_ENGLISH_DICTIONARY
    }