from __future__ import annotations
from dataclasses import dataclass, field
from schemas import ClinicalIntake


@dataclass
class EvaluatorResult:
    evidence_coverage: float
    completeness_score: float
    gap_count: int
    schema_valid: bool
    overall_score: float
    missing_required: list[str]


def evaluate(intake: ClinicalIntake) -> EvaluatorResult:
    evidence_fields = 0
    total_evidence_fields = 0

    total_evidence_fields += 1
    if intake.chief_complaint.evidence_quote:
        evidence_fields += 1

    for s in intake.symptoms:
        total_evidence_fields += 1
        if s.evidence_quote:
            evidence_fields += 1

    for m in intake.medications:
        total_evidence_fields += 1
        if m.evidence_quote:
            evidence_fields += 1

    for a in intake.allergies:
        total_evidence_fields += 1
        if a.evidence_quote:
            evidence_fields += 1

    for h in intake.medical_history:
        total_evidence_fields += 1
        if h.evidence_quote:
            evidence_fields += 1

    evidence_coverage = evidence_fields / total_evidence_fields if total_evidence_fields > 0 else 1.0

    missing_required: list[str] = []
    if not intake.patient_name:
        missing_required.append("patient_name")
    if not intake.date_of_birth:
        missing_required.append("date_of_birth")
    if not intake.chief_complaint:
        missing_required.append("chief_complaint")
    if not intake.symptoms:
        missing_required.append("symptoms")

    completeness_score = 1.0 - len(missing_required) / 4

    # -10 pts per gap, floored at 0
    gap_score = max(0.0, 1.0 - len(intake.gaps) * 0.1)

    overall_score = evidence_coverage * 50 + completeness_score * 30 + gap_score * 20

    return EvaluatorResult(
        evidence_coverage=evidence_coverage,
        completeness_score=completeness_score,
        gap_count=len(intake.gaps),
        schema_valid=True,
        overall_score=overall_score,
        missing_required=missing_required,
    )
