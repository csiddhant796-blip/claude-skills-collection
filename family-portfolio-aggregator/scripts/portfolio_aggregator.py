"""
portfolio_aggregator.py — Unified family portfolio across all asset classes

Pulls holdings from each skill (real estate, SCSS, MFs, gold, REITs, FDs, NPS, PPF)
and produces a consolidated per-member portfolio view with:
  - Total net worth by member
  - Asset allocation breakdown (vs. target weights)
  - Drift flags (where actual > 1.5x target or < 0.5x)
  - Annual cash flow projection
  - Currency exposure (₹ vs USD)
  - Concentration risk metrics
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional

# Import from sibling skills (real estate registry already provides PropertyHolding)
from real_estate_tracker import (
    PropertyHolding, PropertyHoldingsRegistry, FamilyMember, PropertyType, inr,
)


# ─── ENUMS ─────────────────────────────────────────────────────
class AssetClass(str, Enum):
    INDIAN_EQUITY = "indian_equity"           # Direct stocks + equity MFs
    FOREIGN_EQUITY = "foreign_equity"          # US/Japan/etc. (LRS route)
    INDIAN_DEBT = "indian_debt"                # SCSS, FD, PPF, NPS-G, FRSB, G-Sec
    GOLD = "gold"                              # ETF or physical or grandfathered SGB
    REAL_ESTATE = "real_estate"                # Direct property
    REIT = "reit"                              # Listed REITs
    CASH = "cash"                              # Liquid funds, savings, emergency


# ─── TARGET ALLOCATIONS (from research) ────────────────────────
TARGET_ALLOCATIONS = {
    FamilyMember.FATHER: {
        AssetClass.INDIAN_EQUITY:  0.15,  # 15-20%
        AssetClass.FOREIGN_EQUITY: 0.05,  # 5%
        AssetClass.INDIAN_DEBT:    0.55,  # 50-55%
        AssetClass.GOLD:           0.07,  # 5-8%
        AssetClass.REAL_ESTATE:    0.00,  # Existing residence — not "invested"
        AssetClass.REIT:           0.07,  # 5-8%
        AssetClass.CASH:           0.10,  # 5-10%
    },
    FamilyMember.MOTHER: {
        AssetClass.INDIAN_EQUITY:  0.40,
        AssetClass.FOREIGN_EQUITY: 0.13,
        AssetClass.INDIAN_DEBT:    0.30,
        AssetClass.GOLD:           0.07,
        AssetClass.REAL_ESTATE:    0.00,
        AssetClass.REIT:           0.10,
        AssetClass.CASH:           0.05,
    },
    FamilyMember.SID: {
        AssetClass.INDIAN_EQUITY:  0.55,
        AssetClass.FOREIGN_EQUITY: 0.22,
        AssetClass.INDIAN_DEBT:    0.08,
        AssetClass.GOLD:           0.05,
        AssetClass.REAL_ESTATE:    0.00,
        AssetClass.REIT:           0.03,
        AssetClass.CASH:           0.05,
    },
}


# ─── DATACLASSES ───────────────────────────────────────────────
@dataclass
class GenericHolding:
    """Generic non-real-estate holding."""
    holding_id: str
    member: FamilyMember
    asset_class: AssetClass
    instrument: str  # Free-text: "SBI BlueChip", "SCSS", "RBI FRSB", etc.
    purchase_date: date
    purchase_price: float
    current_value: float
    annual_income: float = 0  # Dividend, interest, rent
    notes: str = ""


@dataclass
class MemberPortfolioSnapshot:
    member: FamilyMember
    total_value: float
    actual_allocation: dict[AssetClass, float]  # Class → ₹
    actual_allocation_pct: dict[AssetClass, float]  # Class → %
    target_allocation_pct: dict[AssetClass, float]
    drift_pct: dict[AssetClass, float]  # actual - target
    drift_flags: dict[AssetClass, str]  # "BELOW" / "OK" / "ABOVE"
    annual_income: float
    holdings_count: int
    warnings: list[str] = field(default_factory=list)


@dataclass
class FamilyPortfolioSnapshot:
    snapshot_date: date
    members: dict[FamilyMember, MemberPortfolioSnapshot]
    total_net_worth: float
    concentration_warnings: list[str] = field(default_factory=list)


# ─── PORTFOLIO AGGREGATOR ──────────────────────────────────────
class PortfolioAggregator:
    """
    Combines:
      - PropertyHoldingsRegistry (real estate)
      - GenericHolding list (all non-real-estate)
    
    Produces unified per-member and family-level snapshots.
    """

    def __init__(self, real_estate_registry: Optional[PropertyHoldingsRegistry] = None):
        self.real_estate = real_estate_registry or PropertyHoldingsRegistry()
        self.holdings: list[GenericHolding] = []

    def add_holding(self, h: GenericHolding) -> None:
        if any(x.holding_id == h.holding_id for x in self.holdings):
            raise ValueError(f"Holding ID {h.holding_id} already exists")
        self.holdings.append(h)

    def add_property(self, h: PropertyHolding) -> None:
        self.real_estate.add(h)

    def _holdings_for_member(self, member: FamilyMember) -> list[GenericHolding]:
        return [h for h in self.holdings if h.member == member]

    def member_snapshot(self, member: FamilyMember) -> MemberPortfolioSnapshot:
        """Compute snapshot for one member."""
        generic = self._holdings_for_member(member)
        properties = self.real_estate.by_member(member)

        # Aggregate by asset class
        actual = {ac: 0.0 for ac in AssetClass}
        for h in generic:
            actual[h.asset_class] += h.current_value

        # Real estate: split between REAL_ESTATE and REIT based on property type
        for p in properties:
            val = p.current_estimated_value or p.purchase_price
            if p.property_type == PropertyType.REIT:
                actual[AssetClass.REIT] += val
            else:
                actual[AssetClass.REAL_ESTATE] += val

        total = sum(actual.values())
        actual_pct = {ac: (v / total if total > 0 else 0) for ac, v in actual.items()}

        target_pct = TARGET_ALLOCATIONS.get(member, {})
        drift_pct = {ac: actual_pct[ac] - target_pct.get(ac, 0) for ac in AssetClass}

        # Drift flags
        flags = {}
        for ac in AssetClass:
            tgt = target_pct.get(ac, 0)
            act = actual_pct[ac]
            if tgt == 0:
                flags[ac] = "N/A"
            elif act > 1.5 * tgt:
                flags[ac] = "ABOVE"
            elif act < 0.5 * tgt:
                flags[ac] = "BELOW"
            else:
                flags[ac] = "OK"

        # Annual income
        annual_income = sum(h.annual_income for h in generic)
        annual_income += sum(p.annual_rent_income for p in properties if p.is_let_out)

        warnings = []
        if total == 0:
            warnings.append(f"No holdings registered for {member.value}")
        for ac, flag in flags.items():
            if flag == "ABOVE":
                warnings.append(
                    f"⚠️ {ac.value} concentration: {actual_pct[ac]*100:.1f}% vs target {target_pct.get(ac, 0)*100:.1f}%"
                )

        return MemberPortfolioSnapshot(
            member=member,
            total_value=total,
            actual_allocation=actual,
            actual_allocation_pct=actual_pct,
            target_allocation_pct=target_pct,
            drift_pct=drift_pct,
            drift_flags=flags,
            annual_income=annual_income,
            holdings_count=len(generic) + len(properties),
            warnings=warnings,
        )

    def family_snapshot(self, as_of_date: Optional[date] = None) -> FamilyPortfolioSnapshot:
        """Compute snapshot across all family members."""
        if as_of_date is None:
            as_of_date = date.today()

        members = {m: self.member_snapshot(m) for m in FamilyMember}
        total_nw = sum(s.total_value for s in members.values())

        concentration = []
        # Check single-instrument concentration
        all_holdings = [(h.instrument, h.current_value) for h in self.holdings]
        all_holdings += [(p.location or p.holding_id, p.current_estimated_value or p.purchase_price)
                         for p in self.real_estate.holdings]
        for instrument, val in all_holdings:
            if total_nw > 0 and val / total_nw > 0.25:
                concentration.append(
                    f"⚠️ Single holding {instrument} is {val/total_nw*100:.1f}% of family net worth"
                )

        return FamilyPortfolioSnapshot(
            snapshot_date=as_of_date,
            members=members,
            total_net_worth=total_nw,
            concentration_warnings=concentration,
        )

    def print_member_summary(self, member: FamilyMember) -> None:
        """Pretty-print a member's snapshot."""
        s = self.member_snapshot(member)
        print(f"\n{'═' * 72}")
        print(f"  {member.value.upper()} — Portfolio Snapshot")
        print('═' * 72)
        print(f"  Total value:    {inr(s.total_value)}")
        print(f"  Annual income:  {inr(s.annual_income)}")
        print(f"  Holdings:       {s.holdings_count}")

        print(f"\n  {'Asset Class':<22}{'Value':>16}{'Actual':>10}{'Target':>10}{'Drift':>10}  Flag")
        print(f"  {'-' * 22}{'-' * 16}{'-' * 10}{'-' * 10}{'-' * 10}  {'-' * 6}")
        for ac in AssetClass:
            v = s.actual_allocation[ac]
            ap = s.actual_allocation_pct[ac] * 100
            tp = s.target_allocation_pct.get(ac, 0) * 100
            dp = s.drift_pct[ac] * 100
            fl = s.drift_flags[ac]
            print(f"  {ac.value:<22}{inr(v):>16}{ap:>9.1f}%{tp:>9.1f}%{dp:>+9.1f}%  {fl}")

        if s.warnings:
            print(f"\n  Warnings:")
            for w in s.warnings:
                print(f"    {w}")

    def print_family_summary(self) -> None:
        """Pretty-print family-level snapshot."""
        snap = self.family_snapshot()
        print(f"\n{'═' * 72}")
        print(f"  FAMILY PORTFOLIO SNAPSHOT — {snap.snapshot_date.isoformat()}")
        print('═' * 72)
        print(f"  Total family net worth: {inr(snap.total_net_worth)}")
        for member, sub in snap.members.items():
            pct = (sub.total_value / snap.total_net_worth * 100) if snap.total_net_worth > 0 else 0
            print(f"    {member.value:<10} {inr(sub.total_value):>16}  ({pct:.1f}% of family)")

        if snap.concentration_warnings:
            print(f"\n  Family-level concentration risks:")
            for w in snap.concentration_warnings:
                print(f"    {w}")


__all__ = [
    "AssetClass", "GenericHolding",
    "MemberPortfolioSnapshot", "FamilyPortfolioSnapshot",
    "PortfolioAggregator", "TARGET_ALLOCATIONS",
]
