import spacy

nlp = spacy.load(
    "en_core_web_sm"
)

def preprocess_query(text):

    doc = nlp(text)

    keywords = []

    for token in doc:

        if not token.is_stop \
        and not token.is_punct:

            keywords.append(
                token.lemma_
            )

    return " ".join(
        keywords
    )

def detect_intent(question):

    q = question.lower()

    if "symptom" in q:
        return "symptoms"

    if "diagnosis" in q:
        return "diagnosis"

    if "treatment" in q:
        return "treatment"

    if "medicine" in q:
        return "medicine"

    return "general"