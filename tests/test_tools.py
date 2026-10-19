import json
from pathlib import Path

from app.store import Case
from app.tools import execute_tool, inr

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def sample_case() -> Case:
    case = Case(id="test")
    for path in sorted(SAMPLES.glob("*.txt")):
        case.add_document(path.name, path.read_text(encoding="utf-8"))
    return case


def call(case: Case, name: str, **args):
    return execute_tool(case, name, json.dumps(args))


def test_inr_uses_indian_grouping():
    assert inr(188300) == "₹1,88,300"
    assert inr(500) == "₹500"
    assert inr(12345678) == "₹1,23,45,678"


def test_sample_documents_are_classified():
    types = {doc.filename: doc.doc_type for doc in sample_case().documents.values()}
    assert types == {
        "1_policy_wording.txt": "policy",
        "2_hospital_bill.txt": "hospital_bill",
        "3_discharge_summary.txt": "discharge_summary",
        "4_rejection_letter.txt": "rejection_letter",
    }


def test_search_finds_moratorium_clause_with_citation():
    output = call(sample_case(), "search_documents", query="moratorium non-disclosure sixty months", doc_type="policy")
    top = output.result["hits"][0]
    assert "5.1" in top["section"]
    assert "sixty continuous months" in top["text"]


def test_policy_tenure_clears_moratorium():
    output = call(sample_case(), "calculate_policy_tenure", first_inception_date="2019-04-01", event_date="2026-08-12")
    assert output.result["continuous_months"] == 88
    assert output.result["moratorium_complete"] is True
    assert output.result["specific_disease_waiting_complete"] is True


def test_room_rent_proportionate_deduction():
    output = call(
        sample_case(),
        "calculate_room_rent_deduction",
        eligible_rent_per_day=5000,
        actual_rent_per_day=7500,
        days=3,
        associated_expenses=[
            {"description": "Nursing", "amount": 4500},
            {"description": "Surgeon", "amount": 45000},
            {"description": "Anaesthetist", "amount": 12000},
            {"description": "OT", "amount": 30000},
            {"description": "Consultation", "amount": 6000},
        ],
    )
    assert output.result["room_rent"]["deduction"] == 7500
    assert output.result["total_deduction"] == 40000


def test_bill_assessment_totals_and_mismatch_warning():
    case = sample_case()
    output = call(
        case,
        "record_bill_assessment",
        items=[
            {"description": "Room", "billed_amount": 22500, "payable_amount": 15000, "status": "partially_payable", "reason": "cap"},
            {"description": "Kit", "billed_amount": 3850, "payable_amount": 0, "status": "not_payable", "reason": "Annexure I"},
        ],
        claimed_amount=188300,
    )
    assert output.ok and output.state_changed
    assert case.bill_assessment["payable_total"] == 15000
    assert case.bill_assessment["deduction_total"] == 11350
    assert "warning" in case.bill_assessment


def test_payable_above_billed_is_rejected():
    output = call(
        sample_case(),
        "record_bill_assessment",
        items=[{"description": "Room", "billed_amount": 100, "payable_amount": 200, "status": "payable", "reason": "x"}],
    )
    assert not output.ok
    assert "exceeds" in output.result["error"]


def test_checklist_marks_uploaded_documents_and_extras():
    case = sample_case()
    call(case, "check_required_documents", claim_type="reimbursement", extra_items=["Renewal receipts 2019-2026"])
    statuses = {item["item"]: item["status"] for item in case.checklist}
    assert statuses["Discharge summary"] == "uploaded"
    assert statuses["Claim form, filled and signed by the insured"] == "keep_ready"
    assert statuses["Renewal receipts 2019-2026"] == "to_obtain"
    assert "FIR or medico-legal certificate (MLC)" not in statuses


def test_bad_inputs_become_tool_errors_not_crashes():
    case = sample_case()
    assert not call(case, "read_document", doc_id="doc99").ok
    assert not call(case, "calculate_policy_tenure", first_inception_date="yesterday", event_date="2026-01-01").ok
    assert not call(case, "record_verdict", headline="missing outcome").ok
    assert not execute_tool(case, "no_such_tool", "{}").ok
    assert not execute_tool(case, "list_documents", "{not json").ok
