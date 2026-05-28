# local-ai-search

A private AI search app that runs on your own machine. It searches the web, gathers text and images, and uses a local Ollama model to stream an AI answer into a simple browser UI.

No paid API keys are required.

---

## Features

- Live AI answer streaming in the browser.
- Web search context from DDGS/DuckDuckGo-style search results.
- Related image search with thumbnails.
- Separate Images tab with paginated "Load More" support.
- Markdown rendering for AI answers.
- Local Ollama model support.

---

## Things Used

### Backend

- **Python** - Main programming language.
- **FastAPI** - Creates the local backend API.
- **Uvicorn** - Runs the FastAPI development server.
- **DDGS** - Fetches web text results and image results.
- **Ollama Python package** - Talks to the local Ollama app/model.
- **Python `os` module** - Checks and reads `index.html`.

### AI

- **Ollama** - Runs the LLM locally on your computer.
- **Model used in code:** `llama3.2:1b`
- **Generation setting:** `temperature: 0.0` for more deterministic answers.
- **Streaming mode:** enabled through `ollama.chat(..., stream=True)`.

### Frontend

- **HTML, CSS, JavaScript** - Builds the web UI.
- **Browser Fetch API** - Calls the backend `/search` and `/images` APIs.
- **ReadableStream API** - Reads the streamed AI answer chunk by chunk.
- **TextDecoder API** - Converts streamed bytes into text.
- **Marked.js CDN** - Converts Markdown from the AI response into HTML.

Marked.js is loaded from:

```html
https://cdn.jsdelivr.net/npm/marked/marked.min.js
```

---

## APIs Used

### 1. FastAPI Backend APIs

These APIs are created in `main.py`.

#### `GET /`

Serves the main UI from `index.html`.

Response type:

```text
text/html
```

#### `GET /search`

Streams the AI search answer.

Query parameter:

- `q` - Search question/query.

Example:

```text
http://127.0.0.1:8000/search?q=current%20news
```

What it does:

1. Calls `get_web_ctx(q)` from `search_engine.py`.
2. Uses DDGS text search to collect up to 5 relevant web results.
3. Sends that web context to `ask_ai_stream(q, web_ctx)` in `ai_model.py`.
4. Streams the Ollama answer back to the browser as plain text.

Response type:

```text
text/plain
```

#### `GET /images`

Returns image search results.

Query parameters:

- `q` - Image search query.
- `limit` - Number of images to return. Default: `8`.
- `offset` - Starting position for pagination. Default: `0`.

Example:

```text
http://127.0.0.1:8000/images?q=mountains&limit=20&offset=0
```

What it does:

1. Calls `get_web_images(q, max_images=offset + limit)`.
2. Uses DDGS image search.
3. Returns only the requested slice of images.

Response format:

```json
[
  {
    "title": "Image title",
    "image_url": "Full image URL",
    "thumbnail_url": "Thumbnail image URL"
  }
]
```

---

## External / Local Services

### DDGS Search

Used in `search_engine.py`.

- `ddgs.text(...)` fetches text search results.
- `ddgs.images(...)` fetches image search results.

This project uses DDGS through the Python `ddgs` package. It does not use a paid search API key.

### Ollama

Used in `ai_model.py`.

- `ollama.chat(...)` sends the prompt to the local Ollama model.
- `stream=True` returns the answer in chunks.
- The configured model is `llama3.2:1b`.

Ollama must be installed and running locally before starting the app.

### jsDelivr CDN

Used in `index.html` to load Marked.js for Markdown parsing.

---

## Project Flow

1. User enters a search query in the browser.
2. Frontend calls `/images` to load related images.
3. Frontend calls `/search` to start the answer stream.
4. Backend searches the web using DDGS.
5. Backend sends the collected web context and user query to Ollama.
6. Ollama streams the answer back.
7. Browser reads the stream, parses Markdown with Marked.js, and updates the page live.

---

## Prerequisites

1. Python 3.10+
2. Ollama installed and running
3. Local Ollama model, for example `llama3.2:1b`

---

## Quick Setup & Run

### 1. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install uvicorn fastapi ddgs ollama
```

### 3. Download / run the AI model

Make sure Ollama is running, then run:

```bash
ollama run llama3.2:1b
```

### 4. Start the app

```bash
python main.py
```

Open this URL in your browser:

```text
http://127.0.0.1:8000
```

---

## Folder Layout

- `main.py` - FastAPI app, API routes, and Uvicorn server startup.
- `search_engine.py` - DDGS text search, image search, and basic relevance filtering.
- `ai_model.py` - Ollama chat call, prompt setup, model selection, and streaming response.
- `index.html` - Frontend UI, tabs, image gallery, API calls, stream reading, and Markdown rendering.
- `readme.md` - Project documentation.
