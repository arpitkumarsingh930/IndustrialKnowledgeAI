import spacy

nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities


def extract_relationships(text):

    entities = extract_entities(text)

    relationships = []

    person = None

    for e in entities:

        if e["label"] == "PERSON":
            person = e["text"]
            break

    if person is None:
        return relationships

    for e in entities:

        if e["text"] == person:
            continue

        label = e["label"]

        if label == "ORG":

            relationships.append({
                "source": person,
                "relation": "AFFILIATED_WITH",
                "target": e["text"]
            })

        elif label == "GPE":

            relationships.append({
                "source": person,
                "relation": "LOCATED_IN",
                "target": e["text"]
            })

        elif label == "DATE":

            relationships.append({
                "source": person,
                "relation": "RELATED_TO_DATE",
                "target": e["text"]
            })

    return relationships
def extract_question_entities(question):

    doc = nlp(question)

    entities = []

    for ent in doc.ents:
        entities.append(ent.text)

    return entities