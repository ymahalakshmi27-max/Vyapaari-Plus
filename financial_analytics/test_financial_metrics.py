import unittest

from financial_metrics import FinancialMetrics


class TestFinancialMetrics(unittest.TestCase):

    def test_gross_profit(self):
        metrics = FinancialMetrics(10000, 6000)
        self.assertEqual(metrics.gross_profit, 4000)

    def test_gross_margin(self):
        metrics = FinancialMetrics(10000, 6000)
        self.assertEqual(metrics.gross_margin_percent, 40.0)

    def test_zero_revenue(self):
        metrics = FinancialMetrics(0, 0)
        self.assertEqual(metrics.gross_margin_percent, 0.0)


if __name__ == "__main__":
    unittest.main()


def test_net_margin_percent():
    assert FinancialMetrics.net_margin_percent(1000, 150) == 15.0


def test_net_margin_percent_zero_revenue():
    assert FinancialMetrics.net_margin_percent(0, 150) == 0.0


def test_inventory_turnover():
    assert FinancialMetrics.inventory_turnover(500, 100) == 5.0


def test_inventory_turnover_zero_inventory():
    assert FinancialMetrics.inventory_turnover(500, 0) == 0.0