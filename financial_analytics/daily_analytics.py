from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Sale:
    sale_date: date
    revenue: float
    cost_of_goods_sold: float


@dataclass(frozen=True)
class DailySummary:
    sale_date: date
    total_revenue: float
    total_cost: float
    gross_profit: float
    gross_margin_percent: float


def aggregate_daily_sales(sales: Iterable[Sale]) -> list[DailySummary]:
    totals: dict[date, list[float]] = {}

    for sale in sales:
        if sale.revenue < 0 or sale.cost_of_goods_sold < 0:
            raise ValueError("Revenue and cost cannot be negative")

        if sale.sale_date not in totals:
            totals[sale.sale_date] = [0.0, 0.0]

        totals[sale.sale_date][0] += sale.revenue
        totals[sale.sale_date][1] += sale.cost_of_goods_sold

    summaries = []

    for sale_date, (revenue, cost) in sorted(totals.items()):
        profit = revenue - cost
        margin = (profit / revenue * 100) if revenue else 0.0

        summaries.append(
            DailySummary(
                sale_date=sale_date,
                total_revenue=revenue,
                total_cost=cost,
                gross_profit=profit,
                gross_margin_percent=margin,
            )
        )

    return summaries


if __name__ == "__main__":
    sales = [
        Sale(date(2026, 10, 12), 10000, 6000),
        Sale(date(2026, 10, 12), 5000, 2500),
        Sale(date(2026, 10, 11), 2000, 1200),
    ]

    for summary in aggregate_daily_sales(sales):
        print(summary)