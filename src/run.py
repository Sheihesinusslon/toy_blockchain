import uvicorn

if __name__ == "__main__":
    """For Dev run only"""
    uvicorn.run("web_service.api:app", host="127.0.0.1", port=8000, reload=True)
