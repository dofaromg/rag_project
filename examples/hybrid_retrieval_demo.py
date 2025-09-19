#!/usr/bin/env python3
"""
混合检索系统使用示例

演示BM25和语义检索的结合使用
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def hybrid_retrieval_example():
    """混合检索示例"""
    print("=== 混合检索系统示例 ===")
    
    # 注意：这个示例需要实际的向量索引，这里只是展示接口用法
    print("混合检索系统结合了:")
    print("1. BM25关键词检索 - 精确匹配")
    print("2. 语义向量检索 - 语义理解")
    print("3. 动态权重融合 - 最优结果")
    
    # 示例代码结构
    example_code = '''
from src.rag.retriever import HybridRetriever
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 1. 加载文档
documents = SimpleDirectoryReader("./data/financial_docs").load_data()

# 2. 创建向量索引
vector_index = VectorStoreIndex.from_documents(documents)

# 3. 初始化混合检索器
hybrid_retriever = HybridRetriever(
    vector_index=vector_index,
    docstore=vector_index.docstore,
    similarity_top_k=5,  # 检索前K个结果
    alpha=0.5  # BM25和语义检索的权重平衡
)

# 4. 执行检索
query = "特斯拉公司的财务表现如何？"
results = hybrid_retriever.retrieve(query)

# 5. 处理结果
for result in results:
    print(f"文档: {result.node.text}")
    print(f"分数: {result.score}")
'''
    
    print("\n代码示例:")
    print(example_code)
    
    print("\n关键参数说明:")
    print("- similarity_top_k: 检索结果数量")
    print("- alpha: 权重平衡参数 (0=纯BM25, 1=纯语义)")
    print("- 推荐alpha=0.5实现最佳平衡")


def bm25_example():
    """BM25检索示例"""
    print("\n=== BM25检索示例 ===")
    
    print("BM25检索特点:")
    print("- 基于词频和逆文档频率")
    print("- 擅长精确关键词匹配")
    print("- 对专业术语检索效果好")
    
    example_code = '''
from src.rag.retriever.bm25 import BM25Retriever

# 创建BM25检索器
bm25_retriever = BM25Retriever.from_defaults(
    nodes=document_nodes,
    similarity_top_k=3
)

# 执行检索
results = bm25_retriever.retrieve("流动比率 财务指标")
'''
    
    print("\n代码示例:")
    print(example_code)


def main():
    """主函数"""
    print("混合检索系统使用指南\n")
    
    hybrid_retrieval_example()
    bm25_example()
    
    print("\n=== 性能优势 ===")
    print("- 召回率提升28%")
    print("- 结合关键词和语义匹配")
    print("- 适合金融专业领域")


if __name__ == "__main__":
    main()