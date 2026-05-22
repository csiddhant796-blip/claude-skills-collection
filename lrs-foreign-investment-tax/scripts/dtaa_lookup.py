"""
SKILL 2: dtaa_lookup
Returns DTAA dividend withholding rate and capital gains treatment for any country.
Computes net DTAA credit claimable when filing Form 67.

Usage:
    from dtaa_lookup import get_dtaa_info, compute_dtaa_credit
    info = get_dtaa_info("USA")
    credit = compute_dtaa_credit(country="USA", dividend_usd=100, indian_slab_pct=30, usd_inr=84)
"""
import json
import os

KB_PATH = os.path.join(os.path.dirname(__file__), "regulatory_knowledge_base.json")

def _load_kb():
    with open(KB_PATH) as f:
        return json.load(f)


def get_dtaa_info(country_code):
    """Get DTAA details for a country. country_code: 'USA', 'JAPAN', 'TAIWAN', etc."""
    kb = _load_kb()
    code = country_code.upper().replace(" ", "_")
    if code not in kb["dtaa_rates"]:
        return {
            "error": f"No DTAA data for {country_code}",
            "available_countries": list(kb["dtaa_rates"].keys())
        }
    return kb["dtaa_rates"][code]


def compute_dtaa_credit(country, dividend_usd, indian_slab_pct, usd_inr=84.0):
    """
    Compute the foreign tax credit you can claim via Form 67.

    Args:
        country: country code (USA, JAPAN, etc.)
        dividend_usd: gross dividend received in USD
        indian_slab_pct: your marginal slab rate in India (e.g., 30)
        usd_inr: exchange rate

    Returns: full breakdown of credit calculation
    """
    info = get_dtaa_info(country)
    if "error" in info:
        return info

    wht_pct = info.get("dividend_portfolio_pct", 0)
    dividend_inr = dividend_usd * usd_inr
    foreign_wht_inr = dividend_inr * (wht_pct / 100)
    indian_tax_on_dividend_inr = dividend_inr * (indian_slab_pct / 100)
    # FTC is LOWER of foreign tax paid OR Indian tax liability on that income
    ftc_claimable_inr = min(foreign_wht_inr, indian_tax_on_dividend_inr)
    net_indian_tax_payable = max(0, indian_tax_on_dividend_inr - ftc_claimable_inr)
    irrecoverable_wht = max(0, foreign_wht_inr - ftc_claimable_inr)

    warning = None
    if irrecoverable_wht > 0:
        warning = (
            f"\u26a0\ufe0f \u20b9{int(irrecoverable_wht):,} of foreign WHT is irrecoverable — "
            "your Indian slab is below the foreign WHT rate, and FTC carry-forward is NOT allowed."
        )

    return {
        "country": country.upper(),
        "dividend_usd": dividend_usd,
        "dividend_inr": round(dividend_inr, 2),
        "foreign_wht_rate_pct": wht_pct,
        "foreign_wht_paid_inr": round(foreign_wht_inr, 2),
        "indian_slab_pct": indian_slab_pct,
        "indian_tax_on_dividend_inr": round(indian_tax_on_dividend_inr, 2),
        "ftc_claimable_via_form67_inr": round(ftc_claimable_inr, 2),
        "net_indian_tax_payable_inr": round(net_indian_tax_payable, 2),
        "irrecoverable_wht_inr": round(irrecoverable_wht, 2),
        "filing_required": {
            "form_67": True,
            "rule": "Rule 128 IT Rules 1962",
            "deadline": "31 March of AY (best filed with ITR)",
            "supporting_docs": ["Form 1042-S from US broker", "TRC (Form 10FB)", "SBI TTBR rates"]
        },
        "warning": warning
    }


def compare_dtaa_dividend_costs(countries=None, dividend_usd=1000, indian_slab_pct=30):
    """Compare DTAA dividend WHT costs across countries — useful for portfolio allocation decisions."""
    if countries is None:
        kb = _load_kb()
        countries = list(kb["dtaa_rates"].keys())

    results = []
    for c in countries:
        r = compute_dtaa_credit(c, dividend_usd, indian_slab_pct)
        if "error" not in r:
            results.append({
                "country": c,
                "wht_rate_pct": r["foreign_wht_rate_pct"],
                "wht_paid_inr": r["foreign_wht_paid_inr"],
                "ftc_claimable_inr": r["ftc_claimable_via_form67_inr"],
                "irrecoverable_inr": r["irrecoverable_wht_inr"]
            })
    return sorted(results, key=lambda x: x["wht_rate_pct"])


if __name__ == "__main__":
    print("─── DTAA info for USA ───")
    print(json.dumps(get_dtaa_info("USA"), indent=2))
    print("\n─── DTAA credit example ($1000 US dividend, 30% slab) ───")
    print(json.dumps(compute_dtaa_credit("USA", 1000, 30), indent=2, ensure_ascii=False))
    print("\n─── Comparison across countries ───")
    print(json.dumps(compare_dtaa_dividend_costs(), indent=2, ensure_ascii=False))
