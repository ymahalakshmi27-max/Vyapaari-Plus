import json
import unittest

from json_reporting import generate_financial_report, report_to_json


class TestJSONReporting(unittest.TestCase):

    def test_financial_report_calculations(self):
        report = generate_financial_report(
            revenue=100000,
            cost_of_goods_sold=60000,
            operating_expenses=15000,
            depreciation=2000,
            amortization=1000,
        )

        self.assertEqual(report["gross_profit"], 40000)
        self.assertEqual(report["ebitda"], 25000)
        self.assertEqual(
            report["ebit"], 22000
        )
        self.assertEqual(report["gross_margin_percent"], 40.0)
        self.assertEqual(report["ebit_margin_percent"], 22.0)

    def test_zero_revenue(self):
        report = generate_financial_report(0, 0, 0)
        self.assertEqual(report["gross_margin_percent"], 0.0)
        self.assertEqual(report["ebit"], 0.0)

    def test_negative_input(self):
        with self.assertRaises(ValueError):
            generate_financial_report(-100, 50, 20)

    def test_report_to_json(self):
        report = generate_financial_report(100, 40, 20)
        json_output = report_to_json(report)
        parsed_report = json.loads(json_output)
        self.assertEqual(parsed_report["gross_profit"], 60)


if __name__ == "__main__":
    unittest.main()
