from ollama import Client


try:
    client = Client(
        host="http://localhost:11434"
    )

    response = client.embed(
        model="nomic-embed-text",
        input="Employees receive 20 days of annual leave."
    )

    embedding = response["embeddings"][0]

    print(len(embedding))

    print(embedding[:10])
except Exception as e:
    print(f"Error: {e}")
    print(f"Make sure Ollama is running at http://localhost:11434")
    print(f"And nomic-embed-text model is loaded")