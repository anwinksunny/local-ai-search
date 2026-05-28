import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, StreamingResponse

# import local functions
from search_engine import get_web_ctx
from ai_model import ask_ai_stream

# init app
app = FastAPI()

# serve main web page
@app.get("/", response_class=HTMLResponse)
def home():
    # check if file is present
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: index.html not found</h1>"

# stream search response to ui
@app.get("/search")
def search(q: str = Query(..., description="search query")):
    # fetch raw web content
    web_ctx = get_web_ctx(q)
    
    # if empty return notice
    if not web_ctx.strip():
        def empty_gen():
            yield "No search results found on the web."
        return StreamingResponse(empty_gen(), media_type="text/plain")
        
    # stream final response
    return StreamingResponse(ask_ai_stream(q, web_ctx), media_type="text/plain")

# run backend
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)