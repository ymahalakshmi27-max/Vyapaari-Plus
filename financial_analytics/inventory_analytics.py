from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class InventoryItem:
    name: str
    quantity_on_hand: int
    unit_cost: float
    units_sold_last_30_days: int
    last_sold_date: date | None


@dataclass(frozen=True)
class InventorySummary:
    name: str
    inventory_value: float
    daily_sales_velocity: float
    days_since_last_sale: int | None
    is_dead_stock: bool


def analyze_inventory(
    items: list[InventoryItem],
    as_of_date: date,
    dead_stock_days: int = 90,
) -> list[InventorySummary]:

    if dead_stock_days < 0:
        raise ValueError("Dead-stock threshold cannot be negative")

    summaries = []

    for item in items:
        if item.quantity_on_hand < 0:
            raise ValueError("Stock quantity cannot be negative")

        if item.unit_cost < 0 or item.units_sold_last_30_days < 0:
            raise ValueError("Cost and sales quantity cannot be negative")

        if item.last_sold_date is not None and item.last_sold_date > as_of_date:
            raise ValueError("Last sale date cannot be in the future")

        days_since_sale = (
            (as_of_date - item.last_sold_date).days
            if item.last_sold_date is not None
            else None
        )

        is_dead_stock = (
            days_since_sale is None
            or days_since_sale >= dead_stock_days
        )

        summaries.append(
            InventorySummary(
                name=item.name,
                inventory_value=item.quantity_on_hand * item.unit_cost,
                daily_sales_velocity=item.units_sold_last_30_days / 30,
                days_since_last_sale=days_since_sale,
                is_dead_stock=is_dead_stock,
            )
        )

    return summaries