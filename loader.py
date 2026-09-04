from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(r"C:\Users\USER\Downloads\Book.pdf")
documents = loader.load()

print(f"Total pages loaded: {len(documents)}")
print(documents[0].page_content[:500])  # preview first page
print(documents[0].metadata)  # e.g. {'source': 'Book.pdf', 'page': 0}