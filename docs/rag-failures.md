# RAG Failure Analysis

## Objective

Investigate retrieval quality and answer grounding in the Day 4 Mini RAG application using a small, manually written knowledge base of 12 computer science chunks.

## System under test

- Embedding model: `all-MiniLM-L6-v2`
- Vector store: ChromaDB
- Distance metric: cosine distance
- Retrieval: top 3 chunks
- Generation: Groq chat completion
- Experimental relevance threshold: `0.50`

## Experiment 1: Exact-match question

**Question:** What are the four necessary conditions for deadlock?

**Observed retrieval before filtering:**

| Rank | Topic          | Cosine distance |
| ---: | -------------- | --------------: |
|    1 | Deadlocks      |          0.2308 |
|    2 | ACID           |          0.6354 |
|    3 | CPU Scheduling |          0.7005 |

**Observation:** The relevant Deadlocks chunk ranked first, while the other two chunks were unnecessary for answering the question.

**Result after filtering:** Only the Deadlocks chunk passed the threshold. The answer correctly identified all four conditions.

**Finding:** Top-k retrieval can return irrelevant chunks even when the most relevant chunk ranks first.

## Experiment 2: Paraphrased question

**Question:** Why might processes be stuck waiting forever for resources?

**Observed retrieval before filtering:**

| Rank | Topic          | Cosine distance |
| ---: | -------------- | --------------: |
|    1 | Deadlocks      |          0.4393 |
|    2 | CPU Scheduling |          0.6336 |
|    3 | Semaphores     |          0.6484 |

**Observation:** The retriever found the correct Deadlocks chunk despite different wording.

**Result after filtering:** Only the Deadlocks chunk passed the threshold. The LLM produced an appropriate high-level answer but expanded on the four conditions beyond what the retrieved chunk explicitly stated.

**Finding:** Semantic retrieval handled this paraphrase, but the generated answer was not fully supported by the supplied evidence.

## Experiment 3: Question absent from the knowledge base

**Question:** What is the capital of Japan?

**Observed retrieval before filtering:**

| Rank | Topic            | Cosine distance |
| ---: | ---------------- | --------------: |
|    1 | Semaphores       |          0.9418 |
|    2 | Database Indexes |          0.9467 |
|    3 | TCP              |          0.9726 |

**Observation:** None of the retrieved chunks contained the answer.

**Result after filtering:** No chunks passed the threshold. The application abstained without calling the LLM.

**Finding:** Top-k retrieval always returns the nearest available chunks unless the application adds a relevance check. Filtering can prevent irrelevant context from reaching the generator.

## Limitations

- Only three questions were tested.
- The threshold of `0.50` is provisional and is not a universal relevance boundary.
- Distances are similarity signals, not probabilities or guarantees of relevance.
- A correct-looking answer does not prove that every claim is supported by the retrieved context.
- More evaluation questions are needed to measure false rejection of relevant chunks and acceptance of irrelevant chunks.

## Potential improvements

1. Build a larger evaluation set with known relevant sources and questions whose answers are absent from the knowledge base.
2. Tune the relevance threshold against that evaluation set rather than choosing it from a few examples.
3. Improve grounding by checking generated claims against retrieved evidence and evaluating abstention behavior.
4. Track retrieval quality separately from answer quality.

## Conclusion

The experimental threshold improved the tested cases by filtering out irrelevant chunks. However, these results are preliminary. The next step is broader evaluation to determine whether the threshold generalizes and whether generated answers remain faithful to the retrieved evidence.
