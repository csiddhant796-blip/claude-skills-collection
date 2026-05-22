"""
SKILL 3: capital_gains_calculator
Computes capital gains tax for:
  - Direct foreign stocks/ETFs (Section 112: 12.5% LTCG, slab STCG)
  - Indian MF FoFs acquired post-April 2023 (Section 50AA: all slab)
  - Indian MF FoFs acquired pre-April 2023 (12.5% LTCG if >24m, else slab)

Usage:
    from capital_gains_calculator import calc_gains_tax
    result = calc_gains_tax(
        asset_type="foreign_stock",
        buy_price_usd=100, sell_price_usd=150, qty=10,
        holding_days=800,
        slab_rate_pct=30,
        usd_inr=84
    )
"""
import json
import os
from datetime import datetime

KB_PATH = os.path.join(os.path.dirname(__file__), "regulatory_knowledge_base.json")

def _load_kb():
    with open(KB_PATH) as f:
        return json.load(f)


def calc_gains_tax(asset_type, buy_price_usd, sell_price_usd, qty,
                   holding_days, slab_rate_pct, usd_inr=84.0,
                   acquisition_date=None):
    """
    Calculate capital gains tax in INR.

    asset_type: 'foreign_stock', 'foreign_etf', 'mf_fof_post_2023', 'mf_fof_pre_2023'
    holding_days: days held
    slab_rate_pct: investor's marginal Indian slab rate
    acquisition_date: ISO date string, used to validate MF FoF classification
    """
    kb = _load_kb()
    cg = kb["capital_gains_rules"]

    gain_usd = (sell_price_usd - buy_price_usd) * qty
    gain_inr = gain_usd * usd_inr

    holding_months = holding_days / 30.44

    rules_used = None
    is_ltcg = False
    tax_rate_pct = 0
    surcharge_pct = 15  # max
    cess_pct = 4

    if asset_type in ("foreign_stock", "foreign_etf"):
        rules = cg["foreign_stocks_and_etfs"]
        rules_used = "Section 112 (foreign stocks treated as unlisted securities)"
        if holding_months > rules["ltcg_holding_period_months"]:
            is_ltcg = True
            tax_rate_pct = rules["ltcg_rate_pct"]
        else:
            tax_rate_pct = slab_rate_pct

    elif asset_type == "mf_fof_post_2023":
        rules_used = "Section 50AA (Specified Mutual Fund — all gains taxed at slab regardless of holding)"
        tax_rate_pct = slab_rate_pct
        is_ltcg = False

    elif asset_type == "mf_fof_pre_2023":
        rules = cg["indian_mf_fof_pre_april2023"]
        rules_used = "Pre-April 2023 MF units — Section 112 treatment (12.5% LTCG if >24m)"
        if holding_months > rules["ltcg_holding_period_months"]:
            is_ltcg = True
            tax_rate_pct = rules["ltcg_rate_pct"]
        else:
            tax_rate_pct = slab_rate_pct
    else:
        return {"error": f"Unknown asset type: {asset_type}"}

    base_tax_inr = gain_inr * (tax_rate_pct / 100)
    # Effective rate at top bracket with surcharge and cess
    effective_pct = tax_rate_pct * (1 + surcharge_pct/100) * (1 + cess_pct/100) if is_ltcg else tax_rate_pct
    effective_tax_inr = gain_inr * (effective_pct / 100) if is_ltcg else base_tax_inr

    return {
        "asset_type": asset_type,
        "gain_usd": round(gain_usd, 2),
        "gain_inr": round(gain_inr, 2),
        "holding_days": holding_days,
        "holding_months": round(holding_months, 1),
        "classification": "LTCG" if is_ltcg else "STCG",
        "tax_rate_pct": tax_rate_pct,
        "effective_rate_pct_with_surcharge_cess": round(effective_pct, 2) if is_ltcg else slab_rate_pct,
        "base_tax_inr": round(base_tax_inr, 2),
        "estimated_tax_inr": round(effective_tax_inr, 2),
        "rules_applied": rules_used,
        "exemption_available_inr": 0,
        "indexation_available": False,
        "notes": [
            "Foreign stocks: NO ₹1.25L exemption (that applies only to Section 112A Indian listed equities).",
            "MF FoF post-April 2023: All gains taxed at slab rate regardless of holding period.",
            "Indexation removed from 23 July 2024 by Finance Act 2024.",
            "Verify exact rate including applicable surcharge with your CA."
        ]
    }


def compare_routes_for_tax(buy_usd, sell_usd, qty, holding_months, slab_pct):
    """Compare tax across direct US ETF vs Indian MF FoF for same investment."""
    holding_days = int(holding_months * 30.44)

    direct = calc_gains_tax("foreign_etf", buy_usd, sell_usd, qty, holding_days, slab_pct)
    fof_post = calc_gains_tax("mf_fof_post_2023", buy_usd, sell_usd, qty, holding_days, slab_pct)

    direct_tax = direct["estimated_tax_inr"]
    fof_tax = fof_post["estimated_tax_inr"]
    saving = fof_tax - direct_tax

    return {
        "direct_us_etf": direct,
        "indian_mf_fof_post_2023": fof_post,
        "tax_saving_direct_route_inr": round(saving, 2),
        "recommendation": (
            "Direct US ETF (via LRS) is more tax-efficient when held >24 months at high slab rates."
            if saving > 0 else
            "Indian MF FoF route is more tax-efficient for short holdings or low slab rates."
        )
    }


if __name__ == "__main__":
    print("─── Foreign stock held 30 months (LTCG case) ───")
    print(json.dumps(calc_gains_tax("foreign_stock", 100, 200, 50, 900, 30), indent=2))
    print("\n─── Indian MF FoF post-2023 (same gain) ───")
    print(json.dumps(calc_gains_tax("mf_fof_post_2023", 100, 200, 50, 900, 30), indent=2))
    print("\n─── Route comparison ───")
    print(json.dumps(compare_routes_for_tax(100, 200, 50, 30, 30), indent=2, ensure_ascii=False))
