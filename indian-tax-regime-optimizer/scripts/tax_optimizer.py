"""
tax_optimizer.py — Old vs New regime decision tool

Computes income tax under both Indian regimes for FY 2025-26 (AY 2026-27) and
recommends the optimal one. Handles age-based slabs (general / senior 60-79 / super-senior 80+).

Verified May 2026 against:
  - Finance (No.2) Act 2024 (new regime slabs and rebate)
  - Finance Act 2025 (TDS senior threshold; standard deduction confirmation)
  - Income Tax Act Sections 87A, 80C, 80CCD, 80D, 80TTB, 24(b)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ─── CONSTANTS — FY 2025-26 ────────────────────────────────────
# New regime slabs (Finance Act No.2 2024)
NEW_REGIME_SLABS = [
    (0,         4_00_000,  0.00),
    (4_00_000,  8_00_000,  0.05),
    (8_00_000,  12_00_000, 0.10),
    (12_00_000, 16_00_000, 0.15),
    (16_00_000, 20_00_000, 0.20),
    (20_00_000, 24_00_000, 0.25),
    (24_00_000, float("inf"), 0.30),
]
NEW_REGIME_REBATE_LIMIT_INR: float = 12_00_000
NEW_REGIME_REBATE_AMOUNT_INR: float = 60_000  # Effectively zero tax up to ₹12L

# Old regime slabs (FY 2025-26)
OLD_REGIME_SLABS_GENERAL = [
    (0,        2_50_000,  0.00),
    (2_50_000, 5_00_000,  0.05),
    (5_00_000, 10_00_000, 0.20),
    (10_00_000, float("inf"), 0.30),
]
OLD_REGIME_SLABS_SENIOR = [   # Age 60-79
    (0,        3_00_000,  0.00),
    (3_00_000, 5_00_000,  0.05),
    (5_00_000, 10_00_000, 0.20),
    (10_00_000, float("inf"), 0.30),
]
OLD_REGIME_SLABS_SUPER_SENIOR = [  # Age 80+
    (0,        5_00_000,  0.00),
    (5_00_000, 10_00_000, 0.20),
    (10_00_000, float("inf"), 0.30),
]
OLD_REGIME_REBATE_LIMIT_INR: float = 5_00_000
OLD_REGIME_REBATE_AMOUNT_INR: float = 12_500

# Cess (Health & Education) — applies to both regimes
CESS_RATE: float = 0.04

# Standard deduction (both regimes)
STANDARD_DEDUCTION_INR: float = 75_000  # Raised from ₹50K in Budget 2024

# Deduction caps (OLD regime)
CAP_80C: float = 1_50_000
CAP_80CCD_1B: float = 50_000  # Over & above 80C
CAP_80D_SELF_NON_SENIOR: float = 25_000
CAP_80D_SELF_SENIOR: float = 50_000
CAP_80D_PARENTS_NON_SENIOR: float = 25_000
CAP_80D_PARENTS_SENIOR: float = 50_000
CAP_80TTB: float = 50_000  # 60+ only
CAP_80TTA: float = 10_000  # Non-senior; savings account interest only


# ─── ENUMS ─────────────────────────────────────────────────────
class AgeBracket(str, Enum):
    GENERAL = "general"          # < 60
    SENIOR = "senior"             # 60-79
    SUPER_SENIOR = "super_senior" # 80+


class Regime(str, Enum):
    OLD = "old"
    NEW = "new"


# ─── DATACLASSES ───────────────────────────────────────────────
@dataclass
class DeductionBreakdown:
    """OLD-regime deductions — components and caps."""
    sec_80c: float = 0
    sec_80ccd_1b: float = 0
    sec_80d_self: float = 0
    sec_80d_parents: float = 0
    sec_80ttb: float = 0  # 60+ only
    sec_80tta: float = 0  # <60 only
    home_loan_interest_sop: float = 0  # Sec 24(b), capped ₹2L self-occupied
    home_loan_interest_let_out: float = 0  # Uncapped
    other: float = 0  # Catch-all for 80E, 80G, etc.


@dataclass
class RegimeTaxResult:
    regime: Regime
    gross_income: float
    standard_deduction: float
    total_deductions_applied: float
    deductions_capped: dict[str, float]  # Component → applied amount after caps
    deduction_overages: dict[str, float]  # Component → amount over cap (informational)
    taxable_income: float
    tax_before_rebate: float
    rebate_applied: float
    tax_after_rebate: float
    cess: float
    total_tax: float
    age_bracket: AgeBracket
    notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class RegimeComparisonResult:
    old_result: RegimeTaxResult
    new_result: RegimeTaxResult
    recommended_regime: Regime
    tax_saved: float
    rationale: str


# ─── HELPERS ───────────────────────────────────────────────────
def get_age_bracket(age: int) -> AgeBracket:
    if age < 60:
        return AgeBracket.GENERAL
    if age < 80:
        return AgeBracket.SENIOR
    return AgeBracket.SUPER_SENIOR


def _compute_slab_tax(taxable_income: float, slabs: list[tuple[float, float, float]]) -> float:
    """Generic slab-based tax calculation."""
    tax = 0
    for low, high, rate in slabs:
        if taxable_income <= low:
            break
        in_slab = min(taxable_income, high) - low
        tax += in_slab * rate
    return tax


def _apply_old_regime_caps(deductions: DeductionBreakdown, age_bracket: AgeBracket) -> tuple[dict, dict]:
    """Apply statutory caps to old-regime deductions. Returns (applied, overages)."""
    applied = {}
    overages = {}

    # 80C — straight cap
    applied["80C"] = min(deductions.sec_80c, CAP_80C)
    if deductions.sec_80c > CAP_80C:
        overages["80C"] = deductions.sec_80c - CAP_80C

    # 80CCD(1B) — separate from 80C
    applied["80CCD(1B)"] = min(deductions.sec_80ccd_1b, CAP_80CCD_1B)
    if deductions.sec_80ccd_1b > CAP_80CCD_1B:
        overages["80CCD(1B)"] = deductions.sec_80ccd_1b - CAP_80CCD_1B

    # 80D — age-dependent
    if age_bracket == AgeBracket.GENERAL:
        applied["80D_self"] = min(deductions.sec_80d_self, CAP_80D_SELF_NON_SENIOR)
    else:
        applied["80D_self"] = min(deductions.sec_80d_self, CAP_80D_SELF_SENIOR)
    applied["80D_parents"] = min(deductions.sec_80d_parents, CAP_80D_PARENTS_SENIOR)

    # 80TTB / 80TTA — age-dependent, mutually exclusive
    if age_bracket in (AgeBracket.SENIOR, AgeBracket.SUPER_SENIOR):
        applied["80TTB"] = min(deductions.sec_80ttb, CAP_80TTB)
        applied["80TTA"] = 0
        if deductions.sec_80tta > 0:
            overages["80TTA_not_eligible"] = deductions.sec_80tta
    else:
        applied["80TTB"] = 0
        applied["80TTA"] = min(deductions.sec_80tta, CAP_80TTA)
        if deductions.sec_80ttb > 0:
            overages["80TTB_not_eligible"] = deductions.sec_80ttb

    # Home loan — let-out has no cap; SOP capped ₹2L
    applied["24b_sop"] = min(deductions.home_loan_interest_sop, 200_000)
    if deductions.home_loan_interest_sop > 200_000:
        overages["24b_sop"] = deductions.home_loan_interest_sop - 200_000
    applied["24b_let_out"] = deductions.home_loan_interest_let_out

    applied["other"] = deductions.other

    return applied, overages


# ─── PUBLIC API ────────────────────────────────────────────────
def calculate_old_regime_tax(
    gross_income: float,
    deductions: DeductionBreakdown,
    age: int,
) -> RegimeTaxResult:
    """Compute tax under OLD regime."""
    age_bracket = get_age_bracket(age)
    applied, overages = _apply_old_regime_caps(deductions, age_bracket)

    total_ded = STANDARD_DEDUCTION_INR + sum(applied.values())
    taxable = max(0, gross_income - total_ded)

    # Pick correct slabs
    if age_bracket == AgeBracket.GENERAL:
        slabs = OLD_REGIME_SLABS_GENERAL
    elif age_bracket == AgeBracket.SENIOR:
        slabs = OLD_REGIME_SLABS_SENIOR
    else:
        slabs = OLD_REGIME_SLABS_SUPER_SENIOR

    tax_pre_rebate = _compute_slab_tax(taxable, slabs)

    # Section 87A rebate (old regime): if taxable ≤ ₹5L, rebate ₹12,500
    rebate = min(OLD_REGIME_REBATE_AMOUNT_INR, tax_pre_rebate) if taxable <= OLD_REGIME_REBATE_LIMIT_INR else 0
    tax_post_rebate = max(0, tax_pre_rebate - rebate)

    cess = tax_post_rebate * CESS_RATE
    total = tax_post_rebate + cess

    notes = [f"Age bracket: {age_bracket.value}"]
    if overages:
        notes.append(f"Deductions exceeded caps: {overages}")
    if age_bracket == AgeBracket.SENIOR:
        notes.append("Senior slabs: 0-3L=0%, 3-5L=5%, 5-10L=20%, 10L+=30%")

    return RegimeTaxResult(
        regime=Regime.OLD,
        gross_income=gross_income,
        standard_deduction=STANDARD_DEDUCTION_INR,
        total_deductions_applied=total_ded,
        deductions_capped=applied,
        deduction_overages=overages,
        taxable_income=taxable,
        tax_before_rebate=tax_pre_rebate,
        rebate_applied=rebate,
        tax_after_rebate=tax_post_rebate,
        cess=cess,
        total_tax=round(total),
        age_bracket=age_bracket,
        notes=notes,
    )


def calculate_new_regime_tax(
    gross_income: float,
    age: int,
    employer_nps_contribution: float = 0,  # 80CCD(2) — available in new regime
) -> RegimeTaxResult:
    """Compute tax under NEW regime."""
    age_bracket = get_age_bracket(age)

    # New regime deductions: only standard deduction + 80CCD(2)
    total_ded = STANDARD_DEDUCTION_INR + employer_nps_contribution
    taxable = max(0, gross_income - total_ded)

    tax_pre_rebate = _compute_slab_tax(taxable, NEW_REGIME_SLABS)

    # Section 87A rebate (new regime): if taxable ≤ ₹12L, full tax rebated (capped ₹60K)
    rebate = min(NEW_REGIME_REBATE_AMOUNT_INR, tax_pre_rebate) if taxable <= NEW_REGIME_REBATE_LIMIT_INR else 0
    tax_post_rebate = max(0, tax_pre_rebate - rebate)

    cess = tax_post_rebate * CESS_RATE
    total = tax_post_rebate + cess

    notes = [
        f"Age bracket: {age_bracket.value} (new regime uses SAME slabs for all ages)",
        f"₹60K rebate covers ALL tax up to ₹12L taxable income",
        "Only std deduction ₹75K + employer 80CCD(2) allowed; no other deductions",
    ]

    return RegimeTaxResult(
        regime=Regime.NEW,
        gross_income=gross_income,
        standard_deduction=STANDARD_DEDUCTION_INR,
        total_deductions_applied=total_ded,
        deductions_capped={"std_deduction": STANDARD_DEDUCTION_INR, "80CCD(2)_employer": employer_nps_contribution},
        deduction_overages={},
        taxable_income=taxable,
        tax_before_rebate=tax_pre_rebate,
        rebate_applied=rebate,
        tax_after_rebate=tax_post_rebate,
        cess=cess,
        total_tax=round(total),
        age_bracket=age_bracket,
        notes=notes,
    )


def compare_regimes(
    gross_income: float,
    deductions: DeductionBreakdown,
    age: int,
    employer_nps_contribution: float = 0,
) -> RegimeComparisonResult:
    """Compute tax both ways and recommend the winning regime."""
    old = calculate_old_regime_tax(gross_income, deductions, age)
    new = calculate_new_regime_tax(gross_income, age, employer_nps_contribution)

    if new.total_tax < old.total_tax:
        recommended = Regime.NEW
        saved = old.total_tax - new.total_tax
        rationale = (
            f"NEW regime saves ₹{saved:,.0f}/year. "
            f"Old regime allowed ₹{old.total_deductions_applied:,.0f} deductions but new regime's "
            f"₹{NEW_REGIME_REBATE_AMOUNT_INR:,} rebate + lower slabs win at this income level."
        )
    elif old.total_tax < new.total_tax:
        recommended = Regime.OLD
        saved = new.total_tax - old.total_tax
        rationale = (
            f"OLD regime saves ₹{saved:,.0f}/year. "
            f"Total deductions of ₹{old.total_deductions_applied:,.0f} (incl. 80C/D/CCD/24b) make old regime more efficient at this income."
        )
    else:
        recommended = Regime.NEW
        saved = 0
        rationale = "Both regimes give same tax (₹0). New regime preferred for simplicity."

    return RegimeComparisonResult(
        old_result=old,
        new_result=new,
        recommended_regime=recommended,
        tax_saved=saved,
        rationale=rationale,
    )


__all__ = [
    "AgeBracket", "Regime", "DeductionBreakdown",
    "RegimeTaxResult", "RegimeComparisonResult",
    "calculate_old_regime_tax", "calculate_new_regime_tax", "compare_regimes",
    "get_age_bracket",
    "STANDARD_DEDUCTION_INR", "NEW_REGIME_REBATE_LIMIT_INR",
]
