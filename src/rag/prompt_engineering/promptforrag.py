import os
import openai
os.environ["HTTP_PROXY"] = "http://127.0.0.1:10802"
os.environ["HTTPS_PROXY"]= "http://127.0.0.1:10802"
os.environ["OPENAI_API_KEY"] = "sk-WXcy8xtOxqH7hWC0wfprvFUVjrnifKngp6XZ5wLrUD0Sc4xc"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = "https://api.chatanywhere.tech/v1"

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex
from llama_index.core import PromptTemplate

from llama_index.readers.file import PyMuPDFReader

loader = PyMuPDFReader()
documents = loader.load(file_path="/Users/plastic/Documents/code/project/data/llama2.pdf")

from llama_index.llms.openai import OpenAI
# gpt35_llm = OpenAI(model = "gpt-3.5-turbo")
gpt4_llm = OpenAI(model="gpt-4",temperature=0)

index = VectorStoreIndex.from_documents(documents)

query_str = "What are the potential risks associated with the use of Llama 2 as mentioned in the context?"
query_engine = index.as_query_engine(similarity_top_k=2,llm=gpt4_llm)

vector_retriever = index.as_retriever(similarity_top_k=2)

# # response = query_engine.query(query_str)
# # print(str(response))

# prompts_dict = query_engine.get_prompts()
# # print(prompts_dict)

# from langchain import hub
# langchain_prompt = hub.pull("rlm/rag-prompt")
# from llama_index.core.prompts import LangchainPromptTemplate

# lc_prompt_tmpl = LangchainPromptTemplate(
#     template=langchain_prompt,
#     template_var_mappings={
#         "query_str": "question",
#         "context_str": "context",
#     }
# )

# query_engine.update_prompts(
#     {"response_synthesizer:text_qa_template": lc_prompt_tmpl}
# )
# prompts_dict = query_engine.get_prompts()
# # print(prompts_dict)

# # response = query_engine.query(query_str)
# # print(str(response))

# from llama_index.core.schema import TextNode

# few_shot_nodes = []
# for line in open("/Users/plastic/Documents/code/project/data/rlhf_citations.jsonl"):
#     node = TextNode(text=line)
#     few_shot_nodes.append(node)

# few_shot_index = VectorStoreIndex(few_shot_nodes)
# few_shot_retriever = few_shot_index.as_retriever(similarity_top_k=2)

# import json

# def few_shot_examples_fn(**kwargs):
#     query_str = kwargs["query_str"]
#     retrieved_nodes = few_shot_retriever.retrieve(query_str)

#     result_strs = []
#     for n in retrieved_nodes:
#         raw_dict = json.loads(n.get_content())
#         query = raw_dict["query"]
#         response = raw_dict["response"]
#         print(type(response))
#         response_dict = json.loads(json.dumps(response))
#         result_str = f"""\
# Query: {query}
# Response: {response_dict}"""
#         result_strs.append(result_str)
#     return "\n\n".join(result_strs)

# qa_prompt_tmpl_str = """\
# Context information is below.
# ----------------------
# {context_str}
# ----------------------
# Given the context information and not prior knowledge, answer the query
# asking about citations over different topics.
# Please provide your asnwer in the form of as structured JSON format containing
# a list of authors as the citations. Some examples are given below.remember give me the structured JSON format.

# {few_shot_examples}

# Query: {query_str}
# Answer:\
# """

# qa_prompt_tmpl = PromptTemplate(
#     qa_prompt_tmpl_str,
#     function_mappings={
#         "few_shot_examples": few_shot_examples_fn,}
# )
# citation_query_str = (
#     "which citation is more relevant to the role of RLHF in the development of large language models?"
# )
# print(
#     qa_prompt_tmpl.format(
#         query_str=citation_query_str,
#         context_str="test_context"
#     )
# )

# query_engine.update_prompts(
#     {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
# )
# # prompt = query_engine.get_prompts()
# # print(prompt)
# response = query_engine.query(citation_query_str)
# print(str(response))
# print(1)

from llama_index.core.postprocessor import (
    NERPIINodePostprocessor,
    SentenceEmbeddingOptimizer
)
from llama_index.core import QueryBundle
from llama_index.core.schema import NodeWithScore, TextNode

pii_processor = NERPIINodePostprocessor(llm=gpt4_llm)

def filter_pii_fn(**kwargs):
    query_bundle = QueryBundle(query_str=kwargs["query_str"])

    new_nodes = pii_processor.postprocess_nodes(
        [NodeWithScore(node=TextNode(text=kwargs["context_str"]))],
        query_bundle=query_bundle,
    )
    new_node = new_nodes[0]
    return new_node.get_content()

qa_prompt_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)
qa_prompt_tmpl = PromptTemplate(
    qa_prompt_tmpl_str,function_mappings={"context_str": filter_pii_fn}
)

# take a look at the prompt
retrieved_nodes = vector_retriever.retrieve(query_str)
context_str = "\n\n".join([n.get_content() for n in retrieved_nodes])

qa_prompt_tmpl.format(
    query_str=query_str,
    context_str=context_str
)
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
)
response = query_engine.query(query_str)
print(str(response))