import os
import shutil
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

if os.path.exists('./nba_bios_vectordb'): # Check if the vector DB folder already exists
    shutil.rmtree('./nba_bios_vectordb') # Delete the entire folder and its contents


load_dotenv() # Load environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

chunk_size = 1000
chunk_overlap = 150

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

folder_path = 'bios'

chunks = []

for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, mode='r', encoding='utf-8') as file:
            raw_text = file.read()
        
        metadatas = [{'player_name' : file_name.replace('.txt', '')}]
        chunks.extend(r_splitter.create_documents([raw_text], metadatas = metadatas))

print(f"Total chunks: {len(chunks)}")


# Embedding

embeddings = OpenAIEmbeddings()

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory='./nba_bios_vectordb'
)

print(vectordb._collection.count())

results = vectordb.similarity_search("How many championships did Kobe Bryant win?", k=3)

for r in results:
    print(r.metadata['player_name'])
    print(r.page_content[:200])
    print("---")