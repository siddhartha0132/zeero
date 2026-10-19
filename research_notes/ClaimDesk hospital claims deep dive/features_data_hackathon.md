# ClaimDesk: High-Impact Features, Public Data Sources, Agent Architecture and What Wins Agentic-AI Hackathons

Research date: 3 Oct 2026. Scope: an agentic AI for Indian private hospitals' insurance/TPA desks ("ClaimDesk") plus the free patient version "ClaimSaathi", built in a 6-day online sprint (Ziro Agentic AI Hackathon, 18-23 Oct 2026) on a free Gemini tier with FastAPI.

Note on the event itself: a web search for "Ziro Agentic AI Hackathon 2026" returned no page for the event, only other 2026 agentic hackathons ([Reskilll list](https://blogs.reskilll.com/agentic-ai-hackathons-2026-build-autonomous-agents/)). The team should use the organiser's own rubric, which these notes could not check.

---

## Q1. What leading US RCM-AI products do agentically, and what carries over to India

### Takeaway
The US leaders share four patterns:
1. Every output comes with **evidence and citations** that a reviewer can click through to the exact sentence in the source document.
2. The AI **never denies or submits on its own when it is unsure**. It escalates to a human with an "evidence packet".
3. They **predict denials before submission**.
4. They **draft appeals by checking the denial reason against the full record**.

Voice agents that call payers are impressive, but they carry over poorly to India's TPA workflow, which runs on portals, email and WhatsApp. Patterns 1-4 carry over directly and can be built in 6 days.

### Cited Findings
**Anterior (payer-side prior auth / utilization review; AI agent "Florence")**
- Florence handles medical-record preparation and clinical reasoning for prior authorization. It reportedly cuts processing time by 74%, and Anterior reports 99.24% clinical accuracy, which it says was verified by KLAS. — [Fast Company](https://www.fastcompany.com/91255586/this-startup-says-its-ai-can-speed-insurance-approval-of-health-treatments); [Reducto case study](https://reducto.ai/blog/anterior-case-study)
- In the UI, reviewers can "toggle between Florence's analysis and specific sections of relevant documents cited by the AI". To make this work, Anterior needed **sentence-level bounding boxes** so each extracted insight can be located and checked in the original PDF. — [Reducto case study](https://reducto.ai/blog/anterior-case-study)
- Gated autonomy: "work completes automatically only where criteria are clearly met; otherwise Florence escalates to a qualified human with a sourced evidence packet." Every outcome includes "the reasoning and supporting evidence behind it — relevant record findings and the specific policy criteria applied." Products named: Relay (prior-auth automation end to end) and Flow (UM/CM acceleration). In the MedWatch deployment Anterior reports 3x clinician productivity, 92% clinician satisfaction and 97% clinical accuracy. — [anterior.com](https://www.anterior.com/)
- Raised a $20M Series A in June 2024. — [BusinessWire](https://www.businesswire.com/news/home/20240610719247/en/Anterior-Secures-$20-Million-Series-A-to-Unlock-Administrative-Efficiencies-for-Healthcare-Payers)

**AKASA (provider-side generative AI for RCM)**
- Uses LLMs tuned to each institution, for patient records that average about 60 documents and 50,000 words. Covers prior auth, coding, claims management and denial prevention. — [AKASA solutions](https://akasa.com/solutions/); [AKASA blog](https://akasa.com/blog/the-future-of-ai-in-healthcare-revenue-cycle)
- Authorization Advisor: "reduce the time spent on prior authorization by up to 50%" and "finding 15% more relevant clinical documents" for more complete submissions. — [AKASA press](https://akasa.com/press/akasa-launches-authorization-advisor)
- Strategic collaboration with Cleveland Clinic (April 2025) to launch AI tools for the revenue cycle. — [Cleveland Clinic newsroom](https://newsroom.clevelandclinic.org/2025/04/29/cleveland-clinic-and-akasa-announce-strategic-collaboration-to-launch-ai-tools-for-the-revenue-cycle)

**Infinitus (voice AI agents that call payers)**
- Voice agents call payers for benefit verification, prior-auth follow-up and claim status. They get through IVRs, hold times and transfers to humans. Claims: 98% call success rate, data collected about 10% more accurately, and over 200 data points captured per call. — [Infinitus AI agents](https://www.infinitus.ai/product/ai-agents/); [prior-auth follow-up](https://www.infinitus.ai/solutions/prior-authorization/); [benefit verification](https://www.infinitus.ai/solutions/benefit-verification/)
- Infinitus describes an "AI review" layer that checks call outputs, i.e. a second model or process auditing the first. — [Infinitus blog](https://www.infinitus.ai/blog/guardians-of-healthcare-calls-ai-review-in-action/)
- Integrates with Salesforce Health Cloud. — [HIT Consultant](https://hitconsultant.net/2025/06/25/infinitus-integrates-voice-ai-agents-with-salesforce-health-cloud/)

**Waystar AltitudeAI**
- Has three parts:
  - **AltitudeCreate** autonomously drafts appeal letters with generative AI.
  - **AltitudePredict** uses predictive analytics to "surface potential denials before they happen".
  - **AltitudeAssist** automates workflow tasks.
- Reported results: 70% time saved on building appeal packages, a 40% higher denial overturn rate, and more than $15B in denials prevented in under a year. — [Waystar blog](https://www.waystar.com/blog-powerful-ai-examining-results-of-waystar-altitudeai-in-rcm/); [Waystar Denial + Appeal Manager](https://www.waystar.com/our-platform/denial-prevention-recovery/denial-appeal-management/); [Waystar Spring Showcase](https://www.waystar.com/news/waystar-accelerates-the-autonomous-revenue-cycle-with-ai-powered-innovations-featured-at-spring-showcase/)
- CNBC covered the January 2025 launch of the appeal tool. — [CNBC](https://www.cnbc.com/2025/01/13/health-waystar-generative-ai-new-tool-will-help-fight-health-insurance-denials.html) (the page returned 403 to the fetcher; only the headline was confirmed)

**SmarterDx (SmarterDenials)**
- Generates evidence-backed appeal letters by checking the payer's denial reason against the full patient record (notes, labs, coding). Appeals are produced "in minutes". — [CombineHealth roundup](https://www.combinehealth.ai/blog/ai-denial-management-solutions) (secondary vendor-roundup source)

**Cohere Health, Adonis, Thoughtful AI**
- Cohere Health works on the front end (prior-auth approval) rather than on denials and appeals. Adonis works denial queues. Thoughtful AI works claims and denials. — [CombineHealth roundup](https://www.combinehealth.ai/blog/ai-denial-management-solutions) (secondary, thin detail)

**India: existing competitor and market signal**
- LeapHealth sells an "Insurance & TPA AI Agent" for Indian hospitals. What it does:
  - assembles cashless files and checks that mandatory documents are attached before TPA submission;
  - scores cases against **historical TPA decisions** for denial risk;
  - flags non-payable line items;
  - tracks approval timelines across TPAs and answers routine TPA queries over email and **WhatsApp**.

  Claimed results: approval turnaround cut from 5 days to 2, denial-risk check in under 10 seconds, initial denial rate down 12%. Onboarding takes 3-4 weeks and includes "TPA panel mapping and denial history analysis". — [LeapHealth](https://theleaphealth.com/ai-agents/insurance-tpa)
- Star Health plans to settle 50% of routine cashless claims through AI straight-through processing within two years, up from 20% today. This means the insurer side is automating too, so the hospital side needs matching tooling. — [Digital Health News](https://www.digitalhealthnews.com/star-health-targets-ai-driven-settlement-for-majority-of-cashless-claims); [India Blooms](https://www.indiablooms.com/health/star-health-aims-for-50-of-routine-cashless-claims-to-be-settled-through-ai-in-two-years/details)

### Inferences
- **What carries over directly to India:**
  - (a) Click-to-source citations on every flag. This is Anterior's pattern, and it is the single most "expert-credible" UI element.
  - (b) Gated autonomy with an evidence packet: the agent auto-clears clean files and escalates unclear ones.
  - (c) A pre-submission denial/query risk score with fix-it suggestions (AltitudePredict, LeapHealth).
  - (d) Appeal/contest letters generated by checking the denial reason against the record and the policy (AltitudeCreate, SmarterDenials).
- **What carries over poorly:**
  - IVR-navigating voice agents (Infinitus). Indian TPA communication is mostly portal, email and WhatsApp, and a voice demo is risky to build on a free tier in 6 days.
  - A cheaper Indian version of the "voice" idea would be a Hindi/Telugu voice note or TTS status update for patients, which is more relevant to the patient side.
- **Positioning:** LeapHealth already claims denial prediction and file assembly. ClaimDesk needs a sharper edge, such as citation-grounded IRDAI clause reasoning, NHCX FHIR output, settlement reconciliation with deduction contest letters, and a measured eval harness. Simply "we predict denials" is not enough.
- Expect jurors to ask "how is this different from LeapHealth or the insurers' own AI?". A good answer: "We're on the hospital's side, against insurer-side straight-through-processing AI. We make the file adjudication-proof."

### Gaps
- No primary product pages were fetched for Cohere Health, Adonis or Thoughtful AI, so feature detail for them is thin and comes from a secondary roundup.
- None of the vendor metrics (99.24%, 40% overturn, etc.) are independently audited, apart from Anterior's claim that KLAS verified its figure.
- No evidence was found of autonomous browser agents navigating Indian TPA portals (e.g., Medi Assist, Paramount, FHPL). Whether that is technically or legally feasible was not checked.

---

## Q2. Non-obvious differentiators: which impress most and can be built in days

### Takeaway
For a 6-day build, the best "wow per hour" comes from five features:
1. A **pre-submission "TPA query predictor"** with document-gap detection and clause-cited fixes.
2. **Settlement-letter parsing and reconciliation**, producing auto-drafted deduction contest letters that cite IRDAI clauses.
3. A **one-click NHCX FHIR R4 ClaimBundle export**, validated against the NRCES profiles.
4. A **human-in-the-loop approval queue with an audit trail and confidence scores**.
5. A **visible eval harness** that shows accuracy on ground-truth cases.

The regulatory timers (1-hour cashless, 3-hour discharge) make a live **SLA clock** a cheap but strong demo element.

### Cited Findings
- **Regulatory hooks for SLA features:**
  - The IRDAI Master Circular on Health Insurance Business (IRDAI/HLT/CIR/PRO/84/5/2024, 29 May 2024) repealed 55 circulars. Insurers must decide cashless authorization "immediately but not more than one hour", and give final discharge authorization within 3 hours. If the delay beyond 3 hours causes extra hospital charges, the insurer pays them from shareholders' funds. — [Deloitte tax alert](https://www2.deloitte.com/in/en/pages/tax/articles/tax-alert-insurance-regulator-releases-new-guidelines.html); [RTI Wiki summary](https://righttoinformation.wiki/irdai-cashless-claim-1-hour-3-hour-rule); [TaxGuru on the Products Master Circular](https://taxguru.in/corporate-law/master-circular-irdai-insurance-productsregulations-2024health-insurance.html)
  - Existing products had to comply by 30 September 2024. — [Stable Investor](https://stableinvestor.com/2024/05/irda-master-circular-2024-pdf-download.html)
- **NHCX is real and growing:** it processed its first claim in June 2024. As of May 2026, 12,600+ hospitals were onboarded (2,236 private, 10,370 government) with 160 integrators live. — [Wikipedia: NHCX](https://en.wikipedia.org/wiki/National_Health_Claims_Exchange); [NATHEALTH NHCX deck](https://nathealthindia.org/wp-content/uploads/2025/06/National-Health-Claims-Exchange_Latest.pdf)
- **NRCES NHCX FHIR IG (v6.5.0):**
  - Bundle profiles: ClaimBundle, ClaimResponseBundle, CoverageEligibilityRequestBundle, CoverageEligibilityResponseBundle, InsurancePlanBundle and TaskBundle.
  - Resource profiles: Claim, ClaimResponse, Communication, CommunicationRequest, Coverage, CoverageEligibilityRequest/Response, InsurancePlan, PaymentNotice, **PaymentReconciliation** and Task.
  - Examples are published (all-examples page), and the IG is based on FHIR 4.0.1. — [NRCES HCX profiles](https://nrces.in/ndhm/fhir/r4/hcx-profile.html); [CoverageEligibilityRequest examples](https://nrces.in/ndhm/fhir/r4/StructureDefinition-CoverageEligibilityRequest-examples.html)
- The ClaimBundle "allow[s] sharing of all supporting information required for processing claims", covering financial, clinical and service information. CoverageEligibilityRequest purposes include validation, discovery, auth-requirement and benefits. — [NRCES](https://nrces.in/ndhm/fhir/r4/hcx-profile.html)
- **Open HCX specs:** volunteer-built protocol specs (v0.7 draft, Jan 2022) covering pre-determination, pre-auth, the claim cycle, and communication/status APIs. — [GitHub hcx-specs](https://github.com/Swasth-Digital-Health-Foundation/hcx-specs); [docs.swasth.app](https://docs.swasth.app/hcx-specifications/)
- **Why deduction contests matter:** the "InsurancePlan" FHIR profile is meant for encoding policies digitally. — [GitHub hcx-specs](https://github.com/Swasth-Digital-Health-Foundation/hcx-specs)
- **Denial prediction from historical TPA decisions** is LeapHealth's core pitch, and onboarding includes "denial history analysis". — [LeapHealth](https://theleaphealth.com/ai-agents/insurance-tpa)
- **Proven appeal-letter value:** Waystar reports a 40% higher overturn rate and 70% time saved on appeal packages. — [Waystar](https://www.waystar.com/blog-powerful-ai-examining-results-of-waystar-altitudeai-in-rcm/)
- **Evaluation norms for agents:** AngelHack's 2026 agent-hackathon playbook says evaluation should cover "task completion rate, tool-use accuracy, cost per run, and latency, not just demo quality", and that teams should "build against a shared eval harness from day one". — [AngelHack playbook](https://angelhack.com/blog/ai-agent-hackathon/)

### Inferences: feature ranking for a 6-day build (impact x feasibility)
| # | Feature | Why jurors say "wow" | Build effort | Notes |
|---|---|---|---|---|
| 1 | **Pre-submission "Query/Deduction Predictor"** for each preauth or final-bill file. It outputs a list of likely TPA queries ("ICP notes missing", "duration of ailment not stated → PED query likely", "room category > eligible → proportionate deduction ₹X") with a fix and a cited clause for each | Turns a reactive tool into a preventive one, which is the TPA desk's real pain point | 1.5 days | Mostly rules plus LLM extraction. Seed it with a hand-written "TPA query taxonomy" (about 25 common query types) |
| 2 | **Document-gap checklist by procedure/insurer** (e.g., cataract needs biometry/A-scan; fracture needs X-ray report; MLC/FIR for RTA) | Concrete and fast to show. Mirrors AKASA's "15% more relevant documents" | 0.5-1 day | Hand-curate 10-15 procedure checklists |
| 3 | **Settlement-letter parser and reconciliation**: parse the TPA settlement/deduction letter, match each deduction against bill lines, label it as justified, contestable or error, and draft a contest letter citing the policy clause, IRDAI non-payables list or Master Circular | The "money recovered" metric is easy to grasp. It is the biggest gap in existing tools and reuses ClaimSaathi's line-item engine | 1 day | Show "₹18,400 recoverable out of ₹31,200 deducted" |
| 4 | **NHCX FHIR R4 ClaimBundle export** (Claim + Coverage + Patient + Condition + DocumentReference), validated with the HAPI FHIR validator or a schema check | Signals "production-grade, fits India's rails". Technical jurors from health or govtech will notice | 1 day | Use NRCES examples as templates. Even without an NHCX sandbox, a validated bundle is credible |
| 5 | **Human-in-the-loop approval queue with confidence scores and an audit trail** (every agent action logged with tool, input hash, cited source and approver) | Covers the "responsible AI" criterion and mirrors Anterior's gated autonomy | 0.5 day | A simple table UI with Approve/Edit/Reject |
| 6 | **Eval harness tab**: 20-40 ground-truth cases (synthetic but realistic bills and policies) with precision/recall for non-payable detection, ₹ error in deduction calculations, citation validity rate, latency and cost per case | Very few student teams show measured accuracy. Matches the AngelHack eval advice | 1 day | Ground truth comes from deterministic rules (room-rent proportionate deduction is arithmetic) |
| 7 | **SLA clock**: 1-hour preauth and 3-hour discharge timers, auto-escalation emails/WhatsApp drafts at T-15 min, and a note that a delay past 3 hours is borne by the insurer | Cheap. Ties to a real regulatory right | 0.3 day | Strong as a demo moment |
| 8 | **Multilingual patient status updates** (Hindi/Telugu text, plus optional TTS voice note) in a WhatsApp-style mock | Hyderabad finale, so Telugu will land with the audience. Bridges ClaimDesk and ClaimSaathi | 0.5 day | Use a WhatsApp-styled UI mock or wa.me deep links. Setting up the WhatsApp Business API in 6 days is risky |
| 9 | **Insurer-specific rulebook learned from past queries** (store each resolved query as a rule with insurer, procedure and trigger; retrieve it on new files) | Shows memory and "self-improving" behaviour, which agent hackathons value | 1 day | Demo: process file A, get query, resolve; process similar file B and the agent pre-empts it |
| 10 | **Precedent library for appeals** (Ombudsman awards and consumer-court judgments retrieved by issue type) | Expert jurors notice legal grounding | 1 day | See Q3 for sources and licensing |
| 11 | Cost/latency dashboard | Nice to have | 0.3 day | Log tokens per call |
| 12 | Voice agent calling the TPA | High wow, low India fit, high risk | 2+ days | Skip, or show only as a "roadmap" slide |

- **Recommended core loop for the demo:** Upload discharge summary, bill and policy → agent plans → gap check plus query prediction (with citations) → human approves fixes → generate FHIR ClaimBundle → (simulated) TPA settlement letter arrives with deductions → agent reconciles and drafts a contest letter citing clauses → patient gets a Telugu/Hindi update. One story covers the full claim lifecycle and shows several tools and real autonomy.
- **The "memory" demo (#9) is the most "agentic"-looking feature per hour of work.** It shows that the system learns from outcomes.

### Gaps
- No public dataset of Indian TPA query letters or settlement letters was found. Test cases will have to be synthesised. Be transparent about this with jurors.
- No public NHCX sandbox credentials or onboarding process for students were confirmed. The NRCES IG publishes the package "ndhm.in#6.5.0", but whether a public validator endpoint exists was not confirmed.
- No sourced data was found on how common each TPA query type is in India, so the query taxonomy has to come from domain knowledge or interviews.

---

## Q3. Public data sources to ground the agent (with links and licensing/access)

### Takeaway
Most of the high-value grounding is freely downloadable government PDFs: IRDAI circulars, CGHS rates, PM-JAY HBP manuals, NRCES FHIR IG and Ombudsman awards. Treat them as public documents, cite them, don't redistribute them as your own dataset, and check terms on the live sites. The one paid but cheap source is the Indian Kanoon API: ₹500 free credit for new users, and ₹10,000 a month free for verified non-commercial use.

### Cited Findings
**IRDAI regulatory corpus**
- Master Circular on Health Insurance Business, 29 May 2024 (IRDAI/HLT/CIR/PRO/84/5/2024). It consolidates policyholder entitlements and covers cashless TATs, the moratorium and more. — [Deloitte summary](https://www2.deloitte.com/in/en/pages/tax/articles/tax-alert-insurance-regulator-releases-new-guidelines.html); [Deloitte PDF](https://www2.deloitte.com/content/dam/Deloitte/in/Documents/tax/in-tax-gbt-insurance-regulator-releases-new-guidelines-noexp.pdf); [Stable Investor PDF mirror](https://stableinvestor.com/2024/05/irda-master-circular-2024-pdf-download.html). The original is on [irdai.gov.in](https://irdai.gov.in), but no direct URL was confirmed.
- The 60-month moratorium and other 2024 changes. — [Oquilia explainer](https://www.oquilia.com/news/irdai-health-master-circular-2024-cashless-moratorium) (secondary)
- **Non-payables / standardisation:**
  - The 2019-2020 modification guidelines on standardisation sort expenses into four lists: optional items, items subsumed into room charges, items subsumed into procedure charges, and items subsumed into treatment costs.
  - The non-medical expense list was cut from 95 to 68 items.
  - A TPA-hosted PDF copy is available. — [Paramount TPA PDF](https://www.paramounttpa.com/Home/Download/Modification_Guidelines_on_Standardzation.pdf); [Zurich Kotak guideline page](https://www.zurichkotak.com/health-insurance-guidelines); [Ditto explainer](https://joinditto.in/articles/health-insurance/non-medical-expenses-and-exclusion-in-health-insurance-policies/)
  - Licensing: these are regulatory public documents, freely downloadable.
- **Insurers' policy wordings and Customer Information Sheets:** IRDAI requires insurers to publish these on their websites. Collect PDFs for 5-6 major products (e.g., Star, Niva Bupa, Care, HDFC ERGO, ICICI Lombard, plus the standard "Arogya Sanjeevani" product). No single repository URL was confirmed in this research, so see Gaps.

**Rate benchmarks (for detecting overcharging and checking "reasonable and customary" charges)**
- **CGHS rates:** a revised package was notified by an Office Memorandum dated 3 Oct 2025, effective 13 Oct 2025, replacing earlier lists.
  - Rates vary by accreditation: non-NABH is 15% lower, super-speciality 15% higher.
  - Rates vary by city tier: Tier II is 10% lower and Tier III 20% lower than Tier I.
  - Rates vary by ward: base rates are for a semi-private ward; general ward is 5% lower and private ward 5% higher.
  - Official site: [cghs.mohfw.gov.in](https://cghs.mohfw.gov.in); summaries at [StaffNews](https://www.staffnews.in/2025/10/cghs-rates-applicable-for-treatment-at-healthcare-organisation.html) and [Outlook Money](https://www.outlookmoney.com/personal-finance/cghs-rates-revised-know-changes-and-benefits-effective-october-13-2025)
  - The tiered structure maps cleanly onto a deterministic rate-lookup tool.
- **PM-JAY Health Benefit Packages:** HBP 2022 (April 2022) has more than 1,900 packages. Surgical packages are single all-inclusive bundled payments. Medical packages are paid per day by admission unit. — [HBP 2.2 manual (NHA)](https://nha.gov.in/img/resources/HBP-2.2-manual.pdf); [Provider Payment in PM-JAY (NHA)](https://nha.gov.in/img/pmjay-files/Provider-Payment-in-PM-JAY.pdf); [BMJ Global Health analysis](https://gh.bmj.com/content/9/6/e015079)
  - Rates for about 400 procedures were later raised. — [Money9](https://www.money9.com/news/insurance/rates-of-400-treatment-procedures-under-the-pm-jay-hiked-87627.html)
  - NHA is revising packages. — [BW Healthcare](https://bwhealthcareworld.com/article/under-ab-pm-jay-scheme-nha-is-revising-health-benefit-packages-407552)
  - Use these mainly as a procedure taxonomy and for "mandatory documents per package". The HBP manuals list the pre-auth and claim documents required for each package, which makes a ready-made document-gap checklist source.
- Public government documents: no licence restriction is stated, but the current HBP Excel file was not found at a confirmed URL (see Gaps).

**ABDM / NHCX standards**
- NRCES FHIR IG for ABDM, NHCX profiles, v6.5.0 (examples available; "IG © 2024+ NRCES", based on the open FHIR 4.0.1 standard). — [nrces.in HCX profiles](https://nrces.in/ndhm/fhir/r4/hcx-profile.html); [v4.0.0](https://nrces.in/ndhm/fhir/r4/4.0.0/hcx-profile.html); [CoverageEligibilityRequest profile](https://www.nrces.in/preview/ndhm/fhir/r4/StructureDefinition-CoverageEligibilityRequest.html)
- HCX protocol specs (open source, GitHub). — [hcx-specs](https://github.com/Swasth-Digital-Health-Foundation/hcx-specs); [docs.swasth.app](https://docs.swasth.app/hcx-specifications/)
- NHCX adoption deck (NATHEALTH, June 2025). — [PDF](https://nathealthindia.org/wp-content/uploads/2025/06/National-Health-Claims-Exchange_Latest.pdf)

**Dispute precedents (for appeal/contest letters)**
- **Insurance Ombudsman awards:** the Council for Insurance Ombudsmen (CIO) publishes award PDFs by month and office, at URLs like `https://www.cioins.co.in/AwardsMonthwise/Apr2023/1004_MiscellaneousApr2023.pdf`. — [example award PDF](https://www.cioins.co.in/AwardsMonthwise/Apr2023/1004_MiscellaneousApr2023.pdf); [CIO About](https://www.cioins.co.in/About)
  - Annual reports. — [CIO Annual Report 2023-24 PDF](https://cioins.co.in/annualreports/AnnualReport2023-2024.pdf)
  - The awards are public PDFs. No licence is stated, so cite them and link back.
- **Ombudsman statistics (for the pitch):**
  - FY25: health complaints received rose from 34,203 in FY24 to 37,431. 29,017 were disposed of, with 6,126 decided in the policyholder's favour and 9,417 recommended for settlement. 41% were resolved in favour or settled, down from 55% in FY24. Decisions in favour of insurers rose from 4,122 to 4,897. — [Cafemutual](https://cafemutual.com/news/industry/36635-41-of-health-insurance-complaints-were-resolved-in-favour-of-policyholders-in-fy25)
  - **Conflict:** an aggregator ([BimaKavach](https://www.bimakavach.com/blog/insurance-ombudsman-guide/)) claims 53,184 complaints in FY25 across all lines, with about 71% settled in the policyholder's favour, and says "95% of health complaints were claim repudiation" (via [basunivesh](https://www.basunivesh.com/top-5-health-insurance-companies-by-complaints-cio-report/)). The figures don't line up (they may be all lines vs health only). Use the Cafemutual figures, or check against the [CIO annual reports](https://www.cioins.co.in/About) before quoting.
- **Consumer-court and Supreme Court judgments:**
  - [Indian Kanoon API](https://api.indiankanoon.org/) covers "more than 3 crore orders". It offers enriched HTML with paragraph classification (Facts, Issues, Arguments, Precedent Analysis, Law Analysis, Court Discourse, Conclusion), citation extraction and AI tags.
  - Pricing: ₹0.50 per search, ₹0.20 per document, ₹0.05 per fragment, ₹0.02 per metainfo call. New users get ₹500 free credit. **Non-commercial users get ₹10,000 free every month** after admin verification. — [Indian Kanoon API pricing](https://api.indiankanoon.org/pricing/)
  - Example: NCDRC upheld an order requiring Niva Bupa to pay ₹9.2 lakh plus ₹82,000 compensation to a 78-year-old (Oct 2025). — [Moneylife](https://moneylife.in/article/niva-bupa-health-insurance-ordered-to-pay-rs92-lakh-mediclaim-rs82000-compensation-to-78yearold-policyholder/78639.html)
  - A principle reported from consumer-commission decisions: the insurer carries the burden of proving that a pre-existing disease was suppressed, and producing medical records alone is not enough. — [SupremeToday NCDRC doc](https://supremetoday.ai/doc/judgement/01200045233) (secondary aggregator; check the exact wording)
  - Supreme Court judgment PDF example (4 Jul 2023, civil appeal 10585/2019). — [sci.gov.in](https://api.sci.gov.in/supremecourt/2019/10585/10585_2019_15_1504_44763_Judgement_04-Jul-2023.pdf)
- **Coding:** ICD-10 is available from the WHO browser at [icd.who.int/browse10](https://icd.who.int/browse10). Licensing terms were **not checked** in this research (see Gaps).

### Inferences
- **Minimum viable grounding corpus for a 6-day build (about 1 day of curation):**
  - the IRDAI Master Circular 2024 (health);
  - the standardisation / non-payables guidelines (four lists);
  - 5 insurer policy wordings and CIS documents;
  - the CGHS 2025 rate list (subset for 30 common procedures);
  - PM-JAY HBP document requirements for those procedures;
  - 30-50 hand-picked Ombudsman awards on health repudiation, tagged by issue (PED/non-disclosure, room-rent proportionate deduction, consumables, waiting period, "not requiring hospitalisation", day care).
- Chunk every source with **stable IDs (doc, clause/para, page)** so citations can deep-link to them. This copies Anterior's sentence-level citation UX.
- A curated set of 30-50 Ombudsman awards is enough for a demo precedent library. Pull judgments live from Indian Kanoon only if credits are approved in time; otherwise pre-fetch a few with the ₹500 free credit.

### Gaps
- No direct irdai.gov.in URL was confirmed for the Master Circular PDF or the 2020 non-payables circular. Check these on the IRDAI site.
- No public download URL was confirmed for the current PM-JAY HBP rate Excel or the STG documents (pmjay.gov.in / nha.gov.in). Only the HBP 2.2 manual and payment-design PDFs were confirmed.
- No public GIPSA PPN package-rate list was found (and none was searched for directly). Assume it is proprietary.
- WHO ICD-10 licensing and API registration terms were not checked.
- Whether CIO award PDFs can be bulk-downloaded, and how they are organised by category, was not confirmed. The Awards index page fetch returned no detail.
- No consolidated public repository of insurer policy wordings was found.

---

## Q4. Agent architecture best practices (2025-2026) for this build

### Takeaway
Use **deterministic workflows with LLM steps** (prompt chaining, routing, an evaluator-optimizer loop) rather than a free-roaming multi-agent swarm. Put money arithmetic in Python tools, put extraction and drafting in the LLM, and gate every money-affecting action behind human approval with cited evidence. Treat the free Gemini quota as the scarcest resource: limits are undocumented and have been cut repeatedly.

### Cited Findings
- **Anthropic, "Building effective agents":**
  - Workflows use "predefined code paths"; agents "dynamically direct their own processes".
  - The five patterns: prompt chaining, routing, parallelization, orchestrator-workers and evaluator-optimizer.
  - "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs."
  - Put as much effort into the agent-computer interface (tool docs, examples, edge cases, mistake-proofing) as into human UIs.
  - Agents need guardrails and sandboxed testing because of compounding errors. — [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- **Gated autonomy and evidence packets** (Anterior) and an **AI review layer** auditing agent outputs (Infinitus) are production patterns in US health RCM. — [Anterior](https://www.anterior.com/); [Infinitus blog](https://www.infinitus.ai/blog/guardians-of-healthcare-calls-ai-review-in-action/)
- **Sentence-level citation grounding** with bounding boxes for verification. — [Reducto/Anterior](https://reducto.ai/blog/anterior-case-study)
- **Evaluation:** measure task completion, tool-use accuracy, cost per run and latency, with an eval harness from day one. — [AngelHack](https://angelhack.com/blog/ai-agent-hackathon/)
- **Gemini free tier is unstable:**
  - Google's official rate-limits page does not list free-tier numbers. It says limits "can be viewed in Google AI Studio". — [Google AI rate limits](https://ai.google.dev/gemini-api/docs/rate-limits); [AI Studio rate-limit page](https://aistudio.google.com/rate-limit)
  - Third-party sources conflict. One reports Gemini 2.5 Flash at 10 RPM / 250k TPM / 500 RPD; others report 1,500 RPD; another says quotas were cut 50-80% on 7 Dec 2025, to as low as 20-50 RPD in some configurations. — [aifreeapi](https://www.aifreeapi.com/en/posts/gemini-api-free-tier-rate-limits); [HowToGeek](https://www.howtogeek.com/gemini-slashed-free-api-limits-what-to-use-instead/); [pecollective](https://pecollective.com/tools/gemini-free-tier-guide/)
  - **These sources conflict. Check the team's actual quota in AI Studio before the build.**

### Inferences
- **Suggested architecture (single orchestrator plus specialised tools, not multi-agent chatter):**
  1. *Ingest/extract*: one LLM call per document with a strict JSON schema (structured output). Pydantic validates it and retries on failure.
  2. *Deterministic rule tools* (pure Python): moratorium and waiting-period calculation, room-rent proportionate deduction, non-payable lookup against the four lists, CGHS/HBP rate comparison, SLA timers. **No LLM arithmetic.**
  3. *Retrieval tool* over the clause-chunked corpus (IRDAI, policy wording, awards). Every claim the LLM makes must cite a chunk ID, and a post-check rejects any citation whose ID is not in the retrieved set. This "citation validity" check is cheap and can be shown in the demo.
  4. *Planner*: an orchestrator LLM chooses which tools to run based on claim stage (preauth / enhancement / final bill / settlement / rejection). This is a routing pattern, and it shows agency without the risk of a swarm.
  5. *Evaluator-optimizer*: a second pass critiques drafted letters against a checklist (cites clause? correct ₹? polite tone? correct addressee?).
  6. *HITL queue and audit log*: every action is stored with tool, inputs, outputs, citations, confidence, model and tokens.
  7. *Memory*: insurer-specific "learned rules" table (see Q2 #9).
- **Coping with the free tier:**
  - Cache LLM outputs by document hash, which also makes demo runs reproducible.
  - Batch bill-line assessment into one call instead of one call per line.
  - Use the cheaper Flash/Flash-Lite model for extraction and a stronger model only for drafting.
  - Pre-compute the demo cases. Keep a "replay mode" so the live demo survives quota exhaustion.
  - Rotate across several team members' API keys only if the provider's terms allow it (not checked).
- **PII:** redact names, phone numbers, policy numbers, Aadhaar and ABHA IDs with regex plus simple NER before sending text to a free-tier LLM. Show a "redacted view" toggle; responsible-AI jurors notice it. Free-tier data-use terms were not confirmed (see Gaps). Use synthetic or consented documents in the demo.
- **Confidence scores:** derive them from signals the team can defend, not LLM self-reports alone. Examples: extraction schema completeness, agreement between rule engine and LLM, retrieval similarity, and whether the citation check passed.

### Gaps
- Gemini free-tier data-use and training terms were not confirmed. The rate-limits page doesn't cover them, so check the Gemini API terms.
- Exact current free-tier quotas are unverified because of conflicting sources.
- No India-specific guidance was found on handling health data under the DPDP Act for hackathon prototypes (not searched).

---

## Q5. What wins agentic-AI hackathons, and demo/pitch best practices

### Takeaway
Agentic-AI hackathon rubrics usually weight **real-world impact/idea, technical execution, autonomy (acting with minimal manual intervention), use of tools, and the demo** roughly equally. Winners show a working end-to-end product live within 3 minutes, tell a story, and can explain their own differentiating code in Q&A.

### Cited Findings
- **Example rubric** (an agent hackathon on Devpost): Idea 20%, Technical Implementation 20%, Tool Use 20%, Presentation/Demo (3 minutes) 20%, and **Autonomy 20%**, defined as "how well the agent acts on real-time data without manual intervention". — [Devpost: AI Agents Hackathon (NVIDIA GTC 2025)](https://ai-agents-hackathon-gtc.devpost.com/) (rubric attributed via search snippet; other Devpost agent hackathons listed: [TiDB AgentX](https://tidb-2025-hackathon.devpost.com/), [Autonomous Agents Hackathon](https://autonomous-agents-hackathon.devpost.com/), [Forum Ventures x Anthropic](https://forum-x-anthropic-hackathon.devpost.com/))
- **Microsoft AI Agents Hackathon 2025:** judged by Microsoft engineers, PMs and developer advocates on "innovation, impact, technical usability, and alignment with corresponding hackathon category". The Best Overall Agent ($20,000) went to **RiskWise: Supply Chain Risk Analysis System**, a domain-specific risk-analysis agent. — [Microsoft AI Agents Hackathon](https://microsoft.github.io/AI_Agents_Hackathon/)
- Agent hackathons ask for agents that "use tools, take actions... sense, think, plan, retrieve, and execute", shown through an interactive UX. Autonomy and self-improvement are emphasised. — [AngelHack playbook](https://angelhack.com/blog/ai-agent-hackathon/); [Self-Evolving Agents Hack](https://self-evolving-agents-hack.devpost.com/)
- **What judges look for:** whether it works (most important), whether real people would use it, UX, technical innovation and scalability. They judge the product, not the code. — [Reskilll playbook](https://blogs.reskilll.com/how-to-win-hackathon-2026-complete-playbook/)
- **3-minute demo formula:** problem (10 s) → solution (10 s) → **live demo (90 s)** → how it works (30 s) → next steps (20 s). Write the 90-second demo script before writing code. — [Reskilll demo tips](https://blogs.reskilll.com/hackathon-demo-presentation-tips-pitch-3-minutes-win-2026/)
- **Further tips:**
  - Read the judging rubric before the problem statement.
  - Scope the idea so it is done in the first 25% of the time.
  - Use AI coding agents for the 80% of boilerplate, and write the differentiating 20% yourselves, because teams that can't explain it lose in Q&A.
  - Judges remember stories over features, so the problem should land within 30 seconds.
  - Sources: [Reskilll playbook](https://blogs.reskilll.com/how-to-win-hackathon-2026-complete-playbook/); [Masai](https://www.masaischool.com/blog/how-to-win-an-ai-hackathon-in-2026-full-guide/); [HackerEarth](https://www.hackerearth.com/blog/10-tips-win-hackathon); [ODSC Google Cloud hackathon winners](https://opendatascience.com/insights-from-the-winners-of-the-2025-odsc-google-cloud-hackathon/)
- **Eval and metrics:** show task completion, tool-use accuracy, cost per run and latency, not just a polished demo. — [AngelHack](https://angelhack.com/blog/ai-agent-hackathon/)

### Inferences
- **How each typical criterion maps to ClaimDesk:**
  - *Impact*: Ombudsman FY25 figures (37,431 health complaints) plus hospitals' cashless working-capital pain plus IRDAI's 1-hour and 3-hour rules.
  - *Autonomy*: the agent plans its tools by claim stage, processes a settlement letter end to end, and pre-empts queries from learned insurer rules.
  - *Technical*: citation-validated retrieval, a deterministic rule engine, FHIR ClaimBundle validation, and an eval harness.
  - *Tool use*: around 8-10 named tools visible in a live "agent trace" panel.
  - *Responsible AI*: HITL queue, audit log, PII redaction toggle, "AI never sends without approval".
  - *Business*: SaaS per bed or per claim for hospitals, with free ClaimSaathi for patients as a distribution and data flywheel. Mention LeapHealth as proof the market exists, and explain how ClaimDesk differs.
- **Demo plan:**
  - Open with a real-looking (synthetic, redacted) case: "A ₹2.4 lakh knee replacement; TPA deducted ₹38,000."
  - Show the agent trace streaming. End with the ₹ recovered, the contest letter citing the exact clause (click → highlighted PDF paragraph), and the patient's Telugu WhatsApp update.
  - Close with an eval scoreboard ("on 30 ground-truth cases: 94% non-payable detection, 100% citation validity, ₹ deduction calculations exact, 11 s per case, ₹0 LLM cost"). **These numbers are placeholders. Report only what the team actually measures.**
- **Live-demo risk:** keep a cached replay of each demo case and a screen-recorded backup, because the free-tier quota could run out during jury day.
- **For the Hyderabad finale:** Telugu output and a CGHS Tier-I/Tier-II comparison or a local hospital persona add local relevance.

### Gaps
- The Ziro hackathon's actual judging rubric, weights and juror profiles could not be found online.
- No detailed write-ups were found of what made specific winners (e.g., RiskWise) win. The winners pages give names and prizes only.
- No Indian (Devfolio/Unstop) agentic-hackathon winner write-ups were found in this research.
