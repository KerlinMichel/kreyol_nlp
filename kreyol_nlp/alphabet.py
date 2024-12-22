KREYÒL_ALPHABET = [
    'a', 'an', 'b', 'ch', 'd', 'e', 'è', 'en',
    'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'ng', 'o', 'ò', 'on', 'ou', 'oun', 'p',
    'r', 's', 't', 'ui', 'v', 'w', 'y', 'z',
]

KREYÒL_UNIGRAPH_ALPHABET = [
    'a', 'b', 'c', 'd', 'e', 'è', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'ò', 'p', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z'
]

def encode_alphabet_multigraphs(alphabet: list, prefix: str='<', postfix: str='>'):
    return [grapheme if len(grapheme) == 1 else f"{prefix}{grapheme}{postfix}"
            for grapheme in alphabet]

KREYÒL_ALPHABET_WITH_ENCODED_MULTIGRAPHS = encode_alphabet_multigraphs(KREYÒL_ALPHABET)