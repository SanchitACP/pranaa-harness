PRIMARY_CARE = """\
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

URGENT_CARE = """\
MA: Hi, I'm Tyler, I'll be taking your intake today. Can I get your full name?
Patient: Sarah Chen.
MA: Date of birth?
Patient: July 12, 1965.
MA: What brings you in today?
Patient: I've been having chest pain on and off since this morning.
MA: Can you describe the pain — sharp, pressure, burning?
Patient: It feels like pressure, like something heavy sitting on my chest.
MA: Any shortness of breath?
Patient: Yes, it comes and goes.
MA: Does it radiate anywhere — arm, jaw, back?
Patient: Actually yeah, my left arm has felt kind of heavy and numb.
MA: On a scale of 1 to 10 how bad is the pain right now?
Patient: About a 6. It was an 8 earlier this morning.
MA: Any sweating, nausea, or lightheadedness?
Patient: A little nauseous, yes. No sweating.
MA: Are you on any medications?
Patient: I take Lipitor — 40mg every night. And aspirin, 81mg daily.
MA: Any allergies?
Patient: Sulfa drugs. I got a bad rash the last time I took them.
MA: Any history of heart disease or prior heart attacks?
Patient: My father had a heart attack at 58. I've never had one myself.
MA: Any history of high cholesterol or diabetes?
Patient: High cholesterol, yes — that's why I'm on Lipitor. No diabetes.
MA: We'll get your vitals and an EKG right away.
"""

MED_SPA = """\
MA: Hello! I'm Ashley, I'll be doing your intake today. Can I get your name?
Patient: Marcus Webb.
MA: Date of birth?
Patient: November 2nd, 1988.
MA: What brings you in today?
Patient: I want to talk about Botox for my forehead lines and maybe filler for my nasolabial folds.
MA: Have you had any injectables before?
Patient: Botox, yes — about a year ago at a different place. No filler before.
MA: Any reactions or bruising from the Botox?
Patient: No, it went totally fine.
MA: Are you on any medications, including blood thinners or supplements?
Patient: I take fish oil, 1000mg daily. And vitamin D. No prescription medications.
MA: Any known allergies?
Patient: None that I know of.
MA: Any history of cold sores or herpes simplex?
Patient: Yes, I do get cold sores occasionally — maybe once or twice a year.
MA: Any autoimmune conditions or active skin conditions?
Patient: No, nothing like that.
MA: Are you pregnant or planning to become pregnant?
Patient: No.
MA: Perfect. We'll take some photos of the treatment areas before we begin.
"""

CONCIERGE = """\
MA: Good morning, I'm Ben, I'll do your intake. Full name?
Patient: Diana Okonkwo.
MA: Date of birth?
Patient: February 18, 1972.
MA: What brings you in today?
Patient: Annual physical. I've also been more tired than usual for the past few months.
MA: Can you describe the fatigue?
Patient: It's all day, not just mornings. I used to run three miles every day — now I can barely get through one.
MA: Any other symptoms? Shortness of breath, hair loss, weight changes?
Patient: Some hair thinning, yes. And I've gained about 8 pounds in the last four months without changing my diet at all.
MA: Any temperature sensitivity — feeling colder than usual?
Patient: Yes, my hands are always cold. I've been wearing extra layers even when my husband thinks it's warm.
MA: Current medications?
Patient: Just a daily multivitamin. I was on metformin about two years ago but stopped after I lost weight. Nothing prescription right now.
MA: Any allergies?
Patient: Contrast dye — I had a reaction during a CT scan a few years ago. Hives and some throat tightness. No other allergies.
MA: Any family history I should know?
Patient: My mother has hypothyroidism. My father had colon cancer diagnosed at 67.
MA: Any personal history of thyroid issues, anemia, or autoimmune conditions?
Patient: Not that I've ever been diagnosed with, no.
MA: When was your last physical?
Patient: About two years ago. Everything came back normal at that time.
MA: We'll run a full panel today including thyroid function, CBC, and metabolic panel.
"""

ADVERSARIAL_TRAP_MEDICATION_CONTRADICTION = """\
MA: Hi, I'm Lisa, I'll be doing your intake today. Can I get your name?
Patient: Sure, Kevin Marsh.
MA: Date of birth?
Patient: August 9th, 1983.
MA: What brings you in today?
Patient: I've had lower back pain for about two weeks. It's constant, maybe a 5 out of 10.
MA: Are you on any medications?
Patient: I was taking naproxen for the pain — 500mg twice a day. Actually wait, no, I stopped that about a week ago. My stomach couldn't handle it.
MA: So you're not currently taking naproxen?
Patient: Right, I stopped. I'm not on anything right now.
MA: Any allergies?
Patient: None that I know of.
MA: Any relevant medical history?
Patient: I had a herniated disc about three years ago. Resolved on its own.
MA: We'll get your vitals shortly.
"""

ADVERSARIAL_TRAP_AMBIGUOUS_DOSE = """\
MA: Hi, I'm Priya, I'll be taking your intake. Can I get your full name?
Patient: Janet Osei.
MA: Date of birth?
Patient: March 22nd, 1971.
MA: What brings you in today?
Patient: I've had a sinus infection for about five days. Lots of pressure around my eyes and forehead.
MA: On a scale of 1 to 10?
Patient: About a 4. Annoying but manageable.
MA: Are you taking anything for it?
Patient: I've been taking ibuprofen — whatever the recommended dose says on the bottle. And some generic decongestant, I don't remember the name or how much.
MA: Any allergies?
Patient: Amoxicillin. I got a rash from it as a kid.
MA: Any medical history?
Patient: Seasonal allergies, that's about it.
MA: We'll check your temperature and blood pressure.
"""

ADVERSARIAL_TRAP_NO_NAME = """\
MA: Hi, I'm Carlos, I'll be doing your intake. So what brings you in today?
Patient: I've been having really bad stomach cramps since yesterday. On and off, but pretty sharp when they hit.
MA: On a scale of 1 to 10?
Patient: Like a 7 when it peaks.
MA: Any nausea or vomiting?
Patient: Some nausea, no vomiting.
MA: Any diarrhea?
Patient: Yes, since this morning.
MA: Are you on any medications?
Patient: Just a daily probiotic. Nothing prescription.
MA: Any allergies?
Patient: Shellfish. I swell up badly.
MA: Any relevant medical history?
Patient: I had my appendix out about eight years ago. Nothing else significant.
MA: Date of birth?
Patient: December 1st, 1990.
MA: Alright, let me grab your vitals.
"""

ADVERSARIAL_TRAP_ALLERGY_NO_REACTION = """\
MA: Good morning, I'm Diane, I'll be taking your intake. Full name?
Patient: Robert Finch.
MA: Date of birth?
Patient: June 14th, 1965.
MA: What brings you in today?
Patient: I've had a persistent cough for three weeks. Dry, doesn't bring anything up.
MA: Any shortness of breath or chest tightness?
Patient: A little tightness, yeah, but no trouble breathing.
MA: Any fever?
Patient: No fever.
MA: Are you on any medications?
Patient: Lisinopril, 10mg once a day, for blood pressure.
MA: Any allergies?
Patient: I can't take penicillin. And I've been told to avoid codeine.
MA: Do you know what happens when you take them?
Patient: I honestly don't remember. I was just told not to take them.
MA: Any medical history?
Patient: Hypertension, diagnosed about five years ago.
MA: We'll get your vitals now.
"""

ADVERSARIAL_TRANSCRIPTS = {
    "⚠️ Adversarial — Medication Contradiction": ADVERSARIAL_TRAP_MEDICATION_CONTRADICTION,
    "⚠️ Adversarial — Ambiguous Dose": ADVERSARIAL_TRAP_AMBIGUOUS_DOSE,
    "⚠️ Adversarial — Name Never Stated": ADVERSARIAL_TRAP_NO_NAME,
    "⚠️ Adversarial — Allergy No Reaction": ADVERSARIAL_TRAP_ALLERGY_NO_REACTION,
}

ADVERSARIAL_DESCRIPTIONS = {
    "⚠️ Adversarial — Medication Contradiction": {
        "trap": "Patient mentions a medication then retracts it.",
        "correct": "Medications list should be empty. Claude should not extract naproxen as a current medication and should flag it as a gap or note the contradiction.",
    },
    "⚠️ Adversarial — Ambiguous Dose": {
        "trap": "Patient takes medications but states no dose or name.",
        "correct": "Ibuprofen should be extracted with dose and frequency as gaps. The unnamed decongestant should either be omitted or flagged — Claude should not invent a name or dose.",
    },
    "⚠️ Adversarial — Name Never Stated": {
        "trap": "MA forgets to ask for the patient's name.",
        "correct": "patient_name should be null and flagged as a gap. Claude should not infer a name from context.",
    },
    "⚠️ Adversarial — Allergy No Reaction": {
        "trap": "Patient lists allergies but cannot describe any reaction.",
        "correct": "Both allergies should have reaction as null and status as unknown. Claude should not invent a reaction.",
    },
}

TRANSCRIPTS = {
    "Primary Care — James Holloway": PRIMARY_CARE,
    "Urgent Care — Sarah Chen": URGENT_CARE,
    "Med Spa — Marcus Webb": MED_SPA,
    "Concierge Care — Diana Okonkwo": CONCIERGE,
    **ADVERSARIAL_TRANSCRIPTS,
}
