import math
import re


class Contraction:
    PRONOUN_CONTRACTIONS = {
        'mwen': 'm',
        'ou': 'w',
        'li': 'l',
        'nou': 'n',
        'yo': 'y',
        'ki': 'k'
    }

    def __init__(self, full_form, contracted_form):
        self.full_form = full_form
        self.contracted_form = contracted_form
        self.contracted_form_pattern = re.compile(rf'\b{self.contracted_form}\b', re.IGNORECASE)

    def expand(self, text: str) -> str:
        """
        Expands the contraction in text 
        """
        def case_sensistive_repl(match):
            contracted_g = match.group()
            first_contracted_char = contracted_g[0]
            if first_contracted_char.isupper(): return self.full_form.capitalize()
            return self.full_form

        return re.sub(self.contracted_form_pattern, case_sensistive_repl, text)

    def __repr__(self):
        return f"\"{self.full_form}\" : \"{self.contracted_form}\""

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def pronoun_contractions() -> list:
        return [Contraction(full_form_pronoun, contracted_pronoun)
                for full_form_pronoun, contracted_pronoun 
                in Contraction.PRONOUN_CONTRACTIONS.items()]

    @staticmethod
    def pronoun_with_word_contractions(contracted_pronoun_with_word: str) -> list:
        """
        Creates list of contractions by swapping {pwonon} in
        contracted_pronoun_with_word with all the contracted pronoun forms.
        """
        contractions = []
        for full_form_pronoun, contracted_pronoun in Contraction.PRONOUN_CONTRACTIONS.items():
            pwonon_tag_pattern = re.compile('{pwonon}')
            full_form = re.sub(pwonon_tag_pattern, full_form_pronoun + ' ', contracted_pronoun_with_word)
            contracted_form = re.sub(pwonon_tag_pattern, contracted_pronoun, contracted_pronoun_with_word)
            contractions.append(Contraction(full_form, contracted_form))
        return contractions

TE_CONTRACTIONS = [
    Contraction('te', 't'),
    Contraction('te ap', 'tap')
]

KREYÒL_CONTRACTIONS = (Contraction.pronoun_contractions() +
                       Contraction.pronoun_with_word_contractions('{pwonon}ap') +
                       TE_CONTRACTIONS +
                       [Contraction('ale', 'al')])

def expand_kreyòl_contractions(text):
    for contraction in KREYÒL_CONTRACTIONS:
        text = contraction.expand(text)
    return text

FIRST_TWENTY_INT_TO_NUMBER_WORD = {
    0: 'zewo',
    1: 'en',
    2: 'de',
    3: 'twa',
    4: 'kat',
    5: 'senk',
    6: 'sis',
    7: 'sèt',
    8: 'uit',
    9: 'nèf',
    11: 'onz',
    10: 'dis',
    12: 'douz',
    13: 'trez',
    14: 'katòz',
    15: 'kinz',
    16: 'sèz',
    17: 'disèt',
    18: 'dizwit',
    19: 'diznèf',
    20: 'ven',
}

# 'n' should be added to stem if next least significant digit in number is 2-7
# 't' if next least significant digit in number is 1 or 8 or 9
MULITPLE_OF_10_INT_NUMBER_WORD_STEM = {
    20: 'ven',
    30: 'tran',
    40: 'karan',
    50: 'senkan',
    60: 'swasan',
}

MULITPLE_OF_10_INT_NUMBER_WORD = {
    **{70 + i : f'swasann-{FIRST_TWENTY_INT_TO_NUMBER_WORD[10 + i]}' for i in range(10)},
    80: 'katreven',
    **{80 + i: f'katreven-{FIRST_TWENTY_INT_TO_NUMBER_WORD[i]}' for i in range(1, 20)}
}

MULITPLE_OF_10_PLUS_1_INT_NUMBER_WORD = {
    number + 1: f'{number_word}teyen' for number, number_word in MULITPLE_OF_10_INT_NUMBER_WORD_STEM.items()
}

INT_TO_NUMBER_WORD = {
    **FIRST_TWENTY_INT_TO_NUMBER_WORD,
    **MULITPLE_OF_10_INT_NUMBER_WORD,
    **MULITPLE_OF_10_PLUS_1_INT_NUMBER_WORD,
    100: 'san'
}

def int_to_number_word(number: int, zewo_to_empty_string: bool = False):
    if number == 0 and zewo_to_empty_string:
        return ''
    if number in INT_TO_NUMBER_WORD:
        return INT_TO_NUMBER_WORD[number]
    digits = []
    while number != 0:
        digits.append(number % 10)
        number //= 10
    digits.reverse()

    if len(digits) == 2:
        multiple_of_10_digit = digits[0]

        multiple_of_10_int_number_word_leaf = 'n' if digits[1] in range(2, 7+1) else 't'

        number_word = (MULITPLE_OF_10_INT_NUMBER_WORD_STEM[multiple_of_10_digit * 10] +
                    multiple_of_10_int_number_word_leaf)
        number_word = f"{number_word}{int_to_number_word(digits[1], zewo_to_empty_string=True)}"
        return number_word
    elif len(digits) == 3:
        multiple_of_100_digit = digits[0]
        number_word = 'san' if multiple_of_100_digit == 1 else f'{int_to_number_word(multiple_of_100_digit, zewo_to_empty_string=True)} san'
        number_word = f'{number_word} {int_to_number_word((digits[1] * 10) + digits[2])}'
        return number_word
    elif len(digits) == 4:
        multiple_of_1000_digit = digits[0]
        number_word = 'mil' if multiple_of_1000_digit == 1 else f'{int_to_number_word(multiple_of_1000_digit, zewo_to_empty_string=True)} mil'

        number_word = f'{number_word} {int_to_number_word((digits[1] * 100) + (digits[2] * 10) + digits[3], zewo_to_empty_string=True)}'
        return number_word
    elif len(digits) == 5:
        multiple_of_10000_digit = digits[0]
        multiple_of_1000_digit = digits[1]
        number_word = f'{int_to_number_word((multiple_of_10000_digit * 10) + multiple_of_1000_digit, zewo_to_empty_string=True)} mil'
        number_word = f'{number_word} {int_to_number_word((digits[2] * 100) + (digits[3] * 10) + digits[4], zewo_to_empty_string=True)}'
        return number_word
    else:
        raise NotImplementedError()