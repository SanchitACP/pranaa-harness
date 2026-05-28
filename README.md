# Praana Intake Reliability Harness

A GenAI QA system that tests whether ambient clinical intake conversations can be reliably converted into accurate, evidence-backed, EMR-ready structured data.

Built as a prototype for a Praana Assist internship proposal.

## What it does

1. **Extracts** chief complaint, symptoms, medications, allergies, medical history, and vitals from a patient–MA conversation transcript
2. **Requires evidence** — every extracted field must be backed by a verbatim quote from the transcript ("no evidence, no field")
3. **Detects gaps** — missing medication doses, unconfirmed allergy status, unclear symptom duration, missing vitals, etc. — and suggests the next best follow-up question
4. **Scores** each extraction for evidence coverage, completeness, and gap risk
5. **Exports** a FHIR R4-compatible bundle (Patient, Encounter, Condition, MedicationStatement, AllergyIntolerance, Observation) ready for eClinicalWorks / athenahealth handoff

## Demo

Select one of four built-in synthetic transcripts (urgent care, primary care, med spa, concierge care) or paste your own, then click **Extract & Evaluate**.

The four built-in transcripts run on pre-computed results — no API key required. Custom transcripts require an Anthropic API key.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

To run live extraction on custom transcripts, set your Anthropic API key first:

```bash
export ANTHROPIC_API_KEY=sk-...   # Mac/Linux
$env:ANTHROPIC_API_KEY="sk-..."   # Windows PowerShell
```

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit dashboard |
| `extractor.py` | Claude-powered transcript → structured intake |
| `schemas.py` | Pydantic models for all extracted fields |
| `evaluator.py` | Scores extraction quality |
| `fhir_export.py` | Converts intake to FHIR R4 bundle |
| `transcripts.py` | Four synthetic intake transcripts |
| `ground_truth.py` | Pre-computed extractions for offline demo |

## Evaluator score

```
Score = Evidence Coverage × 50 + Completeness × 30 + Gap Score × 20
```

- **Evidence coverage** — % of fields backed by a verbatim transcript quote
- **Completeness** — % of required fields (name, DOB, chief complaint, symptoms) populated
- **Gap score** — starts at 100, loses 10 points per flagged gap

## Scope and safety

Synthetic data only. No PHI. No diagnosis. No treatment recommendations. No clinical decision-making. This project is about intake structuring, evidence grounding, QA, and EMR-readiness.
