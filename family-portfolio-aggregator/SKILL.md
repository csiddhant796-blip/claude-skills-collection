---
name: family-portfolio-aggregator
description: "Use this skill whenever someone wants to consolidate, review, or rebalance a multi-member household investment portfolio. Triggers include: 'family portfolio', 'household net worth', 'consolidated investment view', 'portfolio rollup', 'asset allocation drift', 'rebalance my family', 'overall portfolio across family', 'father's + mother's + my investments together', 'spouse and I combined portfolio', 'review our investments', 'asset class breakdown', 'concentration risk', 'too much in one asset', 'how much equity vs debt'. ALSO trigger when the user describes holdings across multiple people in the same household and asks any 'should we' / 'how are we doing' question. Computes: per-member portfolio totals, asset allocation by class (Indian equity, foreign equity, debt, gold, real estate, REIT, cash), drift detection against age-appropriate target allocations, single-holding concentration warnings (any holding > 25% of family NW), and annual income projection per member. Designed for typical 2-3 member Indian families (parents + adult child), with target allocations that adjust by age."
---

# Family Portfolio Aggregator

You build a unified, per-member portfolio view for a multi-generation Indian family and surface allocation drift, concentration risk, and rebalancing actions.

## When this skill matters

Most personal finance tools track ONE person's portfolio. Indian families operate as economic units — parents' retirement income depends partly on the working child, the child's emergency fund may be partly the parents' liquid savings, and asset allocation needs to be age-appropriate per member but coordinated as a whole.

This skill is the consolidation layer.

## Step 1: Inventory holdings per member

For each family member, collect:
- **Member identity**: name and age
- **Holdings list**: each holding has `asset_class`, `instrument`, `purchase_date`, `purchase_price`, `current_value`, `annual_income`
- **Real estate**: tracked separately via the real-estate registry (use `indian-real-estate-bhopal` skill)

Asset classes the skill supports:
1. `indian_equity` — direct stocks + Indian equity MFs
2. `foreign_equity` — US/Japan/etc. via LRS
3. `indian_debt` — SCSS, PPF, NPS-G, FRSB, G-Sec, FDs
4. `gold` — ETF, physical, SGB grandfathered
5. `real_estate` — direct property
6. `reit` — listed REITs (Embassy, Mindspace, Brookfield, etc.)
7. `cash` — savings, liquid funds, emergency fund

## Step 2: Build the aggregator

```python
from scripts.portfolio_aggregator import (
    PortfolioAggregator, GenericHolding, AssetClass, FamilyMember
)
from datetime import date

agg = PortfolioAggregator()

agg.add_holding(GenericHolding(
    holding_id="father_scss_001",
    member=FamilyMember.FATHER,
    asset_class=AssetClass.INDIAN_DEBT,
    instrument="SCSS @ 8.20%",
    purchase_date=date(2025, 4, 1),
    purchase_price=30_00_000,
    current_value=30_00_000,
    annual_income=2_46_000,
))
# ... add all holdings per member
```

For real estate, use `add_property()` with a `PropertyHolding` instance from the real-estate skill.

## Step 3: Per-member snapshot

```python
snap = agg.member_snapshot(FamilyMember.FATHER)
# snap.total_value
# snap.actual_allocation     → dict[AssetClass, ₹]
# snap.actual_allocation_pct → dict[AssetClass, %]
# snap.target_allocation_pct → dict[AssetClass, %]
# snap.drift_pct             → dict[AssetClass, drift]
# snap.drift_flags           → "BELOW" / "OK" / "ABOVE" / "N/A"
# snap.annual_income
# snap.warnings              → list of concentration warnings
```

## Step 4: Default target allocations (age-based)

The skill ships with reasonable defaults — adjust per family if circumstances differ:

### Retiree / pensioner (Father 60+)
- Indian equity 15% | Foreign equity 5% | Indian debt 55% | Gold 7% | REIT 7% | Cash 10%
- Real estate excluded from allocation (primary residence is consumption, not investment)

### Pre-retirement (Mother 50-59)
- Indian equity 40% | Foreign equity 13% | Indian debt 30% | Gold 7% | REIT 10% | Cash 5%

### Early career (Sid 20-30)
- Indian equity 55% | Foreign equity 22% | Indian debt 8% | Gold 5% | REIT 3% | Cash 5%

These are **starting points**, not gospel. Adjust if:
- Family has high real estate concentration → lower other allocations
- Member is the sole earner → push more conservative
- Specific goals near-term (Sid's home purchase in 3 years) → boost cash + debt

## Step 5: Drift detection

A class is flagged as:
- **ABOVE** if actual > 1.5 × target (e.g., target 8%, actual 13% → flag)
- **BELOW** if actual < 0.5 × target (e.g., target 22%, actual 9% → flag)
- **OK** otherwise

```python
fam = agg.family_snapshot()
for member, sub in fam.members.items():
    print(f"{member.value}: ₹{sub.total_value:,}")
    for ac, flag in sub.drift_flags.items():
        if flag in ("ABOVE", "BELOW"):
            print(f"  {ac.value}: {flag}")
```

## Step 6: Concentration warnings

Family-level rule: any single instrument > 25% of family net worth gets flagged. This catches:
- One property dominating family NW (typical Indian household — flag it for discussion, not action)
- A single stock holding from RSU/ESOP
- Over-concentration in one mutual fund

## Step 7: Output structure

When presenting a family review, follow this structure:

1. **Family headline:** total NW, count per member, % of family per person
2. **Per-member breakdown:**
   - Total value
   - Allocation table (class | actual ₹ | actual % | target % | drift % | flag)
   - Annual income from holdings
   - Specific drift warnings
3. **Family-level concentration warnings**
4. **Action items per member** (prioritized: tax planning, rebalancing, gaps)

## Coordination with other skills

This skill is the integration point. It uses outputs from:
- `indian-tax-regime-optimizer` (for per-member regime decisions)
- `indian-real-estate-bhopal` (for property holdings)
- `senior-citizen-savings-scheme` (for SCSS in Father's debt allocation)
- `indian-mutual-fund-tax` (for MF holdings)
- `lrs-foreign-investment-tax` (for foreign equity)

When the user asks a question that spans multiple skills (e.g., "should we sell the home and put it in MFs?"), this skill orchestrates the analysis across all of them.

## When NOT to use this skill

- Single-person portfolio with no family complication → use individual planning skills directly
- Net worth calculation only, no rebalancing question → simpler aggregation suffices
- Estate planning / inheritance — that's a different specialty (Wills Act, HSA, joint family vs HUF) and this skill doesn't handle it

## Limitations to flag upfront

- **No live price refresh.** `current_value` must be updated manually. The skill is a snapshot tool, not a market-data feed.
- **Target allocations are heuristics**, not gospel. Override per family circumstances.
- **Doesn't model joint accounts.** Each holding is owned by one member. If genuine joint ownership matters for tax (e.g., who gets credited for interest), record under the primary holder and add a note.
- **Real estate primary residence is excluded from target % math** by design — it's consumption, not portfolio. But it IS counted in family net worth.
