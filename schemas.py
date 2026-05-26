from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AllergyStatus(str, Enum):
    confirmed = "confirmed"
    suspected = "suspected"
    unconfirmed = "unconfirmed"
    unknown = "unknown"


class EvidenceField(BaseModel):
    value: str
    evidence_quote: str = Field(
        description="Verbatim excerpt from transcript that supports this value"
    )


class Medication(BaseModel):
    name: str
    dose: Optional[str] = None
    frequency: Optional[str] = None
    evidence_quote: str


class Allergy(BaseModel):
    substance: str
    reaction: Optional[str] = None
    status: AllergyStatus = AllergyStatus.unknown
    evidence_quote: str


class Symptom(BaseModel):
    description: str
    onset: Optional[str] = None
    duration: Optional[str] = None
    severity: Optional[str] = None
    evidence_quote: str


class Vitals(BaseModel):
    blood_pressure: Optional[str] = None
    heart_rate: Optional[str] = None
    temperature: Optional[str] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    oxygen_saturation: Optional[str] = None


class Gap(BaseModel):
    field: str
    reason: str
    suggested_followup: str


class ClinicalIntake(BaseModel):
    patient_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    chief_complaint: EvidenceField
    symptoms: list[Symptom] = Field(default_factory=list)
    medications: list[Medication] = Field(default_factory=list)
    allergies: list[Allergy] = Field(default_factory=list)
    medical_history: list[EvidenceField] = Field(default_factory=list)
    vitals: Vitals = Field(default_factory=Vitals)
    gaps: list[Gap] = Field(default_factory=list)
