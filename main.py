import os

from langchain_ollama import ChatOllama
from huggingface_hub import InferenceClient
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Common setup
llama_llm = ChatOllama(model="llama3.2", temperature=0.6)

hf_client = InferenceClient(
    api_key=os.environ["HF_TOKEN"]
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Option 1
def ask_llama(query):
    response = llama_llm.invoke(query)
    return response.content


# Option 2
def ask_deepseek(query):
    response = hf_client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ]
    )
    return response.choices[0].message.content


# PDF RAG
def build_prompt(query, retrieved_docs):

    context = "\n\n".join(
        [doc.page_content for doc in retrieved_docs]
    )

    prompt = f"""You are a helpful assistant. Answer the question using ONLY
the context provided below. If the answer is not in the context, say
"I don't have enough information to answer that."

Context:

{context}

Question: {query}

Answer:"""

    return prompt


def ask_pdf(query, pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    retrieved_docs = retriever.invoke(query)

    final_prompt = build_prompt(
        query,
        retrieved_docs
    )

    response = llama_llm.invoke(final_prompt)

    return response.content


# Quick test
if __name__ == "__main__":

    try:
        print("1. LLAMA:", ask_llama("What is RAG?"))
    except Exception as e:
        print("LLAMA Error:", e)

    try:
        print("2. DeepSeek:", ask_deepseek("What is RAG?"))
    except Exception as e:
        print("DeepSeek Error:", e)

    try:
        print(
            "3. PDF:",
            ask_pdf(
                "Who is the Author of the book ?",
                r"C:\Users\USER\Downloads\Book.pdf"
            )
        )
    except Exception as e:
        print("PDF Error:", e)