from kreyol_nlp.alphabet import KREYÒL_ALPHABET, KREYÒL_UNIGRAPH_ALPHABET


def wav2vec_vocab(vocab: list,
                  space_token: str = '|',
                  unknown_token:str='[UNK]',
                  pad_token:str='[PAD]') -> dict:
    special_tokens = [space_token, unknown_token, pad_token]
    return {
        grapheme: index for index, grapheme in enumerate(vocab + special_tokens)
    }

KREYÒL_WAV2VEC_VOCAB = wav2vec_vocab(KREYÒL_ALPHABET)
KREYÒL_WAV2VEC_UNIGRAM_VOCAB = wav2vec_vocab(KREYÒL_UNIGRAPH_ALPHABET)