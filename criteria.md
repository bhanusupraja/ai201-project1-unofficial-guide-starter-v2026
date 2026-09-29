# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
My corpus is short, student-written posts, so the useful fact is often contained in a single sentence. I picked 4 of 5 because one question is about a policy detail that appears in fewer documents than the others, so that one is naturally a little harder without making the target too loose.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
This setup is meant to be evidence-based, not an opaque model answer. In a document-grounded system, missing a source is a basic failure, and having all five answers cite a file is a realistic standard for this small corpus.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
The gate should be a strong filter on a small, focused corpus. I want a clean separation between in-corpus and out-of-corpus questions, and 4 of 5 leaves room for one edge case without allowing the system to drift into hallucination.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks read as a complete thought, with no sentence cut in half at either end.

**Why this target:**
The campus_life documents are short posts, so a chunk should keep the useful fact intact instead of slicing through a sentence. If the chunk boundaries break a thought in the middle, the retrieval layer can still find the right document but the answer becomes much less reliable.

---

## 5. Your choice

For at least 4 of my 5 in-corpus questions, the relevance gate does not refuse the question before the model answers it.

**Why this target:**
This matters because a good retrieval system should not over-reject questions that are actually covered by the corpus. The corpus is small and targeted, so a refusal on more than one in-corpus question would mean the cutoff is too strict rather than the retrieval being appropriately cautious.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
