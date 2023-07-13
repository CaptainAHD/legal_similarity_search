from llama_index.query_engine import RetrieverQueryEngine
from llama_index import StorageContext, load_index_from_storage
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores.faiss import FaissVectorStore
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

query_engine = None 

storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir='./store'),
    vector_store=FaissVectorStore.from_persist_dir(persist_dir='./store'),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir='./store'),)

def initialise_index():
    global query_engine
    index = load_index_from_storage(storage_context)
    retriever = index.as_retriever(retriever_mode='embedding')
    query_engine = RetrieverQueryEngine(retriever)

def extract_info(node):
    relationships = node.node.relationships
    text = node.node.get_text()
    summary = node.node.metadata.get('meta data')
    score = node.score
    for relationship, related_node_info in relationships.items():
        node_id = related_node_info.node_id
    data,res = {},{}
    data["RelevanceScore"] = score
    data["FileName"] = node_id
    data["Facts"] = text
    data["CaseSummary"] = summary
    res["Output"] = data
    return res

def output(query): 
    response = query_engine.retrieve(query)
    res = []
    for i in range(len(response)):
        node_info = extract_info(response[i])
        res.append(node_info)
    
    return res