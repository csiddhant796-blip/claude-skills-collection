"""
SKILL 1: tcs_calculator
Computes TCS deduction for any LRS remittance using current rules.
Auto-detects whether the user is above/below threshold and which purpose category.

Usage:
    from tcs_calculator import calculate_tcs
    result = calculate_tcs(amount_inr=1500000, purpose="investment", fy="2025-26")

Returns:
    {
      "remittance_inr": 1500000,
      "tcs_threshold_inr": 1000000,
      "tcs_rate_pct": 20.0,
      "tcs_amount_inr": 100000,
      "net_remittance_inr": 1400000,
      "net_usd_at_84": 16666.67,
      "is_refundable": True,
      "refund_method": "Schedule TCS in ITR-2 or ITR-3",
      "warning": None
    }
"""
import json
import os
from datetime import date

KB_PATH = os.path.join(os.path.dirname(__file__), "regulatory_knowledge_base.json")

def _load_kb():
    with open(KB_PATH) as f:
        return json.load(f)

def calculate_tcs(amount_inr, purpose="investment", fy="2025-26", usd_inr=84.0):
    """
    Calculate TCS on LRS remittance.

    Args:
        amount_inr: remittance amount in INR
        purpose: one of 'investment', 'education_loan', 'education_self', 'medical', 'tour'
        fy: financial year, e.g. '2025-26' or '2026-27'
        usd_inr: current USD/INR rate

    Returns: dict with TCS calculation
    """
    kb = _load_kb()
    tcs = kb["tcs_rules"]
    threshold = tcs["threshold_inr"]
    rates = tcs["rates_by_purpose"]

    # Determine effective rate based on FY
    is_post_april_2026 = fy >= "2026-27"

    if purpose == "investment":
        rate_pct = 20.0  # unchanged
    elif purpose == "education_loan":
        rate_pct = 0.0
    elif purpose == "education_self" or purpose == "medical":
        rate_pct = 2.0 if is_post_april_2026 else 5.0
    elif purpose == "tour":
        rate_pct = 2.0 if is_post_april_2026 else 20.0  # simplified
    else:
        return {"error": f"Unknown purpose: {purpose}"}

    if amount_inr <= threshold and purpose != "tour":
        tcs_amount = 0
        applied_rate = 0
    else:
        applied_rate = rate_pct
        excess = amount_inr - threshold if purpose != "tour" else amount_inr
        tcs_amount = excess * (rate_pct / 100)

    net = amount_inr - tcs_amount

    warning = None
    if amount_inr > threshold:
        warning = (
            f"TCS of \u20b9{int(tcs_amount):,} will be deducted by your AD bank. "
            "This is REFUNDABLE — claim full credit in Schedule TCS when filing ITR."
        )

    if is_post_april_2026 and purpose == "investment":
        warning = (warning or "") + " Investment TCS rate unchanged at 20% for FY 2026-27."

    return {
        "remittance_inr": amount_inr,
        "tcs_threshold_inr": threshold,
        "tcs_rate_pct": applied_rate,
        "tcs_amount_inr": round(tcs_amount, 2),
        "net_remittance_inr": round(net, 2),
        "net_usd": round(net / usd_inr, 2),
        "is_refundable": tcs_amount > 0,
        "refund_method": "Schedule TCS in ITR-2 or ITR-3 (TCS is creditable, not a final tax)",
        "governing_section": tcs["governing_section"],
        "fy": fy,
        "warning": warning
    }


def calculate_family_tcs(per_person_inr, num_accounts=3, purpose="investment", fy="2025-26"):
    """Convenience wrapper for the 3-account family setup."""
    per_person = calculate_tcs(per_person_inr, purpose, fy)
    return {
        "per_person": per_person,
        "total_remittance_inr": per_person_inr * num_accounts,
        "total_tcs_inr": per_person["tcs_amount_inr"] * num_accounts,
        "total_net_inr": per_person["net_remittance_inr"] * num_accounts,
        "total_refundable_inr": per_person["tcs_amount_inr"] * num_accounts,
        "num_accounts": num_accounts
    }


if __name__ == "__main__":
    # Quick test
    print("─── Test 1: ₹7L (below threshold) ───")
    print(json.dumps(calculate_tcs(700000), indent=2, ensure_ascii=False))
    print("\n─── Test 2: ₹15L investment ───")
    print(json.dumps(calculate_tcs(1500000), indent=2, ensure_ascii=False))
    print("\n─── Test 3: Family ₹7L × 3 ───")
    print(json.dumps(calculate_family_tcs(700000), indent=2, ensure_ascii=False))
