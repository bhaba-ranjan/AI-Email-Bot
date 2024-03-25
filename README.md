## Sample Response


![Demo of chatting with the assistang](/src/assets/DemoChat.png)


## Retrieval Augmented Generation (RAG) on Emails

- Export emails from your provider (Gmail/Outlook) it should be in .mobx format.
- Keep the folder in the root directory and adjust the path in `src/reader.py`
- Install Ollama `https://ollama.com/download` 
- Mistral 7B LLM. `ollama run mistral`
- Install Nomic text embedding model. `ollama pull nomic-embed-text`
- Install `langchain` and `chromdb` client with `pip install`.
- Setup chromadb through docker  `docker pull chromadb/chroma:0.4.25.dev58`.
- Run `write-Embedding.py`
- Run `server.py`
- Open the `index.html` file and interact chat with the LLM.


## Checkout the Video

- Click on the image or follow this link: https://www.youtube.com/watch?v=VpcC195Y0UY

[![RAG on EMAIL](https://img.youtube.com/vi/VpcC195Y0UY/0.jpg)](https://www.youtube.com/watch?v=VpcC195Y0UY)