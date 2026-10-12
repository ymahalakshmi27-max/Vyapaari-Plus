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