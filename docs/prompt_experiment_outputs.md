# Day 7 — Prompt Experiment Outputs

Run time: 2026-10-12T22:29+05:30

These are raw model outputs, not scores or conclusions.
All variants used the same `generate_response()` function and the same fixed context.

Context:

```text
Library hours:
Monday–Friday: 9 AM–8 PM
Saturday: 10 AM–4 PM
Sunday: Closed
```

## V1 — Baseline

### Test A — Supported answer

**Question:** Is the library open on Sunday? If so, what are its hours?

**Model output:**

No. The library is closed on Sundays.

### Test B — Missing information

**Question:** What are the library's holiday hours?

**Model output:**

I’m sorry, but I don’t have that information.

---

## V2 — Grounding and abstention

### Test A — Supported answer

**Question:** Is the library open on Sunday? If so, what are its hours?

**Model output:**

The library is closed on Sunday.

### Test B — Missing information

**Question:** What are the library's holiday hours?

**Model output:**

I’m sorry, but that information isn’t provided in the supplied context.

---

## V3 — Delimited context

### Test A — Supported answer

**Question:** Is the library open on Sunday? If so, what are its hours?

**Model output:**

The library is **closed on Sunday**.

### Test B — Missing information

**Question:** What are the library's holiday hours?

**Model output:**

The information is unavailable.

---

## V4 — Few-shot example

### Test A — Supported answer

**Question:** Is the library open on Sunday? If so, what are its hours?

**Model output:**

The library is **closed on Sunday**. It does not have any opening hours for that day.

### Test B — Missing information

**Question:** What are the library's holiday hours?

**Model output:**

The supplied context does not specify the library’s holiday hours, so I cannot provide that information.

---

## V5 — Structured JSON

### Test A — Supported answer

**Question:** Is the library open on Sunday? If so, what are its hours?

**Model output:**

{"answer":"No, the library is closed on Sunday.","supported":true,"missing_information":null}

### Test B — Missing information

**Question:** What are the library's holiday hours?

**Model output:**

{"answer":"I don't have that information.","supported":false,"missing_information":"Holiday hours are not mentioned in the supplied context."}

---
