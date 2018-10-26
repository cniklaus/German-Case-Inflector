import spacy
from spacy_iwnlp import spaCyIWNLP

nlp = spacy.load('de')
iwnlp = spaCyIWNLP(lemmatizer_path='case_dict/IWNLP.Lemmatizer_20181001.json')
nlp.add_pipe(iwnlp)

#doc = nlp("Wir mögen jene Fußballspiele mit jenen Verlängerungen, welche bei diesem Wetter stattfinden.")

#for token in doc:
#    print('POS: {}\tIWNLP:{}'.format(token.pos_, token._.iwnlp_lemmas))


def lemmatize_adjective(token):
    lem = token._.iwnlp_lemmas
    #print("token:", token, "spacy: ", token.lemma_, "IWNLP: ", lem)
    #if token.text.endswith('ete') or token.text.endswith('eter') or token.text.endswith('eten') or token.text.endswith('etem') or token.text.endswith('etes'):
        #print("?????", token)

    if lem:
        lemmatized_adjective = lem[0]
    else:
        lemmatized_adjective = token.lemma_ #fallback-strategie: use spacy-lemmatizer

    if lemmatized_adjective.endswith('e'): #TODO is this necessary?
        lemmatized_adjective = lemmatized_adjective[:-1]

    if lemmatized_adjective.endswith('en'): # prevent sth like verbündeter -> verbündener
        #print('###########', lemmatized_adjective)
        if not lemmatized_adjective in token.text:
            lemmatized_adjective = lemmatized_adjective[:-1] + 't'
            if not lemmatized_adjective in token.text:
                lemmatized_adjective = lemmatized_adjective[:-2] + 't'
                #if not lemmatized_adjective in token.text:
                 #   print('**************')

    #print("lemmatized: ", lemmatized_adjective)
    #if lemmatized_adjective.endswith('ter'):
        #print("!!!!!!!!!!", lemmatized_adjective[:-2])
    return lemmatized_adjective


def decline_adjective_STRONG(lemmatized_adjective, case, number, gender):
    #print("STRONG")

    if (number == 'pl') and (case == 'dat'):
        declined_adjective = lemmatized_adjective + 'en'

    elif (gender == 'f') or (number == 'Pl'):
        if case in ('nom', 'acc'):
            declined_adjective = lemmatized_adjective + 'e'
        else:
            declined_adjective = lemmatized_adjective + 'er'

    elif case == 'dat':
        declined_adjective = lemmatized_adjective + 'em'

    elif case == 'gen':
        declined_adjective = lemmatized_adjective + 'en'

    elif gender == 'n':
        declined_adjective = lemmatized_adjective + 'es'

    elif case == 'acc':
        declined_adjective = lemmatized_adjective + 'en'

    else:
        declined_adjective = lemmatized_adjective + 'er'

    #print("declined adjective strong:", declined_adjective)
    return declined_adjective


def decline_adjective_WEAK(lemmatized_adjective, case, gender):
    #print("WEAK")

    if (case == 'nom') and (gender in ('m', 'f', 'n')):
        declined_adjective = lemmatized_adjective + 'e'

    elif (case == 'acc') and (gender in ('n', 'f')):
        declined_adjective = lemmatized_adjective + 'e'

    else:
        declined_adjective = lemmatized_adjective + 'en'

   # print("declined adjective weak:", declined_adjective)
    return declined_adjective


def decline_adjective(token, case, number, gender, type):

    lemmatized_adjective = lemmatize_adjective(token)

    if type==1:
        return decline_adjective_STRONG(lemmatized_adjective, case, number, gender)
    else:
        return decline_adjective_WEAK(lemmatized_adjective, case, gender)


#for token in doc:
 #   print(token.lemma_)
  #  if token.tag_ == 'ADJA':
   #     lemmatize_adjective(token)