"""
indian_mf_calculator.py — Indian Mutual Fund tax & lock-in calculator

Covers:
  - Equity MF capital gains (12.5% LTCG above ₹1.25L, post Budget 2024)
  - Debt MF Section 50AA penalty (slab rate on ALL gains, post April 2023)
  - Grandfathered debt MF units (pre-Apr 2023, indexation still available)
  - ELSS 3-year lock-in tracking (PER SIP installment, not just initial)
  - Hybrid fund classification (equity-oriented if >65% equity)
  - Gold MF FoF (avoid — same as debt MF post Apr 2023)

Verified May 2026 against:
  - Finance (No.2) Act 2024 (LTCG rate, exemption threshold)
  - Finance Act 2023 (Section 50AA introduction)
  - Income Tax Act Sections 111A, 112A, 50AA
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Literal, Optional
from enum import Enum

# ─── CONSTANTS ─────────────────────────────────────────────────
EQUITY_LTCG_RATE_PCT: float = 12.5
EQUITY_STCG_RATE_PCT: float = 20.0  # Raised from 15% in Budget 2024
EQUITY_LTCG_EXEMPTION_INR: float = 1_25_000  # Raised from ₹1L in Budget 2024
EQUITY_HOLDING_MONTHS: int = 12

SECTION_50AA_EFFECTIVE_DATE: date = date(2023, 4, 1)
ELSS_LOCKIN_MONTHS: int = 36
EQUITY_THRESHOLD_FOR_HYBRID_PCT: float = 65.0

GOLD_ETF_LTCG_HOLDING_MONTHS: int = 12  # Listed
GOLD_ETF_LTCG_RATE_PCT: float = 12.5
GOLD_PHYSICAL_LTCG_HOLDING_MONTHS: int = 24


# ─── ENUMS ─────────────────────────────────────────────────────
class MFCategory(str, Enum):
    EQUITY_LARGE_CAP = "equity_large_cap"
    EQUITY_MID_CAP = "equity_mid_cap"
    EQUITY_SMALL_CAP = "equity_small_cap"
    EQUITY_FLEXI_CAP = "equity_flexi_cap"
    EQUITY_INDEX = "equity_index"
    ELSS = "elss"
    DEBT_LIQUID = "debt_liquid"
    DEBT_SHORT_DURATION = "debt_short_duration"
    DEBT_LONG_DURATION = "debt_long_duration"
    DEBT_CORPORATE_BOND = "debt_corporate_bond"
    HYBRID_AGGRESSIVE = "hybrid_aggressive"  # >65% equity → equity tax
    HYBRID_CONSERVATIVE = "hybrid_conservative"  # <65% equity → debt tax
    ARBITRAGE = "arbitrage"  # Treated as equity
    GOLD_ETF = "gold_etf"
    GOLD_MF_FOF = "gold_mf_fof"  # AVOID — Section 50AA


# ─── RESULT DATACLASSES ────────────────────────────────────────
@dataclass
class MFTaxResult:
    purchase_amount: float
    purchase_date: date
    sale_amount: float
    sale_date: date
    holding_months: int
    is_ltcg: bool
    category: MFCategory
    tax_treatment: str  # "equity_ltcg" | "equity_stcg" | "section_50aa_slab" | "debt_pre_2023_indexed"
    gain: float
    taxable_gain: float  # After ₹1.25L exemption for equity LTCG
    tax_amount: float
    effective_rate_pct: float
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class ELSSLockInResult:
    sip_date: date
    units_invested: float
    investment_amount: float
    lockin_expiry_date: date
    is_locked_in: bool
    days_remaining: int
    notes: list[str] = field(default_factory=list)


# ─── HELPERS ───────────────────────────────────────────────────
def _months_between(start: date, end: date) -> int:
    if end < start:
        return 0
    return (end.year - start.year) * 12 + (end.month - start.month)


def _classify_tax_treatment(category: MFCategory, purchase_date: date, sale_date: date) -> str:
    """Determine tax regime applicable to this sale."""
    holding = _months_between(purchase_date, sale_date)
    is_ltcg = holding > EQUITY_HOLDING_MONTHS

    equity_treated = {
        MFCategory.EQUITY_LARGE_CAP, MFCategory.EQUITY_MID_CAP,
        MFCategory.EQUITY_SMALL_CAP, MFCategory.EQUITY_FLEXI_CAP,
        MFCategory.EQUITY_INDEX, MFCategory.ELSS,
        MFCategory.HYBRID_AGGRESSIVE, MFCategory.ARBITRAGE,
        MFCategory.GOLD_ETF,  # Listed gold ETF treated as equity for LTCG purposes
    }

    if category in equity_treated:
        return "equity_ltcg" if is_ltcg else "equity_stcg"

    # Debt MFs (and hybrid conservative + gold MF FoF)
    if purchase_date >= SECTION_50AA_EFFECTIVE_DATE:
        return "section_50aa_slab"
    else:
        # Pre-April 2023 units: grandfathered to old regime
        if is_ltcg:  # Note: pre-2023 debt MFs had 36-month LTCG threshold
            holding_36mo = _months_between(purchase_date, sale_date) > 36
            return "debt_pre_2023_indexed" if holding_36mo else "debt_pre_2023_slab"
        return "debt_pre_2023_slab"


# ─── PUBLIC API ────────────────────────────────────────────────
def calculate_mf_tax(
    purchase_amount: float,
    purchase_date: date,
    sale_amount: float,
    sale_date: date,
    category: MFCategory,
    tax_slab_pct: float = 30.0,
    other_equity_ltcg_in_fy: float = 0,
) -> MFTaxResult:
    """
    Compute capital gains tax on Indian mutual fund redemption.

    Args:
        purchase_amount: Cost of acquisition
        purchase_date: When units were bought (critical for Sec 50AA grandfathering)
        sale_amount: Redemption proceeds
        sale_date: When units sold
        category: MF type (drives tax treatment)
        tax_slab_pct: Marginal rate for Section 50AA / debt slab
        other_equity_ltcg_in_fy: Other equity LTCG in same FY (consumes ₹1.25L exemption)
    """
    holding = _months_between(purchase_date, sale_date)
    is_ltcg = holding > EQUITY_HOLDING_MONTHS
    gain = sale_amount - purchase_amount
    treatment = _classify_tax_treatment(category, purchase_date, sale_date)
    warnings = []
    notes = []

    # ─── EQUITY LTCG ────────────────────────────────────────────
    if treatment == "equity_ltcg":
        # ₹1.25L exemption per FY, shared across all equity LTCG
        remaining_exemption = max(0, EQUITY_LTCG_EXEMPTION_INR - other_equity_ltcg_in_fy)
        taxable = max(0, gain - remaining_exemption)
        tax = taxable * EQUITY_LTCG_RATE_PCT / 100
        notes.append(f"Equity LTCG @ 12.5% above ₹1.25L exemption")
        notes.append(f"Exemption used: ₹{min(gain, remaining_exemption):,.0f} of available ₹{remaining_exemption:,.0f}")
        if category == MFCategory.ELSS and holding < ELSS_LOCKIN_MONTHS:
            warnings.append(f"⚠️ ELSS 36-month lock-in not yet met (held {holding} months)")

    # ─── EQUITY STCG ────────────────────────────────────────────
    elif treatment == "equity_stcg":
        taxable = gain
        tax = max(0, gain) * EQUITY_STCG_RATE_PCT / 100
        notes.append(f"Equity STCG @ 20% (raised from 15% in Budget 2024)")
        notes.append(f"Holding period {holding} months < 12 months")

    # ─── SECTION 50AA — THE BIG TRAP ─────────────────────────────
    elif treatment == "section_50aa_slab":
        taxable = gain
        tax = max(0, gain) * tax_slab_pct / 100
        warnings.append(
            f"⚠️ Section 50AA applies — debt MF purchased after 1 Apr 2023. "
            f"ALL gains taxed at slab ({tax_slab_pct}%). No LTCG benefit. No indexation."
        )
        notes.append("Consider exiting and switching to: G-Sec via RBI Retail Direct, or bank FD (similar risk, similar tax, no MF expense ratio)")
        if category == MFCategory.GOLD_MF_FOF:
            warnings.append("⚠️ Gold MF FoF specifically — switch to Gold ETF (listed) for 12.5% LTCG treatment")

    # ─── PRE-2023 DEBT MF — GRANDFATHERED ───────────────────────
    elif treatment == "debt_pre_2023_indexed":
        # 20% with indexation on real gain
        notes.append("Pre-1-Apr-2023 debt MF units — grandfathered to OLD regime")
        notes.append("20% with CII indexation available; 36-month holding period")
        notes.append("Caller should provide indexed cost for accurate calculation; assuming nominal for now")
        taxable = max(0, gain)
        tax = taxable * 20 / 100
        warnings.append("⚠️ Calculation uses NOMINAL gain — for true indexed value, run capital_gains_calculator")

    elif treatment == "debt_pre_2023_slab":
        taxable = gain
        tax = max(0, gain) * tax_slab_pct / 100
        notes.append("Pre-2023 debt MF held < 36 months — slab rate (old regime STCG-equivalent)")
    else:
        taxable = gain
        tax = max(0, gain) * tax_slab_pct / 100

    effective_rate = (tax / gain * 100) if gain > 0 else 0

    return MFTaxResult(
        purchase_amount=purchase_amount,
        purchase_date=purchase_date,
        sale_amount=sale_amount,
        sale_date=sale_date,
        holding_months=holding,
        is_ltcg=is_ltcg,
        category=category,
        tax_treatment=treatment,
        gain=gain,
        taxable_gain=taxable,
        tax_amount=tax,
        effective_rate_pct=effective_rate,
        warnings=warnings,
        notes=notes,
    )


def check_elss_lockin(sip_date: date, current_date: date, investment_amount: float, units: float = 0) -> ELSSLockInResult:
    """
    Check if an ELSS SIP installment is still locked in.

    CRITICAL: ELSS lock-in is PER SIP installment, not from the initial investment.
    A monthly SIP starting Jan 2024 has 36 separate lock-in expiries through Dec 2026.
    """
    from datetime import timedelta
    days_locked = ELSS_LOCKIN_MONTHS * 30  # Approximate; actual is 3 years calendar
    # Better: add 3 years to month
    expiry_year = sip_date.year + 3
    try:
        expiry = date(expiry_year, sip_date.month, sip_date.day)
    except ValueError:
        # Leap day edge case
        expiry = date(expiry_year, sip_date.month, 28)

    is_locked = current_date < expiry
    days_remaining = (expiry - current_date).days if is_locked else 0

    notes = [
        f"SIP date: {sip_date}",
        f"Lock-in expires: {expiry}",
        f"Status: {'LOCKED' if is_locked else 'UNLOCKED — can redeem'}",
    ]
    if is_locked:
        notes.append(f"⚠️ Cannot redeem for another {days_remaining} days ({days_remaining/30:.1f} months)")
    notes.append("Each monthly SIP installment has its own 36-month lock-in. Track separately.")

    return ELSSLockInResult(
        sip_date=sip_date,
        units_invested=units,
        investment_amount=investment_amount,
        lockin_expiry_date=expiry,
        is_locked_in=is_locked,
        days_remaining=days_remaining,
        notes=notes,
    )


def classify_hybrid_fund(equity_allocation_pct: float) -> dict:
    """
    Classify hybrid fund taxation based on equity percentage.
    Equity-oriented = equity LTCG/STCG rules apply.
    """
    is_equity_oriented = equity_allocation_pct > EQUITY_THRESHOLD_FOR_HYBRID_PCT
    return {
        "equity_allocation_pct": equity_allocation_pct,
        "is_equity_oriented": is_equity_oriented,
        "tax_treatment": "equity (12.5% LTCG above ₹1.25L)" if is_equity_oriented else "debt — Section 50AA slab",
        "threshold_pct": EQUITY_THRESHOLD_FOR_HYBRID_PCT,
        "common_examples_equity_oriented": ["Aggressive Hybrid", "Balanced Advantage (most)", "Equity Savings"],
        "common_examples_debt_oriented": ["Conservative Hybrid", "Multi-Asset Allocation (some)"],
    }


def section_50aa_warning() -> dict:
    """Standardized warning block for any debt MF discussion post April 2023."""
    return {
        "rule": "Section 50AA (introduced Finance Act 2023)",
        "effective_date": SECTION_50AA_EFFECTIVE_DATE.isoformat(),
        "applies_to": ["Debt MFs", "Gold MF FoF", "Conservative Hybrid (<65% equity)", "International FoF"],
        "tax_treatment": "ALL gains taxed at SLAB rate, regardless of holding period",
        "no_benefits": ["No LTCG rate", "No indexation", "No holding period advantage"],
        "alternatives_to_consider": [
            "G-Sec via RBI Retail Direct (direct bond, same risk, slab on interest + 12.5% LTCG on capital gains)",
            "Bank FD (taxable but predictable, DICGC ₹5L coverage)",
            "SCSS for seniors (8.20%, quarterly payout, 80C eligible)",
            "RBI Floating Rate Savings Bonds 2020 (8.05%)",
        ],
        "exception": "Units PURCHASED before 1 Apr 2023 are grandfathered to old regime (20% with indexation after 36mo)",
    }


__all__ = [
    "EQUITY_LTCG_RATE_PCT", "EQUITY_LTCG_EXEMPTION_INR", "SECTION_50AA_EFFECTIVE_DATE",
    "MFCategory", "MFTaxResult", "ELSSLockInResult",
    "calculate_mf_tax", "check_elss_lockin", "classify_hybrid_fund", "section_50aa_warning",
]
