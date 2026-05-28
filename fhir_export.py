from __future__ import annotations
import uuid
from datetime import datetime, timezone
from schemas import ClinicalIntake


def _uid() -> str:
    return str(uuid.uuid4())


def to_fhir_bundle(intake: ClinicalIntake) -> dict:
    patient_id = _uid()
    encounter_id = _uid()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    entries: list[dict] = []

    # Patient
    patient: dict = {
        "resourceType": "Patient",
        "id": patient_id,
        "meta": {"lastUpdated": now},
    }
    if intake.patient_name:
        patient["name"] = [{"text": intake.patient_name}]
    if intake.date_of_birth:
        patient["birthDate"] = intake.date_of_birth
    entries.append({"fullUrl": f"urn:uuid:{patient_id}", "resource": patient})

    # Encounter
    encounter: dict = {
        "resourceType": "Encounter",
        "id": encounter_id,
        "status": "in-progress",
        "class": {"code": "AMB", "display": "ambulatory"},
        "subject": {"reference": f"Patient/{patient_id}"},
    }
    if intake.chief_complaint:
        encounter["reasonCode"] = [{"text": intake.chief_complaint.value}]
    entries.append({"fullUrl": f"urn:uuid:{encounter_id}", "resource": encounter})

    # Chief complaint as Condition
    if intake.chief_complaint:
        cid = _uid()
        entries.append({
            "fullUrl": f"urn:uuid:{cid}",
            "resource": {
                "resourceType": "Condition",
                "id": cid,
                "clinicalStatus": {"coding": [{"code": "active"}]},
                "category": [{"coding": [{"code": "encounter-diagnosis"}]}],
                "code": {"text": intake.chief_complaint.value},
                "subject": {"reference": f"Patient/{patient_id}"},
                "encounter": {"reference": f"Encounter/{encounter_id}"},
            },
        })

    # Symptoms as Conditions
    for symptom in intake.symptoms:
        cid = _uid()
        cond: dict = {
            "resourceType": "Condition",
            "id": cid,
            "clinicalStatus": {"coding": [{"code": "active"}]},
            "category": [{"coding": [{"code": "problem-list-item"}]}],
            "code": {"text": symptom.description},
            "subject": {"reference": f"Patient/{patient_id}"},
        }
        notes = []
        if symptom.onset:
            notes.append(f"Onset: {symptom.onset}")
        if symptom.duration:
            notes.append(f"Duration: {symptom.duration}")
        if symptom.severity:
            notes.append(f"Severity: {symptom.severity}")
        if notes:
            cond["note"] = [{"text": "; ".join(notes)}]
        entries.append({"fullUrl": f"urn:uuid:{cid}", "resource": cond})

    # Medications as MedicationStatement
    for med in intake.medications:
        mid = _uid()
        med_res: dict = {
            "resourceType": "MedicationStatement",
            "id": mid,
            "status": "active",
            "medicationCodeableConcept": {"text": med.name},
            "subject": {"reference": f"Patient/{patient_id}"},
        }
        dosage: dict = {}
        if med.dose:
            dosage["text"] = med.dose
        if med.frequency:
            dosage["timing"] = {"code": {"text": med.frequency}}
        if dosage:
            med_res["dosage"] = [dosage]
        entries.append({"fullUrl": f"urn:uuid:{mid}", "resource": med_res})

    # Allergies as AllergyIntolerance
    for allergy in intake.allergies:
        aid = _uid()
        al_res: dict = {
            "resourceType": "AllergyIntolerance",
            "id": aid,
            "verificationStatus": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                    "code": allergy.status.value,
                }]
            },
            "code": {"text": allergy.substance},
            "patient": {"reference": f"Patient/{patient_id}"},
        }
        if allergy.reaction:
            al_res["reaction"] = [{"description": allergy.reaction}]
        entries.append({"fullUrl": f"urn:uuid:{aid}", "resource": al_res})

    # Medical history as Conditions
    for hist in intake.medical_history:
        cid = _uid()
        entries.append({
            "fullUrl": f"urn:uuid:{cid}",
            "resource": {
                "resourceType": "Condition",
                "id": cid,
                "clinicalStatus": {"coding": [{"code": "active"}]},
                "category": [{"coding": [{"code": "problem-list-item"}]}],
                "code": {"text": hist.value},
                "subject": {"reference": f"Patient/{patient_id}"},
            },
        })

    # Vitals as Observations
    LOINC: dict[str, tuple[str, str]] = {
        "blood_pressure": ("55284-4", "Blood Pressure"),
        "heart_rate": ("8867-4", "Heart Rate"),
        "temperature": ("8310-5", "Body Temperature"),
        "weight": ("29463-7", "Body Weight"),
        "height": ("8302-2", "Body Height"),
        "oxygen_saturation": ("59408-5", "Oxygen Saturation"),
    }
    for field_name, (loinc_code, display) in LOINC.items():
        val = getattr(intake.vitals, field_name)
        if val:
            oid = _uid()
            entries.append({
                "fullUrl": f"urn:uuid:{oid}",
                "resource": {
                    "resourceType": "Observation",
                    "id": oid,
                    "status": "preliminary",
                    "category": [{"coding": [{"code": "vital-signs"}]}],
                    "code": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": loinc_code,
                            "display": display,
                        }]
                    },
                    "subject": {"reference": f"Patient/{patient_id}"},
                    "encounter": {"reference": f"Encounter/{encounter_id}"},
                    "valueString": val,
                },
            })

    return {
        "resourceType": "Bundle",
        "id": _uid(),
        "type": "collection",
        "timestamp": now,
        "entry": entries,
    }
