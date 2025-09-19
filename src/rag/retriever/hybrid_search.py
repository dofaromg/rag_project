from llama_index.core.retrievers import SummaryIndexRetriever,BaseRetriever
from llama_index.core.indices.query.embedding_utils import get_top_k_embeddings
from llama_index.core import QueryBundle
from llama_index.core.schema import NodeWithScore
from typing import List, Any, Optional
from llama_index.core import Settings
from llama_index.core import SummaryIndex,VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
# You can set the API key in the embeddings or env
import os


from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
Settings.llm = OpenAI(model="gpt-4o")
Settings.embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
documents = SimpleDirectoryReader("/Users/plastic/Documents/code/project/data/telsa").load_data()
splitter = SentenceSplitter(chunk_size=512,chunk_overlap=20)
nodes = splitter.get_nodes_from_documents(documents)
vector_index = VectorStoreIndex(nodes)

index = SummaryIndex(nodes)
retriever = SummaryIndexRetriever(index)
vector_retriever = vector_index.as_retriever(similarity_top_k=2)
engine = RetrieverQueryEngine(retriever)
# result_nodes = engine.query("summary this document")
# print(result_nodes)
# answer = engine.query("What happened after the writer's mom died?")
# print(answer)
class HybridRetriever(BaseRetriever):
    """Hybrid retriever."""

    def __init__(
        self,
        vector_index,
        docstore,
        similarity_top_k: int = 2,
        out_top_k: Optional[int] = None,
        alpha: float = 0.5,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(**kwargs)
        self._vector_index = vector_index
        self._embed_model = vector_index._embed_model
        self._retriever = vector_index.as_retriever(
            similarity_top_k=similarity_top_k
        )
        self._out_top_k = out_top_k or similarity_top_k
        self._docstore = docstore
        self._alpha = alpha

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes given query."""

        # first retrieve chunks
        nodes = self._retriever.retrieve(query_bundle.query_str)

        # get documents, and embedding similiaryt between query and documents

        ## get doc embeddings
        doc_embeddings = []
        docs = [self._docstore.get_document(n.node.node_id) for n in nodes]
        for doc in docs:
            doc_embedding = self._embed_model.get_text_embedding(doc.text)
            # print(doc_embedding)
            doc_embeddings.append(doc_embedding)
        # doc_embeddings = [d.embedding for d in docs]
        # print(f"doc_embeddings: {doc_embeddings}")
        query_embedding = self._embed_model.get_query_embedding(
            query_bundle.query_str
        )

        ## compute doc similarities
        doc_similarities, doc_idxs = get_top_k_embeddings(
            query_embedding, doc_embeddings
        )

        ## compute final similarity with doc similarities and original node similarity
        result_tups = []
        for doc_idx, doc_similarity in zip(doc_idxs, doc_similarities):
            node = nodes[doc_idx]
            # weight alpha * node similarity + (1-alpha) * doc similarity
            full_similarity = (self._alpha * node.score) + (
                (1 - self._alpha) * doc_similarity
            )
            # print(
            #     f"Doc {doc_idx} (node score, doc similarity, full similarity): {(node.score, doc_similarity, full_similarity)}"
            # )
            result_tups.append((full_similarity, node))

        result_tups = sorted(result_tups, key=lambda x: x[0], reverse=True)
        # update scores
        for full_score, node in result_tups:
            node.score = full_score

        return [n for _, n in result_tups][:self._out_top_k]
hybrid_retriever = HybridRetriever(
    vector_index=vector_index,
    docstore=vector_index.docstore,
    similarity_top_k=2,
    out_top_k=2,
    alpha=0.5,
)
engine = RetrieverQueryEngine(hybrid_retriever)
result = engine.query("特斯拉公司在2月第二周的交付数据如何")
print(result)

