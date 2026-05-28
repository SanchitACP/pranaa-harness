import json
import os
import anthropic
from schemas import ClinicalIntake
from ground_truth import GROUND_TRUTH

SYSTEM_PROMPT = """\
You are a clinical intake extraction assistant. Given a patient–medical assistant conversation transcript, extract structured clinical data.

Rules:
- Every extracted value MUST include a verbatim evidence_quote from the transcript.
- If a value cannot be found or is ambiguous, omit it and add a Gap entry.
- Never hallucinate or infer values not stated in the transcript.
- For gaps, write a concrete suggested_followup question the MA should ask next.
- Return only valid JSON matching the schema. No prose.

Schema:
{
  "patient_name": "string or null",
  "date_of_birth": "string or null",
  "chief_complaint": {"value": "string", "evidence_quote": "string"},
  "symptoms": [{"description": "string", "onset": "string|null", "duration": "string|null", "severity": "string|null", "evidence_quote": "string"}],
  "medications": [{"name": "string", "dose": "string|null", "frequency": "string|null", "evidence_quote": "string"}],
  "allergies": [{"substance": "string", "reaction": "string|null", "status": "confirmed|suspected|unconfirmed|unknown", "evidence_quote": "string"}],
  "medical_history": [{"value": "string", "evidence_quote": "string"}],
  "vitals": {"blood_pressure": "string|null", "heart_rate": "string|null", "temperature": "string|null", "weight": "string|null", "height": "string|null", "oxygen_saturation": "string|null"},
  "gaps": [{"field": "string", "reason": "string", "suggested_followup": "string"}]
}
"""

FAKE_TRANSCRIPT = """\
MA: Hi, I'm Maria, I'll be helping with your intake today. Can I get your name?
Patient: Sure, I'm James Holloway.
MA: Date of birth?
Patient: March 4th, 1978.
MA: What brings you in today?
Patient: I've had this really bad headache for the past three days. It's mostly on the left side.
MA: On a scale of 1 to 10 how bad is the pain?
Patient: Like a 7 most of the time, but it spikes to a 9.
MA: Any nausea or sensitivity to light?
Patient: Yeah, lights really bother me. No vomiting though.
MA: Are you on any medications?
Patient: I take metformin for diabetes. And I started taking ibuprofen for the headache — not sure of the dose, whatever's in the bottle.
MA: Any allergies?
Patient: Penicillin. I break out in hives.
MA: Any other medical history I should know about?
Patient: I have type 2 diabetes, diagnosed about six years ago. And hypertension, but I don't take anything for that right now.
MA: We'll get your vitals in a moment — the nurse will do blood pressure and weight.
"""


def extract_intake(transcript: str) -> ClinicalIntake:
    key = transcript.strip()

    # Offline mode: use pre-computed ground truth if no API key is available
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        if key in GROUND_TRUTH:
            return ClinicalIntake.model_validate(GROUND_TRUTH[key])
        raise ValueError(
            "No ANTHROPIC_API_KEY set. Custom transcripts require an API key. "
            "Use one of the four built-in transcripts to run without a key."
        )

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Transcript:\n{transcript}"}],
    )

    raw = response.content[0].text
    data = json.loads(raw)
    return ClinicalIntake.model_validate(data)


if __name__ == "__main__":
    intake = extract_intake(FAKE_TRANSCRIPT)
    print(intake.model_dump_json(indent=2))
