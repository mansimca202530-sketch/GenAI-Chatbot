from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# =====================================
# 1. LOAD PDF
# =====================================

loader = PyPDFLoader(
    r"C:\Users\USER\Downloads\book.pdf"
)

documents = loader.load()

print(f"Total pages loaded: {len(documents)}")


# =====================================
# 2. PREVIEW PDF CONTENT
# =====================================

print("\nFirst page preview:\n")
print(documents[0].page_content[:500])


# =====================================
# 3. SPLIT DOCUMENT INTO CHUNKS
# =====================================

splitter = RecursiveCharacterTextSplitter(
    separators=["\n"],
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"\nTotal chunks: {len(chunks)}")


# =====================================
# 4. CREATE EMBEDDING MODEL
# =====================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("\nEmbedding model loaded successfully!")


# =====================================
# 5. CREATE CHROMA VECTOR DATABASE
# =====================================

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)

print("\nVector database created successfully!")


# =====================================
# 6. RELOAD VECTOR DATABASE
# =====================================

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)

print("Vector database loaded successfully!")


# =====================================
# 7. ASK QUERY / SIMILARITY SEARCH
# =====================================

query = "Who is the main character?"

results = vectorstore.similarity_search(
    query,
    k=3
)


# =====================================
# 8. DISPLAY RESULTS
# =====================================

print("\n========== SEARCH RESULTS ==========\n")

for i, result in enumerate(results):
    print(f"Result {i + 1}:")
    print(result.page_content[:500])
    print("\n" + "-" * 60 + "\n")

    retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
# todays code

query = "What does the book say about reading one chapter a day?"

retrieved_docs = retriever.invoke(query)


def build_prompt(query, retrieved_docs):
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""You are a helpful assistant. Answer the question using ONLY
the context provided below. If the answer is not in the context, say
"I don't have enough information to answer that."

Context:
{context}

Question: {query}

Answer:"""
    return prompt


final_prompt = build_prompt(query, retrieved_docs)

import os
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.environ["HF_TOKEN"])
response = client.chat.completions.create(model="deepseek-ai/DeepSeek-V3-0324", messages=[{"role": "user", "content": final_prompt}])
print(response.choices[0].message.content)