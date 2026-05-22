---
name: senior-citizen-savings-scheme
description: "Use this skill whenever a senior citizen (60+) or anyone planning retirement income asks about SCSS — Senior Citizen Savings Scheme. Triggers include: 'SCSS', 'Senior Citizen Savings Scheme', 'best investment for parents', 'best income for retired', 'safe investment senior', 'SCSS rate', 'SCSS quarterly interest', 'SCSS vs FD', 'SCSS vs RBI bonds', 'best for father / mother / dad / mom retirement', 'invest for parents', 'quarterly income retirement', 'SCSS extension after 5 years', 'SCSS premature withdrawal', 'SCSS TDS', 'Form 15H', '80TTB', 'Section 80C SCSS'. ALSO trigger proactively when someone mentions a parent's pension, retirement corpus, or asks about 'safe' / 'fixed income' / 'guaranteed return' instruments for someone over 60. Computes: quarterly cashflow at current 8.20% rate (Q1 FY 2026-27), TDS implications with the ₹1L senior threshold from April 2025, 80TTB and 80C deduction eligibility, premature withdrawal penalty schedule (<1yr no interest, 1-2yr 1.5%, 2-5yr 1%), and post-tax yield comparison with FRSB / Post Office TD / bank FD."
---

# Senior Citizen Savings Scheme (SCSS) Planner

You help senior citizens (and their families) plan SCSS deposits — Indian government's safest small-savings vehicle for retirees.

## Verified against (May 2026)

- SB Order 01/2026 (Q1 FY 2026-27 interest rate)
- Finance Act 2025 (TDS senior threshold raised from ₹50K to ₹1L, effective 1 Apr 2025)
- Income Tax Act Sections 80TTB, 80C
- Government Savings Promotion Act
- Re-verify each quarter (rate announced quarterly: 1 Apr / 1 Jul / 1 Oct / 1 Jan)

## Quick reference (memorize these)

| Parameter | Value |
|---|---|
| Current rate (Q1 FY 2026-27) | **8.20%** p.a. |
| Maximum deposit per investor | **₹30 lakh** (raised from ₹15L in Budget 2023) |
| Minimum deposit | ₹1,000 (multiples of ₹1,000) |
| Tenure | 5 years |
| Extension option | 3 more years (one-time, applied within 1 year of maturity) |
| Interest payout | Quarterly (1 Apr, 1 Jul, 1 Oct, 1 Jan) |
| Eligibility | 60+, OR 55+ with VRS, OR 50+ retired defence personnel |
| TDS threshold (senior) | ₹1,00,000 interest/year (raised from ₹50K on 1 Apr 2025) |
| TDS rate | 10% (with PAN) / 20% (without PAN) |
| 80C eligible | ₹1.5 lakh deposit (within shared 80C cap) |
| 80TTB deduction | ₹50,000 max — **OLD REGIME ONLY**, senior 60+ only |

## Step 1: Compute the cashflow

```python
from scripts.scss_planner import calculate_scss_cashflow

cf = calculate_scss_cashflow(deposit_amount=30_00_000)
# cf.annual_interest → ₹2,46,000
# cf.quarterly_payout → ₹61,500
# cf.total_interest_over_tenure → ₹12,30,000
```

For a maxed-out ₹30L deposit at 8.20%:
- ₹2,46,000/year
- ₹61,500/quarter
- ₹12,30,000 total over 5 years
- Principal returned at maturity

## Step 2: Tax implications

```python
from scripts.scss_planner import calculate_scss_tax

tx = calculate_scss_tax(
    deposit_amount=30_00_000,
    other_interest_income=80_000,    # FD interest, savings interest etc.
    is_old_regime=False,             # Check user's regime
    has_pan=True,
)
# tx.tds_applies → True (total ₹3.26L > ₹1L senior threshold)
# tx.tds_amount → ₹24,600 (10% × ₹2.46L)
# tx.section_80ttb_used → ₹0 (not old regime)
```

Three things to flag in any SCSS tax response:

1. **TDS recovery via ITR.** Even if TDS is deducted, the depositor can claim refund in ITR if total income falls below taxable threshold (very common for retirees in NEW regime — total tax often ₹0).

2. **Form 15H to halt TDS.** If estimated total tax = ₹0, submit Form 15H to bank/post office at the start of FY. Saves the cash-flow hassle.

3. **80TTB requires OLD regime.** Many users assume ₹50K 80TTB applies in new regime — it does NOT. The full ₹2.46L SCSS interest is taxable in new regime (recoverable only via ₹60K Section 87A rebate if total taxable income ≤ ₹12L).

## Step 3: Post-tax yield comparison

```python
from scripts.scss_planner import post_tax_yield_comparison
comp = post_tax_yield_comparison(tax_slab_pct=30)
```

At 30% slab:

| Instrument | Pre-tax | Post-tax | Notes |
|---|---|---|---|
| **SCSS** | 8.20% | **5.74%** | Best senior post-tax + 80C + 80TTB |
| RBI FRSB 2020 | 8.05% | 5.63% | 7-year tenure, floating |
| Post Office 5-yr TD | 7.50% | 5.25% | 80C-eligible |
| Bank FD (Senior) | 7.50% | 5.25% | DICGC ₹5L coverage |

**SCSS wins on post-tax yield.** Plus the quarterly payout structure is unmatched for retirees needing predictable income.

## Step 4: Premature withdrawal penalty

| Months held | Penalty |
|---|---|
| < 12 months | **ALL interest paid is recovered** (effectively zero return) |
| 12–24 months | 1.5% of deposit deducted |
| 24–60 months | 1.0% of deposit deducted |
| ≥ 60 months | No penalty (matured) |

```python
from scripts.scss_planner import calculate_scss_premature_withdrawal
from datetime import date

r = calculate_scss_premature_withdrawal(
    deposit_amount=30_00_000,
    deposit_date=date(2025, 4, 1),
    withdrawal_date=date(2027, 10, 1),  # 30 months held
)
# r.penalty_rate_pct → 1.0
# r.penalty_amount → ₹30,000
# r.net_received → deposit + interest - ₹30,000
```

## Step 5: When to recommend SCSS

✅ Recommend SCSS when:
- Investor is 60+ (or 55+ with VRS, or 50+ ex-defence)
- Has lump sum ≥ ₹2-5 lakh available
- Wants safe, government-backed, predictable quarterly income
- Has room within the ₹30L per-investor limit
- Joint account with spouse is fine (limit still applies per investor, not per account)

❌ Don't push SCSS when:
- Investor will likely need the full deposit before 5 years (penalty erodes returns)
- Total interest income would push effective marginal rate above 20% (FRSB or G-Sec via RBI Retail Direct may give better post-tax)
- Investor is under 60 and not VRS/ex-defence (not eligible)

## Step 6: Extension decision (at year 5)

At maturity, the investor can:
1. **Withdraw full principal** — no further penalty
2. **Extend by 3 years** — at the rate prevailing at extension start (not current rate)
3. **Withdraw with penalty after extension** — 1% penalty if exited mid-extension

Extension is usually worth it if rates haven't fallen sharply. Don't extend if rates have dropped >100bps below the original 8.20%.

## Critical warnings

- **PAN required.** Without PAN, TDS is 20% (penalty rate) and refund is harder.
- **SCSS interest is FULLY TAXABLE.** Common misconception that it's tax-free.
- **Joint account doesn't double the limit.** ₹30L is per investor.
- **Nomination is mandatory.** Take care of this at deposit time to avoid succession hassle.

## When NOT to use this skill

- For non-senior investors → use Indian MF / debt instruments instead
- For specifically Mahila Samman Savings Certificate (different scheme)
- For PMVVY — discontinued since March 2023; cannot subscribe new

## Disclaimers (always include)

Rates change quarterly via SB Order notifications. Verify current rate at indiapost.gov.in or with your bank/post office before deposit. The 8.20% rate is for Q1 FY 2026-27; the Q2 rate may differ.
