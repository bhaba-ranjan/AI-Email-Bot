import chromadb
from reader import extract_messages
from langchain_community.vectorstores import chroma
from langchain_community import embeddings
from langchain_community.chat_models import ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter


model_local = ollama.ChatOllama(model='mistral')
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
chroma_collection = chroma_client.create_collection("email_db", get_or_create=True,  metadata={"hnsw:space": "cosine"})
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)

print("reading documents")
documents = extract_messages()
print("document reading successful...")


doc_splits = []

for text in documents:
    doc_splits += text_splitter.split_text(text)

print(doc_splits[0])

ids = [str(i) for i in range(len(doc_splits))]
embedding_function= embeddings.OllamaEmbeddings(model='nomic-embed-text')

embedded_documents = embedding_function.embed_documents(doc_splits)

print(embedded_documents[0])
print(len(embedded_documents))

chroma_collection.add(ids=ids, documents=doc_splits, embeddings=embedded_documents)

print(chroma_collection.count())


vector_store = chroma.Chroma(
    client= chroma_client,
    collection_name = "email_db",
    embedding_function = embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text')
)

retriever = vector_store.as_retriever(search_kwargs={'k': 10})

after_rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt
    | model_local
    | StrOutputParser()
)

for chunk in after_rag_chain.stream("what kind of traveling related mails I am getting?"):
    if '\n' in chunk:
        print(chunk)
    else:        
        print(chunk, end=" ")