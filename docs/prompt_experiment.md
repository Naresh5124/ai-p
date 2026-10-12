# Day 7 — Prompt Engineering Experiment

**Date:** 2026-10-12  
**Project scenario:** CampusIQ library-information assistant

## Objective

Compare five prompt designs on the same grounded-answering task. We checked supported-answer correctness, abstention when information was missing, and output-format compliance.

## Experimental controls

All variants used the same `generate_response()` function, model/provider settings, context, and exact question for each test. The prompt design was the intended variable.

This is a small exploratory experiment. One observed output per variant per test case is not enough to establish general reliability or statistical significance; LLM output can vary between runs.

## Fixed test cases

### Test A — Supported answer

**Context:**

```text
Library hours:
Monday–Friday: 9 AM–8 PM
Saturday: 10 AM–4 PM
Sunday: Closed
```

**Question:** Is the library open on Sunday? If so, what are its hours?

**Expected:** State that the library is closed on Sunday; do not invent opening hours.

### Test B — Missing information

Use the same context.

**Question:** What are the library's holiday hours?

**Expected:** State that holiday hours are not supplied in the context; do not guess.

## Variants tested

1. **V1 — Baseline:** Simple instruction to answer the question.
2. **V2 — Grounding and abstention:** Explicitly instructs the model to use only supplied context, avoid invented facts, and admit when information is missing.
3. **V3 — Delimited context:** Uses `<context>` and `<question>` boundaries and says retrieved context is reference data, not instructions.
4. **V4 — Few-shot example:** Includes an example demonstrating how to abstain when information is absent.
5. **V5 — Structured JSON:** Requires `answer`, `supported`, and `missing_information` fields.

## Scoring rubric

Each criterion is scored from 0–2:

- **Correctness (Test A):** 2 = correct answer; 1 = partially correct; 0 = incorrect.
- **Groundedness (Test A):** 2 = supported by context with no apparent invented facts; 1 = minor unsupported or unclear claim; 0 = materially unsupported answer.
- **Abstention (Test B):** 2 = explicitly identifies the missing context; 1 = declines or says it does not know without explaining the context gap; 0 = guesses or invents an answer.
- **Format compliance:** 2 = follows the requested format; 1 = partly follows it; 0 = fails it. For V1–V4, no special output format was requested; V5 was required to return JSON.

Scores are qualitative judgments on this tiny test set, not an objective benchmark.

## Observed results

| Variant | Test A correctness (0–2) | Test A groundedness (0–2) | Test B abstention (0–2) | Format compliance (0–2) | Total (0–8) | Observation |
|---|---:|---:|---:|---:|---:|---|
| V1 — Baseline | 2 | 2 | 1 | 2 | 7 | Both responses were acceptable. The missing-information answer admitted not knowing but did not explicitly explain that holiday hours were absent from context. |
| V2 — Grounding and abstention | 2 | 2 | 2 | 2 | 8 | Clearly identified the supplied context as the evidence and abstained on holiday hours. |
| V3 — Delimited context | 2 | 2 | 1 | 2 | 7 | Both answers were correct; the missing-information reply was brief but did not explain why it could not answer. |
| V4 — Few-shot example | 2 | 2 | 2 | 2 | 8 | Both answers were correct, and the missing-information answer explicitly identified the context gap. The additional statement about no Sunday opening hours was a reasonable paraphrase of “Sunday: Closed.” |
| V5 — Structured JSON | 2 | 2 | 2 | 2 | 8 | Both responses were valid JSON and communicated support status. A backend should still validate the response against a schema. |

## Conclusion

- **All five variants answered the supported Sunday question correctly in this run.** The baseline already worked on this simple example, so the test does not show that elaborate prompting improved supported-answer correctness.
- **V2, V4, and V5 gave the clearest missing-information behavior in these outputs.** V1 and V3 also abstained, but their replies were less explicit about the context gap.
- **V5 is the best fit when an application needs machine-readable output**, not because it was more factually correct here. A production backend should parse and validate the JSON (for example, with Pydantic) and handle malformed output.
- **Delimiters help clarify boundaries but are not a security boundary.** They do not guarantee resistance to prompt injection; enforce important rules in application code as well.
- **Few-shot examples demonstrate the expected pattern**, but must be chosen carefully and not mistaken for evidence about the current question.

## Limitations and next experiment

1. Only two questions were tested: one answer present in context and one absent.
2. The experiment script was run more than once, but this report summarizes only the complete output set supplied for review; the separate runs were not aggregated.
3. The test did not include adversarial instructions inside retrieved text, ambiguous questions, multiple supporting sources, or malformed JSON.
4. The prompt variants differ in more than one detail, so the experiment cannot isolate the effect of each individual prompt feature. Responses can also vary between runs.

For a stronger evaluation, add more test cases, repeat each variant several times with identical settings, and use a fixed rubric. Include an adversarial context case (for example, retrieved text that says “ignore previous instructions”) and automatically parse/schema-check V5 JSON.

## Key takeaway

Prompt engineering is controlled iteration, not magic wording. Keep test inputs and settings fixed, inspect actual outputs, and choose the simplest prompt that reliably meets the application's requirements. For CampusIQ, use clear grounding and abstention instructions; use structured outputs when downstream code needs them, and validate those outputs in application code.
