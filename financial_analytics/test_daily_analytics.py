import unittest
from datetime import date

from daily_analytics import Sale, aggregate_daily_sales


class TestDailyAnalytics(unittest.TestCase):

    def test_aggregates_sales_by_date(self):
        sales = [
            Sale(date(2026, 10, 12), 10000, 6000),
            Sale(date(2026, 10, 12), 5000, 2500),
            Sale(date(2026, 10, 11), 2000, 1200),
        ]

        results = aggregate_daily_sales(sales)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].sale_date, date(2026, 10, 11))
        self.assertEqual(results[0].total_revenue, 2000)
        self.assertEqual(results[0].gross_profit, 800)

        self.assertEqual(results[1].total_revenue, 15000)
        self.assertEqual(results[1].total_cost, 8500)
        self.assertEqual(results[1].gross_profit, 6500)
        self.assertAlmostEqual(
            results[1].gross_margin_percent, 43.3333, places=3
        )

    def test_rejects_negative_revenue(self):
        sales = [Sale(date(2026, 10, 12), -100, 50)]

        with self.assertRaises(ValueError):
            aggregate_daily_sales(sales)


if __name__ == "__main__":
    unittest.main()