# RAG项目 - 金融分析检索增强生成系统

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个专注于金融分析的RAG（检索增强生成）系统，结合了Text2SQL、混合检索策略和领域适配技术。

## 🎯 项目特色

- **📊 金融数据处理**: 支持结构化（MySQL财务指标）和非结构化数据（PDF/Word研报）的混合检索
- **🔍 混合检索策略**: 结合BM25关键词检索和语义向量检索，召回率提升28%
- **💬 Text2SQL**: 基于LlamaIndex实现自然语言到SQL的转换
- **🧠 多层级思维链**: 针对财务公式计算设计的推理框架
- **📈 专业术语支持**: 基于220个金融术语的领域知识注入
- **📋 报告生成**: 六维度财务分析报告生成框架

## 🏗️ 项目结构

```
rag_project/
├── README.md                    # 项目说明
├── requirements.txt             # 依赖包
├── src/                        # 源代码
│   ├── rag/                    # RAG核心模块
│   │   ├── enhancer.py         # RAG增强器
│   │   ├── retriever/          # 检索模块
│   │   │   ├── hybrid_search.py
│   │   │   └── bm25.py
│   │   └── prompt_engineering/  # 提示工程
│   ├── text2sql/               # Text2SQL模块
│   └── utils/                  # 工具函数
├── project/                    # 财务分析项目
│   ├── project_describe.md     # 项目详细描述
│   ├── finetune_reranker/      # 重排序器微调
│   └── llm/                    # 语言模型相关
├── tests/                      # 测试文件
├── docs/                       # 文档
└── examples/                   # 使用示例
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenAI API密钥（用于LLM调用）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```python
from src.rag import RAGEnhancer

# 初始化RAG增强器
config = {
    "similarity_threshold": 0.2,
    "max_results": 5
}
enhancer = RAGEnhancer(config)

# 使用示例
query = "什么是流动比率？"
context = [
    "流动比率是衡量企业短期偿债能力的指标",
    "流动比率 = 流动资产 / 流动负债",
    "一般认为流动比率在2左右比较合适"
]

result = await enhancer.enhance_retrieval(query, context)
print(result)
```

## 🔧 核心功能

### 1. 混合检索系统

```python
from src.rag.retriever import HybridRetriever

# 创建混合检索器
hybrid_retriever = HybridRetriever(
    vector_index=vector_index,
    docstore=docstore,
    similarity_top_k=2,
    alpha=0.5  # BM25和向量检索的权重平衡
)
```

### 2. Text2SQL功能

支持自然语言查询转换为SQL，用于财务数据库查询：

```python
# 示例：将自然语言转换为SQL查询
query = "查询苹果公司2023年的营收数据"
# 转换为: SELECT revenue FROM financial_data WHERE company='Apple' AND year=2023
```

### 3. 金融报告生成

六维度报告生成框架：
- 财务表现分析
- 研发进展评估  
- 市场分析
- 风险提示
- 投资建议
- 合规性检查

## 📊 技术特点

### 多层级思维链设计

针对30个财务公式构建多层级推理：
1. **变量定义** - 理解指标含义
2. **数据校验** - 验证数据完整性
3. **分步计算** - 逐步推理过程
4. **合理性验证** - 结果合理性检查

### 评估体系

三维评估指标：
- **事实准确性** - 人工校验
- **术语专业性** - 专家打分
- **逻辑合理性** - GPT-4评估（达到4.8/5分）

## 🧪 测试

运行测试套件：

```bash
python -m pytest tests/ -v
```

## 📝 文档

详细文档请查看：
- [技术架构文档](docs/technical-architecture.md)
- [项目详细描述](project/project_describe.md)
- [Text2SQL使用指南](src/text2sql/Text2SQL.md)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目。

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系

如有问题或建议，请提交Issue或联系项目维护者。

---

**注意**: 本项目重点关注金融领域的RAG应用，如需了解更多技术细节请查看项目文档。