def get_ending(case, gender, number):

    if number == 'Sg':
        if case == 'nom':
            if gender in ('m', 'n'):
                ending = ''
            else:
                ending = 'e'

        elif case == 'acc':
            if gender == 'm':
                ending = 'en'
            elif gender == 'f':
                ending = 'e'
            else:
                ending = ''

        elif case == 'gen':
            if gender in ('m', 'n'):
                ending = 'es'
            else:
                ending = 'er'

        else:
            if gender in ('m', 'n'):
                ending = 'em'
            else:
                ending = 'er'

    else:
        if case in ('nom', 'akk'):
            ending = 'e'
        elif case == 'gen':
            ending = 'er'
        else:
            ending = 'en'

    return ending


def decline_definite_article(case, gender, number): # der, die, das

    if number == 'Sg':
        if gender == 'f':
            if case in ('nom', 'akk'):
                article = 'die'
            else:
                article = 'der'

        elif gender == 'n':
            if case in ('nom', 'akk'):
                article = 'das'
            elif case == 'dat':
                article = 'dem'
            else:
                article = 'des'

        else:
            if case == 'nom':
                article = 'der'
            elif case == 'akk':
                article = 'den'
            elif case == 'dat':
                article = 'dem'
            else:
                article = 'des'

    else:
        if case in ('nom', 'akk'):
            article = 'die'
        elif case == 'dat':
            article = 'den'
        else:
            article = 'der'

    return article


def decline_indefinite_article(token, case, gender, number): # ein, kein

    if token.text.lower().startswith('e'):
        lemma = 'ein'
    else:
        lemma = 'kein' # TODO: other indefinite articles?

    if number == 'Pl' and lemma == 'ein':
        article = ''
    else:
        article = lemma + get_ending(case, gender, number)

    return article


def decline_possessives(token, case, gender, number): # mein, dein, sein, unser, euer, ihr

    if token.text.lower() in ("mein", "meine", "meinen", "meinem", "meiner", "meines"):
        lemma = 'mein'
    elif token.text.lower() in ("dein", "deine", "deinen", "deinem", "deiner", "deines"):
        lemma = 'dein'
    elif token.text.lower() in ("sein", "seine", "seinen", "seinem", "seiner", "seines"):
        lemma = 'sein'
    elif token.text.lower() in ("ihr", "ihre", "ihren", "ihrem", "ihrer", "ihres"):
        lemma = 'ihr'
    elif token.text.lower() in ("euer", "eure", "euren", "eurem", "eurer", "eures", "euere", "eueren", "euerem", "euerer", "eueres"):
        lemma = 'euer'
    else:
        lemma = 'unser'

    declined_possessive = lemma + get_ending(case, gender, number)

    return declined_possessive


def decline_demonstratives(token, case, gender, number): # dieser, jener TODO other demonstratives?

    if token.text.lower() in ("dies", "diese", "diesen", "diesem", "dieser", "dieses"):
        lemma = "dies"
    elif token.text.lower() in ("jene", "jenen", "jenem", "jenes"):
        lemma = "jen"
    else:
        lemma = token.lemma_

    declined_demonstrative = lemma + get_ending(case, gender, number)

    return declined_demonstrative


def decline_interrogatives(token, case, gender, number): # welcher TODO other interrogatives?

    if token.text.lower() in ("welch", "welche", "welchen", "welchem", "welcher", "welches"):
        lemma = "welch"
    else:
        lemma = token.lemma_

    declined_interrogative = lemma + get_ending(case, gender, number)

    return declined_interrogative


def decline_indefinites(token, case, gender, number): # TODO
    pass


