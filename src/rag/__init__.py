"""
RAG (Retrieval-Augmented Generation) package for financial analysis.

This package provides tools for:
- Document retrieval using hybrid search (BM25 + semantic)
- Text2SQL capabilities for financial data
- Prompt engineering for financial domain
- RAG enhancement and optimization
"""

__version__ = "1.0.0"
__author__ = "RAG Project Team"

from .enhancer import RAGEnhancer

__all__ = ["RAGEnhancer"]