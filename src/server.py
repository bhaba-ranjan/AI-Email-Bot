from flask import Flask, request, jsonify
from flask_cors import CORS

import chromadb
# from reader import extract_messages
from langchain_community.vectorstores import chroma
from langchain_community import embeddings
from langchain_community.chat_models import ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
# from langchain.text_splitter import CharacterTextSplitter

app = Flask(__name__)
CORS(app)
model_local = ollama.ChatOllama(model='mistral:7b-instruct-v0.2-q4_1')
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
chroma_collection = chroma_client.create_collection("email_db", get_or_create=True)

vector_store = chroma.Chroma(
    client=chroma_client,
    collection_name="email_db",
    embedding_function=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text')
)

retriever = vector_store.as_retriever(search_kwargs={'k': 5})

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

@app.route('/query', methods=['POST'])
def query_handler():
    try:
        data = request.json
        question = data['question']
        result = after_rag_chain.invoke(question)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
