from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class RecurringPayable:
    name: str
    amount: float
    first_due_date: date
    interval_days: int


@dataclass(frozen=True)
class CashFlowForecast:
    days: int
    forecast_end_date: date
    opening_cash: float
    expected_receipts: float
    recurring_payables: float
    projected_closing_cash: float


def forecast_cash_flow(
    as_of_date: date,
    opening_cash: float,
    expected_daily_receipts: float,
    payables: Iterable[RecurringPayable],
) -> list[CashFlowForecast]:

    if expected_daily_receipts < 0:
        raise ValueError("Expected daily receipts cannot be negative")

    payable_list = tuple(payables)

    for payable in payable_list:
        if payable.amount < 0:
            raise ValueError("Payable amount cannot be negative")

        if payable.interval_days <= 0:
            raise ValueError("Payment interval must be positive")

    forecasts = []

    for days in (30, 60, 90):
        end_date = as_of_date + timedelta(days=days)
        total_payables = 0.0

        for payable in payable_list:
            due_date = payable.first_due_date

            while due_date <= as_of_date:
                due_date += timedelta(days=payable.interval_days)

            while due_date <= end_date:
                total_payables += payable.amount
                due_date += timedelta(days=payable.interval_days)

        receipts = expected_daily_receipts * days
        closing_cash = opening_cash + receipts - total_payables

        forecasts.append(
            CashFlowForecast(
                days=days,
                forecast_end_date=end_date,
                opening_cash=opening_cash,
                expected_receipts=receipts,
                recurring_payables=total_payables,
                projected_closing_cash=closing_cash,
            )
        )

    return forecasts