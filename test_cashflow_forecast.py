import unittest
from datetime import date

from cashflow_forecast import (
    RecurringPayable,
    forecast_cash_flow,
)


class TestCashFlowForecast(unittest.TestCase):

    def test_30_60_90_day_forecasts(self):
        forecasts = forecast_cash_flow(
            as_of_date=date(2026, 10, 13),
            opening_cash=10000,
            expected_daily_receipts=500,
            payables=[
                RecurringPayable(
                    name="Rent",
                    amount=2000,
                    first_due_date=date(2026, 10, 20),
                    interval_days=30,
                )
            ],
        )

        self.assertEqual(len(forecasts), 3)

        self.assertEqual(forecasts[0].days, 30)
        self.assertEqual(forecasts[0].expected_receipts, 15000)
        self.assertEqual(forecasts[0].recurring_payables, 2000)
        self.assertEqual(forecasts[0].projected_closing_cash, 23000)

        self.assertEqual(forecasts[1].days, 60)
        self.assertEqual(forecasts[1].expected_receipts, 30000)
        self.assertEqual(forecasts[1].recurring_payables, 4000)
        self.assertEqual(forecasts[1].projected_closing_cash, 36000)

        self.assertEqual(forecasts[2].days, 90)
        self.assertEqual(forecasts[2].expected_receipts, 45000)
        self.assertEqual(forecasts[2].recurring_payables, 6000)
        self.assertEqual(forecasts[2].projected_closing_cash, 49000)

    def test_rejects_negative_receipts(self):
        with self.assertRaises(ValueError):
            forecast_cash_flow(
                as_of_date=date(2026, 10, 13),
                opening_cash=10000,
                expected_daily_receipts=-100,
                payables=[],
            )

    def test_rejects_invalid_payment_interval(self):
        with self.assertRaises(ValueError):
            forecast_cash_flow(
                as_of_date=date(2026, 10, 13),
                opening_cash=10000,
                expected_daily_receipts=500,
                payables=[
                    RecurringPayable(
                        name="Rent",
                        amount=2000,
                        first_due_date=date(2026, 10, 20),
                        interval_days=0,
                    )
                ],
            )


if __name__ == "__main__":
    unittest.main()