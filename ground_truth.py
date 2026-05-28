"""
Pre-computed ClinicalIntake extractions for the four built-in transcripts.
Keyed by stripped transcript text so extractor.py can do a fast lookup
and skip the API call entirely when no key is present.
"""
from transcripts import PRIMARY_CARE, URGENT_CARE, MED_SPA, CONCIERGE

GROUND_TRUTH: dict[str, dict] = {
    PRIMARY_CARE.strip(): {
        "patient_name": "James Holloway",
        "date_of_birth": "March 4, 1978",
        "chief_complaint": {
            "value": "Severe left-sided headache lasting three days",
            "evidence_quote": "I've had this really bad headache for the past three days. It's mostly on the left side.",
        },
        "symptoms": [
            {
                "description": "Left-sided headache",
                "onset": "three days ago",
                "duration": "three days",
                "severity": "7/10, spikes to 9/10",
                "evidence_quote": "I've had this really bad headache for the past three days. It's mostly on the left side. Like a 7 most of the time, but it spikes to a 9.",
            },
            {
                "description": "Photosensitivity",
                "onset": None,
                "duration": None,
                "severity": None,
                "evidence_quote": "Yeah, lights really bother me.",
            },
        ],
        "medications": [
            {
                "name": "Metformin",
                "dose": None,
                "frequency": None,
                "evidence_quote": "I take metformin for diabetes.",
            },
            {
                "name": "Ibuprofen",
                "dose": "unknown",
                "frequency": None,
                "evidence_quote": "I started taking ibuprofen for the headache — not sure of the dose, whatever's in the bottle.",
            },
        ],
        "allergies": [
            {
                "substance": "Penicillin",
                "reaction": "hives",
                "status": "confirmed",
                "evidence_quote": "Penicillin. I break out in hives.",
            }
        ],
        "medical_history": [
            {
                "value": "Type 2 diabetes, diagnosed approximately 6 years ago",
                "evidence_quote": "I have type 2 diabetes, diagnosed about six years ago.",
            },
            {
                "value": "Hypertension (currently untreated)",
                "evidence_quote": "And hypertension, but I don't take anything for that right now.",
            },
        ],
        "vitals": {},
        "gaps": [
            {
                "field": "medications.ibuprofen.dose",
                "reason": "Patient does not know the ibuprofen dose",
                "suggested_followup": "What dose of ibuprofen are you taking — is it 200mg, 400mg, or 600mg per tablet?",
            },
            {
                "field": "vitals",
                "reason": "Vitals not yet collected at time of transcript",
                "suggested_followup": "Can we get your blood pressure and weight before the nurse comes in?",
            },
        ],
    },

    URGENT_CARE.strip(): {
        "patient_name": "Sarah Chen",
        "date_of_birth": "July 12, 1965",
        "chief_complaint": {
            "value": "Chest pressure on and off since this morning",
            "evidence_quote": "I've been having chest pain on and off since this morning.",
        },
        "symptoms": [
            {
                "description": "Chest pressure",
                "onset": "this morning",
                "duration": "on and off since morning",
                "severity": "6/10 (was 8/10 earlier)",
                "evidence_quote": "It feels like pressure, like something heavy sitting on my chest. About a 6. It was an 8 earlier this morning.",
            },
            {
                "description": "Shortness of breath",
                "onset": None,
                "duration": None,
                "severity": None,
                "evidence_quote": "Yes, it comes and goes.",
            },
            {
                "description": "Left arm heaviness and numbness",
                "onset": None,
                "duration": None,
                "severity": None,
                "evidence_quote": "my left arm has felt kind of heavy and numb.",
            },
            {
                "description": "Nausea",
                "onset": None,
                "duration": None,
                "severity": None,
                "evidence_quote": "A little nauseous, yes.",
            },
        ],
        "medications": [
            {
                "name": "Atorvastatin (Lipitor)",
                "dose": "40mg",
                "frequency": "every night",
                "evidence_quote": "I take Lipitor — 40mg every night.",
            },
            {
                "name": "Aspirin",
                "dose": "81mg",
                "frequency": "daily",
                "evidence_quote": "And aspirin, 81mg daily.",
            },
        ],
        "allergies": [
            {
                "substance": "Sulfa drugs",
                "reaction": "rash",
                "status": "confirmed",
                "evidence_quote": "Sulfa drugs. I got a bad rash the last time I took them.",
            }
        ],
        "medical_history": [
            {
                "value": "Family history: father had heart attack at age 58",
                "evidence_quote": "My father had a heart attack at 58. I've never had one myself.",
            },
            {
                "value": "High cholesterol",
                "evidence_quote": "High cholesterol, yes — that's why I'm on Lipitor.",
            },
        ],
        "vitals": {},
        "gaps": [
            {
                "field": "vitals",
                "reason": "Vitals not yet collected — critical given chest pain presentation",
                "suggested_followup": "Can we get your blood pressure, heart rate, and oxygen saturation right now?",
            },
        ],
    },

    MED_SPA.strip(): {
        "patient_name": "Marcus Webb",
        "date_of_birth": "November 2, 1988",
        "chief_complaint": {
            "value": "Consultation for Botox (forehead lines) and dermal filler (nasolabial folds)",
            "evidence_quote": "I want to talk about Botox for my forehead lines and maybe filler for my nasolabial folds.",
        },
        "symptoms": [],
        "medications": [
            {
                "name": "Fish oil",
                "dose": "1000mg",
                "frequency": "daily",
                "evidence_quote": "I take fish oil, 1000mg daily.",
            },
            {
                "name": "Vitamin D",
                "dose": None,
                "frequency": "daily",
                "evidence_quote": "And vitamin D.",
            },
        ],
        "allergies": [],
        "medical_history": [
            {
                "value": "Previous Botox treatment approximately 1 year ago, no adverse reactions",
                "evidence_quote": "Botox, yes — about a year ago at a different place. No filler before.",
            },
            {
                "value": "History of herpes simplex / cold sores (occasional, ~1–2x per year)",
                "evidence_quote": "Yes, I do get cold sores occasionally — maybe once or twice a year.",
            },
        ],
        "vitals": {},
        "gaps": [
            {
                "field": "allergies",
                "reason": "No known allergies reported, but patient has not been formally tested for injectable components (lidocaine, hyaluronic acid)",
                "suggested_followup": "Have you ever had a reaction to a numbing cream or local anesthetic like lidocaine?",
            },
            {
                "field": "medications.vitamin_d.dose",
                "reason": "Vitamin D dose not specified",
                "suggested_followup": "What dose of vitamin D are you taking — is it 1000 IU, 2000 IU, or higher?",
            },
        ],
    },

    CONCIERGE.strip(): {
        "patient_name": "Diana Okonkwo",
        "date_of_birth": "February 18, 1972",
        "chief_complaint": {
            "value": "Annual physical with new concern: persistent fatigue for several months",
            "evidence_quote": "Annual physical. I've also been more tired than usual for the past few months.",
        },
        "symptoms": [
            {
                "description": "Persistent fatigue with reduced exercise tolerance",
                "onset": "past few months",
                "duration": "several months",
                "severity": "significant — reduced daily run from 3 miles to under 1 mile",
                "evidence_quote": "I used to run three miles every day — now I can barely get through one.",
            },
            {
                "description": "Hair thinning",
                "onset": None,
                "duration": None,
                "severity": None,
                "evidence_quote": "Some hair thinning, yes.",
            },
            {
                "description": "Unexplained weight gain",
                "onset": "past 4 months",
                "duration": "4 months",
                "severity": "approximately 8 lbs without dietary change",
                "evidence_quote": "I've gained about 8 pounds in the last four months without changing my diet at all.",
            },
            {
                "description": "Cold intolerance",
                "onset": None,
                "duration": None,
                "severity": None,
                "evidence_quote": "Yes, my hands are always cold. I've been wearing extra layers even when my husband thinks it's warm.",
            },
        ],
        "medications": [
            {
                "name": "Multivitamin",
                "dose": None,
                "frequency": "daily",
                "evidence_quote": "Just a daily multivitamin.",
            }
        ],
        "allergies": [
            {
                "substance": "Iodinated contrast dye",
                "reaction": "hives and throat tightness",
                "status": "confirmed",
                "evidence_quote": "Contrast dye — I had a reaction during a CT scan a few years ago. Hives and some throat tightness.",
            }
        ],
        "medical_history": [
            {
                "value": "Previously on metformin; discontinued approximately 2 years ago after weight loss",
                "evidence_quote": "I was on metformin about two years ago but stopped after I lost weight.",
            },
            {
                "value": "Family history: mother has hypothyroidism",
                "evidence_quote": "My mother has hypothyroidism.",
            },
            {
                "value": "Family history: father had colon cancer diagnosed at age 67",
                "evidence_quote": "My father had colon cancer diagnosed at 67.",
            },
        ],
        "vitals": {},
        "gaps": [
            {
                "field": "vitals",
                "reason": "Vitals not yet collected",
                "suggested_followup": "Can we take your blood pressure, weight, and temperature now?",
            },
            {
                "field": "medical_history.thyroid_personal",
                "reason": "Strong family history of hypothyroidism but no personal diagnosis confirmed or ruled out",
                "suggested_followup": "Have you ever had thyroid function tests done? If so, do you know what the results were?",
            },
        ],
    },
}
