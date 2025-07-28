from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

labels = ["Trabajo", "Estudio", "Salud", "Reunión", "Ocio", "Otro"]

def classify_event(description: str) -> str:
    result = classifier(description, candidate_labels=labels)
    return result["labels"][0]
