---
name: indian-mutual-fund-tax
description: "Use this skill whenever an Indian investor asks about mutual fund taxation, capital gains on MFs, ELSS lock-in, or debt MF tax treatment. Triggers include: 'mutual fund tax', 'equity MF LTCG', 'debt fund tax', 'Section 50AA', 'ELSS lock-in', 'SIP lock-in', 'when can I redeem ELSS', 'hybrid fund taxation', '65% equity threshold', 'arbitrage fund tax', 'gold MF vs gold ETF', 'international FoF tax', 'liquid fund tax', 'short-term capital gains MF', 'long-term capital gains MF', '₹1.25 lakh exemption', 'grandfathered debt MF', 'MF FoF taxation'. CRITICAL: ALSO trigger PROACTIVELY whenever a user mentions buying or holding a debt MF, gold MF, international FoF, or conservative hybrid purchased AFTER 1 April 2023 — these fall into the Section 50AA trap (slab-rate taxation on ALL gains, no LTCG benefit, no indexation). The user usually doesn't know about this and the skill must surface it. Computes: equity LTCG (12.5% above ₹1.25L/year), Section 50AA debt trap detection, ELSS per-SIP lock-in tracking (36 months per installment), hybrid fund classification using 65% equity threshold, grandfathering for pre-April-2023 debt MF units."
---

# Indian Mutual Fund Tax Calculator

You handle Indian mutual fund taxation with special focus on the Section 50AA debt-MF trap — a 2023 rule that catches many investors unaware.

## Verified against (May 2026)

- Finance (No.2) Act 2024 (changed equity LTCG rate, STCG rate, exemption threshold)
- Finance Act 2023 (introduced Section 50AA effective 1 April 2023)
- Income Tax Act Sections 111A, 112A, 50AA
- Re-verify each February post-Budget

## Step 1: Identify the fund category

This drives everything. Map the fund to one category:

| Category | Tax treatment |
|---|---|
| Equity large/mid/small/flexi/index cap | Equity LTCG/STCG |
| ELSS | Equity LTCG/STCG (with 36-mo lock-in per SIP) |
| Arbitrage funds | Equity LTCG/STCG (treated as equity) |
| Hybrid Aggressive (>65% equity) | Equity LTCG/STCG |
| Hybrid Conservative (<65% equity) | Debt — Section 50AA if bought post Apr 2023 |
| Debt liquid / short-duration / long-duration / corporate bond | Debt — Section 50AA if bought post Apr 2023 |
| Gold ETF (listed) | Equity-like: 12.5% LTCG after 12 months |
| Gold MF FoF | **Section 50AA trap** — avoid |
| International FoF | Section 50AA |

## Step 2: The Section 50AA trap (most important)

Effective **1 April 2023**, ANY fund where Indian-domiciled debt component > 65% (or non-equity fund) loses LTCG benefit:
- ALL gains taxed at **slab rate**
- No 12.5% LTCG rate
- No indexation
- Holding period irrelevant

**Grandfathering exception:** Units purchased BEFORE 1 April 2023 retain the old regime:
- LTCG after 36 months: 20% with CII indexation
- STCG before 36 months: slab rate

```python
from scripts.indian_mf_calculator import calculate_mf_tax, MFCategory
from datetime import date

r = calculate_mf_tax(
    purchase_amount=10_00_000,
    purchase_date=date(2024, 1, 1),   # Post-cutoff
    sale_amount=12_00_000,
    sale_date=date(2027, 6, 1),
    category=MFCategory.DEBT_CORPORATE_BOND,
    tax_slab_pct=30,
)
# r.tax_treatment → "section_50aa_slab"
# r.tax_amount → 60_000 (30% on ₹2L gain)
# r.warnings → ["⚠️ Section 50AA applies..."]
```

When Section 50AA applies, **proactively recommend alternatives**:
- G-Sec via RBI Retail Direct (slab on coupon + 12.5% LTCG on capital gain — better)
- Bank FD (predictable, DICGC ₹5L cover, slab interest)
- SCSS for seniors (8.20%, quarterly, 80C-eligible)
- RBI Floating Rate Savings Bonds 2020 (8.05%, FRSB)

## Step 3: Equity MF taxation (post Budget 2024)

| Holding period | Tax |
|---|---|
| < 12 months | **STCG @ 20%** (raised from 15% in Budget 2024) |
| ≥ 12 months | **LTCG @ 12.5%** above ₹1,25,000 exemption per FY |

The ₹1.25L exemption is **shared across all equity LTCG in the FY**:

```python
r = calculate_mf_tax(
    purchase_amount=5_00_000,
    purchase_date=date(2023, 1, 1),
    sale_amount=8_00_000,
    sale_date=date(2026, 6, 1),
    category=MFCategory.EQUITY_LARGE_CAP,
    other_equity_ltcg_in_fy=25_000,  # Already used ₹25K of exemption from another redemption
)
# Remaining exemption: ₹1L
# Taxable gain: ₹3L - ₹1L = ₹2L
# Tax: 12.5% × ₹2L = ₹25,000
```

## Step 4: ELSS lock-in — per-SIP tracking

**This is where most people get it wrong:** ELSS 3-year lock-in is **PER SIP installment**, not from the initial investment.

A monthly SIP from Jan 2024 has 36 separate lock-in expiries through Dec 2026. The first installment unlocks in Jan 2027, the second in Feb 2027, and so on.

```python
from scripts.indian_mf_calculator import check_elss_lockin
from datetime import date

r = check_elss_lockin(
    sip_date=date(2024, 5, 1),
    current_date=date(2026, 5, 22),
    investment_amount=10_000,
)
# r.is_locked_in → True
# r.lockin_expiry_date → date(2027, 5, 1)
# r.days_remaining → 344
```

When advising on ELSS redemption, always:
1. Ask for the SIP start date (or transaction list)
2. Identify which installments are unlocked
3. Note that redeeming locked units triggers a violation — units stay frozen

## Step 5: Hybrid fund 65% threshold

Equity-oriented hybrid = > 65% in Indian-domiciled equity → equity tax rules.

```python
classify_hybrid_fund(equity_allocation_pct=72)
# {is_equity_oriented: True, tax_treatment: "equity (12.5% LTCG above ₹1.25L)"}
```

Common examples:
- **Equity-oriented:** Aggressive Hybrid, most Balanced Advantage Funds (BAF), Equity Savings, Arbitrage
- **Debt-oriented (Section 50AA):** Conservative Hybrid, some Multi-Asset Allocation funds

⚠️ Some BAFs dynamically rebalance equity below 65% — verify the actual reporting on AMFI before assuming equity treatment.

## Step 6: SGB and Gold MF FoF caveats

- **Sovereign Gold Bonds (SGB):** DISCONTINUED since Feb 2024. Existing holders keep all benefits — coupon at 2.5% taxable, capital gains exempt at maturity, premature exit on exchange = 12.5% LTCG after 12 months.
- **Gold ETF (listed):** Treated as equity for LTCG — 12.5% after 12 months. Recommend over Gold MF FoF.
- **Gold MF FoF:** Section 50AA — slab rate on all gains. Avoid.

## Step 7: Presenting tax-treatment answers

Always include:

1. **Tax category** ("equity LTCG", "Section 50AA slab", etc.)
2. **Computed tax** with breakdown (gain → exemption → taxable → rate → tax)
3. **Warnings** specifically flagged by the calculator
4. **Alternative recommendation** if Section 50AA applies
5. **Next-action checklist** (file Form 67 if foreign element, report in Schedule CG, etc.)

## When NOT to use this skill

- Foreign mutual funds — use `lrs-foreign-investment-tax`
- Real estate REITs as units (not MFs) — use `indian-real-estate-bhopal`
- Direct stock investments — equity MF rules don't apply identically; Section 112A has nuanced rules for STT-paid listed equity

## Source citations for code comments

When generating code or explanation that references tax rules, include:
- Section number (e.g., "Section 50AA")
- Effective date (e.g., "from 1 April 2023")
- Verification date ("verified May 2026")

This is high-stakes financial code. Sources matter.
