# Mini RAG — College Notes Assistant

A small Retrieval-Augmented Generation (RAG) application that answers computer science questions using a curated set of college-note snippets. It embeds the notes, retrieves semantically relevant chunks with ChromaDB, filters them by cosine distance, and passes the selected context to an LLM for a grounded answer.

The project is being built incrementally as a hands-on learning project for Python, embeddings, vector search, RAG, and maintainable LLM application architecture.

## What it does

- Stores a small knowledge base covering OS, DBMS, networking, and AI/RAG concepts.
- Generates document embeddings with `sentence-transformers` using `all-MiniLM-L6-v2`.
- Uses ChromaDB with cosine distance to retrieve the three nearest chunks for a question.
- Filters retrieved chunks using an experimental cosine-distance threshold (`0.50`).
- Abstains when no retrieved chunk passes the threshold.
- Sends the question and filtered context to a model served through Groq.
- Displays the generated answer and the sources that passed the relevance filter.
- Keeps provider-specific API code in `llm_client.py`, separate from the RAG workflow in `main.py`.

## How it works

```text
User question
     |
     v
Embedding model (all-MiniLM-L6-v2)
     |
     v
ChromaDB vector search (top 3 chunks)
     |
     v
Cosine-distance threshold filter (distance <= 0.50)
     |
     +---- No chunks pass ----> Abstain and return no sources
     |
     v
Build prompt from question + filtered context
     |
     v
llm_client.generate_response(prompt)
     |
     v
Groq API / openai/gpt-oss-20b
     |
     v
Answer + source list
```

## Architecture

### `main.py`

Responsible for the RAG workflow:

1. Defines the knowledge-base documents and their metadata.
2. Generates document embeddings.
3. Creates a ChromaDB collection and adds the documents.
4. Embeds each user query and retrieves the three nearest chunks.
5. Filters the results by cosine distance.
6. Builds a prompt from the question and the selected context.
7. Calls `generate_response()` and returns the answer with source information.

### `llm_client.py`

Responsible for communicating with the LLM provider:

- Loads environment variables from `.env`.
- Checks that `GROQ_API_KEY` is available.
- Initializes the Groq SDK client.
- Sends a prompt to the configured model.
- Extracts and returns the answer text.
- Raises an error for an empty prompt or empty model response.

This boundary means the RAG code does not directly initialize the Groq client. Switching providers may still require changes to `llm_client.py` because SDKs, request parameters, and response formats can differ.

## Tech stack

- **Python** — application logic
- **Sentence Transformers** — text embeddings (`all-MiniLM-L6-v2`)
- **ChromaDB** — vector storage and similarity search
- **Groq Python SDK** — LLM API client
- **`python-dotenv`** — loads the local API key from `.env`
- **Model:** `openai/gpt-oss-20b`, served through Groq

## Project structure

```text
ai-p/
├── main.py
├── llm_client.py
├── .env                 # Local secret; do not commit
├── .gitignore
├── docs/
│   ├── llm-client-refactoring.md
│   └── rag-failures.md  # Learning notes on retrieval failures
└── README.md
```

Your local environment folder (for example, `.venv/`) may also be present. It should not be committed to Git.

## Requirements

- Python 3.10 or later is recommended.
- A Groq API key with access to the configured model.
- Internet access when downloading the embedding model for the first time and when calling the LLM API.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Naresh5124/ai-p.git
cd ai-p
```

### 2. Create and activate a virtual environment (recommended)

**Windows — PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows — Command Prompt:**

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install chromadb sentence-transformers groq python-dotenv
```

### 4. Configure the API key

Create a `.env` file in the project root, alongside `main.py` and `llm_client.py`:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual key. Do not add quotation marks unless your key format specifically requires them. **Never commit or publish `.env` or expose your API key in screenshots or logs.** Verify that `.env` is listed in `.gitignore`.

### 5. Run the app

```bash
python main.py
```

On Windows, `py main.py` is also commonly available.

Example session:

```text
Mini RAG is ready!
Ask a computer science question.
Type 'exit' to quit.

You: What are the four necessary conditions for deadlock?

Answer:
[Generated answer]

Retrieved sources:
- Deadlocks (os_notes.txt) - distance: [measured distance]
```

The generated answer and distance values depend on the model response and retrieval results.

Type `exit` or `quit` to stop the application.

## Current retrieval behavior

- The app retrieves at most three nearest chunks for each question.
- It uses cosine distance, where a lower distance indicates greater similarity.
- A chunk is retained when its distance is less than or equal to `DISTANCE_THRESHOLD`, currently `0.50`.
- If no chunks pass the threshold, the app returns an abstention message without calling the LLM.
- The threshold is experimental and has not been calibrated on a large evaluation set. It may need adjustment as the knowledge base and query set grow.

## Tests performed so far

Manual checks have been run for:

1. **Known-answer question:** “What are the four necessary conditions for deadlock?”
2. **Paraphrased question:** “Why can processes get stuck waiting for resources forever?”
3. **Unsupported question:** “What is the capital of Japan?”

All three behaved as expected in the reported run. These are manual smoke tests, not an automated test suite or a comprehensive quality benchmark.

## Current limitations

- The knowledge base is a small, manually written list of snippets rather than an ingestion pipeline for arbitrary files.
- The ChromaDB client is created with `chromadb.Client()`, so the collection is in-memory and is rebuilt when the program starts; it is not persisted between runs.
- Retrieval uses one embedding model and a fixed top-k of three.
- The distance threshold is experimental and may produce false positives or false negatives.
- The prompt is sent as a single user message; the instructions and retrieved context have not yet been separated into distinct system and user messages in the wrapper.
- Automated unit tests, a retrieval benchmark, retries, and timeout policies are not yet implemented.

## Learning log

### Day 6 — LLM client refactoring

- Extracted provider-specific code into `llm_client.py`.
- Added the reusable `generate_response(prompt: str) -> str` function.
- Updated `main.py` to call the wrapper rather than directly making a Groq API request.
- Preserved retrieval, relevance filtering, and source reporting.
- Practiced Python modules/imports, client objects, environment variables, chat roles, response extraction, and completion-token limits.

Additional project notes live in [`docs/`](docs/).

## Roadmap

Potential next improvements, not yet implemented:

- Add automated tests for retrieval, abstention, and LLM-client behavior.
- Build a labeled query set and measure retrieval quality.
- Compare the current embedding retrieval against lexical search such as BM25.
- Experiment with hybrid retrieval and reranking.
- Add persistent ChromaDB storage.
- Improve API failure handling, retries, and timeouts.
- Move the model instructions into a dedicated system message while keeping the wrapper reusable.

## Security notes

- Keep API keys in environment variables, not source code.
- Keep `.env` and `.venv/` out of version control.
- Rotate the API key immediately if it is accidentally exposed.

## License

No license has been specified yet. Unless a license is added, others should not assume they have permission to reuse, modify, or redistribute this project.
