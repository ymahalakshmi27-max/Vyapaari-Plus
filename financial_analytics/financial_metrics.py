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

    @staticmethod
    def net_margin_percent(
        revenue: float,
        net_profit: float,
    ) -> float:
        if revenue == 0:
            return 0.0
        return (net_profit / revenue) * 100

    @staticmethod
    def inventory_turnover(
        cost_of_goods_sold: float,
        average_inventory_value: float,
    ) -> float:
        if average_inventory_value == 0:
            return 0.0
        return cost_of_goods_sold / average_inventory_value




if __name__ == "__main__":
    metrics = FinancialMetrics(
        revenue=10000,
        cost_of_goods_sold=6000,
    )

    print(f"Revenue: ₹{metrics.revenue:.2f}")
    print(f"Gross profit: ₹{metrics.gross_profit:.2f}")
    print(f"Gross margin: {metrics.gross_margin_percent:.2f}%")