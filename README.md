# The Unofficial Guide

By: Bhanusupraja | Corpus: campus_life

---

# Unit 1

## What This Does

This project indexes the `campus_life` corpus and answers questions about student life, registration, housing, and campus admin policies using the retrieved source documents. I chose this corpus because the documents are short, student-written, and usually center on a single fact or rule, which makes them a good fit for grounded retrieval and concise answers.

## Chunking Strategy

**Chunk size:** 450 characters
**Overlap:** 70 characters

I picked these numbers after reading the student posts in `campus_life`. Most documents are already one short paragraph and usually convey one complete thought in a sentence or two, so the generic 800-character split was not helpful: it left many posts unchanged and risked slicing only when a paragraph was especially dense. A 450-character cap keeps each post whole when it is already a single idea, while still letting longer records break on paragraph boundaries without chopping through the answer itself.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_exams.txt` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology — assessment

Four unit tests and a cumulative final. Not curved.

The unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_math_220_exams.txt` — produced by: `chunker.py::split_documents`

```
MATH 220 Linear Algebra — assessment

Two midterms and a cumulative final. Curved to a b- median.

The problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe.txt` — produced by: `chunker.py::split_documents`

```
The Ridgeway Café

Second-year here. Wait times: 10 to 15 minutes at 12:30, none after 2:00. The thing worth going for is the only place on campus with real espresso. The thing to know is that seating is tight; about 40 seats for a building of 900.

Hours are 7:00am to 4:00pm weekdays only. Costs declining balance only, no meal swipes.
```

**Chunk 5** — source: `housing_morrow_house.txt` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

The bad: known damp problem on the ground floor; two rooms were taken offline in 2024.
```

## Sample Answer

**Question:** Is the housing lottery random?

**Answer:**

```
The housing lottery is not entirely random in the way most people assume. While rising sophomores get a number drawn at random, juniors and seniors are ordered by accumulated credit hours first, with random tie-breaks used only afterward (admin_housing_lottery.txt).
```

**My relevance cutoff:**

I kept the default cutoff at `0.6` because the best in-corpus distances were all well below it and the out-of-scope distances were all well above it. The gap was clean enough to use without tightening the gate too much.

| Question | In corpus? | Best distance |
|---|---|---|
| Is the housing lottery random? | Yes | 0.2541 |
| When do the housing lottery numbers come out? | Yes | 0.3558 |
| How long does your student account stay active after graduation? | Yes | 0.3569 |
| Before registration, what do you need to do with your adviser? | Yes | 0.4986 |
| How are registration times assigned? | Yes | 0.4769 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9340 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8960 |

## How I Used AI

**1.** I asked an AI model to help me reason about the chunk-size problem for short posts, specifically whether a 800-character fixed window was still a good match for the `campus_life` documents. It suggested a paragraph-aware, shorter chunk size, and I changed the implementation to keep whole posts together unless they clearly held separate ideas.

**2.** I used AI to pressure-test my acceptance criteria by asking whether each sentence was observable and measurable without my interpretation. That helped me tighten the language so each criterion had a clear pass/fail test, especially the source-naming and out-of-scope gate rules.

---

# Unit 2

## Run Log — Before

I ran `python run_eval.py --label before` with the final chunker and threshold in place. The run log is in `results/run_2026-09-29_1537_before.md`, and it shows the in-corpus questions being answered while all five off-topic questions were refused by the gate.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. At least 4 of 5 sampled chunks read as a complete thought | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. For at least 4 of my 5 in-corpus questions, the gate does not refuse the question | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All five in-corpus questions produced answers from relevant chunks and stayed under the retrieval cutoff. |
| 2 | Every answer names a source | MET | The model cited a file name in the generated answer, and the retrieved sources matched the documents it used. |
| 3 | Gate stops out-of-corpus questions | MET | All five off-topic questions were refused with the “I don't have enough information...” gate. |
| 4 | Sampled chunks read as a complete thought | MET | The five chunks printed by `python app.py chunks -n 5` stayed on a single idea and did not cut through a sentence or topic. |
| 5 | In-corpus questions are not rejected by the gate | MET | The best retrieved distances for all five in-corpus questions were below the 0.6 cutoff, so the gate allowed them through. |

## Diagnoses

I did not miss any of the targets, so there was no failing diagnosis to repair. The root cause for the earlier generic chunking problem was not a model issue; it was that the default fixed-width chunker treated short student posts as if they were the same shape as long guides. The paragraph-aware approach improved that by keeping each post intact while still allowing longer pages to split cleanly.

## The Improvement

**What I changed:** I replaced the fixed-size splitter with a paragraph-aware chunker that keeps short posts intact and only splits on paragraph or sentence boundaries when a document is too long.

**Why I picked it:** The corpus is composed of short posts whose useful information is usually contained in one sentence or one short paragraph, so keeping each thought intact was the biggest improvement to the retrieval quality.

### Run Log — After

This run used the final chunker and cutoff after the milestone work was complete. Evidence is in the same `results/` directory, and the results were consistent with the target values above.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. At least 4 of 5 sampled chunks read as a complete thought | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. For at least 4 of my 5 in-corpus questions, the gate does not refuse the question | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
