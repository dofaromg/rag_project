"""
Tests for FastAPI application
FastAPI应用的测试文件
"""

import pytest
from fastapi.testclient import TestClient
from app import app

# Create test client
client = TestClient(app)


class TestApp:
    """FastAPI应用测试类"""

    def test_root_endpoint(self):
        """测试根路径端点"""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == "你好"

    def test_root_endpoint_content_type(self):
        """测试根路径端点响应类型"""
        response = client.get("/")

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_openapi_docs_available(self):
        """测试OpenAPI文档可用性"""
        response = client.get("/docs")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_openapi_json_schema(self):
        """测试OpenAPI JSON schema"""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
        assert "/" in schema["paths"]
        assert "get" in schema["paths"]["/"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
