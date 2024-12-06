import uvicorn
from api import app

if __name__ == "__main__":
    """For Dev run only"""
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
