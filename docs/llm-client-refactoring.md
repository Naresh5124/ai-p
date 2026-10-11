## Day 6 — LLM Client Refactoring

### Objective
Separate LLM provider-specific code from the Mini RAG pipeline to improve modularity and maintainability.

### What I Built
- Created `llm_client.py` to manage Groq client initialization, API requests, and response extraction.
- Implemented `generate_response(prompt: str) -> str` as a reusable LLM interface.
- Updated `main.py` to construct the prompt and call `generate_response()`.
- Preserved ChromaDB retrieval, cosine-distance filtering, and source reporting.

### Architecture
- `main.py`: document embeddings, retrieval, relevance filtering, prompt construction, and source handling.
- `llm_client.py`: API key loading, Groq client setup, model configuration, and answer generation.

### Concepts Learned
- Python imports and module separation.
- Client objects, classes, constructors, and keyword arguments.
- Environment variables and API key management.
- Chat message roles: `system` and `user`.
- Extracting answer text from an API response object.
- Completion-token limits and basic input validation.

### Testing
Tested the application with:
1. A known deadlock question.
2. A paraphrased question.
3. An unsupported question.

All three tests produced the expected behavior in my run.

### Key Takeaway
The RAG pipeline now uses a provider-independent function interface. Changing providers may still require modifications to `llm_client.py`, but the retrieval pipeline does not need to manage provider-specific API calls.
