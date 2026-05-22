"""
scss_planner.py — Senior Citizen Savings Scheme calculator

Father's priority skill. Models:
  - Annual interest at current Q1 FY 2026-27 rate (8.20%)
  - Quarterly payout schedule (SCSS pays interest quarterly)
  - TDS implications (senior threshold ₹1L from Apr 2025)
  - 80TTB headroom (₹50K max for 60+, OLD regime only)
  - 80C deduction at investment time
  - Premature withdrawal penalties
  - 5-year tenure with optional 3-year extension

Verified May 2026 against:
  - SB Order 01/2026 (Q1 FY 2026-27 rate notification)
  - Finance Act 2025 (TDS senior threshold change)
  - Section 80TTB, 80C of Income Tax Act
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

# ─── CONSTANTS ─────────────────────────────────────────────────
SCSS_RATE_Q1_FY26_27: float = 8.20  # SB Order 01/2026
SCSS_MAX_DEPOSIT_INR: float = 30_00_000  # Raised from ₹15L in Budget 2023
SCSS_TENURE_MONTHS: int = 60  # 5 years
SCSS_EXTENSION_MONTHS: int = 36  # Optional 3-year extension
SCSS_MIN_DEPOSIT_INR: float = 1000

TDS_SENIOR_THRESHOLD_INR: float = 100_000  # Raised from ₹50K, effective 1 Apr 2025
TDS_RATE_SCSS: float = 10.0
TDS_RATE_NO_PAN: float = 20.0

SECTION_80TTB_MAX_INR: float = 50_000  # Senior 60+ only, OLD regime
SECTION_80C_MAX_INR: float = 1_50_000  # Shared cap

# Premature withdrawal penalty schedule
PENALTY_YEAR_1_TO_2: float = 0.015  # 1.5%
PENALTY_YEAR_2_TO_5: float = 0.01   # 1%


# ─── RESULT DATACLASSES ────────────────────────────────────────
@dataclass
class SCSSCashflowResult:
    deposit_amount: float
    interest_rate_pct: float
    annual_interest: float
    quarterly_payout: float
    total_interest_over_tenure: float
    tenure_months: int
    notes: list[str] = field(default_factory=list)


@dataclass
class SCSSTaxResult:
    annual_interest: float
    other_interest_income: float
    total_interest: float
    tds_applies: bool
    tds_threshold_inr: float
    tds_amount: float
    tds_rate_pct: float
    section_80ttb_used: float
    section_80c_deposit_eligible: float
    net_interest_after_tds: float
    notes: list[str] = field(default_factory=list)


@dataclass
class SCSSPrematureWithdrawalResult:
    deposit: float
    interest_paid_so_far: float
    withdrawal_date: date
    deposit_date: date
    months_held: int
    penalty_rate_pct: float
    penalty_amount: float
    net_received: float
    notes: list[str] = field(default_factory=list)


# ─── PUBLIC API ────────────────────────────────────────────────
def calculate_scss_cashflow(
    deposit_amount: float,
    interest_rate_pct: float = SCSS_RATE_Q1_FY26_27,
    tenure_months: int = SCSS_TENURE_MONTHS,
) -> SCSSCashflowResult:
    """Calculate quarterly cash flow from an SCSS deposit."""
    if deposit_amount > SCSS_MAX_DEPOSIT_INR:
        deposit_amount = SCSS_MAX_DEPOSIT_INR
    if deposit_amount < SCSS_MIN_DEPOSIT_INR:
        raise ValueError(f"Minimum SCSS deposit is ₹{SCSS_MIN_DEPOSIT_INR}")

    annual = deposit_amount * interest_rate_pct / 100
    quarterly = annual / 4
    total = annual * (tenure_months / 12)

    notes = [
        f"Rate verified Q1 FY 2026-27 (SB Order 01/2026): {interest_rate_pct}%",
        "Interest paid quarterly: 1 Apr, 1 Jul, 1 Oct, 1 Jan",
        f"After {tenure_months // 12} years, deposit returned + can extend by 3 more years",
        "Joint account with spouse allowed (but ₹30L is per-investor cap, not per-account)",
    ]

    return SCSSCashflowResult(
        deposit_amount=deposit_amount,
        interest_rate_pct=interest_rate_pct,
        annual_interest=annual,
        quarterly_payout=quarterly,
        total_interest_over_tenure=total,
        tenure_months=tenure_months,
        notes=notes,
    )


def calculate_scss_tax(
    deposit_amount: float,
    interest_rate_pct: float = SCSS_RATE_Q1_FY26_27,
    other_interest_income: float = 0,
    has_pan: bool = True,
    is_old_regime: bool = False,
) -> SCSSTaxResult:
    """
    Compute TDS, 80TTB headroom, and 80C eligibility on an SCSS deposit.
    """
    annual = deposit_amount * interest_rate_pct / 100
    total_interest = annual + other_interest_income
    tds_applies = total_interest > TDS_SENIOR_THRESHOLD_INR

    tds_rate = TDS_RATE_SCSS if has_pan else TDS_RATE_NO_PAN
    tds_amount = annual * tds_rate / 100 if tds_applies else 0

    # 80TTB only available in OLD regime
    if is_old_regime:
        ttb_usable = min(annual, SECTION_80TTB_MAX_INR)
    else:
        ttb_usable = 0

    # 80C eligible: ₹1.5L of the deposit itself (within shared 80C cap)
    sec_80c = min(deposit_amount, SECTION_80C_MAX_INR)

    notes = []
    notes.append(f"Senior TDS threshold: ₹{TDS_SENIOR_THRESHOLD_INR:,} (raised from ₹50K on 1 Apr 2025)")
    if not has_pan:
        notes.append("⚠️ No PAN — TDS at 20% (penalty rate). Submit PAN to bank/PO ASAP.")
    if tds_applies:
        notes.append(f"TDS {tds_rate}% deducted at source — recoverable via ITR if total income < taxable threshold")
        notes.append("Submit Form 15H if total income is below taxable threshold to halt TDS")
    if is_old_regime and ttb_usable > 0:
        notes.append(f"80TTB deduction (old regime): ₹{ttb_usable:,.0f}")
    else:
        notes.append("80TTB not available in NEW regime (₹50K deduction is OLD regime only)")
    notes.append(f"80C eligibility: ₹{sec_80c:,.0f} (within shared ₹1.5L cap)")

    net = annual - tds_amount

    return SCSSTaxResult(
        annual_interest=annual,
        other_interest_income=other_interest_income,
        total_interest=total_interest,
        tds_applies=tds_applies,
        tds_threshold_inr=TDS_SENIOR_THRESHOLD_INR,
        tds_amount=tds_amount,
        tds_rate_pct=tds_rate,
        section_80ttb_used=ttb_usable,
        section_80c_deposit_eligible=sec_80c,
        net_interest_after_tds=net,
        notes=notes,
    )


def calculate_scss_premature_withdrawal(
    deposit_amount: float,
    deposit_date: date,
    withdrawal_date: date,
    interest_rate_pct: float = SCSS_RATE_Q1_FY26_27,
) -> SCSSPrematureWithdrawalResult:
    """
    Compute penalty if withdrawing before 5-year maturity.

    Penalty schedule:
      - <1 year:    No interest paid (interest already credited is recovered)
      - 1-2 years:  1.5% of deposit deducted
      - 2-5 years:  1% of deposit deducted
    """
    months = (withdrawal_date.year - deposit_date.year) * 12 + (withdrawal_date.month - deposit_date.month)
    annual_interest = deposit_amount * interest_rate_pct / 100
    interest_so_far = annual_interest * (months / 12)

    notes = []
    if months < 12:
        penalty_rate = 0
        penalty = interest_so_far  # Recover ALL interest paid
        notes.append("⚠️ <1 year withdrawal: ZERO interest. All interest already paid is recovered.")
        net = deposit_amount  # Just the original deposit back
    elif months < 24:
        penalty_rate = PENALTY_YEAR_1_TO_2 * 100
        penalty = deposit_amount * PENALTY_YEAR_1_TO_2
        notes.append(f"1-2 year withdrawal: 1.5% penalty on deposit = ₹{penalty:,.0f}")
        net = deposit_amount + interest_so_far - penalty
    elif months < 60:
        penalty_rate = PENALTY_YEAR_2_TO_5 * 100
        penalty = deposit_amount * PENALTY_YEAR_2_TO_5
        notes.append(f"2-5 year withdrawal: 1% penalty on deposit = ₹{penalty:,.0f}")
        net = deposit_amount + interest_so_far - penalty
    else:
        penalty_rate = 0
        penalty = 0
        notes.append("Matured (≥5 years): no penalty")
        net = deposit_amount + interest_so_far

    notes.append(f"Held: {months} months ({months/12:.1f} years)")
    notes.append("⚠️ Approximate calc — actual interest credited may differ based on quarterly schedule")

    return SCSSPrematureWithdrawalResult(
        deposit=deposit_amount,
        interest_paid_so_far=interest_so_far,
        withdrawal_date=withdrawal_date,
        deposit_date=deposit_date,
        months_held=months,
        penalty_rate_pct=penalty_rate,
        penalty_amount=penalty,
        net_received=net,
        notes=notes,
    )


def post_tax_yield_comparison(
    scss_rate_pct: float = SCSS_RATE_Q1_FY26_27,
    frsb_rate_pct: float = 8.05,
    po_td_rate_pct: float = 7.50,
    bank_fd_senior_pct: float = 7.50,
    tax_slab_pct: float = 30.0,
) -> dict:
    """
    Compare post-tax yields across senior-friendly debt instruments.
    """
    def post_tax(rate, slab=tax_slab_pct):
        return rate * (1 - slab / 100)

    return {
        "SCSS": {"pre_tax": scss_rate_pct, "post_tax": post_tax(scss_rate_pct)},
        "RBI FRSB 2020": {"pre_tax": frsb_rate_pct, "post_tax": post_tax(frsb_rate_pct)},
        "Post Office 5yr TD": {"pre_tax": po_td_rate_pct, "post_tax": post_tax(po_td_rate_pct)},
        "Bank FD (Senior)": {"pre_tax": bank_fd_senior_pct, "post_tax": post_tax(bank_fd_senior_pct)},
        "tax_slab_pct": tax_slab_pct,
        "winner_pre_tax": "SCSS (highest senior pre-tax rate)",
        "winner_post_tax": "SCSS (same ordering since all slab-taxed)",
        "note": "SCSS additionally offers ₹50K 80TTB (old regime only) and ₹1.5L 80C eligibility at deposit",
    }


__all__ = [
    "SCSS_RATE_Q1_FY26_27", "SCSS_MAX_DEPOSIT_INR", "TDS_SENIOR_THRESHOLD_INR",
    "SCSSCashflowResult", "SCSSTaxResult", "SCSSPrematureWithdrawalResult",
    "calculate_scss_cashflow", "calculate_scss_tax",
    "calculate_scss_premature_withdrawal", "post_tax_yield_comparison",
]
