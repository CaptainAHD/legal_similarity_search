from llama_index.query_engine import RetrieverQueryEngine
from llama_index import StorageContext, load_index_from_storage
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores.faiss import FaissVectorStore
import openai
import os
from dotenv import load_dotenv

load_dotenv()

storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir='./store'),
    vector_store=FaissVectorStore.from_persist_dir(persist_dir='./store'),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir='./store'),)


index = load_index_from_storage(storage_context)
openai.api_key = os.getenv("OPENAI_API_KEY")

retriever = index.as_retriever(retriever_mode='embedding')
query_engine = RetrieverQueryEngine(retriever)
response = query_engine.retrieve('John was hit by a car. The driver of the car was drunk.')

def extract_info(node):
    relationships = node.node.relationships
    text = node.node.get_text()
    summary = node.node.metadata.get('meta data')
    score = node.score
    for relationship, related_node_info in relationships.items():
        node_id = related_node_info.node_id
    return f"Relevance Score: {score} \n File Name: {node_id} \n Facts: {text} \n Case Summary: {summary} \n\n "


for i in range(len(response)):
  node_info = extract_info(response[i])
  print(f"Result {i+1}\n {node_info} \n\n")