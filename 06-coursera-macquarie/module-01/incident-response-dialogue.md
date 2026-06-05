# Module 01 — Incident Response Dialogue
## First Responder: Navigating Your Digital Crime Scene

**Course:** Cybersecurity: Digital Forensics — Macquarie University (Coursera)
**Module:** 01 — Introduction to Digital Forensics Processes
**Activity:** Simulated Dialogue — First Responder Scenario
**Scenario:** Lead digital forensic investigator responding to a suspected corporate data breach

---

## Scenario Brief

A company has experienced a suspected data breach. As the lead digital forensic investigator, decisions had to be made in real time regarding initial assessment, evidence prioritization, procedural justification, and legal/ethical navigation.

---

## My Approach — What I Got Right

### Initial Assessment & Triage

Upon arriving at the scene, my immediate priorities were:

- Pull CCTV footage of the server room for the **48 hours prior** to the reported breach
- Obtain an **access log** — a complete list of personnel who entered the server room during that window
- Secure the **server logs** as primary digital evidence
- Physically sweep the area for **discarded storage media** (USB drives, pen drives, other devices) and confiscate as evidence

For the server logs specifically — before any analysis, I would:
1. Make a verified copy of the original log file
2. Calculate SHA-256 hashes of both the original and the copy
3. Confirm both hashes match before beginning examination
4. Work exclusively on the copy, never the original

This ensures the chain of custody is established from the first moment of contact with digital evidence.

### Evidence Preservation

SHA-256 hashes were identified as the correct preservation mechanism for all evidence categories:

- CCTV footage files
- Server logs
- Any confiscated physical storage media (forensic images of these devices)

Hashing all evidence before examination establishes a cryptographic fingerprint that proves in any subsequent legal proceeding that the evidence was not altered during the investigation.

### Investigation Strategy — Cross-Referencing Evidence Sources

Rather than immediately interviewing employees, I chose to review CCTV footage first and use it as an objective baseline to inform the interview process. The strategy:

1. Review CCTV footage and establish a factual record of who was present, when, and what they did
2. Conduct employee interviews **without revealing** that footage has already been reviewed
3. If an employee's account contradicts what the footage shows — surface the contradiction during the interview directly

This approach leverages objective evidence to detect deception in real time, rather than relying solely on witness accounts which are inherently subjective and malleable.

### Legal & Ethical Considerations

- All suspects retain the **right to legal counsel** at any point during questioning — this was identified and would be explicitly communicated before any interview begins
- CCTV footage handling would comply fully with **company data protection policies** — retention periods, access controls, and permissible use cases
- Interview scope would be **strictly limited** to matters directly relevant to the data breach and server room access — no encroachment on personal matters unless a direct connection to the incident emerges
- Questions would remain operationally focused: movements, activities, whereabouts at specific times — nothing beyond what the investigation requires

---

## Gap Identified

When asked to articulate the broader digital forensics process lifecycle beyond log analysis, I could not independently recall the complete framework without prompting.

**The correct sequence — to be internalized:**

| Phase | What Happens |
|---|---|
| **Identification** | Recognize what digital evidence exists and where |
| **Preservation** | Secure and protect evidence from alteration — hashing, write blocking |
| **Collection** | Forensically acquire evidence — disk imaging, log extraction |
| **Examination** | Process the collected data to surface relevant artifacts |
| **Analysis** | Interpret the artifacts to reconstruct events and draw conclusions |
| **Reporting** | Document findings in a clear, objective, legally admissible format |

My instinct in the scenario jumped directly from Identification to Examination — skipping the explicit Preservation and Collection steps as conscious, documented phases. In practice these were implicit in my response, but in a real investigation they must be deliberate and documented in sequence. A court will scrutinize whether each phase was followed correctly, not just whether the right technical actions were taken.

---

## Legal Framework — What I Learned

Even in urgent incident response scenarios, the following legal considerations apply and cannot be bypassed:

**Data Protection Laws**
In India, the **Digital Personal Data Protection Act (DPDPA) 2023** governs how personal data — including employee access records and CCTV footage — can be collected, stored, and processed. Equivalent frameworks internationally include GDPR (EU) and CCPA (US). An investigator operating in a corporate setting must ensure their evidence collection methods comply with whichever framework applies to the organization.

**Employee Rights During Questioning**
The term "interrogation" carries specific legal connotations in formal proceedings. In a corporate investigation context, employee interviews must:
- Be conducted with informed consent regarding the purpose of the interview
- Allow for legal representation if requested
- Remain scoped strictly to the matter under investigation
- Be documented accurately for potential use in proceedings

**Chain of Custody Documentation**
Every piece of evidence — digital or physical — must have a documented chain of custody from the moment of collection. This includes: who collected it, when, from where, how it was transported, who had access to it, and every hash verification performed. Any break in this chain can render evidence inadmissible.

---

## Key Takeaway

Technical instincts were sound throughout — evidence preservation via hashing, physical sweep for discarded media, strategic sequencing of CCTV review before interviews, and scoping of questioning to the incident. The gap is in the **explicit internalization of the forensic process lifecycle as a conscious framework**, not just as implicit technical actions. In real investigations and in legal proceedings, being able to articulate which phase you are in and why each step was taken in sequence is as important as the technical execution itself.

---

## Evaluator Feedback Summary

**Strengths identified:**
- Strong grasp of evidence preservation and chain of custody
- Effective cross-referencing strategy between CCTV and interview evidence
- Thoughtful articulation of legal and ethical boundaries

**Area for improvement:**
- Internalize the full forensic lifecycle (Identification → Preservation → Collection → Examination → Analysis → Reporting) so it can be recalled and applied independently without prompting