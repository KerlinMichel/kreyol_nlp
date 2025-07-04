from transformers import Wav2Vec2CTCTokenizer

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

def torchaudio_ctc_decoder_lexicon(words: set[str], tokenizer: Wav2Vec2CTCTokenizer, file_path: str=None):
    unknown_token = tokenizer.special_tokens_map['unk_token']
    unkown_token_id = tokenizer.encode(unknown_token)[0]

    lexicon_words = []

    for word in words:
        tokenized_word = tokenizer.tokenize(word)
        e_tokenized_word = tokenizer.encode(tokenized_word)
        # skip any words that has an unknown token
        if unkown_token_id in e_tokenized_word:
            continue
        lexicon_words.append(f'{word} {" ".join(tokenized_word)} |')

    if file_path != None:
        with open(file_path, 'w+') as lexicon_file:
            lexicon_file.write('\n'.join(lexicon_words))

    return lexicon_words