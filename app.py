"""
FastAPI application for RAG project
Minimal web server with root endpoint serving Chinese greeting
"""

from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(title="RAG Project API", description="RAG项目API")


@app.get("/")
async def root():
    """
    Root endpoint returning Chinese greeting
    根路径端点，返回中文问候语
    """
    return "你好"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
