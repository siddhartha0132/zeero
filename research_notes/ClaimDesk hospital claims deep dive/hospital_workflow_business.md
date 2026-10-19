# Indian Private Hospital Insurance/TPA Desk: Workflow, Leakage, Buyer, Pricing and GTM for "ClaimDesk"

Research date: 3 Oct 2026. Labels used: **[measured]** = regulator, filing or audited data; **[vendor claim]** = marketing or self-reported figure; **[anecdotal]** = practitioner or hospital self-description; **[unverified]** = single, low-authority source that could not be confirmed. Items in "Inferences" are my synthesis and domain knowledge. They are not independently sourced in this session and should be checked with 3–5 hospital TPA-desk heads before the pitch.

---

## 1. End-to-end cashless/reimbursement workflow, turnaround times and staffing

### Takeaway
The cashless flow runs in this order: eligibility/e-card check → pre-auth (doctor + patient + hospital form, estimate, notes and reports) → TPA queries → initial approval → enhancement(s) → final bill + discharge summary → discharge approval → (weeks later) settlement letter with deductions → NEFT/UTR reconciliation → follow-up on short or unpaid claims. IRDAI's May 2024 Master Circular sets 1 hour for a pre-auth decision and 3 hours for discharge approval, and insurers report high compliance. The money is not lost at authorisation. It leaks afterwards, through deductions, settlement delay and unreconciled short-payments. PM-JAY runs a separate, stricter, timer-driven workflow on TMS 2.0.

### Cited Findings
- **Pre-auth form structure [anecdotal, hospital SOP]:** the patient collects the pre-auth form from the TPA counter. It has three parts: one for the patient or relatives, one for the treating doctor, and one for the TPA cell. The doctor completes his part, the TPA cell attaches the required documents and fills in the cost estimate, and the file is forwarded for scrutiny. For planned admissions, hospitals ask patients to apply about 3 days before admission so TPA queries can be resolved — [Jaslok Hospital CAHO case study via search snippet](https://caho.in/files/AB_537-JASLOK%20HOSPITAL.pdf) (PDF returned HTTP 500 on fetch; content from search snippet only).
- **Discharge bottleneck [anecdotal, pre-2024]:** at Jaslok, internal work (returning or indenting medicines, preparing the bill and discharge summary, sending the file to the TPA desk) took about 2 hours. TPA/insurer approval then took at least 3–4 hours more. The hospital set a target of cutting discharge time from 6 hours to 3 hours for 80% of patients — [Jaslok/CAHO](https://caho.in/files/AB_537-JASLOK%20HOSPITAL.pdf).
- **Regulatory TATs [measured/regulatory]:** under the IRDAI Health Insurance Master Circular (May 2024), insurers must decide cashless requests "immediately but not more than one hour" after receipt and grant final discharge authorisation within 3 hours. If the delay goes beyond 3 hours, the insurer pays any extra hospital charges out of shareholders' funds. Systems had to be in place by 31 Jul 2024 — [Moneylife](https://moneylife.in/article/health-insurance-decide-cashless-request-in-1-hour-provide-final-authorisation-for-discharge-within-3-hours-says-irdai/74269.html); [OnePercentClub summary](https://news.onepercentclub.io/insurance/irdai-updates-health-insurance-master-circular-sets-3-hour-time-limit-for-cashless-claims/13503/).
- **Reported compliance [measured, insurer-reported], 1 Aug 2024 – 31 May 2025:** 86.88% of pre-auth requests were decided within 1 hour (55,35,353 of 63,71,620). 96.69% of final authorisations were completed within 3 hours (54,92,758 of 56,80,998). These figures come from a Parliament reply — [Angel One summarising data](https://oga-prod.angelone.in/news/personal-finance/cashless-health-insurance-claim-authorisation-in-2025-how-long-does-it-take-irdai-s-new-rules-and-data); [Sansad Q&A PDF](https://eparlib.sansad.in/bitstream/123456789/3015516/1/AS20_AaaDVE.pdf). Note: the clock starts when a *complete* request is received, so query loops do not count against the TAT.
- **Claims volume, FY24 [measured, IRDAI Annual Report 2023-24]:** 3.26 crore health claims were filed and 2.69 crore settled (82.46%). The average claim was Rs 31,086. 66.16% of claims were settled cashless and about 39% by reimbursement. 72% were settled through TPAs and 28% in-house by insurers — [Outlook Business, 30 Dec 2024](https://www.outlookbusiness.com/economy-and-policy/health-insurers-disallowed-claims-worth-rs-15100-crore-during-fy24). (The cashless and reimbursement shares sum to more than 100% as reported; they likely use different bases.)
- **TPA landscape:** there were more than 30 IRDAI-licensed TPAs by late 2024. Another source counted 20 on the IRDAI list as of Sep 2023, so the counts conflict — [Bajaj Finserv Markets / search summary](https://www.bajajfinservmarkets.in/insurance/health-insurance/tpa-insurance-companies-list.html). Medi Assist (the largest TPA) had a provider network of 20,204 hospitals in FY25. It holds a 30.3% share of group premiums under management and a 5.7% share of retail. 19 insurers used its network exclusively. It reports more than 175,000 "express discharges" through its Raksha Prime product — [Medi Assist FY25 press release](https://mediassist.in/assets/pdf/investor-relations/mahs/disclosure-under-reg-30/press-release-q4-and-fy25-results.pdf); [FilingReader summary](https://filingreader.com/news-wire/mumbai/2025-08-30/medi-assist-reports-strong-fy25-performance-ahead-of-25th-agm).
- **PM-JAY / state schemes on TMS 2.0 [regulatory/manual, summarised by an HMIS vendor blog, 18 Sep 2026]:** the stages are beneficiary identification (Ayushman ID/ABHA with Aadhaar), registration, pre-auth, treatment and discharge, claim submission and SHA payment.
  - **Private-hospital pre-auth:** must be initiated within 48 hours. The scheme has 6 working hours to decide, after which the request is auto-approved.
  - **Claim submission:** within 7 days of discharge. This extends to 21 days with SHA approval and 45 days with CEO approval.
  - **Query response:** within 7 days, or the claim is auto-rejected.
  - **Payment:** due within 15 days intra-state and 30 days inter-state.
  - **Packages:** all-inclusive HBP rates. With multiple procedures, the highest is paid at 100%, the second at 50% and later ones at 25%.
  - **Adjudication chain:** Claims Executive → Claims Processing Doctor → Accounts Officer → SHA, and "any one of them can send it back". Appeals go to the District Grievance Nodal Officer within 15 days.
  - **Discharge evidence:** discharge summary plus photographs. LAMA/DAMA cases need consent documents; deaths need a death certificate and mortality audit.
  - Source: [Nirmitee.io blog](https://nirmitee.io/blog/nhcx-pmjay-tms-ayushman-bharat-claims/) (vendor blog citing the TMS 2.0 Provider Manual v12.0, 10 Jan 2025).
- **PM-JAY settlement in practice:** the norm is 15 days, but average TAT is around 90 days per a CAG-linked source. Typical rejection rules: pre-auth initiated after the date of discharge; surgery dated before admission; length of stay inflated in TMS — [CAG audit chapter](https://cag.gov.in/uploads/download_audit_report/2023/09_Chapter-V-064d22bab412c53.02505839.pdf); [Uttarakhand SHA claim-payment guidepoints](https://sha.uk.gov.in/ScannedDocs/WebSite/Uploads/CLAIM_ADJ/guidepoints-for-claimpayment-v1.pdf) (search-snippet level; the "~90 days" figure should be checked against the CAG PDF itself).
- **Medi Assist self-service:** IVR, chatbot and WhatsApp resolve 41% of inbound queries. This shows TPAs are automating their side, so the hospital side is the laggard — [FilingReader FY25](https://filingreader.com/news-wire/mumbai/2025-08-30/medi-assist-reports-strong-fy25-performance-ahead-of-25th-agm).

### Inferences
(Domain knowledge to inform the product. Not sourced in this session; validate with users.)
- **Detailed cashless sequence at a 50–300-bed hospital:**
  1. **Admission/eligibility.** The desk collects the policy e-card or TPA card, photo ID (Aadhaar or PAN), the employee ID for corporate/group policies, and the policy copy. It checks the sum insured remaining, room-rent eligibility, co-pay and sub-limits on the TPA or insurer portal or by phone.
  2. **Pre-auth submission.** Documents: the standard IRDAI cashless request form (Part A patient, Part B hospital/doctor), the doctor's admission note (presenting complaints, duration, clinical findings, provisional diagnosis, line of treatment), investigation reports that support the diagnosis, an itemised cost estimate (room × days, OT, surgeon, anaesthetist, implants, pharmacy, investigations), and ID plus e-card. Channels: the TPA or insurer portal, email to the TPA's cashless ID, or increasingly NHCX/IHX.
  3. **Query.** Typical asks: "provide first consultation paper", "duration of ailment / past history (for PED)", "indoor case papers", "investigation reports supporting diagnosis", "alcohol/RTA – MLC copy/FIR", "implant sticker/invoice".
  4. **Initial approval.** Usually only a portion of the estimate is approved, conservatively.
  5. **Enhancements.** Filed when length of stay or the plan changes (ICU shift, additional surgery), with updated notes and an interim bill.
  6. **Discharge.** Final bill (itemised), discharge summary signed by the treating doctor, final investigation reports, pharmacy bills, implant invoice and stickers, OT notes, and the patient's signed claim form.
  7. **Final approval.** The approval letter lists the approved amount and the patient-payable portion (non-payables, co-pay, proportionate deduction). The patient pays that balance at the counter.
  8. **Physical file.** Original documents are couriered to the TPA within the window stated in the hospital-TPA MoU (often 7–15 days).
  9. **Settlement.** The settlement letter shows claimed vs. approved vs. paid, with deduction heads and a TDS deduction. NEFT arrives with a UTR, often batched across many claims.
  10. **Reconciliation.** Billing/finance matches each UTR to claim IDs in the HIS and books short-payments as write-off or for dispute.
- **Staffing (assumption):** a 100–200-bed hospital typically runs a TPA desk of 3–8 coordinators across shifts (cashless is 24×7 for emergencies), plus 1–2 billing executives on insurance AR. MRD supplies case papers. A doctor or "medical coordinator" handles medical queries. Desk staff are often non-graduate or B.Sc. hires; attrition is high and knowledge sits in people's heads.
- **Reimbursement (non-cashless):** the hospital's role is to provide documents (final bill, discharge summary, reports, payment receipts). The patient files the claim. For a hospital-desk product this is a document-pack generator rather than an AR item.

### Gaps
- Could not fetch the Jaslok CAHO PDF (HTTP 500) for full metrics; only snippet-level data is used.
- No measured Indian data found on the **% of cashless pre-auths that receive at least one query**, the average number of query cycles, or the average number of enhancements per case. Recommend primary interviews.
- No public staffing benchmark (FTE per 100 beds or per 1,000 claims) for TPA desks was found.
- No measured average time from discharge to NEFT receipt for private insurers was found (see Section 2 for anecdotal ranges).

---

## 2. Failure points, query/deduction reasons and quantified leakage

### Takeaway
At industry level, regulator data for FY24 shows insurers **disallowed 12.9% of claimed value (Rs 15,100 crore)**, **repudiated 9.34% (Rs 10,937 crore)** and left **6.48% outstanding**: only 71.29% of claimed value was paid. That is the clearest measured "leakage" number. Deduction drivers are well documented qualitatively: proportionate room-rent deduction, non-payables or consumables, package-rate caps, length of stay, and document or date mismatches. Hospital-level receivable-day data is mostly anecdotal.

### Cited Findings
- **FY24 [measured, IRDAI Annual Report]:** total claims Rs 1.17 lakh crore. Paid Rs 83,493 crore (71.29%), disallowed Rs 15,100 crore (12.9%), repudiated Rs 10,937 crore (9.34%), outstanding Rs 7,585 crore (6.48%) — [Outlook Business](https://www.outlookbusiness.com/economy-and-policy/health-insurers-disallowed-claims-worth-rs-15100-crore-during-fy24); [Cafemutual](https://cafemutual.com/news/press-news/33848-health-insurance-claim-rejections-by-insurance-companies-went-up-by-1910-in-fy24). Caveat: "disallowed" includes deductions borne by patients in reimbursement claims and patient-payable amounts in cashless claims, not only hospital write-offs.
- **Proportionate deduction rule:** when a patient takes a room above the policy's room-rent limit, the insurer cuts associated charges in proportion: room, nursing, doctor fees, OT, anaesthesia, blood and oxygen. Under the 2024 IRDAI Master Circular, pharmacy and consumables, implants and devices, diagnostics and ICU charges are **excluded** from proportionate deduction — [Ditto](https://joinditto.in/articles/health-insurance/proportionate-deduction-in-health-insurance/); [Reliance General](https://www.reliancegeneral.co.in/Insurance/Knowledge-Center/Insurance-Reads/IRDAI-Redefining-Sub-Limit-Rules-for-Health-Insurance.aspx); [Moneylife on prorating](https://moneylife.in/article/mediclaim-should-a-hospital-bill-be-prorated-based-on-your-room-rent-limit/33365.html).
- IRDAI has flagged that high claim-settlement ratios hide frequent **partial payouts** driven by room-rent caps, sub-limits, co-pays and exclusions — [Business Standard, Nov 2025](https://www.business-standard.com/amp/finance/personal-finance/partial-hospital-bill-payout-boost-policy-cover-to-secure-full-claims-125111401478_1.html) (403 on fetch; search snippet only).
- IRDAI's chairman (Sept 2024) said cashless "isn't fully cashless yet" because insurers deduct for consumables and charges — [Outlook Money, updated 6 Sep 2024](https://www.outlookmoney.com/personal-finance/insurance/irdai-to-introduce-100-cashless-insurance-settlement-what-policyholders-need-to-know).
- **Hospital-side grievances (AHPI, Aug 2025):** AHPI advised North-India member hospitals to suspend cashless service for Bajaj Allianz from 1 Sep 2025. The complaints were:
  - tariffs not revised and pressure for further cuts on expired agreements;
  - **unilateral claim deductions**;
  - delays in settlement;
  - lengthy pre-auth and discharge approvals.

  AHPI demanded tariff revisions of 7–8% a year in line with medical inflation and had issued similar warnings to Care Health and Niva Bupa. The advisory was withdrawn on 2 Sep 2025 — [The Week/PTI](https://www.theweek.in/wire-updates/business/2025/08/22/dcm83-biz-hospitals-bajaj.html); [Outlook Money](https://www.outlookmoney.com/news/ahpi-hospitals-to-suspend-cashless-treatment-for-bajaj-allianz-policyholders-from-september-1); [Outlook Money – GI Council pushback](https://www.outlookmoney.com/personal-finance/cashless-care-at-risk-gi-council-pushes-back-what-policyholders-should-know-if-services-stop).
- **PM-JAY rejection triggers:** pre-auth initiated after discharge; treatment or surgery dated before admission; inflated length of stay in TMS — [Uttarakhand SHA guidepoints](https://sha.uk.gov.in/ScannedDocs/WebSite/Uploads/CLAIM_ADJ/guidepoints-for-claimpayment-v1.pdf); [SHA Claims Adjudication FAQs](https://sha.uk.gov.in/ScannedDocs/WebSite/Uploads/CLAIM_ADJ/Claims%20Adjudication%20FAQs.pdf).
- **Receivables [anecdotal / startup pitch claim, unverified]:** "Hospitals wait 45 to 270 days to receive payment from TPAs," fund the gap with 14–24% p.a. overdrafts, and about **Rs 50,000 crore** of approved receivables sit on hospital balance sheets at any time. The burden is concentrated in small and mid-size hospitals, where government and PSU-insurer schemes make up 30–50% of revenue — [iCReDS listing on UP Startup portal](https://www.startinup.up.gov.in/crm/Welcome/startup_user_details/NDMzMTI=). Treat this as an unverified pitch number.
- **Hospital-finance startups confirm the pain:** CareFi offers working-capital financing plus "AI-driven revenue management" for hospitals and was backed by Accion (Feb 2026) — [Accion](https://www.accion.org/building-the-financial-rails-for-cashless-healthcare-in-india). HealthCRED raised US$1.2M seed (Aug 2024) — [TechNode Global](https://technode.global/2024/08/12/indias-healthcred-secures-1-2m-in-seed-funding-round-led-by-antler-india-trtl-vc-devc-iseedvc-and-angel-list-india/).
- **Competitor-claimed impact [vendor claim]:** LeapHealth claims claim-approval turnaround falls from "5d → 2d" and initial denials fall by 12% — [LeapHealth](https://theleaphealth.com/ai-agents/insurance-tpa).
- **US analog [measured, US]:** US hospitals spent about $43B in 2025 seeking payment from insurers. Rework or appeal costs about $181 per claim — [Chief Healthcare Executive](https://www.chiefhealthcareexecutive.com/view/hospitals-spent-43b-to-get-payments-from-insurers-report). Inpatient initial denial rates rose 10–14% in 2025 — [Fierce Healthcare](https://www.fiercehealthcare.com/finance/despite-better-cash-flow-providers-missed-out-more-revenue-2025-due-increased-payer-denials).

### Inferences
- **Deduction taxonomy for product design** (practitioner knowledge, to validate with real settlement letters):
  1. Non-payables under IRDAI's standardised list of excluded items (Annexure/List I to the guidelines on standardisation; for example gloves, masks, admission kit, attendant charges, documentation charges, some consumables);
  2. Proportionate room-rent deduction;
  3. Charges above PPN/GIPSA or negotiated package or tariff ("charges exceed agreed tariff");
  4. "Reasonable and customary" cuts on surgeon or OT fees;
  5. Length-of-stay disallowance ("prolonged stay not justified");
  6. Pharmacy not supported by indoor case papers or prescriptions;
  7. Investigations not related to the diagnosis;
  8. Duplicate or double-billed items (e.g., a consumable billed both inside the package and in pharmacy);
  9. Co-pay or sub-limits (cataract, knee replacement, modern treatments);
  10. Unexplained "TDS" or "MOU discount" lines.

  An agent that parses settlement letters into these buckets and maps each to a hospital action (bill correctly next time, dispute, or recover from patient) is directly valuable.
- **Proxy for hospital leakage:** a reasonable assumption for the pitch, to be validated, is a 5–10% deduction on cashless private-insurer bills, plus 1–3% never reconciled or written off. The FY24 figure of 12.9% disallowed is industry-wide and includes patient-borne deductions, so do not claim it is all hospital loss.
- Many deductions are **preventable at billing time**: room-category mismatch, non-payables billed into the insurer share instead of the patient share, missing implant invoices. That points to a "pre-submission bill scrubber" as the highest-ROI demo feature.
- The **query → response loop** is where coordinator hours go. TAT compliance looks good on paper because the clock restarts with each complete submission.

### Gaps
- No measured Indian data on the **percentage of claims with queries**, the **average deduction % on cashless claims at hospital level**, or **write-off %**. AHPI and NATHEALTH surveys may exist but were not found.
- No measured **insurance receivable days** for unlisted mid-size hospitals. Listed-chain annual reports give overall debtor days, but these were not pulled in this session.
- Specific "reasonable and customary" methodology by insurer is not public.

---

## 3. GIPSA PPN, negotiated tariffs and portal fatigue

### Takeaway
GIPSA (the four PSU insurers: New India, National, Oriental, United India) negotiates standard package rates with PPN hospitals, varied by procedure, city and room category. Private insurers and TPAs each run their own tariffs and MoUs. A hospital empanelled with 20–40 payers maintains many rate cards and logs in to many portals. Two consolidation paths exist, but neither is mandatory for hospitals: NHCX (voluntary; about 34 insurers/TPAs and about 300 hospitals ramping up by July 2024) and the GI Council's work on common empanelment. Fragmentation is therefore still the 2026 reality.

### Cited Findings
- GIPSA is the coordination body of four PSU general insurers. Its PPN is a set of hospitals that agree to negotiated package rates for PSU-insurer policyholders. The package rate depends on procedure, city and eligible room category, and PPN hospitals cannot bill above the package — [Ditto](https://joinditto.in/articles/health-insurance/general-insurance-public-sector-association/); [Acko](https://www.acko.com/group-health-insurance/blogs/gipsa-ppn-empanelment-in-group-health-insurance/); [ICICI Lombard](https://www.icicilombard.com/blogs/online-insurance/article/what-is-gipsa-in-group-health-insurance).
- **Insurer network sizes** (marketing figures): Star Health 14,000+, Cholamandalam MS 10,000+, Aditya Birla Health 9,000+, Manipal Cigna 8,500+ network hospitals — [Oasis Hospital Solutions](https://oasishospitalsolutions.com/tpa-business-company-tie-ups-in-india/). Medi Assist's network was 20,204 hospitals in FY25 — [Medi Assist](https://mediassist.in/assets/pdf/investor-relations/mahs/disclosure-under-reg-30/press-release-q4-and-fy25-results.pdf).
- **CGHS rates revised (effective 13 Oct 2025)** for about 2,000 procedures, the first full revision since 2014. Rates now vary by accreditation and city tier: Tier-II is 19% lower and Tier-III 20% lower. Rates assume a semi-private ward, with general ward 5% lower and private 5% higher — [Tribune](https://www.tribuneindia.com/news/india/centre-revises-rate-of-2000-medical-procedures); [IANS](https://ianslive.in/health-industry-bodies-welcome-cghs-move-to-revise-rates-after-15-years--20251004165312). This matters because CGHS rates often anchor PSU and government tariffs.
- **NHCX:**
  - **Not mandatory:** the IRDAI 8 Jun 2023 circular "advised" insurers and TPAs to adopt it; the May 2024 Master Circular says insurers "may endeavor" to onboard providers.
  - **Adoption:** 34 insurers/TPAs live and about 300 hospitals ramping up (Jul 2024).
  - **Certification and format:** there is no NHCX certification, only self-attestation. Claims use FHIR R4 bundles with async callbacks. It needs ABDM M1–M3 (v3 APIs) plus HFR/HPR registration.
  - **Incentives:** under the DHIS incentive (Corrigendum 7, Apr–Sep 2026), facilities get Rs 200 per claim (or 10%, whichever is lower) and software vendors Rs 10 per claim, for PM-JAY FHIR claims only.
  - **PM-JAY:** still runs on TMS 2.0 in production.
  - Source: [Nirmitee.io, Sep 2026](https://nirmitee.io/blog/is-nhcx-mandatory-hospitals-hmis-2026/) (vendor blog, but cites circular numbers); [BusinessWorld on launch](https://businessworld.in/article/government-poised-to-launch-unified-insurance-claim-portal-520717); [Digital Health News – 10 hospitals, 8 insurers integrated](https://digitalhealthnews.com/nha-s-nhcx-integrates-10-hospitals-8-insurers-marking-significant-achievement).
- **Common empanelment / "Cashless Everywhere":** the GI Council set up a committee on a common hospital empanelment process and standard onboarding prices. IRDAI's chair pushed for "100% cashless" in Sept 2024 — [Outlook Money](https://www.outlookmoney.com/personal-finance/insurance/irdai-to-introduce-100-cashless-insurance-settlement-what-policyholders-need-to-know).
- **[Unverified]** One site claims an IRDAI circular dated 2 Jan 2026 (ref. IRDAI/HLT/MISC/CIR/001/01/2026). It would require 100% cashless at all network hospitals by 1 Oct 2026, phased Metro/50+ beds by 31 Mar 2026, Tier-2 by 30 Jun 2026, and the rest by 1 Oct 2026. Insurers would integrate real-time pre-auth with hospitals' billing software, with penalties up to licence review. The same site says about 40% of private hospitals still use paper billing — [Oquilia](https://www.oquilia.com/news/irdai-100-percent-cashless-mandate-2026). **I could not corroborate this with IRDAI, the mainstream press or any second source. Do not use it in the pitch without checking irdai.gov.in.**

### Inferences
- **Portal fatigue is real but undocumented in measured form.** A mid-size hospital is typically empanelled with the 4 PSU insurers (through PPN or TPAs), 10–20 private and SAHI insurers, and about 10–20 TPAs, plus PM-JAY/state schemes, CGHS/ECHS and corporates. Each has its own portal or email channel, document checklist, tariff and MoU. The agent's core value is a **single desk workbench**: one case record, auto-assembled document packs per payer, portal submission (RPA or API/NHCX), and a unified query inbox across email, portal and WhatsApp.
- NHCX is the strategic "official API" path. Supporting NHCX FHIR claim bundles is a credibility point and lowers ToS risk compared with screen-scraping. Near-term coverage is partial, so RPA or browser agents for the main TPA portals (Medi Assist, MDIndia, FHPL, Paramount, Health India, Vidal, Ericson, Raksha, Heritage, etc.) will still be needed.
- **Tariff management is a sleeper feature:** keep each payer's package and tariff rate card (PPN, CGHS-linked, private MoU) in a structured form. Use it to pre-validate estimates and bills and to flag "charges exceed agreed tariff" before submission.

### Gaps
- No public measured count of how many payers a typical 100–200-bed hospital is empanelled with.
- GIPSA PPN rate cards are not public, and the hospital count in PPN is not confirmed.
- Neither the 2026 status of the GI Council common empanelment nor the reported Jan 2026 IRDAI circular could be verified.

---

## 4. Buyer, hospital segments and insured revenue share

### Takeaway
The economic buyer at a mid-size (50–300-bed) hospital is the owner-promoter (often a doctor) or the CFO/finance head. The administrator or COO, and the TPA/insurance-desk head as the daily user and champion, influence the deal. The segment is large and fragmented. Private hospitals grew from about 30,000 to 38,000 between 2019 and 2024. Facilities under 100 beds are 46% of scheme-empanelled hospitals and handle 54% of hospitalisations. Insured or scheme revenue ranges from about 25% to more than 60% depending on the hospital.

### Cited Findings
- Private hospitals grew about 27%, from about 30,000 to 38,000, between 2019 and 2024. Small and mid-sized facilities (under 100 beds) are 46% of facilities empanelled under government insurance schemes and account for 54% of hospitalisations. Ayushman Bharat covers more than 500 million people and ESIS more than 150 million workers — [Accion, 11 Feb 2026](https://www.accion.org/building-the-financial-rails-for-cashless-healthcare-in-india).
- Among insurance-empanelled hospitals in one dataset: about 65% have 11–50 beds, 13% have 50–100 beds and 8% have more than 100 beds — [NIPFP Working Paper 254 (2019)](https://www.nipfp.org.in/media/medialibrary/2019/02/WP_254_2019.pdf) (older data).
- The private sector has about 60–65% of hospitals and beds; another estimate puts private hospitals and nursing homes at about 72% of beds — [ICRA Dec 2023](https://www.icra.in/Rating/DownloadResearchSummaryReport?id=5426); [Upstox](https://upstox.com/news/upstox-originals/investing/india-s-hospital-bed-shortage-is-private-expansion-enough/article-200750/).
- Private hospitals handled 6.74 crore of the 11.69 crore PM-JAY admissions recorded by Feb 2026 — [Upstox](https://upstox.com/news/upstox-originals/investing/india-s-hospital-bed-shortage-is-private-expansion-enough/article-200750/).
- **Payer mix examples [measured, company disclosures]:**
  - Global Health (Medanta) in-patient revenue: Cash 62.8%, TPA 23.7%, CGHS/ECHS/Railways 8.5%, PSU and corporate 3.3% — [JKBFSL IPO note](https://www.jkbfsl.com/market/ipo/news_details/IPO_News/1659848).
  - Yatharth Hospital (Tier-2 NCR/UP): about 35–37% from government schemes (Ayushman, defence, railways), the rest TPA/insurance and cash — [Value Research](https://www.valueresearchonline.com/stories/225141/yatharth-hospital-stock-breakout/).
  - The small/mid-size claim of government/PSU schemes at 30–50% of revenue is a startup claim — [iCReDS (unverified)](https://www.startinup.up.gov.in/crm/Welcome/startup_user_details/NDMzMTI=).

### Inferences
- **Buyer map:**
  - *Owner-doctor/promoter* (50–150 beds, Tier-2/3): decides fast, very price-sensitive, buys on "cash in hand sooner / fewer deductions" and "reduce my dependence on the one experienced TPA guy".
  - *CFO/finance head* (150–300 beds, small chains): buys on DSO, write-offs and reconciliation.
  - *Unit COO/administrator:* buys on discharge TAT and NABH/patient experience.
  - *TPA desk head:* daily user who can block or champion. Position the product as "co-pilot, not replacement".
- **ICP for ClaimDesk:** 75–300-bed multi-specialty private hospitals in Tier-1/2 cities with more than 40% insured/scheme revenue and roughly 300–1,500 cashless claims a month. These hospitals have enough volume to feel the pain and are often on a mid-tier HIS (or a homegrown one) without a strong claims module.
- **Rough serviceable market (assumption):** with about 38,000 private hospitals, if about 8–10% (about 3,000–4,000) have more than 50 beds and meaningful insured volume, that is the core addressable base. Nursing homes under 30 beds are a long tail better served via HIS partners or a lightweight WhatsApp-first SKU.

### Gaps
- No authoritative 2025–26 count of private hospitals by bed band, or of PPN/TPA-empanelled hospitals by size, was found.
- No measured insured-revenue share for unlisted mid-size hospitals.

---

## 5. Existing HIS/HMS vendors and claims modules

### Takeaway
Most Indian HIS products carry a basic "TPA/insurance billing" module: payer master, tariff per payer, split bill (patient vs. insurer share), pre-auth tracking fields, and sometimes NHCX/ABDM connectors. None was found doing agentic document assembly, query handling or settlement-letter reconciliation. A newer cohort is moving into that space, including LeapHealth's insurance AI agent (customers include Apollo and CloudNine), i3systems' CliniAId (aimed at payers) and InterPixels (TPA-side).

### Cited Findings
- **HIS pricing and module presence (from a vendor-authored listicle, so expect bias):**
  - Insta by Practo: from about Rs 25,000/month, large hospitals, includes "Insurance and TPA claim management". An alternate figure is $15/user/month with a 20-user minimum.
  - Attune NxG: custom pricing, "Insurance and TPA management".
  - Birlamedisoft: about Rs 2.5 lakh one-time.
  - BajajHealth HMS: about Rs 3.5 lakh one-time.
  - MocDoc: from Rs 1,000/month.
  - eHospital (NIC): free, government.
  - Practo Ray: Rs 1,500/month, clinics.
  - Source: [Codingclave (vendor), 2026](https://codingclave.com/blog/best-hospital-management-software-india-2026); [SoftwareAdvice – Insta](https://www.softwareadvice.com/medical/insta-profile/).
- KareXpert lists claims management and policy management features; pricing is per feature or on request — [Techjockey/alternatives listing](https://www.techjockey.com/alternatives/hwai) (search snippet).
- Local billing-software vendors now advertise "Insurance · NHCX · AI" — [OneCity](https://onecity.co.in/hospital-billing-software-bangalore).
- **LeapHealth Insurance & TPA AI agent:**
  - File assembly (consult notes, prescriptions, reports, itemised bills); mandatory-document checks; denial prediction from historical TPA decisions; non-payable flags;
  - Submission, and answering routine TPA queries by WhatsApp or email; TAT monitoring; AR ageing by TPA or branch;
  - Escalates rejections, disputed amounts and medical-necessity queries to humans;
  - Integrates with its own HealthPro CRM and Leap OS, EMRs and Razorpay; DPDPA-aligned, ISO 27001, AWS Mumbai;
  - Customers listed: Apollo, Motherhood, CloudNine, Nova IVF; "live in 3–4 weeks";
  - Volume-tiered pricing, not public.
  - Source: [LeapHealth](https://theleaphealth.com/ai-agents/insurance-tpa).
- **Payer- or TPA-side AI (adjacent, not direct competitors):**
  - i3systems CliniAId reads hospital documents for claim approval "in under 10 minutes instead of 30+" — [CB Insights](https://www.cbinsights.com/company/i3systems-india).
  - InterPixels cut per-claim processing for an Indian insurtech from 40 to 5 minutes across more than 15,000 claims — [InterPixels](https://interpixels.ai/case-studies/).
  - RapidClaims (US-focused coding AI) raised $8M — [Outlook Business](https://www.outlookbusiness.com/news/ai-saas-start-up-rapidclaims-raises-8m-to-expand-healthcare-automation).
- **Outsourced TPA-desk services exist** (Medicon Group, MedCheck Healthcare) and offer staffed desks with standard workflows. Prices are not public — [Medicon](https://www.medicongroupindia.com/tpa-desk-management-services-a-critical-pillar-of-hospital-insurance-operations/); [MedCheck](https://medcheckhealthcare.com/tpa-desk-outsource/).
- **NHCX integration needs** for HMIS: ABDM M1–M3 v3, a valid WASA security audit, FHIR claim bundles, async callbacks, and HFR/HPR registration — [Nirmitee](https://nirmitee.io/blog/is-nhcx-mandatory-hospitals-hmis-2026/).

### Inferences
- **Integration pattern for a hackathon or early product:** do not try to replace the HIS. Read from it through (a) PDF or printout ingestion (bills, discharge summaries, reports: the lowest-friction path for Tier-2 hospitals running Birlamedisoft, Lifeline, Suvarna or homegrown systems), (b) HL7/FHIR or DB views where available, and (c) an HIS partnership in which ClaimDesk ships as the HIS's "AI TPA module" with a revenue share.
- LeapHealth is the closest visible competitor. Its pitch overlaps heavily, so ClaimDesk should differentiate on Tier-2 mid-size focus, multi-portal execution, settlement-letter/UTR reconciliation and deduction analytics, and on working with *any* HIS.

### Gaps
- No direct verification of claims-module depth for Suvarna, Akhil Systems, Lifeline, eHospital or KareXpert. Vendor websites were not fetched.
- No public price for LeapHealth or for outsourced TPA desk services.

---

## 6. Pricing benchmarks, willingness to pay, sales cycle and channels

### Takeaway
There is little public Indian pricing for claims/RCM software. HIS spend for mid-size hospitals is low: roughly Rs 2–3.5 lakh one-time or Rs 5,000–25,000+ per month. US RCM benchmarks are 2–9% of collections for enterprise RCM and 3–5% for comprehensive hospital RCM (KLAS 2023), with services billing at 4–10%. ClaimDesk should price on outcome (per claim or a small % of recovered or accelerated money) with a floor, sized well below US rates.

### Cited Findings
- **US analog:** enterprise RCM is priced at about 2–9% of collections. Hospitals typically pay 3–5% for comprehensive RCM (KLAS 2023), and the percentage falls with volume — [Monetizely](https://www.getmonetizely.com/articles/procurement-guide-how-hospital-revenue-cycle-management-rcm-systems-are-priced-for-enterprises). Billing services run 4–10% of collections, most commonly 5–7%; below 4% usually means a basic or offshore service — [Carepatron 2026](https://www.carepatron.com/blog/how-much-do-medical-billing-services-cost/). Outsourcing makes sense when cost-to-collect exceeds about 4% or denials exceed 10% — [Wisemonk](https://www.wisemonk.io/blogs/outsourcing-revenue-cycle-management).
- **India HIS price points:** Insta about Rs 25,000/month for large hospitals; Birlamedisoft about Rs 2.5 lakh one-time; BajajHealth about Rs 3.5 lakh one-time; budget HMS about Rs 75,000 one-time — [Codingclave (vendor)](https://codingclave.com/blog/best-hospital-management-software-india-2026).
- **Government incentive as a revenue line:** DHIS pays software vendors Rs 10 per PM-JAY NHCX claim and facilities Rs 200 per claim (Apr–Sep 2026; terms changed often — Rs 500 per claim under Corrigendum 6) — [Nirmitee](https://nirmitee.io/blog/is-nhcx-mandatory-hospitals-hmis-2026/).
- **Financing comparison:** hospitals bridge receivables with 14–24% p.a. overdrafts [unverified]. Receivable-financing marketplaces target under 8% p.a. — [iCReDS listing](https://www.startinup.up.gov.in/crm/Welcome/startup_user_details/NDMzMTI=). CareFi bundles financing with RCM software — [Accion](https://www.accion.org/building-the-financial-rails-for-cashless-healthcare-in-india).
- **Channels:** AHPI is the main private-provider association. It negotiates collectively with insurers, as in the Aug 2025 Bajaj Allianz action — [The Week/PTI](https://www.theweek.in/wire-updates/business/2025/08/22/dcm83-biz-hospitals-bajaj.html). CAHO publishes hospital quality and process case studies such as Jaslok's TPA discharge project — [CAHO](https://caho.in/files/AB_537-JASLOK%20HOSPITAL.pdf).

### Inferences
- **Illustrative unit economics (assumption, validate):**
  - A 150-bed hospital with about 60% occupancy, 4-day ALOS and about 40% insured makes roughly 270 insured discharges a month.
  - At an average insured bill of about Rs 60,000–80,000 in Tier-2 private hospitals (above the Rs 31k industry average claim, which includes small claims), monthly insured billing is roughly Rs 1.6–2.2 crore.
  - Recovering even 2 percentage points of deductions is worth about Rs 3–4 lakh a month. Cutting desk effort by 1–2 FTE saves about Rs 25–50k a month (Tier-2 coordinator salaries are about Rs 15–30k a month, per job listings such as [PlacementIndia](https://www.placementindia.com/job-search/tpa-coordinator-jobs.htm), not fetched).
- **Suggested pricing hypotheses:**
  - (a) SaaS of Rs 25,000–75,000 per month per hospital, tiered by claim volume;
  - (b) Rs 150–400 per cashless claim processed;
  - (c) a hybrid base plus 1–2% of *incremental* recoveries (deductions overturned, write-offs collected).

  All are well below US rates (3–5%), reflecting Indian WTP and the HIS spend anchor. A % of total collections is a hard sell to Indian owners. A share of "money we found for you" is easier.
- **Sales cycle (assumption):** owner-run hospitals take 1–3 months with a pilot (decisions are fast, but trust is needed); 3–6+ months for chains, with IT and security review and DPDP vendor diligence.
- **Channels:**
  1. Direct to owner-doctors in 2–3 Tier-2 clusters via AHPI state chapters and local IMA/hospital-owner associations;
  2. HIS vendor partnerships (white-label claims module), the highest-leverage route for the long tail;
  3. Hospital-finance players (CareFi, HealthCRED-type) who want cleaner claims to lend against;
  4. Consultants who do TPA empanelment and NABH;
  5. TPAs themselves: some (Medi Assist) want cleaner first submissions and may co-market. This is risky because of alignment.

### Gaps
- No public pricing for Indian claims/RCM software or outsourced TPA desks (per claim or %). Primary price discovery with 5–10 hospitals is needed.
- No measured sales-cycle data for Indian hospital SaaS.
- No AHPI or NATHEALTH document on software procurement found.

---

## 7. Risks: DPDP, liability, insurer pushback, portal ToS, data access

### Takeaway
DPDP Rules were notified on 13–14 Nov 2025 with an 18-month phase-in, so full obligations apply from about 13 May 2027. Hospitals are data fiduciaries and ClaimDesk would be a processor, so a DPA, consent flows, breach notice within 72 hours and India hosting are table stakes. Bigger practical risks: TPA or insurer portal ToS against bots, liability for wrong clinical or coding content in submissions, and insurers using AI on their side, which raises the evidence bar.

### Cited Findings
- **DPDP Rules 2025** were notified by MeitY on 13–14 Nov 2025 with phased compliance. The Data Protection Board was constituted immediately, consent managers come at about 12 months (Nov 2026), and full compliance is due at 18 months (about 13 May 2027). Obligations include consent, security safeguards and 72-hour breach reporting — [Hogan Lovells](https://ca.hoganlovells.com/en/publications/indias-digital-personal-data-protection-act-2023-brought-into-force-); [PIB document](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf); [Storyboard18](https://www.storyboard18.com/digital/breaking-govt-notifies-final-dpdp-rules-sets-staggered-rollout-with-key-obligations-for-data-fiduciaries-84201.htm). The government signalled it may **shorten** the 18-month timeline — [Storyboard18](https://www.storyboard18.com/how-it-works/govt-to-shorten-dpdp-rules-18-month-compliance-timeline-ib-minister-ashwini-vaishnaw-84323.htm).
- **NHCX** requires a valid WASA security audit and ABDM registration for HMIS integration — [Nirmitee](https://nirmitee.io/blog/is-nhcx-mandatory-hospitals-hmis-2026/).
- **PM-JAY fraud enforcement:** hospitals are de-empanelled for guideline violations, so incorrect or inflated submissions carry real consequences — [Omnicuris, Aug 2026](https://www.omnicuris.com/medshots/editorial_picks/ab-pmjay-guideline-violations-hospitals-de-empanelled_07-Aug-26_16-08); [HSTP summary of CAG shortfalls](https://www.hstp.org.in/wp-content/uploads/2025/05/15-SHORTFALLS-IN-AB-PM-JAY-IDENTIFIED-BY-CAG-PERFORMANCE-AUDIT-TECHNICAL-REVIEW.pdf).
- **Insurer–hospital relations are adversarial at times:** the GI Council pushed back on AHPI's suspension threat — [Outlook Money](https://www.outlookmoney.com/personal-finance/cashless-care-at-risk-gi-council-pushes-back-what-policyholders-should-know-if-services-stop).
- **Competitor compliance positioning:** "DPDPA-aligned, ISO 27001, AWS Mumbai" — [LeapHealth](https://theleaphealth.com/ai-agents/insurance-tpa).

### Inferences
- **Product guardrails:**
  1. Human-in-the-loop sign-off on every submission and every clinical statement; the agent drafts and the coordinator or doctor approves.
  2. Never fabricate or "improve" clinical facts; only assemble and cite from source documents. Present this as a fraud-safety feature to insurers.
  3. Audit trail per claim.
  4. India-region hosting; a DPA with the hospital; PHI minimisation in LLM calls (redaction, or self-hosted/India-region models).
  5. Portal automation through the hospital's own credentials on hospital-controlled machines (browser agent run by the desk user), preferring APIs and NHCX where available.
- **Liability:** contracts should disclaim clinical judgement. Coding or diagnosis suggestions should be labelled as suggestions.
- **Insurer/TPA pushback scenarios:** TPAs may block bot traffic or rate-limit. Mitigations are NHCX-first, a partnership posture ("cleaner first-time-right files reduce your adjudication cost"), and using the in-portal human session.
- **Regulatory tailwinds:** 1-hour/3-hour TATs, NHCX incentives and the "100% cashless" push all raise the premium on fast, complete first submissions. These are good pitch hooks, but the Jan 2026 circular needs verification first.

### Gaps
- No health-specific DPDP rules found (e.g., whether health data gets "sensitive" treatment beyond general rules). ABDM's Health Data Management Policy applies separately and was not reviewed.
- No public TPA portal ToS text reviewed on automation.
- No case law or precedent on vendor liability for claim-submission errors in India.
