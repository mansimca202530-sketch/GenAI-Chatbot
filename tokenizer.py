import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

text = "Hello , I am learning Large Language Models."

tokens = encoding.encode(text)

print("Token IDs:")
print(tokens)

print("\nNumber of Tokens:")
print(len(tokens))



from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I love learning Python",
    "Python programming is very interesting",
    "I want to eat pizza"
]

embeddings = model.encode(sentences)

for sentence, embedding in zip(sentences, embeddings):
    print("\nSentence:")
    print(sentence)

    print("Embedding Shape:")
    print(embedding.shape)