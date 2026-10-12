from dataclasses import dataclass


@dataclass
class FinancialMetrics:
    revenue: float
    cost_of_goods_sold: float

    @property
    def gross_profit(self) -> float:
        return self.revenue - self.cost_of_goods_sold

    @property
    def gross_margin_percent(self) -> float:
        if self.revenue == 0:
            return 0.0
        return (self.gross_profit / self.revenue) * 100


if __name__ == "__main__":
    metrics = FinancialMetrics(
        revenue=10000,
        cost_of_goods_sold=6000,
    )

    print(f"Revenue: ₹{metrics.revenue:.2f}")
    print(f"Gross profit: ₹{metrics.gross_profit:.2f}")
    print(f"Gross margin: {metrics.gross_margin_percent:.2f}%")