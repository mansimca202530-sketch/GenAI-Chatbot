from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence1 = "I love learning Python"
sentence2 = "Python programming is interesting"
sentence3 = "I want to order food"

embedding1 = model.encode(sentence1, convert_to_tensor=True)
embedding2 = model.encode(sentence2, convert_to_tensor=True)
embedding3 = model.encode(sentence3, convert_to_tensor=True)

similarity1 = util.cos_sim(embedding1, embedding2)
similarity2 = util.cos_sim(embedding1, embedding3)

print("Python similarity:")
print(similarity1)

print("\nFood similarity:")
print(similarity2)