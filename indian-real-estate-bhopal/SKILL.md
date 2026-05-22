---
name: indian-real-estate-bhopal
description: "Use this skill whenever the user discusses Indian real estate transactions — buying, selling, renting, or analyzing residential, commercial, or agricultural property in India, especially Madhya Pradesh / Bhopal. Triggers include: 'stamp duty', 'property registration', 'capital gains on property', 'indexation', 'grandfathering 23 July 2024', 'Section 50C', 'Section 54 / 54EC / 54F / 54B exemption', 'CII cost inflation index', 'REIT tax', 'agricultural land', 'urban vs rural land', 'Section 2(14)(iii)', 'TDS on property purchase', '194-IA', '194-IB rent TDS', 'rental income tax Section 24', 'SAMPADA portal', 'MP-RERA', 'Bhopal property prices'. ALSO trigger when the user mentions a city in MP (Bhopal, Indore, Jabalpur, Sehore, Vidisha), or when a property transaction value is mentioned alongside any of: 'should I buy', 'should I sell', 'tax planning', 'invest in real estate'. Computes: MP stamp duty (10.5% total), capital gains with grandfathering decision (Path A 12.5% no-index vs Path B 20%+indexation, lower wins for Resident Ind/HUF on pre-23-Jul-2024 acquisitions), Section 50C deemed value check (10% tolerance), exemption recommender (54/54EC/54F/54B), REIT distribution classifier (interest slab, dividend exempt, rental slab, capital repayment untaxed), rental income under Section 24, TDS on purchase (1%) and rent (2% from Oct 2024), Bhopal agricultural land classification (urban if ≤8 km from BMC aerial)."
---

# Indian Real Estate (Bhopal-Focused)

You handle Indian real estate tax planning, transaction cost analysis, and the grandfathering decision that's worth lakhs to most home-sellers.

## Verified against (May 2026)

- Finance (No. 2) Act 2024 (the big one — changed LTCG rates and grandfathering)
- Finance Act 2025
- CBDT FAQ Press Release August 2024 (grandfathering rules clarified)
- Income Tax Act Sections 50AA, 50C, 54, 54B, 54EC, 54F, 24, 112, 194-IA, 194-IB, 194-I, 2(14)(iii)
- SAMPADA 2.0 (sampada.mpigr.gov.in) — MP stamp duty
- SEBI REIT Regulations 2014 + Budget 2024 amendments
- Re-verify each February (post-Budget) and June (post-CII notification)

## Step 1: Identify the scenario

Match the user's question to one or more of these:

| Question type | Use function |
|---|---|
| "How much stamp duty on a ₹X purchase?" | `calculate_stamp_duty()` |
| "What's the capital gains tax if I sell?" | `calculate_property_capital_gains()` |
| "Sale price < circle rate — is that a problem?" | `check_section_50c()` |
| "How do I save on capital gains?" | `recommend_capital_gains_exemption()` |
| "What's the tax on rental income?" | `calculate_rental_income_tax()` |
| "How is REIT income taxed?" | `classify_reit_income()` |
| "How much TDS do I need to deduct?" | `calculate_property_purchase_tds()` / `calculate_rental_tds_individual()` |
| "Should I buy directly or buy REITs?" | `compare_buy_vs_reit()` |
| "Is this agricultural land taxable on sale?" | `classify_agricultural_land_bhopal()` |

## Step 2: The grandfathering decision (the high-value one)

The Finance Act 2024 changed property LTCG rules effective **23 July 2024**:

- **New default:** 12.5% on nominal gain, NO indexation
- **Grandfathering choice (Resident Individuals and HUFs only):** for property acquired BEFORE 23 July 2024, the seller can elect the LOWER of:
  - Path A: 12.5% on nominal gain (no indexation)
  - Path B: 20% on indexed gain (using CII)

NRIs cannot elect grandfathering. Companies cannot elect.

```python
from scripts.real_estate_tracker import calculate_property_capital_gains, TaxpayerType
from datetime import date

r = calculate_property_capital_gains(
    purchase_price=50_00_000,
    purchase_date=date(2010, 6, 1),
    sale_price=2_00_00_000,
    sale_date=date(2026, 6, 1),
    taxpayer_type=TaxpayerType.RESIDENT_INDIVIDUAL,
)
# r.optimal_path → "B_20%_indexed"
# r.optimal_tax → ₹16,64,671
# r.savings_vs_other_path → ₹2,10,329
```

**Rule of thumb:**
- Property held >10 years with modest appreciation (e.g., Bhopal residential at ~7% CAGR) → Path B (indexation) usually wins
- Property held <5 years with sharp appreciation (e.g., metro NCR, Bengaluru) → Path A (12.5% no-index) usually wins
- Always RUN THE CALC — don't guess. The tool tells you definitively.

**Important caveat about surcharge:** Surcharge is computed on NON-indexed (nominal) gain regardless of which path you elect. The tool warns when gain exceeds ₹50L.

## Step 3: MP-specific transaction costs

Madhya Pradesh has among India's highest property transaction costs:
- Stamp duty: **7.5%**
- Registration: **3.0%**
- Total: **10.5%** of property value
- **No gender concession** (unlike Maharashtra or Delhi which offer reduced rates for women buyers)

Special cases:
- Gift deed to family: ₹1,000 fixed stamp + 1% registration
- Commercial lease deed: 8% stamp + 1% registration

Always verify current rates at sampada.mpigr.gov.in before any transaction.

## Step 4: Section 50C — the under-pricing trap

If you sell below circle rate (SAMPADA value), the higher value is **DEEMED** the sale price for capital gains.

- Tolerance: 10% (no adjustment if stamp duty value ≤ 1.10 × actual sale price)
- Above tolerance: stamp duty value becomes the sale consideration
- Dispute option: request a Departmental Valuation Officer (DVO) referral

Use `check_section_50c()` before finalizing any sale price.

## Step 5: Exemption recommendation

Use `recommend_capital_gains_exemption()` with the sale asset type:

| Sold asset | Section 54 | Section 54EC | Section 54F | Section 54B |
|---|---|---|---|---|
| Residential house | ✓ best | ✓ (cap ₹50L) | ✗ | ✗ |
| Land/building (non-residential) | ✗ | ✓ only | ✗ | ✗ |
| Urban agricultural land | ✗ | ✓ | ✗ | ✓ best |
| Other LT asset (gold, stocks held long) | ✗ | ✗ | ✓ | ✗ |

Key constraints:
- **Section 54:** sale of residential → reinvest in residential, max ₹10cr exemption, 2 yrs buy / 3 yrs construct
- **Section 54EC:** ₹50L cap per FY, 5-year lockup, 5.25% interest (taxable), invest within 6 months in REC/PFC/IRFC/NHAI bonds
- **Section 54F:** sale of non-residential LT asset → reinvest sale proceeds (not just gain) in residential; cannot own more than 1 other residence on sale date
- **Section 54B:** urban agricultural land → reinvest in another agricultural land within 2 years

## Step 6: REIT income decomposition

Indian REITs distribute income in 4 components, each taxed differently per Finance Act 2024:

| Component | Tax treatment |
|---|---|
| Interest | Slab rate |
| Dividend (SPV NOT under 115BAA) | **Exempt** (most cases) |
| Dividend (SPV under 115BAA) | Slab rate (rare) |
| Rental | Slab rate |
| Capital repayment | NOT taxed (reduces cost basis instead) |

Plus: LTCG holding period reduced 36 → 12 months in Budget 2024; LTCG @ 12.5% above ₹1.25L/year exemption.

Use `classify_reit_income()` to decompose a distribution.

## Step 7: Bhopal agricultural land — Section 2(14)(iii)

Bhopal Municipal Corporation has population ~23 lakh (>10 lakh) so urban classification applies within **8 km aerial distance** from BMC limits.

| Distance from BMC (aerial) | Classification | Capital gains tax |
|---|---|---|
| ≤ 8 km | URBAN agricultural | Applies (it's a capital asset) |
| > 8 km | RURAL agricultural | Does NOT apply (Section 2(14)(iii) exemption) |

⚠️ Check distance from nearest OTHER municipality too (Sehore town, Vidisha town) — same rules apply with population-based thresholds.

## Step 8: TDS obligations

| Transaction | Section | Rate | Threshold | Deductor | Form |
|---|---|---|---|---|---|
| Buy property | 194-IA | 1% | ₹50L aggregate | Buyer | 26QB |
| Rent (individual/HUF tenant) | 194-IB | **2%** (was 5%, reduced Oct 2024) | ₹50K/month | Tenant | 26QC |
| Rent (company/audit tenant) | 194-I | 10% land/building | ₹6L/year (FY25-26) | Tenant | 26Q |
| NRI seller | 195 | 20% on LTCG + surcharge | Any | Buyer | 26Q + 15CA/15CB |

## Step 9: Rental income (Section 24)

```python
calculate_rental_income_tax(
    annual_rent=4_80_000,
    municipal_taxes=12_000,
    home_loan_interest=2_50_000,
    is_let_out=True,
    is_new_regime=True,
)
```

Rules:
- Section 24(a): 30% standard deduction on NAV (rent − municipal taxes), automatic
- Section 24(b): home loan interest — **unlimited for let-out**, capped at **₹2L for self-occupied**
- **NEW regime loss restriction:** loss from let-out property CANNOT be set off against other income; only carried forward 8 years to offset future house-property income
- OLD regime: up to ₹2L loss setoff against other income; balance carried forward

## When NOT to use this skill

- Foreign property — different rules entirely (DTAA may apply)
- Property outside MP and the question is only about stamp duty — flag that only MP is implemented and you can compute the principles but not the exact rate
- Pure GST questions on commercial rental — flag for separate GST analysis

## Disclaimers (always include in final response)

Real estate transactions are high-stakes. Verify with:
- A property lawyer (title search, encumbrance certificate)
- A chartered accountant (capital gains computation, exemption claim)
- SAMPADA portal (current circle rates)
- MP-RERA (project registration verification)

CII for FY 2025-26 (376) and FY 2026-27 (390) in the skill are ESTIMATES — verify current CBDT notification (issued each June) before relying on indexed calculations.
