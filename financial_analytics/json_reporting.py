import json
from typing import Any


def generate_financial_report(
    revenue: float,
    cost_of_goods_sold: float,
    operating_expenses: float,
    depreciation: float = 0.0,
    amortization: float = 0.0,
) -> dict[str, Any]:
    """Generate financial KPIs in a dashboard-friendly dictionary."""

    values = [
        revenue,
        cost_of_goods_sold,
        operating_expenses,
        depreciation,
        amortization,
    ]

    if any(value < 0 for value in values):
        raise ValueError("Financial input values cannot be negative")

    gross_profit = revenue - cost_of_goods_sold
    ebitda = gross_profit - operating_expenses
    net_margin_inputs_profit = (
        ebitda - depreciation - amortization
    )

    gross_margin_percent = (
        (gross_profit / revenue) * 100 if revenue else 0.0
    )

    net_margin_percent = (
        (net_margin_inputs_profit / revenue) * 100
        if revenue
        else 0.0
    )

    return {
        "revenue": round(revenue, 2),
        "cost_of_goods_sold": round(cost_of_goods_sold, 2),
        "gross_profit": round(gross_profit, 2),
        "gross_margin_percent": round(gross_margin_percent, 2),
        "operating_expenses": round(operating_expenses, 2),
        "ebitda": round(ebitda, 2),
        "depreciation": round(depreciation, 2),
        "amortization": round(amortization, 2),
        "net_profit_before_interest_and_tax": round(
            net_margin_inputs_profit, 2
        ),
        "net_margin_percent": round(net_margin_percent, 2),
    }


def report_to_json(report: dict[str, Any]) -> str:
    """Convert a financial report into formatted JSON."""
    return json.dumps(report, indent=2)


if __name__ == "__main__":
    report = generate_financial_report(
        revenue=100000,
        cost_of_goods_sold=60000,
        operating_expenses=15000,
        depreciation=2000,
        amortization=1000,
    )

    print(report_to_json(report))