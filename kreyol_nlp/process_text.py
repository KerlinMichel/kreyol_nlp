import re
import unicodedata


def _get_unicode_letters(n: int) -> list:
    alpha_chars = []
    for codepoint in range(0x110000):  # Iterate through all Unicode code points
        char = chr(codepoint)
        # Check if the character is a letter
        if unicodedata.category(char).startswith('L'):
            alpha_chars.append(char)
        if len(alpha_chars) >= n:
            break
    return alpha_chars

_FIRST_256_UNICODE_LETTERS = _get_unicode_letters(256)

# TODO: Source?
# TODO: This only supports lowercase
# àn has à and à is not part of the standard alpabet but has the same sound as
# a. à is always followed by n. Is rare
def process_àn_to_an(text: str):
    return text.replace('àn', 'an')

# TODO: Source?
# TODO: This only supports lowercase
# 'ng' is usually treated as two unigraphs <n> and <g>.
# But in some rare cases words like 'bilding' use the digraph <ng>.
# This seems to only be seen in English loan words in Kreyòl that end in 'ing'.
# Seems that words that end in 'ing' in Kreyòl are always English load words.
def process_ng_as_unigraphs_or_digraph(text: str,
                                       digraph_encode_prefix: str = '<',
                                       digraph_encode_postfix: str = '>',
                                       letters_in_text: str = ''.join(_FIRST_256_UNICODE_LETTERS)):
    # If text contains letters that are not in _FIRST_256_UNICODE_LETTERS then
    # change letters_in_text variable so text is processed correctly. 
    # _FIRST_256_UNICODE_LETTERS should handle most cases
    ing_word_ending_regex = rf"ing([^{letters_in_text}]|$)"
    replace_fn = lambda m: f'i{digraph_encode_prefix}ng{digraph_encode_postfix}' + m.groups()[0]
    return re.sub(ing_word_ending_regex, replace_fn, text)

def remove_comma_punctuation(text: str):
    return text.replace(', ', ' ')

def remove_sentence_ending_punctuation(text: str,
                                       punctuations: str = '.?!:;',
                                       letters_in_text: str = ''.join(_FIRST_256_UNICODE_LETTERS)):
    # Replaces {letter}{punctuation}{whitespace or string end} with {letter}{whitespace or string end}
    punctuations = re.escape(punctuations)
    replace_fn = lambda m: m.groups()[0] + m.groups()[1]
    return re.sub(rf"([{letters_in_text}]){[punctuations]}(\s|$)", replace_fn, text)

def remove_integer_decimal_separator(text: str,
                             decimal_separators = ','):
    decimal_separators = re.escape(decimal_separators)
    replace_fn = lambda m: ''.join([c for c in m.group() if c.isdecimal()])
    return re.sub(rf"[\d{decimal_separators}]+", replace_fn, text)

def remove_hyphens(text: str):
    return text.replace('-', ' ')

NUMBER_PATTERN = re.compile(r"\d([\d,.]*)")

# TODO: Ugly, Nasty, Dirty, low life code
# Can't tell the difference between decimal separator and punctuations in sentence
def process_numbers(text: str,):
    def infer_number(m):
        number_word = m.group().strip()
        if all(c.isdecimal() for c in number_word):
            return m.group()
        else:
            number_parts = []
            collecting_digits = []

            for c in number_word:
                if c.isdecimal():
                    collecting_digits.append(c)
                if c in ['.', ',']:
                    if collecting_digits == []:
                        raise Exception(f'Unable to handle repeating decimal separator: {m.group()}')
                    number_parts.append((collecting_digits, c))
                    collecting_digits = []

            if collecting_digits:
                number_parts.append((collecting_digits, None))
                collecting_digits = []

            if len(number_parts) == 1:
                return ''.join(number_parts[0][0])
            if len(number_parts) == 2 and len(number_parts[1][0]):
                return ''.join(number_parts[0][0] + number_parts[1][0])
            raise Exception(f'Unable to handle: {m.group()}')
    return re.sub(NUMBER_PATTERN, infer_number, text)