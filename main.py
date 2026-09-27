"""
Smart LLM Router Entry Point
Starts the FastAPI application server with uvicorn.
"""
import uvicorn


def main():
    print("🚀 Starting Smart LLM Router on http://localhost:8000 ...")
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
