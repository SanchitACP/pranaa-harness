import os
import json
import streamlit as st
from extractor import extract_intake
from evaluator import evaluate
from fhir_export import to_fhir_bundle
from transcripts import TRANSCRIPTS

st.set_page_config(
    page_title="Praana Intake Harness",
    layout="wide",
)

st.title("Praana Intake Reliability Harness")
st.caption("GenAI QA system for ambient clinical intake — synthetic data only, no PHI")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Transcript Input")

    mode = st.radio("Source", ["Built-in examples", "Paste custom"], horizontal=True)

    if mode == "Built-in examples":
        selected_name = st.selectbox("Select transcript", list(TRANSCRIPTS.keys()))
        transcript_text: str = TRANSCRIPTS[selected_name]
    else:
        selected_name = "Custom"
        transcript_text = st.text_area(
            "Paste transcript",
            height=250,
            placeholder="MA: Hello, can I get your name?\nPatient: ...",
        )

    if transcript_text and transcript_text.strip():
        with st.expander("View raw transcript"):
            st.text(transcript_text.strip())

    st.divider()

    if os.environ.get("ANTHROPIC_API_KEY"):
        st.success("API key set — live extraction enabled")
    else:
        if mode == "Built-in examples":
            st.info("Running on pre-computed results (no API key needed for built-in transcripts)")
        else:
            st.warning("Custom transcripts require ANTHROPIC_API_KEY")

    can_run = bool(transcript_text and transcript_text.strip())
    run_btn = st.button(
        "Extract & Evaluate",
        type="primary",
        use_container_width=True,
        disabled=not can_run,
    )

# ── Session state ─────────────────────────────────────────────────────────────
for key in ("intake", "result", "fhir", "last_key", "error"):
    if key not in st.session_state:
        st.session_state[key] = None

# ── Run extraction ────────────────────────────────────────────────────────────
if run_btn and can_run:
    cache_key = transcript_text.strip()
    if cache_key != st.session_state.last_key:
        with st.spinner("Running extraction with Claude..."):
            try:
                intake = extract_intake(transcript_text)
                result = evaluate(intake)
                fhir_bundle = to_fhir_bundle(intake)
                st.session_state.intake = intake
                st.session_state.result = result
                st.session_state.fhir = fhir_bundle
                st.session_state.last_key = cache_key
                st.session_state.error = None
            except KeyError as e:
                st.session_state.error = f"Missing environment variable: {e}. Make sure ANTHROPIC_API_KEY is set."
            except Exception as e:
                st.session_state.error = f"Extraction failed: {e}"

if st.session_state.error:
    st.error(st.session_state.error)

intake = st.session_state.intake
result = st.session_state.result
fhir_bundle = st.session_state.fhir

# ── Results ───────────────────────────────────────────────────────────────────
if intake and result:

    # Summary metrics
    c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 1, 1])
    with c1:
        st.markdown("**Patient**")
        st.markdown(f"### {intake.patient_name or '—'}")
    with c2:
        st.markdown("**DOB**")
        st.markdown(f"### {intake.date_of_birth or '—'}")
    c3.metric("Score", f"{result.overall_score:.0f} / 100")
    c4.metric("Evidence Coverage", f"{result.evidence_coverage:.0%}")
    c5.metric("Gaps Flagged", result.gap_count)

    st.divider()

    tab_chart, tab_gaps, tab_score, tab_fhir = st.tabs([
        "Chart Data",
        f"Gaps & Follow-ups  ({result.gap_count})",
        "Evaluator Score",
        "FHIR Export",
    ])

    # ── Tab: Chart Data ───────────────────────────────────────────────────────
    with tab_chart:

        st.subheader("Chief Complaint")
        st.markdown(f"**{intake.chief_complaint.value}**")
        st.caption(f'Evidence: "{intake.chief_complaint.evidence_quote}"')

        st.subheader(f"Symptoms ({len(intake.symptoms)})")
        if intake.symptoms:
            for s in intake.symptoms:
                label = s.description
                if s.severity:
                    label += f"  —  severity: {s.severity}"
                with st.expander(label):
                    col_a, col_b, col_c = st.columns(3)
                    col_a.write(f"**Onset:** {s.onset or '—'}")
                    col_b.write(f"**Duration:** {s.duration or '—'}")
                    col_c.write(f"**Severity:** {s.severity or '—'}")
                    st.caption(f'Evidence: "{s.evidence_quote}"')
        else:
            st.info("No symptoms extracted.")

        st.subheader(f"Medications ({len(intake.medications)})")
        if intake.medications:
            for med in intake.medications:
                with st.expander(med.name):
                    col_a, col_b = st.columns(2)
                    col_a.write(f"**Dose:** {med.dose or '—'}")
                    col_b.write(f"**Frequency:** {med.frequency or '—'}")
                    st.caption(f'Evidence: "{med.evidence_quote}"')
        else:
            st.info("No medications extracted.")

        st.subheader(f"Allergies ({len(intake.allergies)})")
        if intake.allergies:
            STATUS_ICON = {
                "confirmed": "✅",
                "suspected": "⚠️",
                "unconfirmed": "❓",
                "unknown": "❓",
            }
            for al in intake.allergies:
                icon = STATUS_ICON.get(al.status.value, "❓")
                with st.expander(f"{icon} {al.substance}"):
                    col_a, col_b = st.columns(2)
                    col_a.write(f"**Reaction:** {al.reaction or '—'}")
                    col_b.write(f"**Status:** {al.status.value}")
                    st.caption(f'Evidence: "{al.evidence_quote}"')
        else:
            st.info("No allergies extracted.")

        st.subheader("Vitals")
        v = intake.vitals
        vc = st.columns(6)
        vc[0].metric("Blood Pressure", v.blood_pressure or "—")
        vc[1].metric("Heart Rate", v.heart_rate or "—")
        vc[2].metric("Temperature", v.temperature or "—")
        vc[3].metric("Weight", v.weight or "—")
        vc[4].metric("Height", v.height or "—")
        vc[5].metric("O₂ Sat", v.oxygen_saturation or "—")

        st.subheader(f"Medical History ({len(intake.medical_history)})")
        if intake.medical_history:
            for hist in intake.medical_history:
                st.markdown(f"- **{hist.value}**")
                st.caption(f'  Evidence: "{hist.evidence_quote}"')
        else:
            st.info("No medical history extracted.")

    # ── Tab: Gaps ─────────────────────────────────────────────────────────────
    with tab_gaps:
        if intake.gaps:
            st.warning(
                f"{len(intake.gaps)} gap(s) detected — missing or ambiguous fields the MA should follow up on."
            )
            for i, gap in enumerate(intake.gaps, 1):
                st.markdown(f"**Gap {i}: `{gap.field}`**")
                st.markdown(f"Reason: {gap.reason}")
                st.info(f'Suggested follow-up: *"{gap.suggested_followup}"*')
                if i < len(intake.gaps):
                    st.divider()
        else:
            st.success("No gaps detected. All critical fields are populated.")

    # ── Tab: Score ────────────────────────────────────────────────────────────
    with tab_score:
        st.subheader("Evaluator Score Breakdown")

        col_left, col_right = st.columns(2)

        with col_left:
            st.metric("Overall Score", f"{result.overall_score:.0f} / 100")
            st.progress(result.overall_score / 100)
            st.write("")

            st.write("**Evidence Coverage**")
            st.caption("Percentage of extracted fields backed by a verbatim transcript quote")
            st.progress(result.evidence_coverage)
            st.write(f"{result.evidence_coverage:.0%}")
            st.write("")

            st.write("**Completeness**")
            st.caption("Percentage of required fields (name, DOB, chief complaint, symptoms) populated")
            st.progress(result.completeness_score)
            st.write(f"{result.completeness_score:.0%}")

        with col_right:
            st.metric("Gaps Flagged", result.gap_count)
            st.metric("Schema Valid", "Yes" if result.schema_valid else "No")
            st.write("")

            if result.missing_required:
                st.write("**Missing required fields:**")
                for f in result.missing_required:
                    st.markdown(f"- `{f}`")
            else:
                st.success("All required fields present")

        st.divider()
        st.caption(
            "Score formula: Evidence Coverage × 50 + Completeness × 30 + Gap Score × 20. "
            "Gap score starts at 100% and loses 10 points per flagged gap."
        )

    # ── Tab: FHIR ─────────────────────────────────────────────────────────────
    with tab_fhir:
        st.subheader("FHIR R4 Bundle")
        st.caption(
            "SMART on FHIR-compatible export — structured for eClinicalWorks, athenahealth, "
            "and other FHIR R4 EMRs. Resources: Patient, Encounter, Condition, "
            "MedicationStatement, AllergyIntolerance, Observation (vitals)."
        )

        fhir_json = json.dumps(fhir_bundle, indent=2)

        st.download_button(
            "Download FHIR Bundle (.json)",
            data=fhir_json,
            file_name=f"intake_{(intake.patient_name or 'patient').replace(' ', '_').lower()}.fhir.json",
            mime="application/json",
        )

        st.code(fhir_json, language="json")

# ── Welcome state ─────────────────────────────────────────────────────────────
else:
    if not st.session_state.error:
        st.markdown("""
### How it works

1. **Select** a synthetic transcript from the sidebar (or paste your own)
2. **Click Extract & Evaluate** — Claude extracts structured clinical data from the conversation
3. **Review** the chart data with transcript evidence citations, gap flags, and QA score
4. **Export** FHIR R4-compatible JSON for EMR handoff

---

**What gets extracted**

| Field | Evidence required |
|---|---|
| Chief complaint | Yes |
| Symptoms (onset, duration, severity) | Yes |
| Medications (name, dose, frequency) | Yes |
| Allergies (substance, reaction, status) | Yes |
| Medical history | Yes |
| Vitals | — |
| Gaps + suggested follow-up questions | — |

---

*All data is synthetic. No PHI. No diagnosis or treatment recommendations.*
        """)
