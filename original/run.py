import uvicorn
from index import app


if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=80, reload=True)
