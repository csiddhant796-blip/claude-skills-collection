---
name: lrs-foreign-investment-tax
description: "Use this skill whenever an Indian resident asks about investing abroad, LRS remittances, foreign equity taxation, US/Japan/Singapore brokerage accounts, DTAA credits, or related compliance. Triggers include: 'LRS', 'Liberalised Remittance Scheme', 'invest in US stocks from India', 'buy VTI from India', 'foreign brokerage', 'Interactive Brokers India', 'Charles Schwab India', 'TCS on foreign remittance', 'TCS refund', 'Section 206C(1G)', 'DTAA', 'double taxation', 'Form 67', 'foreign tax credit', 'US dividend withholding 25%', 'W-8BEN', 'Schedule FA', 'foreign assets disclosure', 'Section 112 LTCG foreign stock', 'capital gains on US ETF', 'Japan stocks tax India', 'TRC', 'foreign income tax India', 'overseas investment'. ALSO trigger when user mentions ANY non-Indian equity holding or asks about diversifying internationally. Computes: TCS on LRS remittance (20% above ₹10L per FY, refundable via ITR), DTAA dividend withholding lookup for 8 countries, Form 67 foreign tax credit math (FTC = lower of foreign WHT or Indian tax — Rule 128), Section 112 LTCG on foreign stocks (12.5% after 24 months post Budget 2024), Schedule FA compliance reminders."
---

# LRS / Foreign Investment Tax

You handle the tax + compliance side of Indian residents investing in foreign equity — US ETFs, Japan stocks, Singapore REITs, and so on. Three skills bundle here: LRS TCS, DTAA + Form 67, and foreign capital gains.

## Verified against (May 2026)

- Finance Act 2023 (raised LRS TCS to 20% above ₹7L initially, then ₹10L post Budget 2025)
- Finance Act 2025 (TCS threshold raised from ₹7L to ₹10L)
- Finance (No.2) Act 2024 (foreign stock LTCG holding 36 → 24 months, rate 20% → 12.5%)
- Income Tax Rule 128 (Form 67 foreign tax credit)
- Income Tax Act Sections 112, 206C(1G), 90, 91
- Schedule FA disclosure requirement (any foreign asset, including bank accounts)
- DTAA agreements with USA (1989, amended 1994), Japan, Singapore, UK, Korea, Taiwan, Australia, Saudi Arabia
- Re-verify each February post-Budget

## Module 1: TCS calculator (Section 206C(1G))

LRS = Liberalised Remittance Scheme = the ₹2.5cr per person per FY cap on outbound remittances. Authorised Dealer banks (HDFC, ICICI, etc.) must collect TCS at source.

| Purpose category | TCS rate | Threshold |
|---|---|---|
| Investment / general | **20%** | Above ₹10L/FY |
| Education (loan-funded) | 0.5% | Above ₹7L/FY |
| Education (self-funded) | 5% | Above ₹7L/FY |
| Medical | 5% | Above ₹7L/FY |
| Tour package | 5% then 20% | Tiered |

```python
from scripts.tcs_calculator import calculate_tcs

r = calculate_tcs(amount_inr=15_00_000, purpose="investment", fy="2025-26")
# r["tcs_amount_inr"] → 100_000 (20% on portion above ₹10L)
# r["net_remittance_inr"] → 14_00_000
# r["is_refundable"] → True (claim via Schedule TCS in ITR-2/3)
```

**TCS is REFUNDABLE.** If the user's actual tax liability is lower than total TCS deducted across all remittances, the excess is refunded with ITR. Many users panic-avoid LRS because of TCS — explain this clearly.

## Module 2: DTAA lookup + Form 67 credit

When the user receives foreign dividends or capital gains, foreign WHT is withheld at source. India lets them claim foreign tax credit (FTC) under Section 90/91, capped at the Indian tax liability on that income (Rule 128).

### DTAA dividend WHT rates (verify with current DTAA text):

| Country | Portfolio dividend WHT |
|---|---|
| USA | 25% |
| Japan | 10% |
| Singapore | 10% / 15% |
| UK | 10% / 15% |
| Korea | 15% |
| Taiwan | 12.5% |
| Australia | 15% |
| Saudi Arabia | 5% |

### Form 67 math

```python
from scripts.dtaa_lookup import compute_dtaa_credit

c = compute_dtaa_credit(
    country="USA",
    dividend_usd=100,
    indian_slab_pct=30,
    usd_inr=95,
)
# c["dividend_inr"] = 9500
# c["foreign_wht_paid_inr"] = 2375  (25% × 9500)
# c["indian_tax_on_dividend_inr"] = 2850  (30% × 9500)
# c["ftc_claimable_via_form67_inr"] = 2375  (min of WHT and Indian tax)
# c["net_indian_tax_payable_inr"] = 475  (2850 - 2375)
# c["irrecoverable_wht_inr"] = 0
```

### The IRRECOVERABLE WHT trap

If foreign WHT > Indian tax on that income, the excess is LOST. FTC carry-forward is NOT allowed under Rule 128. Common for:
- US dividends (25% WHT) when Indian slab is 20% → 5pp loss
- Mid-rate WHT countries with low-slab Indian investors

```python
# 20% slab investor, $1000 US dividend
c = compute_dtaa_credit("USA", dividend_usd=1000, indian_slab_pct=20, usd_inr=95)
# c["irrecoverable_wht_inr"] = ₹4,750 — permanently lost
```

When this triggers, recommend:
1. Hold US ETFs (e.g., VTI) in entities where lower WHT applies, OR
2. Prefer accumulating (re-investing) funds where possible, OR
3. Choose Japan/UK over US for dividend-heavy strategies

### Form 67 filing requirements

- **Mandatory** if claiming FTC
- File **before ITR submission** (deadline aligned with ITR)
- Supporting documents required: Form 1042-S (US), Tax Residency Certificate (Form 10FB for Indian residency), SBI TTBR rate (for INR conversion), broker statement
- Rule 128 strict — missing Form 67 means FTC is disallowed entirely

## Module 3: Foreign capital gains (Section 112)

Budget 2024 simplified this:

| Holding period | Tax treatment |
|---|---|
| ≥ 24 months | **LTCG @ 12.5%** (no indexation) — Section 112 |
| < 24 months | STCG @ slab rate |

The 24-month threshold (down from 36) applies to BOTH listed and unlisted foreign securities.

```python
from scripts.capital_gains_calculator import calc_gains_tax

r = calc_gains_tax(
    asset_type="foreign_stock",
    buy_price_usd=100,
    sell_price_usd=150,
    qty=10,
    holding_days=800,  # >24 months
    slab_rate_pct=30,
    usd_inr=95,
)
# Returns: gain in USD/INR, tax computed, holding period flag, LTCG/STCG classification
```

**Cost computation:**
- Cost = USD purchase × FBIL/SBI TTBR rate on purchase date
- Sale = USD sale × FBIL/SBI TTBR rate on sale date
- Gain in INR = sale − cost (no indexation post Budget 2024)

## Module 4: Schedule FA (mandatory disclosure)

Every Indian resident with ANY foreign asset (even one share, even one bank account with $1) must file Schedule FA with ITR-2 or ITR-3. Failure → ₹10 lakh penalty under Black Money Act (yes, ₹10L).

Disclose:
- Foreign bank accounts (account number, opening balance, peak balance, interest)
- Foreign equity (broker, country, opening shares, peak value, dividend received)
- Foreign immovable property
- Foreign trusts / beneficiary interests
- Any signing authority over foreign accounts

**Reporting cutoff:** assets held at any point during the calendar year preceding the FY. So for ITR for FY 2025-26 (AY 2026-27), report assets held during Jan-Dec 2025.

## Step-by-step user journey (most common case)

User: "I want to invest in US stocks from India. What do I need to know?"

1. **Choose broker.** Two routes: (a) US-based broker (Interactive Brokers, Charles Schwab Global Account, Vested) directly with LRS, or (b) Indian fintechs that pool LRS (Indmoney, Groww, Stockal). Direct brokers usually better for lower fees.
2. **Open brokerage account.** W-8BEN form for US brokers (3-year validity) to get DTAA rate, not the higher 30% non-treaty rate.
3. **Initial remittance.** Bank LRS form, Schedule TCS at deposit. First ₹10L/FY = no TCS. Above = 20% TCS, refundable.
4. **Investing.** Buy stocks/ETFs. Hold periods matter for cap gains.
5. **Dividends.** US WHT (25%) deducted automatically. Keep Form 1042-S.
6. **Annual ITR.** File Schedule FA (mandatory). Claim FTC via Form 67. Report cap gains in Schedule CG.

## Critical compliance reminders

- **Schedule FA is non-negotiable.** ₹10L penalty per year of omission under Black Money Act.
- **W-8BEN must be valid.** Expires every 3 years. If lapsed, US broker withholds at 30% (non-treaty rate) — extra 5pp lost permanently.
- **Form 67 before ITR filing.** Not after. Rule 128 strict.
- **TCS is refundable but creates cash-flow drag.** Plan large remittances early in FY so refund comes in same year as receipt.

## When NOT to use this skill

- Pure Indian holdings → use `indian-mutual-fund-tax` or `indian-tax-regime-optimizer`
- Foreign real estate → DTAA still applies but the property-specific tax rules differ; combine with `indian-real-estate-bhopal` only for the LTCG rate logic

## Honesty about gaps

- The DTAA rates here are for **portfolio investments**. Treaty rates for corporate cross-holdings (>10% ownership) are usually lower. Flag this if user is investing in a substantial stake.
- The `live_data_fetcher` skill can pull FBIL USD/INR for current-date conversion, but historical FBIL rates may need manual lookup.
- Multi-leg DTAA + Singapore-routing structures are out of scope. That's tax-counsel territory.
