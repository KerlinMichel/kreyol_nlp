# TODO: Source?
# TODO: there are 2 ways to spell 8, wit and uit. Need to figure best way to handle
_FIRST_100_INT_TO_WORDS = {
     0: 'zewo', 
     1: 'en',            2: 'de',             3: 'twa',            4: 'kat',             5: 'senk',           6: 'sis',           7: 'sèt',             8: 'uit',              9: 'nèf',              10: 'dis',
    11: 'onz',          12: 'douz',          13: 'trèz',          14: 'katòz',          15: 'kenz',          16: 'sèz',          17: 'disèt',          18: 'dizwit',          19: 'diznèf',           20: 'ven',
    21: 'venteyen',     22: 'vennde',        23: 'venntwa',       24: 'vennkat',        25: 'vennsenk',      26: 'vennsis',      27: 'vennsèt',        28: 'ventuit',         29: 'ventnèf',          30: 'trant',
    31: 'tranteyen',    32: 'trannde',       33: 'tranntwa',      34: 'trannkat',       35: 'tannsenk',      36: 'trannsis',     37: 'trannsèt',       38: 'trantuit',        39: 'trantnèf',         40: 'karant',
    41: 'karanteyen',   42: 'karannde',      43: 'karanntwa',     44: 'karannkat',      45: 'karannsenk',    46: 'karannsis',    47: 'karannsèt',      48: 'karantui',        49: 'karantnèf',        50: 'senkant',
    51: 'senkanteyen',  52: 'senkannde',     53: 'senkanntwa',    54: 'senkannkat',     55: 'senkannsenk',   56: 'senkannsis',   57: 'senkannsèt',     58: 'senkantui',       59: 'senkantnèf',       60: 'swasant',
    61: 'swasanteyen',  62: 'swasannde',     63: 'swasanntwa',    64: 'swasannkat',     65: 'swasannsenk',   66: 'swasannsis',   67: 'swasannsèt',     68: 'swasantui',       69: 'swasantnèf',       70: 'swasann-dis',
    71: 'swasann-onz',  72: 'swasann-douz',  73: 'swasann-trèz',  74: 'swasann-katòz',  75: 'swasann-kenz',  76: 'swasann-sèz',  77: 'swasann-disèt',  78: 'swasann-dizwit',  79: 'swasann-diznèf',   80: 'katreven',
    81: 'katreven-en',  82: 'katreven-de',   83: 'katreven-twa',  84: 'katreven-kat',   85: 'katreven-senk', 86: 'katreven-sis', 87: 'katreven-sèt',   88: 'katreven-wit',    89: 'katreven-nèf',     90: 'katreven-dis',
    91: 'katreven-onz', 92: 'katreven-douz', 93: 'katreven-trèz', 94: 'katreven-katòz', 95: 'katreven-kenz', 96: 'katreven-sèz', 97: 'katreven-disèt', 98: 'katreven-dizwit', 99: 'katreven-diznèf', 100: 'san'
}

def _int_to_digits(int_: int) -> list:
    sign = 1
    if int_ < 0:
        sign = -1
        int_ = -int_

    digits = []
    while int_ != 0:
        digits.append(int_ % 10)
        int_ //= 10

    digits.reverse()
    digits[0] *= sign
    return digits

def _digits_to_int(digits: list) -> int:
    integer = 0
    for digit, place_idx in zip(digits, reversed(range(len(digits)))):
        integer += digit * (10 ** place_idx)
    return integer


# TODO: Source?
# TODO: support negative numbers
# TODO: The English word billion made be used as a load word in Kreyòl (biliyon?)
def int_to_words(integer: int, replace_hyphen_with: str='-') -> str:
    if integer < 0:
        raise NotImplementedError('Negative integers not supported')
    if integer > 999_999_999:
        raise NotImplementedError('Only supports up to 999,999,999')
    
    # handle 0-100
    if integer in _FIRST_100_INT_TO_WORDS:
        return _FIRST_100_INT_TO_WORDS[integer]

    digits = _int_to_digits(integer)
    words = []

    mil_digits = []
    milyon_digits = []
    # process digits above 2nd place in integer
    for digit, place_idx in zip(digits[:-2], range(len(digits), 2, -1)):

        words_to_add = []
        if place_idx == 3:
            if digit > 1:
                words_to_add.append(_FIRST_100_INT_TO_WORDS[digit])
            words_to_add.append('san')
        
        if place_idx == 4:
            mil_digits.append(digit)
            mil_mulitple = _digits_to_int(mil_digits)
            if mil_mulitple > 1:
                words_to_add += int_to_words(mil_mulitple).split()
            words_to_add.append('mil')
        
        if place_idx == 5 or place_idx == 6:
            mil_digits.append(digit)
        
        if place_idx == 7:
            milyon_digits.append(digit)
            milyon_mulitple = _digits_to_int(milyon_digits)
            words_to_add += int_to_words(milyon_mulitple).split()
            words_to_add.append('milyon')

        if place_idx == 8 or place_idx == 9:
            milyon_digits.append(digit)
        
        if digit != 0:
            words += words_to_add
        elif place_idx == 4 and mil_mulitple != 0:
            words += words_to_add
            mil_digits = []

    # process last two digits
    last_two_digits_int_value = (digits[-2] * 10) + digits[-1]
    if last_two_digits_int_value > 0:
        words.append(_FIRST_100_INT_TO_WORDS[last_two_digits_int_value])

    words = ' '.join(words)
    if replace_hyphen_with != '-':
        words.replace('-', replace_hyphen_with)
    
    return words