import spacy
import json
import subprocess
from decline_determiners import decline_definite_article, decline_demonstratives, decline_indefinite_article, decline_indefinites, decline_interrogatives, decline_possessives
from decline_nouns import lemmatize_noun, decline_noun
from decline_adjectives import decline_adjective
import sys


def split_contracted_forms(sentence):
    sentence = sentence.replace(" ans ", " an das ")
    sentence = sentence.replace("Ans ", "An das ")
    sentence = sentence.replace(" im ", " in dem ")
    sentence = sentence.replace("Im ", "In dem ")
    sentence = sentence.replace(" am ", " an dem ")
    sentence = sentence.replace("Am ", "An dem ")
    sentence = sentence.replace(" vom ", " von dem ")
    sentence = sentence.replace("Vom ", "Von dem ")
    sentence = sentence.replace(" beim ", " bei dem ")
    sentence = sentence.replace("Beim ", "Bei dem ")
    sentence = sentence.replace(" zum ", " zu dem ")
    sentence = sentence.replace("Zum ", "Zu dem ")
    sentence = sentence.replace(" ins ", " in das ")
    sentence = sentence.replace("Ins ", "In das ")
    sentence = sentence.replace(" zur ", " zu der ")
    sentence = sentence.replace("Zur ", "Zu der ")

    return sentence


def get_gender(token, sentence):

    lemma = lemmatize_noun(token)

    if lemma in nouns:
        gender = nouns[lemma]["Gender"]
        #('gender wiktionary:', gender)
        if gender == 'Maskulinum':
            return 'm'
        elif gender == 'Femininum':
            return 'f'
        else:
            return 'n'
    else: # in case noun_token is not included in the wiktionary TODO better strategy?
        p1 = subprocess.Popen(["echo", sentence], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["./ParZu/parzu"],
                              stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output, err = p2.communicate()
        parse_output = output.decode('utf-8').split('\n')
        #print("parser output:", parse_output)

        gender_parzu = parse_output[token.i].split('|')[0]
        if gender_parzu.endswith('Fem'):
            return 'f'
        elif gender_parzu.endswith('Masc'):
            return 'm'
        else:
            return 'n'


def inflect(sentence, phrase_to_inflect, target_case, target_number, gender, strong):
    declined = []
    for p in phrase_to_inflect:
        #print(p.text, p.pos_, p.tag_)

        if p.pos_ == 'DET':
            if p.tag_ == 'ART':
                if p.text.lower() in ('der', 'die', 'das', 'den', 'dem', 'des'):
                    declined.append(decline_definite_article(target_case, gender, target_number))
                else:
                    declined.append(decline_indefinite_article(p, target_case, gender, target_number))
            elif p.tag_ == 'PDAT':
                declined.append(decline_demonstratives(p, target_case, gender, target_number))
            elif p.tag_ == 'PPOSAT':
                declined.append(decline_possessives(p, target_case, gender, target_number))
            elif p.tag_ == 'PWAT':
                declined.append(decline_interrogatives(p, target_case, gender, target_number))
            else:  # TODO PIAT, PIDAT, PRELAT
                declined.append(p)

        elif p.pos_ == 'ADJ':
            if p.tag_ == 'ADJA':
                if declined:
                    if (str(declined[-1]).lower() not in ('ein', 'kein', 'mein', 'dein', 'sein', 'unser', 'euer', 'ihr')):
                        strong = 0
                if sentence[p.i - 1].tag_ == 'ADJA':
                    strong = 0
                declined.append(decline_adjective(p, target_case, target_number, gender, strong))
            else:
                declined.append(p)

        elif p.pos_ in ('PROPN', 'NOUN'):
            declined.append(decline_noun(p, target_case, target_number))

        else:
            declined.append(p)

    declined_phrase = ' '
    for d in declined:
        declined_phrase = declined_phrase + ' ' + str(d)

    declined_phrase = declined_phrase.strip()
    return declined_phrase


def inflect_all_noun_phrases(sentence, target_case, target_number):
    sentence = split_contracted_forms(sentence)

    sentence = nlp(sentence)
    phrases = []

    print('sentence:', sentence)
    for token in sentence:
        if token.pos_ in ('PROPN', 'NOUN'):
            inflect_noun_phrase(sentence, token, target_case, target_number)

    print('\n')


def inflect_noun_phrase(sentence, token, target_case, target_number): # TODO inflect only specified phrase
    phrase = sentence[token.left_edge.i: token.right_edge.i + 1]
    #phrases.append(str(phrase))
    print('input phrase:', phrase)

    phrase_to_inflect = sentence[token.left_edge.i: token.i + 1]
    phrase_not_to_inflect = sentence[token.i + 1: token.right_edge.i + 1]

    # print('phrase to inflect:', phrase_to_inflect)
    # print('do not inflect:', phrase_not_to_inflect)
    # print('POS:', phrase_to_inflect[0].pos_)
    determiner_pos = 0
    if phrase_to_inflect[0].pos_ == 'ADP':
        determiner_pos = 1

    #print(";;;;;", phrase_to_inflect[determiner_pos].text.lower())
    if (phrase_to_inflect[determiner_pos].pos_ != 'DET') or (phrase_to_inflect[determiner_pos].text.lower() in (
    'ein', 'kein', 'mein', 'dein', 'sein', 'unser', 'euer', 'ihr')):  # TODO weitere tokens?
        strong = 1
    else:
        strong = 0

    gender = get_gender(token, str(sentence))
    # print("Gender:", gender, token.text)

    declined_phrase = inflect(sentence, phrase_to_inflect, target_case, target_number, gender, strong)
    full_declined_phrase = declined_phrase + ' ' + phrase_not_to_inflect.text
    print("declined phrase:", full_declined_phrase)
    return full_declined_phrase


def inflect_noun_phrase_only(phrase, target_case, target_number): # TODO is parsing accuracy good enough when given only the phrase without full sentence?
    pass


if __name__ == "__main__":
    nlp = spacy.load('de')

    #TODO improve option specification
    input_file = sys.argv[1]
    case = sys.argv[2]
    number = sys.argv[3]

    f_out = open(input_file, 'r')
    doc = f_out.read()
    doc = nlp(doc)
    sentences = [sent.string.strip() for sent in doc.sents]

    with open('case_dict/pretty.json') as f:
        nouns = json.load(f)

    for s in sentences:
        inflect_all_noun_phrases(s, case, number)

