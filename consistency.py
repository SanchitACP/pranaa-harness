from __future__ import annotations
from dataclasses import dataclass
from difflib import SequenceMatcher
from extractor import extract_intake
from schemas import ClinicalIntake


def _quote_similarity(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _min_pairwise_similarity(quotes: list[str]) -> float:
    if len(quotes) < 2:
        return 1.0
    pairs = [
        _quote_similarity(quotes[i], quotes[j])
        for i in range(len(quotes))
        for j in range(i + 1, len(quotes))
    ]
    return min(pairs)


QUOTE_THRESHOLD = 0.75


@dataclass
class FieldResult:
    values: list[str]
    quotes: list[str]

    @property
    def value_consistent(self) -> bool:
        return len(set(self.values)) == 1

    @property
    def quote_similarity(self) -> float:
        return _min_pairwise_similarity(self.quotes)

    @property
    def quote_consistent(self) -> bool:
        return self.quote_similarity >= QUOTE_THRESHOLD

    @property
    def consistent(self) -> bool:
        return self.quote_consistent


@dataclass
class ConsistencyReport:
    n_runs: int
    fields: dict[str, FieldResult]

    @property
    def consistent_count(self) -> int:
        return sum(1 for f in self.fields.values() if f.consistent)

    @property
    def inconsistent_count(self) -> int:
        return sum(1 for f in self.fields.values() if not f.consistent)

    @property
    def consistency_rate(self) -> float:
        if not self.fields:
            return 1.0
        return self.consistent_count / len(self.fields)


def _flatten_intake(intake: ClinicalIntake) -> tuple[dict[str, str], dict[str, str]]:
    values: dict[str, str] = {}
    quotes: dict[str, str] = {}

    values["patient_name"] = intake.patient_name or ""
    quotes["patient_name"] = ""

    values["date_of_birth"] = intake.date_of_birth or ""
    quotes["date_of_birth"] = ""

    values["chief_complaint"] = intake.chief_complaint.value
    quotes["chief_complaint"] = intake.chief_complaint.evidence_quote

    for i, s in enumerate(intake.symptoms):
        values[f"symptom[{i}].description"] = s.description
        quotes[f"symptom[{i}].description"] = s.evidence_quote
        values[f"symptom[{i}].onset"] = s.onset or ""
        quotes[f"symptom[{i}].onset"] = s.evidence_quote
        values[f"symptom[{i}].duration"] = s.duration or ""
        quotes[f"symptom[{i}].duration"] = s.evidence_quote
        values[f"symptom[{i}].severity"] = s.severity or ""
        quotes[f"symptom[{i}].severity"] = s.evidence_quote

    for i, m in enumerate(intake.medications):
        values[f"medication[{i}].name"] = m.name
        quotes[f"medication[{i}].name"] = m.evidence_quote
        values[f"medication[{i}].dose"] = m.dose or ""
        quotes[f"medication[{i}].dose"] = m.evidence_quote
        values[f"medication[{i}].frequency"] = m.frequency or ""
        quotes[f"medication[{i}].frequency"] = m.evidence_quote

    for i, a in enumerate(intake.allergies):
        values[f"allergy[{i}].substance"] = a.substance
        quotes[f"allergy[{i}].substance"] = a.evidence_quote
        values[f"allergy[{i}].reaction"] = a.reaction or ""
        quotes[f"allergy[{i}].reaction"] = a.evidence_quote
        values[f"allergy[{i}].status"] = a.status.value
        quotes[f"allergy[{i}].status"] = a.evidence_quote

    for i, h in enumerate(intake.medical_history):
        values[f"history[{i}].value"] = h.value
        quotes[f"history[{i}].value"] = h.evidence_quote

    values["vitals.blood_pressure"] = intake.vitals.blood_pressure or ""
    quotes["vitals.blood_pressure"] = ""
    values["vitals.heart_rate"] = intake.vitals.heart_rate or ""
    quotes["vitals.heart_rate"] = ""
    values["vitals.temperature"] = intake.vitals.temperature or ""
    quotes["vitals.temperature"] = ""
    values["vitals.weight"] = intake.vitals.weight or ""
    quotes["vitals.weight"] = ""
    values["vitals.height"] = intake.vitals.height or ""
    quotes["vitals.height"] = ""
    values["vitals.oxygen_saturation"] = intake.vitals.oxygen_saturation or ""
    quotes["vitals.oxygen_saturation"] = ""

    values["gap_count"] = str(len(intake.gaps))
    quotes["gap_count"] = ""

    return values, quotes


def run_consistency_test(transcript: str, n: int = 5) -> tuple[ConsistencyReport, list[str]]:
    all_values: dict[str, list[str]] = {}
    all_quotes: dict[str, list[str]] = {}
    errors: list[str] = []

    for i in range(n):
        try:
            intake = extract_intake(transcript)
            values, quotes = _flatten_intake(intake)
            for key, val in values.items():
                all_values.setdefault(key, []).append(val)
            for key, q in quotes.items():
                all_quotes.setdefault(key, []).append(q)
        except Exception as e:
            errors.append(f"Run {i + 1} failed: {e}")

    field_results = {
        key: FieldResult(values=all_values[key], quotes=all_quotes.get(key, []))
        for key in all_values
    }
    report = ConsistencyReport(n_runs=n, fields=field_results)
    return report, errors
