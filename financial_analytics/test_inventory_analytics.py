import unittest
from datetime import date

from inventory_analytics import InventoryItem, analyze_inventory


class TestInventoryAnalytics(unittest.TestCase):

  def test_inventory_value_and_sales_velocity(self):
    item = InventoryItem(
        name="Rice",
        quantity_on_hand=10,
        unit_cost=50.0,
        units_sold_last_30_days=60,
        last_sold_date=date(2026, 10, 1),
    )

    result = analyze_inventory([item], date(2026, 10, 13))[0]

    self.assertEqual(result.inventory_value, 500.0)
    self.assertEqual(result.daily_sales_velocity, 2.0)
    self.assertEqual(result.days_since_last_sale, 12)
    self.assertFalse(result.is_dead_stock)

  def test_dead_stock(self):
    item = InventoryItem(
        name="Old Item",
        quantity_on_hand=5,
        unit_cost=100.0,
        units_sold_last_30_days=0,
        last_sold_date=date(2026, 7, 15),
    )

    result = analyze_inventory([item], date(2026, 10, 13))[0]

    self.assertTrue(result.is_dead_stock)

  def test_never_sold_item_is_dead_stock(self):
    item = InventoryItem(
        name="New Item",
        quantity_on_hand=5,
        unit_cost=20.0,
        units_sold_last_30_days=0,
        last_sold_date=None,
    )

    result = analyze_inventory([item], date(2026, 10, 13))[0]

    self.assertIsNone(result.days_since_last_sale)
    self.assertTrue(result.is_dead_stock)

  def test_negative_stock_raises_error(self):
    item = InventoryItem(
        name="Rice",
        quantity_on_hand=-1,
        unit_cost=50.0,
        units_sold_last_30_days=10,
        last_sold_date=None,
    )

    with self.assertRaises(ValueError):
        analyze_inventory([item], date(2026, 10, 13))

  def test_future_sale_date_raises_error(self):
    item = InventoryItem(
        name="Rice",
        quantity_on_hand=10,
        unit_cost=50.0,
        units_sold_last_30_days=10,
        last_sold_date=date(2026, 10, 14),
    )

    with self.assertRaises(ValueError):
        analyze_inventory([item], date(2026, 10, 13))

if __name__ == "main":
    unittest.main()