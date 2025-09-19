#!/usr/bin/env python3
"""
RAG增强器使用示例

演示如何使用RAG系统进行金融问答
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag import RAGEnhancer


async def basic_example():
    """基本使用示例"""
    print("=== RAG增强器基本使用示例 ===")
    
    # 配置参数
    config = {
        "similarity_threshold": 0.2,
        "max_results": 5
    }
    
    # 初始化增强器
    enhancer = RAGEnhancer(config)
    
    # 示例查询
    query = "什么是流动比率，如何计算？"
    
    # 模拟上下文文档
    context = [
        "流动比率是衡量企业短期偿债能力的重要财务指标",
        "流动比率的计算公式为：流动比率 = 流动资产 / 流动负债",
        "一般认为流动比率在1.5-2.0之间比较合适",
        "流动比率过高可能表示资产利用效率低下",
        "流动比率过低可能存在短期偿债风险"
    ]
    
    print(f"查询: {query}")
    print(f"上下文文档数量: {len(context)}")
    
    try:
        # 执行增强检索
        result = await enhancer.enhance_retrieval(query, context)
        
        print(f"\n检索结果:")
        print(f"- 返回文档数: {len(result['enhanced_context'])}")
        print(f"- 置信度: {result['confidence']:.2f}")
        
        print(f"\n相关文档:")
        for i, doc in enumerate(result['enhanced_context'], 1):
            print(f"{i}. {doc['content']}")
            print(f"   相似度: {doc.get('similarity', 0):.3f}")
            
    except Exception as e:
        print(f"执行出错: {e}")


async def financial_analysis_example():
    """金融分析示例"""
    print("\n=== 金融分析应用示例 ===")
    
    config = {
        "similarity_threshold": 0.3,
        "max_results": 3
    }
    
    enhancer = RAGEnhancer(config)
    
    # 财务分析查询
    queries = [
        "如何分析公司的盈利能力？",
        "债务比率说明了什么问题？",
        "现金流量表的重要性"
    ]
    
    # 财务知识库
    financial_context = [
        "盈利能力分析主要包括毛利率、净利率、ROE等指标",
        "毛利率 = (营业收入 - 营业成本) / 营业收入 × 100%",
        "净利率反映了企业的最终盈利水平",
        "ROE（净资产收益率）是衡量股东投资回报的关键指标",
        "债务比率 = 总负债 / 总资产，反映企业财务杠杆水平",
        "高债务比率可能增加财务风险，但也可能放大收益",
        "现金流量表反映企业现金的流入和流出情况",
        "经营活动现金流是企业造血能力的重要体现",
        "自由现金流 = 经营现金流 - 资本支出"
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        try:
            result = await enhancer.enhance_retrieval(query, financial_context)
            print(f"找到 {len(result['enhanced_context'])} 个相关文档")
            
            for doc in result['enhanced_context']:
                print(f"- {doc['content']}")
                
        except Exception as e:
            print(f"查询失败: {e}")


async def main():
    """主函数"""
    print("RAG系统使用示例\n")
    
    await basic_example()
    await financial_analysis_example()
    
    print("\n=== 示例完成 ===")
    print("更多用法请参考文档：docs/")


if __name__ == "__main__":
    asyncio.run(main())