"""Curated notes on IRDAI health-insurance rules the agent can cite. Keep these up to date before the demo."""

VERIFY_NOTE = (
    "Summarised from IRDAI regulations and circulars as understood in 2024–2026. "
    "Verify against the latest IRDAI circular before relying on it."
)

REGULATIONS = {
    "moratorium": {
        "title": "Moratorium period (60 months)",
        "source": "IRDAI Master Circular on Health Insurance Business, May 2024",
        "rule": (
            "After 60 continuous months of coverage (including portability and migration), no health policy or claim "
            "can be contested by the insurer on grounds of non-disclosure or misrepresentation, except on grounds of "
            "established fraud. The period was reduced from 8 years to 60 months in 2024. Policies remain subject to "
            "limits, sub-limits, co-payments and deductibles. Where the sum insured was enhanced, the 60 months for the "
            "enhanced portion run from the date of enhancement."
        ),
    },
    "waiting_periods": {
        "title": "Waiting periods",
        "source": "IRDAI Master Circular on Health Insurance Business, May 2024",
        "rule": (
            "Pre-existing disease waiting period can be at most 36 months (reduced from 48). Specified disease or "
            "procedure waiting periods can be at most 36 months. The initial waiting period is usually 30 days and does "
            "not apply to accidents. Waiting periods run on continuous coverage, so renewals without a break count."
        ),
    },
    "proportionate_deduction": {
        "title": "Room-rent capping and proportionate deduction",
        "source": "IRDAI Guidelines on Product Filing in Health Insurance (2020), carried into the 2024 Master Circular",
        "rule": (
            "When the insured stays in a room above the eligible room-rent limit, insurers may reduce 'associated medical "
            "expenses' in the same proportion. Proportionate deduction must not be applied to pharmacy, consumables, "
            "implants, medical devices or diagnostics, nor in hospitals that do not follow differential billing by room "
            "category, nor to ICU charges."
        ),
    },
    "claim_settlement_timelines": {
        "title": "Claim settlement timelines",
        "source": "IRDAI (Protection of Policyholders' Interests) Regulations and 2024 Master Circulars",
        "rule": (
            "Reimbursement claims must be settled or rejected within 30 days of receiving the last necessary document "
            "(45 days if an investigation is needed). Delay attracts interest at 2% above the bank rate. Cashless: "
            "pre-authorisation decision within 1 hour and final authorisation within 3 hours of the discharge request."
        ),
    },
    "rejection_communication": {
        "title": "How a rejection must be communicated",
        "source": "IRDAI (Protection of Policyholders' Interests) Regulations",
        "rule": (
            "A rejection (repudiation) must be communicated in writing, stating the specific reasons and the policy "
            "clause relied on, and must tell the insured how to escalate: the insurer's grievance officer, IRDAI's Bima "
            "Bharosa portal and the Insurance Ombudsman. Rejections should be reviewed by the insurer's claims review "
            "committee."
        ),
    },
    "grievance_escalation": {
        "title": "Grievance escalation path",
        "source": "IRDAI Master Circular on Protection of Policyholders' Interests, 2024",
        "rule": (
            "Step 1: write to the insurer's Grievance Redressal Officer (email or letter) and keep proof. The insurer "
            "should acknowledge promptly and resolve within 14 days. Step 2: if unresolved, register on IRDAI's Bima "
            "Bharosa portal (bimabharosa.irdai.gov.in). Step 3: approach the Insurance Ombudsman."
        ),
    },
    "insurance_ombudsman": {
        "title": "Insurance Ombudsman",
        "source": "Insurance Ombudsman Rules, 2017 (as amended)",
        "rule": (
            "Free of cost, no lawyer needed. You can complain if the insurer rejected your grievance, did not reply "
            "within one month of receiving it, or you are not satisfied with the reply. File within one year of the "
            "insurer's reply. Covers claims up to ₹50 lakh. File online at cioins.co.in or at the Ombudsman office "
            "with jurisdiction. The matter must not be pending before a court or consumer forum. The insurer must "
            "comply with an award within 30 days."
        ),
    },
    "non_payable_items": {
        "title": "Non-payable (non-medical) items",
        "source": "IRDAI Guidelines on Standardisation of Exclusions, list of non-medical items (2020)",
        "rule": (
            "IRDAI publishes a standard list of non-medical items that are not payable (List I), e.g. toiletries, "
            "admission kit, attendant charges and food, registration or documentation charges, baby food, beauty "
            "services. Other lists cover items that are subsumed into room, procedure or treatment charges and must not "
            "be deducted separately. The specific policy's annexure applies to that product."
        ),
    },
}
