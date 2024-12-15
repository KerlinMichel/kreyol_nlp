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