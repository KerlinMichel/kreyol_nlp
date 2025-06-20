from transformers.tokenization_utils import PreTrainedTokenizer

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

def torchaudio_ctc_decoder_lexicon(words: set[str], tokenizer: PreTrainedTokenizer, file_path: str=None):
    lexicon_words = []
    for word in words:
        tokenized_word = tokenizer.tokenize(word)
        lexicon_words.append(f'{word} {" ".join(tokenized_word)} |')

    if file_path != None:
        with open(file_path, 'w+') as lexicon_file:
            lexicon_file.write('\n'.join(lexicon_words))

    return lexicon_words