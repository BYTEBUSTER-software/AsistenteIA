from transformers import T5Tokenizer, T5ForConditionalGeneration

# Cargamos el modelo y el tokenizer de HuggingFace
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

def generate_summary(events):
    if not events:
        return "No hay eventos que resumir."

    # Unimos los eventos como texto plano
    content = "\n".join(
        f"{e.start.strftime('%H:%M')} - {e.title}: {e.description}" for e in events
    )

    # Preparamos el prompt para el modelo
    prompt = f"Resume los siguientes eventos del día con otras palabras :\n{content}"

    # Tokenizamos la entrada
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Generamos el resumen
    outputs = model.generate(**inputs, max_new_tokens=150)

    # Decodificamos la salida a texto
    print (outputs)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary
