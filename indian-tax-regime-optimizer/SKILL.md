---
name: indian-tax-regime-optimizer
description: "Use this skill whenever an Indian taxpayer asks about old vs new tax regime, which regime saves more money, deduction caps, or tax computation for FY 2025-26 / AY 2026-27. Triggers include: 'old vs new regime', 'which tax regime', 'should I switch regime', 'how much tax do I save', '80C', '80CCD', '80D', '80TTB', '87A rebate', 'senior citizen tax', 'super senior tax', 'standard deduction', 'tax slabs India', 'Form 10-IEA', 'compute Indian income tax'. ALSO trigger proactively when an Indian salary or income figure appears in conversation and the user is making any financial decision — regime choice is upstream of almost every tax planning question in India. Computes both regimes side-by-side, enforces statutory caps (80C ₹1.5L, 80CCD(1B) ₹50K, 80D age-based, 80TTB ₹50K senior-only), handles general/senior 60-79/super-senior 80+ slabs separately, applies Section 87A rebates (₹60K new regime up to ₹12L, ₹12,500 old regime up to ₹5L), and adds 4% cess. NOT for foreign-source income tax (use lrs-foreign-investment-tax). NOT for capital gains on property or MF (use indian-real-estate-bhopal or indian-mutual-fund-tax)."
---

# Indian Tax Regime Optimizer

You compute Indian income tax under both the old and new regimes for FY 2025-26 (Assessment Year 2026-27) and recommend the optimal one for the user.

## Verified against (May 2026)

- Finance (No.2) Act 2024
- Finance Act 2025
- Income Tax Act Sections 87A, 80C, 80CCD, 80D, 80TTB, 24(b)
- Re-verify each February after the Union Budget

## Step 0: Decide if this skill applies

Apply when the user asks about Indian personal income tax computation, regime choice, or tax planning that depends on regime. Skip if the question is purely about capital gains (property, MF) or foreign-source income.

If the question involves regime choice AND another tax topic (e.g., "which regime if I'm selling property?"), use this skill alongside the relevant capital-gains skill.

## Step 1: Gather inputs

You need:
1. **Gross income (₹/year)** — salary + pension + interest + other taxable income (excludes capital gains, computed separately)
2. **Age** — drives slab selection in old regime
3. **Deductions claimed** — for old regime:
   - 80C contributions (PPF, ELSS, EPF, life insurance, home loan principal, etc.) — cap ₹1,50,000
   - 80CCD(1B) extra NPS — cap ₹50,000 over and above 80C
   - 80D health insurance — self ₹25K (₹50K if senior), parents ₹25K (₹50K if parents senior)
   - 80TTB savings/FD interest — cap ₹50,000, **seniors 60+ only**, **OLD REGIME ONLY**
   - 80TTA savings interest — cap ₹10,000, **non-seniors only**, **OLD REGIME ONLY**
   - 24(b) home loan interest — ₹2L cap for self-occupied, unlimited for let-out
   - Employer 80CCD(2) NPS contribution — available in both regimes

If the user gives partial info, compute what you can and flag what's missing.

## Step 2: Run the calculator

Use `scripts/tax_optimizer.py` to compute both regimes. The skill enforces statutory caps automatically and flags overages.

```python
from scripts.tax_optimizer import DeductionBreakdown, compare_regimes

result = compare_regimes(
    gross_income=15_00_000,
    deductions=DeductionBreakdown(
        sec_80c=1_50_000,
        sec_80ccd_1b=50_000,
        sec_80d_self=25_000,
        sec_80d_parents=50_000,  # senior parents
    ),
    age=53,
)

# result.recommended_regime → "new" or "old"
# result.tax_saved → ₹ saved by choosing the optimal regime
# result.old_result.deduction_overages → dict of caps exceeded
```

## Step 3: Present the answer

Structure the output:

1. **Headline:** "NEW regime saves you ₹X,XXX/year" (or OLD)
2. **Side-by-side:**
   - Old regime tax + breakdown of deductions actually applied (with cap enforcement)
   - New regime tax + standard deduction only
3. **Why this regime wins** — explain the deciding factor (e.g., "your ₹60K rebate covers all tax up to ₹12L taxable income; you don't need the deductions you'd claim in old regime")
4. **How to declare:**
   - New regime: default since FY 2023-24. Salaried: declare to employer at FY start for correct TDS. Otherwise auto-applied at ITR filing.
   - Old regime (if you want to opt back): file **Form 10-IEA** before due date. Once switched out, ability to return is limited (one-time switchback for non-business income).

## Critical rules (high-stakes errors to avoid)

| Rule | Why it matters |
|---|---|
| **80TTB is OLD regime + senior only** | Frequently mis-claimed in new regime — gets disallowed at ITR, with interest and penalty |
| **80CCD(1B) is OVER AND ABOVE 80C** | Not part of the ₹1.5L cap — many users miss this ₹50K extra deduction |
| **Standard deduction is ₹75,000 (raised from ₹50K in Budget 2024)** | Old library code and older tools still show ₹50K |
| **Section 87A rebate threshold is ₹12L in NEW regime** | If taxable income ≤ ₹12L, total tax = ₹0 (rebate capped at ₹60K). Old regime threshold stays ₹5L with ₹12,500 cap |
| **New regime uses SAME slabs for all ages** | Senior/super-senior age-based slab benefits only exist in OLD regime |
| **Cess is 4% on tax post-rebate** | Don't forget to add this — it applies to both regimes |

## Slab reference (FY 2025-26)

### New regime (all ages):
- 0–4L: 0%
- 4–8L: 5%
- 8–12L: 10%
- 12–16L: 15%
- 16–20L: 20%
- 20–24L: 25%
- 24L+: 30%

### Old regime — general (under 60):
- 0–2.5L: 0% | 2.5–5L: 5% | 5–10L: 20% | 10L+: 30%

### Old regime — senior (60–79):
- 0–3L: 0% | 3–5L: 5% | 5–10L: 20% | 10L+: 30%

### Old regime — super-senior (80+):
- 0–5L: 0% | 5–10L: 20% | 10L+: 30%

## When new regime usually wins

- Total deductions < ₹4 lakh
- Income ≤ ₹12 lakh (₹60K rebate eliminates all tax)
- No home loan interest claim
- Younger taxpayers with limited 80D

## When old regime can still win

- Home loan interest > ₹2 lakh + 80C maxed
- Senior with ₹50K 80TTB + ₹50K 80D (parents) + 80C
- High HRA exemption + LTA + 80C + 80D
- Combined deductions ≥ ₹4.5L at income above ₹15L

In practice, for FY 2025-26 most middle-income families with one source of income are better off in NEW regime — but never assume. Always run both.
