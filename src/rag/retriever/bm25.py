import os



from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")


from llama_index.core import SimpleDirectoryReader

# load documents
documents = SimpleDirectoryReader("/Users/plastic/Documents/code/project/data/paul_graham").load_data()

from llama_index.core.node_parser import SentenceSplitter

# initialize node parser
splitter = SentenceSplitter(chunk_size=512)

nodes = splitter.get_nodes_from_documents(documents)


from llama_index.retrievers.bm25 import BM25Retriever
import Stemmer

# We can pass in the index, docstore, or list of nodes to create the retriever
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=2,
    # Optional: We can pass in the stemmer and set the language for stopwords
    # This is important for removing stopwords and stemming the query + text
    # The default is english for both
    stemmer=Stemmer.Stemmer("english"),
    language="english",
)

bm25_retriever.persist("./bm25_retriever")

loaded_bm25_retriever = BM25Retriever.from_persist_dir("./bm25_retriever")


# initialize a docstore to store nodes
# also available are mongodb, redis, postgres, etc for docstores
from llama_index.core.storage.docstore import SimpleDocumentStore

docstore = SimpleDocumentStore()
docstore.add_documents(nodes)

from llama_index.core.response.notebook_utils import display_source_node

# will retrieve context from specific companies
retrieved_nodes = bm25_retriever.retrieve(
    "What happened at Viaweb and Interleaf?"
)

for node in retrieved_nodes:
    display_source_node(node, source_length=5000)