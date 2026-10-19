"""Tools the agent can call.

Each handler returns what the model sees plus a one-line summary for the activity feed. Anything involving
dates or money is computed here, never by the model.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Callable

from .documents import DOC_TYPES
from .documents import search_documents as search_chunks
from .regulations import REGULATIONS, VERIFY_NOTE
from .store import Case

MAX_READ_CHARS = 12_000
PLAN_STATUSES = ("pending", "in_progress", "done")
BILL_STATUSES = ("payable", "partially_payable", "not_payable", "needs_review")
DRAFT_KINDS = ("claim_cover_letter", "grievance_letter", "ombudsman_complaint", "email", "other")
OUTCOMES = (
    "claim_likely_payable",
    "partially_payable",
    "rejection_contestable",
    "rejection_likely_valid",
    "needs_more_information",
)
CONFIDENCE_LEVELS = ("low", "medium", "high")

# (what to submit, uploaded doc type that satisfies it, when it applies)
REQUIRED_DOCUMENTS = (
    ("Claim form, filled and signed by the insured", None, "all"),
    ("Discharge summary", "discharge_summary", "all"),
    ("Final hospital bill with itemised break-up", "hospital_bill", "all"),
    ("Payment receipts for the hospital bill", None, "reimbursement"),
    ("Pharmacy bills with the doctor's prescriptions", None, "reimbursement"),
    ("Investigation and lab reports", None, "reimbursement"),
    ("Policy copy or health card", "policy", "all"),
    ("Photo ID and KYC of the proposer (Aadhaar / PAN)", None, "all"),
    ("Bank details with a cancelled cheque (for NEFT)", None, "reimbursement"),
    ("FIR or medico-legal certificate (MLC)", None, "accident"),
)


@dataclass
class ToolOutput:
    result: Any
    summary: str
    ok: bool = True
    state_changed: bool = False


class ToolError(ValueError):
    """A mistake the model can fix by calling the tool differently."""


def inr(amount: float) -> str:
    """Indian digit grouping: 188300 -> ₹1,88,300."""
    rupees = int(round(amount))
    digits = str(abs(rupees))
    last_three, rest = digits[-3:], digits[:-3]
    groups = []
    while len(rest) > 2:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.insert(0, rest)
    return f"{'-' if rupees < 0 else ''}₹{','.join([*groups, last_three])}"


def _parse_date(value: Any) -> date:
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            continue
    raise ToolError(f"Could not read the date {value!r}. Use YYYY-MM-DD.")


def _amount(value: Any, name: str) -> float:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ToolError(f"{name} must be a number, got {value!r}") from None
    if amount < 0:
        raise ToolError(f"{name} cannot be negative")
    return amount


def _choice(value: Any, allowed: tuple[str, ...], name: str) -> str:
    if value not in allowed:
        raise ToolError(f"{name} must be one of: {', '.join(allowed)}")
    return value


# --- handlers ---------------------------------------------------------------------------------------


def update_plan(case: Case, args: dict[str, Any]) -> ToolOutput:
    steps = [
        {"title": str(step["title"]).strip(), "status": _choice(step.get("status", "pending"), PLAN_STATUSES, "status")}
        for step in args["steps"]
    ]
    if not steps:
        raise ToolError("steps is empty")
    case.plan = steps
    done = sum(step["status"] == "done" for step in steps)
    return ToolOutput({"saved": True}, f"Plan: {done}/{len(steps)} steps done", state_changed=True)


def list_documents(case: Case, args: dict[str, Any]) -> ToolOutput:
    docs = [
        {"doc_id": doc.id, "filename": doc.filename, "doc_type": doc.doc_type, "characters": len(doc.text)}
        for doc in case.documents.values()
    ]
    return ToolOutput({"documents": docs}, f"{len(docs)} documents on file")


def read_document(case: Case, args: dict[str, Any]) -> ToolOutput:
    doc = case.documents.get(args["doc_id"])
    if doc is None:
        raise ToolError(f"No document with id {args['doc_id']!r}. Call list_documents to see valid ids.")
    offset = max(int(args.get("offset") or 0), 0)
    text = doc.text[offset : offset + MAX_READ_CHARS]
    result: dict[str, Any] = {"doc_id": doc.id, "filename": doc.filename, "doc_type": doc.doc_type, "text": text}
    end = offset + len(text)
    if end < len(doc.text):
        result["next_offset"] = end
        result["note"] = "The document continues. Call read_document again with next_offset."
    partial = offset > 0 or "next_offset" in result
    return ToolOutput(result, f"Read {doc.filename}{' (part)' if partial else ''}")


def search_documents(case: Case, args: dict[str, Any]) -> ToolOutput:
    query = str(args["query"]).strip()
    if not query:
        raise ToolError("query is empty")
    doc_type = args.get("doc_type") or None
    if doc_type is not None:
        _choice(doc_type, DOC_TYPES, "doc_type")
    hits = search_chunks(list(case.documents.values()), query, doc_type=doc_type, top_k=int(args.get("top_k") or 5))
    result: dict[str, Any] = {"hits": hits}
    if not hits:
        result["note"] = "No matches. Try other words or read the document directly."
    return ToolOutput(result, f"“{query}” → {len(hits)} passages")


def lookup_regulation(case: Case, args: dict[str, Any]) -> ToolOutput:
    topic = _choice(args["topic"], tuple(REGULATIONS), "topic")
    entry = REGULATIONS[topic]
    return ToolOutput({**entry, "verify": VERIFY_NOTE}, f"IRDAI rule: {entry['title']}")


def calculate_policy_tenure(case: Case, args: dict[str, Any]) -> ToolOutput:
    inception = _parse_date(args["first_inception_date"])
    event = _parse_date(args["event_date"])
    if event < inception:
        raise ToolError("event_date is before first_inception_date")
    months = (event.year - inception.year) * 12 + (event.month - inception.month) - int(event.day < inception.day)
    days = (event - inception).days
    ped_months = int(args.get("pre_existing_waiting_months") or 36)
    specific_months = int(args.get("specific_disease_waiting_months") or 24)
    moratorium_months = int(args.get("moratorium_months") or 60)
    continuous = bool(args.get("continuous_coverage", True))

    result: dict[str, Any] = {
        "continuous_months": months,
        "tenure": f"{months // 12} years {months % 12} months",
        "days": days,
        "initial_30_day_waiting_complete": days >= 30,
        "specific_disease_waiting_complete": months >= specific_months,
        "pre_existing_disease_waiting_complete": months >= ped_months,
        "moratorium_complete": continuous and months >= moratorium_months,
        "periods_used_months": {
            "pre_existing": ped_months,
            "specific_disease": specific_months,
            "moratorium": moratorium_months,
        },
    }
    if not continuous:
        result["note"] = "Coverage had a break, so waiting periods and the moratorium may restart. Check renewal history."
    moratorium = "complete" if result["moratorium_complete"] else "not complete"
    return ToolOutput(result, f"{result['tenure']} of cover; moratorium {moratorium}")


def calculate_room_rent_deduction(case: Case, args: dict[str, Any]) -> ToolOutput:
    eligible = _amount(args["eligible_rent_per_day"], "eligible_rent_per_day")
    actual = _amount(args["actual_rent_per_day"], "actual_rent_per_day")
    days = _amount(args["days"], "days")
    if eligible == 0 or actual == 0:
        raise ToolError("room rents must be greater than zero")

    ratio = min(eligible / actual, 1.0)
    room_billed = round(actual * days)
    room_payable = round(min(actual, eligible) * days)
    items = []
    for item in args.get("associated_expenses") or []:
        billed = round(_amount(item["amount"], "amount"))
        payable = round(billed * ratio)
        items.append({"description": item["description"], "billed": billed, "payable": payable, "deduction": billed - payable})
    total_deduction = (room_billed - room_payable) + sum(item["deduction"] for item in items)

    result = {
        "payable_ratio": round(ratio, 4),
        "payable_percent": f"{ratio:.1%}",
        "room_rent": {"billed": room_billed, "payable": room_payable, "deduction": room_billed - room_payable},
        "associated_expenses": items,
        "total_deduction": total_deduction,
        "reminder": (
            "Do not apply this ratio to pharmacy, consumables, implants, medical devices, diagnostics or ICU charges, "
            "or where the hospital does not bill differently by room category."
        ),
    }
    if ratio < 1:
        summary = f"Room {inr(actual)}/day vs limit {inr(eligible)} → {ratio:.1%} payable, {inr(total_deduction)} deducted"
    else:
        summary = "Room rent within limit, no proportionate deduction"
    return ToolOutput(result, summary)


def record_bill_assessment(case: Case, args: dict[str, Any]) -> ToolOutput:
    items = []
    for raw in args["items"]:
        billed = _amount(raw["billed_amount"], "billed_amount")
        payable = _amount(raw["payable_amount"], "payable_amount")
        if payable > billed:
            raise ToolError(f"payable_amount exceeds billed_amount for {raw['description']!r}")
        items.append(
            {
                "description": str(raw["description"]),
                "billed": round(billed),
                "payable": round(payable),
                "status": _choice(raw.get("status", "payable"), BILL_STATUSES, "status"),
                "reason": str(raw.get("reason", "")),
                "clause_ref": str(raw.get("clause_ref", "")),
            }
        )
    if not items:
        raise ToolError("items is empty. Include every line of the bill.")

    billed_total = sum(item["billed"] for item in items)
    payable_total = sum(item["payable"] for item in items)
    assessment: dict[str, Any] = {
        "items": items,
        "billed_total": billed_total,
        "payable_total": payable_total,
        "deduction_total": billed_total - payable_total,
    }
    if args.get("claimed_amount") is not None:
        claimed = round(_amount(args["claimed_amount"], "claimed_amount"))
        assessment["claimed_amount"] = claimed
        if abs(claimed - billed_total) > 1:
            assessment["warning"] = (
                f"Items add up to {inr(billed_total)} but the claim is {inr(claimed)}. Check for missing or duplicated lines."
            )
    case.bill_assessment = assessment

    totals = {key: value for key, value in assessment.items() if key != "items"}
    summary = f"{len(items)} bill items: {inr(payable_total)} of {inr(billed_total)} payable"
    return ToolOutput(totals, summary, state_changed=True)


def check_required_documents(case: Case, args: dict[str, Any]) -> ToolOutput:
    claim_type = _choice(args.get("claim_type", "reimbursement"), ("reimbursement", "cashless"), "claim_type")
    accident = bool(args.get("accident", False))
    uploaded = {doc.doc_type for doc in case.documents.values()}

    checklist = []
    for label, doc_type, applies_to in REQUIRED_DOCUMENTS:
        if (applies_to == "reimbursement" and claim_type != "reimbursement") or (applies_to == "accident" and not accident):
            continue
        checklist.append({"item": label, "status": "uploaded" if doc_type in uploaded else "keep_ready"})
    if "rejection_letter" in uploaded:
        checklist.append({"item": "Insurer's rejection letter", "status": "uploaded"})
    for extra in args.get("extra_items") or []:
        checklist.append({"item": str(extra), "status": "to_obtain"})
    case.checklist = checklist

    counts = {status: sum(item["status"] == status for item in checklist) for status in ("uploaded", "keep_ready", "to_obtain")}
    summary = f"{len(checklist)} documents: {counts['uploaded']} uploaded, {counts['to_obtain']} to obtain"
    return ToolOutput({"checklist": checklist}, summary, state_changed=True)


def save_draft(case: Case, args: dict[str, Any]) -> ToolOutput:
    kind = _choice(args.get("kind", "other"), DRAFT_KINDS, "kind")
    title = str(args["title"]).strip()
    body = str(args["body"]).strip()
    if len(body) < 50:
        raise ToolError("body is too short. Write the complete document.")
    draft_id = kind if kind != "other" else f"other-{title.lower()}"
    case.drafts[draft_id] = {
        "id": draft_id,
        "kind": kind,
        "title": title,
        "recipient": str(args.get("recipient", "")),
        "body": body,
    }
    result = {"saved": True, "draft_id": draft_id, "note": "Shown to the user for review. Nothing has been sent."}
    return ToolOutput(result, f"Drafted: {title}", state_changed=True)


def record_verdict(case: Case, args: dict[str, Any]) -> ToolOutput:
    verdict: dict[str, Any] = {
        "outcome": _choice(args["outcome"], OUTCOMES, "outcome"),
        "headline": str(args["headline"]),
        "confidence": _choice(args.get("confidence", "medium"), CONFIDENCE_LEVELS, "confidence"),
        "key_findings": [
            {
                "finding": str(item["finding"]),
                "clause_ref": str(item.get("clause_ref", "")),
                "impact": str(item.get("impact", "")),
            }
            for item in args.get("key_findings") or []
        ],
        "next_steps": [
            {"action": str(item["action"]), "deadline": str(item.get("deadline", "")), "who": str(item.get("who", ""))}
            for item in args.get("next_steps") or []
        ],
    }
    for key in ("claimed_amount", "estimated_payable_amount"):
        if args.get(key) is not None:
            verdict[key] = round(_amount(args[key], key))
    case.verdict = verdict
    return ToolOutput({"saved": True}, f"Verdict: {verdict['headline']}", state_changed=True)


# --- schemas ----------------------------------------------------------------------------------------


def _schema(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {"type": "object", "properties": properties, "required": required},
        },
    }


_STRING = {"type": "string"}
_NUMBER = {"type": "number"}

TOOLS: dict[str, tuple[dict[str, Any], Callable[[Case, dict[str, Any]], ToolOutput]]] = {
    "update_plan": (
        _schema(
            "update_plan",
            "Create or update your step-by-step plan for this case. The user sees it as a live checklist. "
            "Send the full list every time.",
            {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"title": _STRING, "status": {"type": "string", "enum": list(PLAN_STATUSES)}},
                        "required": ["title", "status"],
                    },
                }
            },
            ["steps"],
        ),
        update_plan,
    ),
    "list_documents": (
        _schema("list_documents", "List the documents the user uploaded, with their ids and types.", {}, []),
        list_documents,
    ),
    "read_document": (
        _schema(
            "read_document",
            f"Read the full text of one document ({MAX_READ_CHARS} characters at a time; use offset to continue).",
            {"doc_id": _STRING, "offset": {"type": "integer", "description": "Character offset to start from."}},
            ["doc_id"],
        ),
        read_document,
    ),
    "search_documents": (
        _schema(
            "search_documents",
            "Keyword search across the uploaded documents. Returns matching clauses with section and clause numbers "
            "to cite. Use specific words, e.g. 'moratorium non-disclosure sixty months'.",
            {
                "query": _STRING,
                "doc_type": {"type": "string", "enum": list(DOC_TYPES), "description": "Only search this type."},
                "top_k": {"type": "integer", "description": "Number of passages, 1-10 (default 5)."},
            },
            ["query"],
        ),
        search_documents,
    ),
    "lookup_regulation": (
        _schema(
            "lookup_regulation",
            "Look up an IRDAI rule that protects policyholders (moratorium, waiting periods, room-rent deduction, "
            "settlement timelines, rejection letters, grievance escalation, Ombudsman, non-payable items).",
            {"topic": {"type": "string", "enum": list(REGULATIONS)}},
            ["topic"],
        ),
        lookup_regulation,
    ),
    "calculate_policy_tenure": (
        _schema(
            "calculate_policy_tenure",
            "Compute continuous coverage from the FIRST policy inception date to an event (usually the admission "
            "date), and check initial, specific-disease and pre-existing-disease waiting periods and the moratorium.",
            {
                "first_inception_date": {"type": "string", "description": "YYYY-MM-DD"},
                "event_date": {"type": "string", "description": "YYYY-MM-DD, usually the date of admission"},
                "continuous_coverage": {"type": "boolean", "description": "False if the policy ever lapsed."},
                "pre_existing_waiting_months": {"type": "integer", "description": "From the policy (default 36)."},
                "specific_disease_waiting_months": {"type": "integer", "description": "From the policy (default 24)."},
                "moratorium_months": {"type": "integer", "description": "From the policy (default 60)."},
            },
            ["first_inception_date", "event_date"],
        ),
        calculate_policy_tenure,
    ),
    "calculate_room_rent_deduction": (
        _schema(
            "calculate_room_rent_deduction",
            "Compute the proportionate deduction when the room rent exceeds the policy limit. Pass ONLY associated "
            "medical expenses (e.g. nursing, surgeon, anaesthetist, OT, consultation), never pharmacy, consumables, "
            "implants or diagnostics.",
            {
                "eligible_rent_per_day": _NUMBER,
                "actual_rent_per_day": _NUMBER,
                "days": _NUMBER,
                "associated_expenses": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"description": _STRING, "amount": _NUMBER},
                        "required": ["description", "amount"],
                    },
                },
            },
            ["eligible_rent_per_day", "actual_rent_per_day", "days"],
        ),
        calculate_room_rent_deduction,
    ),
    "record_bill_assessment": (
        _schema(
            "record_bill_assessment",
            "Record your line-by-line verdict on the hospital bill. Include EVERY bill line. The tool adds up the totals "
            "and shows the table to the user.",
            {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": _STRING,
                            "billed_amount": _NUMBER,
                            "payable_amount": _NUMBER,
                            "status": {"type": "string", "enum": list(BILL_STATUSES)},
                            "reason": {"type": "string", "description": "Short plain-language reason."},
                            "clause_ref": {"type": "string", "description": "e.g. 'Policy §2.3'"},
                        },
                        "required": ["description", "billed_amount", "payable_amount", "status", "reason"],
                    },
                },
                "claimed_amount": {"type": "number", "description": "Total amount claimed, to cross-check the lines."},
            },
            ["items"],
        ),
        record_bill_assessment,
    ),
    "check_required_documents": (
        _schema(
            "check_required_documents",
            "Build the checklist of documents to submit, marking which are already uploaded. Add case-specific extras "
            "(e.g. renewal proofs, a treating doctor's certificate) in extra_items.",
            {
                "claim_type": {"type": "string", "enum": ["reimbursement", "cashless"]},
                "accident": {"type": "boolean"},
                "extra_items": {"type": "array", "items": _STRING},
            },
            ["claim_type"],
        ),
        check_required_documents,
    ),
    "save_draft": (
        _schema(
            "save_draft",
            "Save a complete, ready-to-send document for the user to review. Saving the same kind again replaces the "
            "earlier version. Nothing is sent automatically.",
            {
                "kind": {"type": "string", "enum": list(DRAFT_KINDS)},
                "title": _STRING,
                "recipient": {"type": "string", "description": "Email address or addressee, if known."},
                "body": {"type": "string", "description": "The full text of the document."},
            },
            ["kind", "title", "body"],
        ),
        save_draft,
    ),
    "record_verdict": (
        _schema(
            "record_verdict",
            "Record your overall conclusion for the case. The user sees it as the headline result.",
            {
                "outcome": {"type": "string", "enum": list(OUTCOMES)},
                "headline": {"type": "string", "description": "One sentence in plain language."},
                "claimed_amount": _NUMBER,
                "estimated_payable_amount": _NUMBER,
                "confidence": {"type": "string", "enum": list(CONFIDENCE_LEVELS)},
                "key_findings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"finding": _STRING, "clause_ref": _STRING, "impact": _STRING},
                        "required": ["finding"],
                    },
                },
                "next_steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"action": _STRING, "deadline": _STRING, "who": _STRING},
                        "required": ["action"],
                    },
                },
            },
            ["outcome", "headline", "confidence", "key_findings", "next_steps"],
        ),
        record_verdict,
    ),
}

TOOL_SCHEMAS = [schema for schema, _ in TOOLS.values()]


def execute_tool(case: Case, name: str, raw_arguments: str) -> ToolOutput:
    try:
        args = json.loads(raw_arguments or "{}")
    except json.JSONDecodeError:
        return ToolOutput({"error": "Arguments were not valid JSON."}, "Invalid arguments", ok=False)
    if not isinstance(args, dict):
        return ToolOutput({"error": "Arguments must be a JSON object."}, "Invalid arguments", ok=False)
    if name not in TOOLS:
        return ToolOutput({"error": f"Unknown tool {name!r}."}, f"Unknown tool {name}", ok=False)
    _, handler = TOOLS[name]
    try:
        return handler(case, args)
    except ToolError as exc:
        return ToolOutput({"error": str(exc)}, f"Error: {exc}", ok=False)
    except (KeyError, TypeError, ValueError) as exc:
        message = f"Missing or invalid argument: {exc}"
        return ToolOutput({"error": message}, message, ok=False)
