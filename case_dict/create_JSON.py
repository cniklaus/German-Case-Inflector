from lxml import etree
import json
import codecs


def parseXML(xmlFile):
    """
    Parse the xml
    """
    with open(xmlFile) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    data = []
    test = {}
    for appt in root.getchildren():

        if appt.attrib.values()[0] == 'Noun':
            cases = {}
            noun_lemma = {}

            for elem in appt.getchildren():

                if elem.tag == 'Text':
                    noun_lemma['Lemma'] = elem.text
                    term = elem.text
                if elem.tag == 'Genus':
                    gen = []
                    for e in elem.getchildren():
                        gen.append(e.text)
                    noun_lemma['Genus'] = gen[0]
                    cases['Gender'] = gen[0]  ##todo: better structure!!!
                noun_lemma['POS'] = 'Noun'

                if elem.tag == 'NominativSingular':
                    for e in elem.getchildren():
                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!
                                c.append(e_child.text)
                                if 'NomSg' not in cases:
                                    cases['NomSg'] = c[0]

                if elem.tag == 'NominativPlural':
                    for e in elem.getchildren():

                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!

                                c.append(e_child.text)
                                if 'NomPl' not in cases:
                                    cases['NomPl'] = c[0]

                if elem.tag == 'GenitivSingular':
                    for e in elem.getchildren():

                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!

                                c.append(e_child.text)
                                if 'GenSg' not in cases:
                                    cases['GenSg'] = c[0]

                if elem.tag == 'GenitivPlural':
                    for e in elem.getchildren():

                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!

                                c.append(e_child.text)
                                if 'GenPl' not in cases:
                                    cases['GenPl'] = c[0]

                if elem.tag == 'DativSingular':
                    for e in elem.getchildren():

                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!

                                c.append(e_child.text)
                                if 'DatSg' not in cases:
                                    cases['DatSg'] = c[0]

                if elem.tag == 'DativPlural':
                    for e in elem.getchildren():

                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!

                                c.append(e_child.text)
                                if 'DatPl' not in cases:
                                    cases['DatPl'] = c[0]

                if elem.tag == 'AkkusativSingular':
                    for e in elem.getchildren():

                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!

                                c.append(e_child.text)
                                if 'AkkSg' not in cases:
                                    cases['AkkSg'] = c[0]

                if elem.tag == 'AkkusativPlural':
                    for e in elem.getchildren():

                        for e_child in e.getchildren():
                            c = []
                            if e_child.tag == 'InflectedWord':  ##todo: list of inflections!

                                c.append(e_child.text)
                                if 'AkkPl' not in cases:
                                    cases['AkkPl'] = c[0]

            # print('cases: ', cases)
            test[term] = cases
            noun_lemma['Cases'] = cases
            data.append(noun_lemma)

    #print(test)
    with codecs.open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(test, outfile, ensure_ascii=False)


if __name__ == "__main__":
    parseXML("parsedIWNLP_latest_current.xml")


