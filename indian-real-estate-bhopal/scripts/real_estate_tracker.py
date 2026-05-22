"""
real_estate_tracker.py — Indian real estate calculator skill for portfolio agent v2/v3

Covers:
  • MP stamp duty + registration calculator
  • Capital gains calculator with grandfathering decision (12.5% no-index vs 20%+index)
  • Section 50C deemed-value check
  • Section 54 / 54EC / 54F / 54B exemption recommender
  • Rental income tax calculator (Section 24)
  • REIT income classifier with FY 2025-26 tax treatment
  • TDS calculator for property transactions (194-IA, 194-IB, 194-I)
  • Property holdings registry (track per-member real estate exposure)
  • Buy vs REIT comparator (10.5% MP transaction cost factored in)

All rates and rules verified May 2026 against:
  • Finance (No. 2) Act 2024
  • CBDT Circulars 3/2014 + 17/2015 (Section 2(14)(iii))
  • CBDT FAQ Press Release August 2024 (grandfathering rules)
  • SAMPADA 2.0 portal — sampada.mpigr.gov.in
  • SEBI REIT Regulations 2014 + 2024 amendments
  • Income Tax Act Sections 50C, 54, 54B, 54EC, 54F, 194-IA, 194-IB, 194-I

⚠️ Re-verify each February post-Budget. CII updates annually in June via CBDT notification.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional, Literal
from enum import Enum
import json
import math


# ═══════════════════════════════════════════════════════════════════
# CONSTANTS — STATUTORY VALUES (verified May 2026)
# ═══════════════════════════════════════════════════════════════════

# Cost Inflation Index table (CBDT-notified annually)
# Source: incometaxindia.gov.in/Communications/Notification
# FY 2025-26 (376) and FY 2026-27 are ESTIMATES — verify with current CBDT notification
CII_TABLE: dict[int, int] = {
    2002: 105, 2003: 109, 2004: 113, 2005: 117, 2006: 122, 2007: 129,
    2008: 137, 2009: 148, 2010: 167, 2011: 184, 2012: 200, 2013: 220,
    2014: 240, 2015: 254, 2016: 264, 2017: 272, 2018: 280, 2019: 289,
    2020: 301, 2021: 317, 2022: 331, 2023: 348, 2024: 363,
    2025: 376,  # ESTIMATE — verify with CBDT
    2026: 390,  # ESTIMATE — verify with CBDT
    2027: 405,  # ESTIMATE — verify with CBDT
}

# Madhya Pradesh transaction costs
MP_STAMP_DUTY_PCT: float = 7.5
MP_REGISTRATION_PCT: float = 3.0
MP_TOTAL_TRANSACTION_PCT: float = 10.5  # No gender concession in MP (verified)

# Grandfathering cutoff (Budget 2024)
GRANDFATHERING_CUTOFF: date = date(2024, 7, 23)

# Holding period thresholds
LTCG_HOLDING_MONTHS_PROPERTY: int = 24
LTCG_HOLDING_MONTHS_REIT: int = 12  # Reduced from 36 in Budget 2024

# LTCG rates
LTCG_RATE_NEW: float = 12.5  # Default post 23 Jul 2024
LTCG_RATE_OLD_WITH_INDEXATION: float = 20.0  # Grandfathering path

# REIT rates (Budget 2024)
REIT_LTCG_RATE: float = 12.5
REIT_LTCG_EXEMPTION_INR: float = 1_25_000  # ₹1.25L threshold per FY
REIT_STCG_RATE: float = 20.0  # Increased from 15% in Budget 2024

# Section 50C tolerance
SECTION_50C_TOLERANCE_RATIO: float = 1.10  # No adjustment if stamp_duty ≤ 1.10 × sale_price

# TDS thresholds (Section 194-IA, 194-IB, 194-I)
SECTION_194IA_THRESHOLD_INR: float = 50_00_000  # ₹50L (aggregate, even if multiple buyers)
SECTION_194IA_RATE: float = 0.01  # 1%

SECTION_194IB_THRESHOLD_MONTHLY: float = 50_000  # ₹50K/month
SECTION_194IB_RATE_FROM_OCT_2024: float = 0.02  # 2% (reduced from 5%)
SECTION_194IB_EFFECTIVE_DATE: date = date(2024, 10, 1)

SECTION_194I_RATE_LAND_BUILDING: float = 0.10  # 10%
SECTION_194I_THRESHOLD_ANNUAL: float = 6_00_000  # ₹6L/year (FY 2025-26)

# Exemption limits
SECTION_54_MAX_EXEMPTION_INR: float = 10_00_00_000  # ₹10 crore
SECTION_54EC_MAX_INR: float = 50_00_000  # ₹50L per FY
SECTION_54EC_LOCKUP_YEARS: int = 5
SECTION_54EC_INTEREST_RATE_PCT: float = 5.25

# Section 24 deductions
SECTION_24A_STD_DED_PCT: float = 30.0
SECTION_24B_SOP_CAP_INR: float = 200_000  # ₹2L for self-occupied
# Let-out has no cap on home loan interest

# Bhopal-specific
BHOPAL_MUNICIPAL_POPULATION: int = 23_00_000
URBAN_AG_LAND_DISTANCE_KM_BHOPAL: int = 8  # Section 2(14)(iii) aerial distance


# ═══════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════

class PropertyType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    LAND_PLOT = "land_plot"
    AGRICULTURAL_URBAN = "agricultural_urban"
    AGRICULTURAL_RURAL = "agricultural_rural"
    REIT = "reit"


class SaleAssetType(str, Enum):
    RESIDENTIAL_HOUSE = "residential_house"
    LAND_OR_BUILDING_NON_RESIDENTIAL = "land_or_building_non_residential"
    AGRICULTURAL_URBAN = "agricultural_urban"
    OTHER_LT_ASSET = "other_lt_asset"  # e.g., gold, listed securities


class TaxpayerType(str, Enum):
    RESIDENT_INDIVIDUAL = "resident_individual"
    RESIDENT_HUF = "resident_huf"
    NRI = "nri"
    COMPANY = "company"


class FamilyMember(str, Enum):
    SID = "Sid"
    MOTHER = "Mother"
    FATHER = "Father"


# ═══════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════

def fy_from_date(d: date) -> int:
    """Return Indian Financial Year (e.g., FY 2024-25 → 2024)."""
    return d.year if d.month >= 4 else d.year - 1


def months_between(start: date, end: date) -> int:
    """Calendar months between two dates (inclusive of partial)."""
    if end < start:
        return 0
    return (end.year - start.year) * 12 + (end.month - start.month)


def get_cii(fy_start_year: int) -> Optional[int]:
    """Get CII for a financial year. Returns None if not in table."""
    return CII_TABLE.get(fy_start_year)


def inr(amount: float) -> str:
    """Format INR amount with comma separators."""
    return f"₹{amount:,.0f}"


# ═══════════════════════════════════════════════════════════════════
# 1. STAMP DUTY CALCULATOR
# ═══════════════════════════════════════════════════════════════════

@dataclass
class StampDutyResult:
    property_value: float
    stamp_duty_pct: float
    stamp_duty_amount: float
    registration_pct: float
    registration_amount: float
    total_govt_charges: float
    total_cash_required: float
    govt_charges_pct_of_price: float
    state: str = "Madhya Pradesh"
    notes: list[str] = field(default_factory=list)


def calculate_stamp_duty(
    property_value: float,
    state: str = "MP",
    is_gift_deed_to_family: bool = False,
    is_commercial_lease: bool = False,
) -> StampDutyResult:
    """
    Calculate stamp duty + registration on Indian property purchase.

    Currently supports Madhya Pradesh (Bhopal-relevant). Other states would need
    their own stamp duty rules added.

    Args:
        property_value: Purchase price (or stamp duty value, whichever higher)
        state: State code (currently only "MP" supported)
        is_gift_deed_to_family: ₹1,000 fixed instead of 7.5% if gift to family
        is_commercial_lease: 8% stamp + 1% registration for lease deeds

    Returns:
        StampDutyResult with breakdown and total
    """
    if state.upper() != "MP":
        raise NotImplementedError(f"State {state} not implemented yet. Only MP supported.")

    notes = []

    if is_gift_deed_to_family:
        stamp_duty_amount = 1000  # Fixed ₹1,000
        registration_amount = property_value * 0.01
        stamp_pct = 0.0
        reg_pct = 1.0
        notes.append("Gift deed to family member: ₹1,000 fixed stamp duty + 1% registration")
    elif is_commercial_lease:
        stamp_pct = 8.0
        reg_pct = 1.0
        stamp_duty_amount = property_value * stamp_pct / 100
        registration_amount = property_value * reg_pct / 100
        notes.append("Commercial lease deed: 8% + 1%")
    else:
        stamp_pct = MP_STAMP_DUTY_PCT
        reg_pct = MP_REGISTRATION_PCT
        stamp_duty_amount = property_value * stamp_pct / 100
        registration_amount = property_value * reg_pct / 100
        notes.append(f"MP standard rate: {stamp_pct}% stamp + {reg_pct}% registration = {MP_TOTAL_TRANSACTION_PCT}%")

    total_govt = stamp_duty_amount + registration_amount

    notes.append("Verify current rates at sampada.mpigr.gov.in before transaction")
    notes.append("Excludes broker (~1-2%), legal fees, and interior costs")

    return StampDutyResult(
        property_value=property_value,
        stamp_duty_pct=stamp_pct,
        stamp_duty_amount=stamp_duty_amount,
        registration_pct=reg_pct,
        registration_amount=registration_amount,
        total_govt_charges=total_govt,
        total_cash_required=property_value + total_govt,
        govt_charges_pct_of_price=(total_govt / property_value * 100) if property_value > 0 else 0,
        notes=notes,
    )


# ═══════════════════════════════════════════════════════════════════
# 2. CAPITAL GAINS CALCULATOR (with grandfathering)
# ═══════════════════════════════════════════════════════════════════

@dataclass
class CapitalGainsResult:
    purchase_price: float
    purchase_date: date
    purchase_fy: int
    purchase_cii: Optional[int]
    sale_price: float
    sale_date: date
    sale_fy: int
    sale_cii: Optional[int]
    holding_months: int
    is_ltcg: bool
    eligible_for_grandfathering: bool
    nominal_gain: float

    # Path A: 12.5% no indexation
    path_a_tax: float

    # Path B: 20% with indexation
    path_b_indexed_cost: Optional[float]
    path_b_indexed_gain: Optional[float]
    path_b_tax: Optional[float]

    # Decision
    optimal_path: str  # "A_12.5%_no_index" | "B_20%_indexed" | "STCG_slab"
    optimal_tax: float
    savings_vs_other_path: float
    decision_rationale: str
    warnings: list[str] = field(default_factory=list)


def calculate_property_capital_gains(
    purchase_price: float,
    purchase_date: date,
    sale_price: float,
    sale_date: date,
    taxpayer_type: TaxpayerType = TaxpayerType.RESIDENT_INDIVIDUAL,
    override_purchase_cii: Optional[int] = None,
    override_sale_cii: Optional[int] = None,
) -> CapitalGainsResult:
    """
    Calculate capital gains on immovable property sale with grandfathering decision.

    Applies Budget 2024 (Finance Act No.2 2024) rules:
      • Property acquired ON OR AFTER 23 Jul 2024 → 12.5% flat, no indexation
      • Property acquired BEFORE 23 Jul 2024 (resident Individual/HUF only):
        - Choose LOWER of: (A) 12.5% no-indexation, OR (B) 20% with CII indexation
      • NRI: 12.5% no-indexation only (no grandfathering)
      • Holding < 24 months → STCG at slab rate (caller computes slab)

    Args:
        purchase_price: Original acquisition cost
        purchase_date: When property was acquired
        sale_price: Consideration received on sale (USE STAMP DUTY VALUE IF HIGHER per Sec 50C)
        sale_date: When sold
        taxpayer_type: Resident Individual/HUF gets grandfathering choice; NRI doesn't
        override_purchase_cii, override_sale_cii: Manual CII (otherwise use table)
    """
    warnings = []

    purchase_fy = fy_from_date(purchase_date)
    sale_fy = fy_from_date(sale_date)
    holding = months_between(purchase_date, sale_date)
    is_ltcg = holding > LTCG_HOLDING_MONTHS_PROPERTY

    purchase_cii = override_purchase_cii or get_cii(purchase_fy)
    sale_cii = override_sale_cii or get_cii(sale_fy)

    nominal_gain = sale_price - purchase_price

    # Eligibility for grandfathering
    eligible_for_grandfathering = (
        is_ltcg
        and purchase_date < GRANDFATHERING_CUTOFF
        and taxpayer_type in (TaxpayerType.RESIDENT_INDIVIDUAL, TaxpayerType.RESIDENT_HUF)
    )

    # STCG case — return early with slab indication
    if not is_ltcg:
        warnings.append(
            f"Holding period {holding} months < {LTCG_HOLDING_MONTHS_PROPERTY} months — "
            f"STCG applies (taxed at slab rate; not computed here)"
        )
        return CapitalGainsResult(
            purchase_price=purchase_price,
            purchase_date=purchase_date,
            purchase_fy=purchase_fy,
            purchase_cii=purchase_cii,
            sale_price=sale_price,
            sale_date=sale_date,
            sale_fy=sale_fy,
            sale_cii=sale_cii,
            holding_months=holding,
            is_ltcg=False,
            eligible_for_grandfathering=False,
            nominal_gain=nominal_gain,
            path_a_tax=0.0,
            path_b_indexed_cost=None,
            path_b_indexed_gain=None,
            path_b_tax=None,
            optimal_path="STCG_slab",
            optimal_tax=0.0,  # Caller computes slab
            savings_vs_other_path=0.0,
            decision_rationale="STCG — add gain to total income, tax at applicable slab",
            warnings=warnings,
        )

    # LTCG — Path A: 12.5% no indexation
    path_a_tax = max(0.0, nominal_gain) * LTCG_RATE_NEW / 100

    # LTCG — Path B: 20% with indexation (only if eligible)
    path_b_indexed_cost = None
    path_b_indexed_gain = None
    path_b_tax = None

    if eligible_for_grandfathering and purchase_cii and sale_cii:
        path_b_indexed_cost = purchase_price * sale_cii / purchase_cii
        path_b_indexed_gain = sale_price - path_b_indexed_cost
        path_b_tax = max(0.0, path_b_indexed_gain) * LTCG_RATE_OLD_WITH_INDEXATION / 100
    elif eligible_for_grandfathering and (not purchase_cii or not sale_cii):
        warnings.append(
            f"CII unavailable (purchase FY {purchase_fy} or sale FY {sale_fy}). "
            "Cannot compute Path B. Pass override_purchase_cii/override_sale_cii or update CII_TABLE."
        )

    # Decision
    if path_b_tax is not None and path_b_tax < path_a_tax:
        optimal_path = "B_20%_indexed"
        optimal_tax = path_b_tax
        savings = path_a_tax - path_b_tax
        rationale = (
            f"Indexed cost ₹{path_b_indexed_cost:,.0f} reduces taxable gain to ₹{path_b_indexed_gain:,.0f}. "
            f"20% on indexed gain (₹{path_b_tax:,.0f}) is lower than 12.5% on nominal gain (₹{path_a_tax:,.0f}). "
            f"Elect grandfathering path."
        )
    elif path_b_tax is not None:
        optimal_path = "A_12.5%_no_index"
        optimal_tax = path_a_tax
        savings = path_b_tax - path_a_tax
        rationale = (
            f"Property appreciated faster than inflation. 12.5% on nominal gain (₹{path_a_tax:,.0f}) "
            f"beats 20% on indexed gain (₹{path_b_tax:,.0f})."
        )
    else:
        # No grandfathering eligibility
        optimal_path = "A_12.5%_no_index"
        optimal_tax = path_a_tax
        savings = 0.0
        if taxpayer_type == TaxpayerType.NRI:
            rationale = "NRI sellers cannot elect grandfathering. 12.5% no-indexation only."
        else:
            rationale = "Post-23-Jul-2024 acquisition: 12.5% no-indexation is the only option."

    # Surcharge warning
    if nominal_gain > 50_00_000:
        warnings.append(
            "⚠️ Surcharge is computed on NON-indexed (raw nominal) gain regardless of path chosen. "
            "For gains > ₹50L, verify surcharge interaction with CA."
        )

    return CapitalGainsResult(
        purchase_price=purchase_price,
        purchase_date=purchase_date,
        purchase_fy=purchase_fy,
        purchase_cii=purchase_cii,
        sale_price=sale_price,
        sale_date=sale_date,
        sale_fy=sale_fy,
        sale_cii=sale_cii,
        holding_months=holding,
        is_ltcg=True,
        eligible_for_grandfathering=eligible_for_grandfathering,
        nominal_gain=nominal_gain,
        path_a_tax=path_a_tax,
        path_b_indexed_cost=path_b_indexed_cost,
        path_b_indexed_gain=path_b_indexed_gain,
        path_b_tax=path_b_tax,
        optimal_path=optimal_path,
        optimal_tax=optimal_tax,
        savings_vs_other_path=savings,
        decision_rationale=rationale,
        warnings=warnings,
    )


# ═══════════════════════════════════════════════════════════════════
# 3. SECTION 50C — DEEMED VALUE CHECK
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Section50CResult:
    actual_sale_price: float
    stamp_duty_value: float
    ratio: float
    tolerance_threshold: float
    adjustment_required: bool
    deemed_sale_consideration: float
    extra_tax_exposure: float
    notes: list[str] = field(default_factory=list)


def check_section_50c(
    actual_sale_price: float,
    stamp_duty_value: float,
) -> Section50CResult:
    """
    Section 50C check: if sale price < stamp duty value, the higher value is DEEMED the sale price.

    10% tolerance: no adjustment if stamp_duty_value ≤ 1.10 × actual_sale_price.

    Args:
        actual_sale_price: Consideration actually received
        stamp_duty_value: SAMPADA / circle rate value of the property at sale
    """
    ratio = stamp_duty_value / actual_sale_price if actual_sale_price > 0 else float("inf")
    notes = []

    if stamp_duty_value <= actual_sale_price * SECTION_50C_TOLERANCE_RATIO:
        adjustment_required = False
        deemed_consideration = actual_sale_price
        extra_exposure = 0.0
        notes.append(
            f"Stamp duty value ({inr(stamp_duty_value)}) within 10% tolerance of actual sale "
            f"({inr(actual_sale_price)}). No Section 50C adjustment."
        )
    else:
        adjustment_required = True
        deemed_consideration = stamp_duty_value
        extra_exposure = (stamp_duty_value - actual_sale_price) * LTCG_RATE_NEW / 100
        notes.append(
            f"⚠️ Section 50C TRIGGERED: stamp duty value ({inr(stamp_duty_value)}) > "
            f"110% of actual sale price ({inr(actual_sale_price)})."
        )
        notes.append(
            f"Capital gains computed using stamp duty value as deemed sale consideration. "
            f"Extra LTCG tax exposure: ~{inr(extra_exposure)} at 12.5%."
        )
        notes.append(
            "Option: dispute via DVO (Departmental Valuation Officer) referral. "
            "If DVO value < stamp duty value, DVO value is used."
        )

    return Section50CResult(
        actual_sale_price=actual_sale_price,
        stamp_duty_value=stamp_duty_value,
        ratio=ratio,
        tolerance_threshold=SECTION_50C_TOLERANCE_RATIO,
        adjustment_required=adjustment_required,
        deemed_sale_consideration=deemed_consideration,
        extra_tax_exposure=extra_exposure,
        notes=notes,
    )


# ═══════════════════════════════════════════════════════════════════
# 4. EXEMPTION RECOMMENDER (Sections 54, 54EC, 54F, 54B)
# ═══════════════════════════════════════════════════════════════════

@dataclass
class ExemptionOption:
    section: str
    max_exemption: float
    time_window: str
    conditions: list[str]
    applicable_to_this_sale: bool
    estimated_tax_saved: float = 0.0


@dataclass
class ExemptionRecommendation:
    sale_asset_type: SaleAssetType
    ltcg_amount: float
    base_tax_without_exemption: float
    options: list[ExemptionOption]
    recommended_option: str
    recommended_rationale: str


def recommend_capital_gains_exemption(
    sale_asset_type: SaleAssetType,
    ltcg_amount: float,
    has_other_residential_house: bool = False,
    can_reinvest_full_amount: bool = True,
) -> ExemptionRecommendation:
    """
    Recommend the best capital gains exemption section based on sale asset type.

    Decision logic:
      • Sale of residential house → Section 54 (best, fully exempt up to ₹10cr) or Section 54EC (up to ₹50L)
      • Sale of land/building NOT residential → Section 54EC ONLY
      • Sale of urban agricultural land → Section 54B (rollover to agricultural land)
      • Sale of other LT asset → Section 54F (if can buy/build residential house and don't own >1 other)
    """
    base_tax = ltcg_amount * LTCG_RATE_NEW / 100  # Assume 12.5% baseline

    options: list[ExemptionOption] = []

    # Section 54 — residential house → residential house
    options.append(ExemptionOption(
        section="Section 54",
        max_exemption=min(ltcg_amount, SECTION_54_MAX_EXEMPTION_INR),
        time_window="Purchase: 1 yr before / 2 yrs after sale; Construction: 3 yrs after sale",
        conditions=[
            "Sale must be of residential house property",
            "Reinvest in another residential house (in India)",
            "Max exemption ₹10 crore",
            "2-house option available once-in-lifetime if LTCG ≤ ₹2 crore",
        ],
        applicable_to_this_sale=(sale_asset_type == SaleAssetType.RESIDENTIAL_HOUSE),
        estimated_tax_saved=base_tax if can_reinvest_full_amount and sale_asset_type == SaleAssetType.RESIDENTIAL_HOUSE else 0,
    ))

    # Section 54EC — land or building → REC/PFC/IRFC/NHAI bonds
    options.append(ExemptionOption(
        section="Section 54EC",
        max_exemption=min(ltcg_amount, SECTION_54EC_MAX_INR),
        time_window="Within 6 months of transfer",
        conditions=[
            f"Max ₹{SECTION_54EC_MAX_INR/100000:.0f} lakh per FY (across current + next FY combined)",
            f"{SECTION_54EC_LOCKUP_YEARS}-year lock-in",
            f"{SECTION_54EC_INTEREST_RATE_PCT}% interest (taxable at slab)",
            "Bonds non-transferable; no premature exit",
        ],
        applicable_to_this_sale=(sale_asset_type in (
            SaleAssetType.RESIDENTIAL_HOUSE,
            SaleAssetType.LAND_OR_BUILDING_NON_RESIDENTIAL,
            SaleAssetType.AGRICULTURAL_URBAN,
        )),
        estimated_tax_saved=min(ltcg_amount, SECTION_54EC_MAX_INR) * LTCG_RATE_NEW / 100,
    ))

    # Section 54F — any other LT asset → residential house
    options.append(ExemptionOption(
        section="Section 54F",
        max_exemption=min(ltcg_amount, SECTION_54_MAX_EXEMPTION_INR),
        time_window="Purchase: 1 yr before / 2 yrs after sale; Construction: 3 yrs",
        conditions=[
            "Sale of ANY long-term capital asset EXCEPT residential house",
            "Reinvest sale proceeds (not just gain) in one residential house",
            "Cannot own more than 1 other residential house on sale date",
            "Max exemption ₹10 crore",
            "Proportionate exemption if partial reinvestment",
        ],
        applicable_to_this_sale=(
            sale_asset_type == SaleAssetType.OTHER_LT_ASSET
            and not has_other_residential_house
        ),
        estimated_tax_saved=base_tax if can_reinvest_full_amount and sale_asset_type == SaleAssetType.OTHER_LT_ASSET and not has_other_residential_house else 0,
    ))

    # Section 54B — agricultural land → other agricultural land
    options.append(ExemptionOption(
        section="Section 54B",
        max_exemption=ltcg_amount,
        time_window="Within 2 years from date of transfer",
        conditions=[
            "Sale must be of agricultural land (urban; rural has no CGT to begin with)",
            "Reinvest in other agricultural land",
            "Land must have been used for agricultural purposes",
            "Individual/HUF only",
        ],
        applicable_to_this_sale=(sale_asset_type == SaleAssetType.AGRICULTURAL_URBAN),
        estimated_tax_saved=base_tax if can_reinvest_full_amount and sale_asset_type == SaleAssetType.AGRICULTURAL_URBAN else 0,
    ))

    # Decision
    applicable_options = [o for o in options if o.applicable_to_this_sale]
    if not applicable_options:
        recommended = "None"
        rationale = "No exemption section applies to this sale type."
    else:
        # Prefer highest tax saved
        best = max(applicable_options, key=lambda o: o.estimated_tax_saved)
        recommended = best.section
        if best.section == "Section 54" and ltcg_amount > SECTION_54EC_MAX_INR:
            rationale = f"Section 54 covers full LTCG (up to ₹10cr) if reinvested in residential property. " \
                        f"Section 54EC only covers ₹{SECTION_54EC_MAX_INR/100000:.0f}L. Prefer 54 if you want to buy another home."
        elif best.section == "Section 54EC":
            rationale = (
                f"Section 54EC bonds give ₹{best.max_exemption:,.0f} exemption (cap ₹50L). "
                f"5-year lockup at {SECTION_54EC_INTEREST_RATE_PCT}%. Best if not planning to buy new property."
            )
        else:
            rationale = f"{best.section} is the most tax-efficient route for this asset type."

    return ExemptionRecommendation(
        sale_asset_type=sale_asset_type,
        ltcg_amount=ltcg_amount,
        base_tax_without_exemption=base_tax,
        options=options,
        recommended_option=recommended,
        recommended_rationale=rationale,
    )


# ═══════════════════════════════════════════════════════════════════
# 5. RENTAL INCOME CALCULATOR (Section 24)
# ═══════════════════════════════════════════════════════════════════

@dataclass
class RentalIncomeResult:
    annual_rent: float
    municipal_taxes: float
    home_loan_interest: float
    is_let_out: bool
    nav: float  # Net Annual Value
    section_24a_std_deduction: float
    section_24b_interest_deduction: float
    taxable_income_from_house_property: float
    tax_at_slab: float
    is_loss: bool
    new_regime_loss_warning: Optional[str]
    notes: list[str] = field(default_factory=list)


def calculate_rental_income_tax(
    annual_rent: float,
    municipal_taxes: float = 0,
    home_loan_interest: float = 0,
    is_let_out: bool = True,
    tax_slab_pct: float = 30.0,
    is_new_regime: bool = True,
) -> RentalIncomeResult:
    """
    Calculate taxable income from house property under Section 24.

    Section 24(a): 30% standard deduction on NAV (flat, no documentation)
    Section 24(b): home loan interest — full for let-out, ₹2L cap for self-occupied

    NEW regime restriction: loss from let-out property CANNOT be set off against other income.
    OLD regime: loss can be set off up to ₹2L/yr against other income; carried forward 8 yrs.
    """
    notes = []

    if is_let_out:
        # Let-out
        nav = annual_rent - municipal_taxes
        std_ded = nav * SECTION_24A_STD_DED_PCT / 100
        interest_ded = home_loan_interest  # No cap for let-out
        notes.append("Let-out property: full home loan interest deductible (no ₹2L cap)")
    else:
        # Self-occupied
        nav = 0  # No rental income
        std_ded = 0
        interest_ded = min(home_loan_interest, SECTION_24B_SOP_CAP_INR)
        if home_loan_interest > SECTION_24B_SOP_CAP_INR:
            notes.append(
                f"Self-occupied: home loan interest CAPPED at ₹{SECTION_24B_SOP_CAP_INR:,}. "
                f"Excess ₹{home_loan_interest - SECTION_24B_SOP_CAP_INR:,} is NOT deductible."
            )

    taxable = nav - std_ded - interest_ded
    is_loss = taxable < 0

    if is_loss:
        tax_at_slab = 0.0
        notes.append(f"Loss from house property: ₹{-taxable:,.0f}")
    else:
        tax_at_slab = taxable * tax_slab_pct / 100

    new_regime_warning = None
    if is_loss and is_new_regime:
        new_regime_warning = (
            "⚠️ NEW REGIME: Loss from let-out property CANNOT be set off against other income. "
            "Only carried forward to offset future house-property income (8-year limit)."
        )
        notes.append(new_regime_warning)
    elif is_loss and not is_new_regime:
        notes.append(
            "OLD REGIME: Loss up to ₹2L can be set off against other income this year. "
            "Balance carried forward 8 years."
        )

    return RentalIncomeResult(
        annual_rent=annual_rent,
        municipal_taxes=municipal_taxes,
        home_loan_interest=home_loan_interest,
        is_let_out=is_let_out,
        nav=nav,
        section_24a_std_deduction=std_ded,
        section_24b_interest_deduction=interest_ded,
        taxable_income_from_house_property=taxable,
        tax_at_slab=tax_at_slab,
        is_loss=is_loss,
        new_regime_loss_warning=new_regime_warning,
        notes=notes,
    )


# ═══════════════════════════════════════════════════════════════════
# 6. REIT INCOME CLASSIFIER
# ═══════════════════════════════════════════════════════════════════

@dataclass
class REITIncomeResult:
    total_distribution: float
    interest_component: float
    dividend_component: float
    rental_component: float
    capital_repayment: float
    tax_slab_pct: float
    spv_under_115baa: bool

    # Per-component tax
    tax_on_interest: float
    tax_on_dividend: float
    tax_on_rental: float
    # Capital repayment is NOT taxed (reduces cost basis)
    total_tax: float
    net_distribution: float
    notes: list[str] = field(default_factory=list)


def classify_reit_income(
    total_distribution: float,
    interest_pct: float = 0.30,
    dividend_pct: float = 0.20,
    rental_pct: float = 0.30,
    capital_repayment_pct: float = 0.20,
    tax_slab_pct: float = 30.0,
    spv_under_115baa: bool = False,
) -> REITIncomeResult:
    """
    Classify REIT distribution into tax components per Finance Act 2024.

    Components are typically disclosed in each REIT's quarterly distribution notice.
    Defaults are illustrative — for real calc, pull actual % from REIT's quarterly notice.

    Tax rules (FY 2025-26):
      • Interest distribution → slab rate
      • Dividend (SPV NOT u/s 115BAA) → EXEMPT (most common)
      • Dividend (SPV under 115BAA) → slab rate (rare)
      • Rental distribution → slab rate
      • Capital repayment → NOT taxed (reduces cost basis)
    """
    notes = []

    # Validate percentages
    total_pct = interest_pct + dividend_pct + rental_pct + capital_repayment_pct
    if abs(total_pct - 1.0) > 0.001:
        notes.append(f"⚠️ Component percentages sum to {total_pct:.3f}, not 1.0. Check input.")

    interest = total_distribution * interest_pct
    dividend = total_distribution * dividend_pct
    rental = total_distribution * rental_pct
    capital_repay = total_distribution * capital_repayment_pct

    # Tax computation
    tax_interest = interest * tax_slab_pct / 100
    tax_dividend = dividend * tax_slab_pct / 100 if spv_under_115baa else 0.0
    tax_rental = rental * tax_slab_pct / 100
    # Capital repayment NOT taxed

    if spv_under_115baa:
        notes.append("SPV opted for Section 115BAA → REIT dividend taxed at slab rate (rare case)")
    else:
        notes.append("Standard case: dividend portion is EXEMPT (most Indian REITs)")

    notes.append(f"Capital repayment ({inr(capital_repay)}) reduces your cost basis; NOT taxed now")
    notes.append("REIT LTCG (held >12 months): 12.5% above ₹1.25L/year (post Budget 2024)")

    total_tax = tax_interest + tax_dividend + tax_rental
    net = total_distribution - total_tax

    return REITIncomeResult(
        total_distribution=total_distribution,
        interest_component=interest,
        dividend_component=dividend,
        rental_component=rental,
        capital_repayment=capital_repay,
        tax_slab_pct=tax_slab_pct,
        spv_under_115baa=spv_under_115baa,
        tax_on_interest=tax_interest,
        tax_on_dividend=tax_dividend,
        tax_on_rental=tax_rental,
        total_tax=total_tax,
        net_distribution=net,
        notes=notes,
    )


# ═══════════════════════════════════════════════════════════════════
# 7. TDS CALCULATOR (Section 194-IA / 194-IB / 194-I)
# ═══════════════════════════════════════════════════════════════════

@dataclass
class TDSResult:
    section: str
    transaction_type: str
    amount: float
    applicable: bool
    rate_pct: float
    tds_amount: float
    threshold_inr: float
    deductor: str  # "buyer" or "tenant"
    form_required: str
    effective_date: Optional[date]
    notes: list[str] = field(default_factory=list)


def calculate_property_purchase_tds(property_value: float) -> TDSResult:
    """
    Section 194-IA: 1% TDS on property purchase ≥ ₹50 lakh.
    Buyer (transferee) deducts. Form 26QB. No TAN required.
    """
    notes = []
    applicable = property_value >= SECTION_194IA_THRESHOLD_INR

    if applicable:
        tds = property_value * SECTION_194IA_RATE
        notes.append(f"Buyer must deduct 1% TDS = {inr(tds)}")
        notes.append("File Form 26QB online within 30 days of month-end of deduction")
        notes.append("Aggregate even if multiple buyers each pay < ₹50L (post Oct 2024 amendment)")
    else:
        tds = 0
        notes.append(f"Below ₹50L threshold ({inr(property_value)}) — no TDS")

    return TDSResult(
        section="194-IA",
        transaction_type="Property purchase",
        amount=property_value,
        applicable=applicable,
        rate_pct=SECTION_194IA_RATE * 100,
        tds_amount=tds,
        threshold_inr=SECTION_194IA_THRESHOLD_INR,
        deductor="buyer",
        form_required="26QB",
        effective_date=None,
        notes=notes,
    )


def calculate_rental_tds_individual(monthly_rent: float) -> TDSResult:
    """
    Section 194-IB: 2% TDS by individual/HUF tenant if monthly rent > ₹50K.
    Reduced from 5% effective 1 October 2024.
    """
    notes = []
    applicable = monthly_rent > SECTION_194IB_THRESHOLD_MONTHLY
    annual_rent = monthly_rent * 12

    if applicable:
        # 2% on annual rent
        tds = annual_rent * SECTION_194IB_RATE_FROM_OCT_2024
        notes.append(f"Rate REDUCED from 5% to 2% effective 1 Oct 2024 (Finance Act No.2 2024)")
        notes.append(f"Tenant (individual/HUF, non-audit) deducts {inr(tds)} once per year")
        notes.append("File Form 26QC (no TAN required)")
        notes.append("If tenant is company OR audit-liable: Section 194-I applies instead (10%)")
    else:
        tds = 0
        notes.append(f"Below ₹50K/month threshold — no TDS")

    return TDSResult(
        section="194-IB",
        transaction_type="Residential rent (individual tenant)",
        amount=annual_rent,
        applicable=applicable,
        rate_pct=SECTION_194IB_RATE_FROM_OCT_2024 * 100,
        tds_amount=tds,
        threshold_inr=SECTION_194IB_THRESHOLD_MONTHLY * 12,
        deductor="tenant",
        form_required="26QC",
        effective_date=SECTION_194IB_EFFECTIVE_DATE,
        notes=notes,
    )


def calculate_rental_tds_commercial(annual_rent: float) -> TDSResult:
    """
    Section 194-I: 10% TDS on rent paid to land/building owner by company or audit-liable tenant.
    Threshold: ₹6 lakh/year (FY 2025-26).
    """
    notes = []
    applicable = annual_rent > SECTION_194I_THRESHOLD_ANNUAL

    if applicable:
        tds = annual_rent * SECTION_194I_RATE_LAND_BUILDING
        notes.append(f"Applies to company tenants or audit-liable individuals")
        notes.append(f"Annual TDS: {inr(tds)} (10% on full year's rent)")
        notes.append("Tenant must have TAN; file Form 26Q quarterly")
    else:
        tds = 0
        notes.append(f"Below ₹6L/year threshold — no TDS")

    return TDSResult(
        section="194-I",
        transaction_type="Commercial/business rent",
        amount=annual_rent,
        applicable=applicable,
        rate_pct=SECTION_194I_RATE_LAND_BUILDING * 100,
        tds_amount=tds,
        threshold_inr=SECTION_194I_THRESHOLD_ANNUAL,
        deductor="tenant",
        form_required="26Q",
        effective_date=None,
        notes=notes,
    )


# ═══════════════════════════════════════════════════════════════════
# 8. BUY vs REIT COMPARATOR
# ═══════════════════════════════════════════════════════════════════

@dataclass
class BuyVsREITResult:
    capital: float
    holding_years: int

    # Direct property scenario
    property_purchase_price: float
    stamp_duty_and_reg: float
    annual_rent: float
    annual_appreciation_pct: float
    gross_yield_pct: float

    # REIT scenario
    reit_yield_pct: float
    reit_appreciation_pct: float

    # End-of-period results
    direct_property_terminal_value: float
    direct_total_rental: float
    direct_total_return_pct: float

    reit_terminal_value: float
    reit_total_distributions: float
    reit_total_return_pct: float

    winner: str
    notes: list[str] = field(default_factory=list)


def compare_buy_vs_reit(
    capital_available: float,
    holding_years: int,
    annual_rent_yield_pct: float = 3.0,
    annual_appreciation_pct: float = 7.0,
    reit_yield_pct: float = 6.5,
    reit_appreciation_pct: float = 4.0,
) -> BuyVsREITResult:
    """
    Apples-to-apples comparison: same capital invested in direct Bhopal property vs REIT.

    Direct property assumes 10.5% MP stamp duty + registration eats into initial buy.
    REIT assumes zero entry cost (just brokerage, negligible).
    """
    notes = []

    # Direct: capital eaten by transaction cost
    # If total cash available = C, property price = C / 1.105
    property_price = capital_available / (1 + MP_TOTAL_TRANSACTION_PCT / 100)
    stamp_reg = capital_available - property_price

    annual_rent = property_price * annual_rent_yield_pct / 100
    total_rental = annual_rent * holding_years  # Simplified — ignores rent escalation
    property_terminal = property_price * ((1 + annual_appreciation_pct / 100) ** holding_years)
    direct_total = (property_terminal + total_rental - capital_available) / capital_available * 100

    # REIT: full capital invested
    reit_initial = capital_available
    reit_distributions = reit_initial * reit_yield_pct / 100 * holding_years
    reit_terminal = reit_initial * ((1 + reit_appreciation_pct / 100) ** holding_years)
    reit_total = (reit_terminal + reit_distributions - reit_initial) / reit_initial * 100

    direct_total_value = property_terminal + total_rental
    reit_total_value = reit_terminal + reit_distributions

    if direct_total_value > reit_total_value:
        winner = f"Direct property by {inr(direct_total_value - reit_total_value)}"
    else:
        winner = f"REIT by {inr(reit_total_value - direct_total_value)}"

    notes.append(f"Initial capital: {inr(capital_available)}")
    notes.append(f"Direct: ₹{property_price:,.0f} property + ₹{stamp_reg:,.0f} govt charges (10.5%)")
    notes.append(f"REIT: ₹{capital_available:,.0f} fully invested (zero entry cost)")
    notes.append(f"Note: ignores tax on rental/distributions, REIT LTCG (12.5% > 12mo), property LTCG (12.5%/20%-indexed)")
    notes.append(f"Note: ignores liquidity premium (REIT exits in 1 day; property in months/years)")

    return BuyVsREITResult(
        capital=capital_available,
        holding_years=holding_years,
        property_purchase_price=property_price,
        stamp_duty_and_reg=stamp_reg,
        annual_rent=annual_rent,
        annual_appreciation_pct=annual_appreciation_pct,
        gross_yield_pct=annual_rent_yield_pct,
        reit_yield_pct=reit_yield_pct,
        reit_appreciation_pct=reit_appreciation_pct,
        direct_property_terminal_value=property_terminal,
        direct_total_rental=total_rental,
        direct_total_return_pct=direct_total,
        reit_terminal_value=reit_terminal,
        reit_total_distributions=reit_distributions,
        reit_total_return_pct=reit_total,
        winner=winner,
        notes=notes,
    )


# ═══════════════════════════════════════════════════════════════════
# 9. PROPERTY HOLDINGS REGISTRY
# ═══════════════════════════════════════════════════════════════════

@dataclass
class PropertyHolding:
    holding_id: str
    member: FamilyMember
    property_type: PropertyType
    purchase_date: date
    purchase_price: float
    current_estimated_value: Optional[float] = None
    annual_rent_income: float = 0.0
    annual_municipal_tax: float = 0.0
    annual_home_loan_interest: float = 0.0
    is_let_out: bool = False
    location: str = ""
    notes: str = ""


class PropertyHoldingsRegistry:
    """In-memory registry of family real estate holdings. Persist via to_json/from_json."""

    def __init__(self):
        self.holdings: list[PropertyHolding] = []

    def add(self, holding: PropertyHolding) -> None:
        if any(h.holding_id == holding.holding_id for h in self.holdings):
            raise ValueError(f"Holding ID {holding.holding_id} already exists")
        self.holdings.append(holding)

    def remove(self, holding_id: str) -> bool:
        before = len(self.holdings)
        self.holdings = [h for h in self.holdings if h.holding_id != holding_id]
        return len(self.holdings) < before

    def by_member(self, member: FamilyMember) -> list[PropertyHolding]:
        return [h for h in self.holdings if h.member == member]

    def total_value_by_member(self, member: FamilyMember) -> float:
        return sum(
            (h.current_estimated_value or h.purchase_price) for h in self.by_member(member)
        )

    def total_annual_rent_by_member(self, member: FamilyMember) -> float:
        return sum(h.annual_rent_income for h in self.by_member(member) if h.is_let_out)

    def simulate_sale(
        self,
        holding_id: str,
        sale_price: float,
        sale_date: date,
        taxpayer_type: TaxpayerType = TaxpayerType.RESIDENT_INDIVIDUAL,
    ) -> dict:
        """
        Simulate selling a holding — returns capital gains + exemption recommendations.
        """
        holding = next((h for h in self.holdings if h.holding_id == holding_id), None)
        if not holding:
            raise ValueError(f"Holding {holding_id} not found")

        cg = calculate_property_capital_gains(
            purchase_price=holding.purchase_price,
            purchase_date=holding.purchase_date,
            sale_price=sale_price,
            sale_date=sale_date,
            taxpayer_type=taxpayer_type,
        )

        # Map property type to sale asset type for exemption recommendation
        if holding.property_type == PropertyType.RESIDENTIAL:
            asset_type = SaleAssetType.RESIDENTIAL_HOUSE
        elif holding.property_type == PropertyType.AGRICULTURAL_URBAN:
            asset_type = SaleAssetType.AGRICULTURAL_URBAN
        elif holding.property_type in (PropertyType.COMMERCIAL, PropertyType.LAND_PLOT):
            asset_type = SaleAssetType.LAND_OR_BUILDING_NON_RESIDENTIAL
        else:
            asset_type = SaleAssetType.OTHER_LT_ASSET

        exemption_rec = recommend_capital_gains_exemption(
            sale_asset_type=asset_type,
            ltcg_amount=cg.nominal_gain if cg.is_ltcg else 0,
        )

        # Section 194-IA TDS that buyer would deduct
        tds_buyer = calculate_property_purchase_tds(sale_price)

        return {
            "holding": asdict(holding),
            "capital_gains": _serializable(asdict(cg)),
            "exemption_recommendation": _serializable(asdict(exemption_rec)),
            "tds_buyer_will_deduct": asdict(tds_buyer),
        }

    def to_dict(self) -> dict:
        return {"holdings": [_serializable(asdict(h)) for h in self.holdings]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)


# ═══════════════════════════════════════════════════════════════════
# 10. UTILITY — Bhopal urban vs rural agricultural land classifier
# ═══════════════════════════════════════════════════════════════════

@dataclass
class AgriLandClassification:
    aerial_distance_km_from_bhopal: float
    is_urban_agricultural: bool
    capital_gains_applicable: bool
    notes: list[str] = field(default_factory=list)


def classify_agricultural_land_bhopal(
    aerial_distance_km_from_bhopal_municipal: float
) -> AgriLandClassification:
    """
    Section 2(14)(iii) — classify agricultural land as urban or rural for Bhopal.

    Bhopal municipal population ~23 lakh (>10 lakh) so urban classification applies
    within 8 km AERIAL distance from BMC limits.

    Land outside Bhopal municipal area but within distance threshold for ANOTHER
    municipality (e.g., Sehore town) needs separate classification.
    """
    is_urban = aerial_distance_km_from_bhopal_municipal <= URBAN_AG_LAND_DISTANCE_KM_BHOPAL

    notes = [
        f"Bhopal municipal population: ~{BHOPAL_MUNICIPAL_POPULATION:,} (> 10 lakh)",
        f"Urban classification threshold: aerial distance ≤ {URBAN_AG_LAND_DISTANCE_KM_BHOPAL} km",
        f"Land at {aerial_distance_km_from_bhopal_municipal} km is classified as: "
        f"{'URBAN agricultural (capital asset)' if is_urban else 'RURAL agricultural (NOT a capital asset)'}",
    ]

    if is_urban:
        notes.append("Sale → capital gains tax applies; Section 54B rollover available")
    else:
        notes.append("Sale → NO capital gains tax (Section 2(14)(iii) exemption)")
        notes.append("⚠️ Check distance from nearest OTHER municipality too — same rules apply")

    return AgriLandClassification(
        aerial_distance_km_from_bhopal=aerial_distance_km_from_bhopal_municipal,
        is_urban_agricultural=is_urban,
        capital_gains_applicable=is_urban,
        notes=notes,
    )


# ═══════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════

def _serializable(d: dict) -> dict:
    """Convert non-JSON-serializable types (date, Enum) to strings recursively."""
    def _coerce(v):
        if isinstance(v, dict):
            return _serializable(v)
        if isinstance(v, list):
            return [_coerce(item) for item in v]
        if isinstance(v, Enum):
            return v.value  # Use Enum value (e.g., "Mother") not str() ("FamilyMember.MOTHER")
        if isinstance(v, date):
            return v.isoformat()
        return v
    return {k: _coerce(v) for k, v in d.items()}


# ═══════════════════════════════════════════════════════════════════
# Module exports
# ═══════════════════════════════════════════════════════════════════

__all__ = [
    # Constants
    "CII_TABLE", "MP_TOTAL_TRANSACTION_PCT", "GRANDFATHERING_CUTOFF",
    # Enums
    "PropertyType", "SaleAssetType", "TaxpayerType", "FamilyMember",
    # Result dataclasses
    "StampDutyResult", "CapitalGainsResult", "Section50CResult",
    "ExemptionRecommendation", "ExemptionOption",
    "RentalIncomeResult", "REITIncomeResult", "TDSResult",
    "BuyVsREITResult", "PropertyHolding", "AgriLandClassification",
    # Functions
    "calculate_stamp_duty",
    "calculate_property_capital_gains",
    "check_section_50c",
    "recommend_capital_gains_exemption",
    "calculate_rental_income_tax",
    "classify_reit_income",
    "calculate_property_purchase_tds",
    "calculate_rental_tds_individual",
    "calculate_rental_tds_commercial",
    "compare_buy_vs_reit",
    "classify_agricultural_land_bhopal",
    "PropertyHoldingsRegistry",
    # Utilities
    "fy_from_date", "months_between", "get_cii", "inr",
]
