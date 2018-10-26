import json
import spacy
from spacy_iwnlp import spaCyIWNLP

nlp = spacy.load('de')
iwnlp = spaCyIWNLP(lemmatizer_path='case_dict/IWNLP.Lemmatizer_20181001.json')
nlp.add_pipe(iwnlp)


with open('case_dict/pretty.json') as f:
    nouns = json.load(f)


def lemmatize_noun(token):
    lem = token._.iwnlp_lemmas
    #print("spacy: ", token.lemma_, "IWNLP: ", lem)

    if lem:
        lemmatized_noun = lem[0]
    else:
        lemmatized_noun = token.lemma_ #fallback-strategie: use spacy-lemmatizer

    #print("lemmatized: ", lemmatized_noun)
    return lemmatized_noun


def decline_noun(token, case, number):

    lemma = lemmatize_noun(token)

    if number == 'Sg':
        if case == 'nom':
            case_num = 'NomSg'
        elif case == 'gen':
            case_num = 'GenSg'
        elif case == 'dat':
            case_num = 'DatSg'
        else:
            case_num = 'AkkSg'

    else:
        if case == 'nom':
            case_num = 'NomPl'
        elif case == 'gen':
            case_num = 'GenPl'
        elif case == 'dat':
            case_num = 'DatPl'
        else:
            case_num = 'AkkPl'

    if lemma in nouns:
        if case_num in nouns[lemma]:
            return nouns[lemma][case_num]
    else:
        return lemma  #TODO wenn nicht in wiktionary enthalten?

#print(decline_noun("Apfel", "gen", "Sg"))