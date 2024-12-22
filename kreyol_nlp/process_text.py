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