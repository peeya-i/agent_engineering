import unittest
from unittest.mock import MagicMock, call
from order_service import (
    Order,
    InventoryService,
    PaymentGateway,
    InventoryShortageError,
    PaymentFailedError,
    InvalidOrderError
)

class TestOrderService(unittest.TestCase):

    def setUp(self):
        """Set up mock dependencies and order instance before each test."""
        self.mock_inventory = MagicMock(spec=InventoryService)
        self.mock_payment = MagicMock(spec=PaymentGateway)
        self.order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="user@example.com",
            is_vip=False
        )

    # --- Standard Item Management Tests ---

    def test_add_item_success(self):
        """Test adding items successfully to the cart."""
        self.order.add_item("prod-1", price=50.0, quantity=2)
        self.assertEqual(len(self.order.items), 1)
        self.assertEqual(self.order.items["prod-1"], {"price": 50.0, "qty": 2})

    def test_add_existing_item_increments_qty(self):
        """Test adding an existing item increments quantity."""
        self.order.add_item("prod-1", price=50.0, quantity=2)
        self.order.add_item("prod-1", price=50.0, quantity=3)
        self.assertEqual(self.order.items["prod-1"]["qty"], 5)

    def test_add_item_negative_price_raises_value_error(self):
        """Test adding an item with negative price raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.order.add_item("prod-1", price=-10.0, quantity=1)
        self.assertIn("Price cannot be negative", str(ctx.exception))

    def test_add_item_zero_or_negative_qty_raises_value_error(self):
        """Test adding an item with quantity <= 0 raises ValueError."""
        with self.assertRaises(ValueError):
            self.order.add_item("prod-1", price=10.0, quantity=0)
        with self.assertRaises(ValueError):
            self.order.add_item("prod-1", price=10.0, quantity=-2)

    def test_remove_item(self):
        """Test removing an item from the cart."""
        self.order.add_item("prod-1", price=20.0, quantity=1)
        self.order.remove_item("prod-1")
        self.assertNotIn("prod-1", self.order.items)

    def test_remove_non_existent_item_does_not_error(self):
        """Test removing a non-existent item handles gracefully."""
        self.order.remove_item("non-existent-id")
        self.assertEqual(len(self.order.items), 0)

    # --- CORNER CASE: Cart Modifications & Zero Prices ---

    def test_add_item_zero_price_allowed(self):
        """Corner Case: Free promotional items with price = 0.0 are allowed."""
        self.order.add_item("free-gift", price=0.0, quantity=1)
        self.assertEqual(self.order.total_price, 0.0)
        self.assertEqual(self.order.apply_discount(), 0.0)

    def test_add_existing_item_preserves_original_price(self):
        """Corner Case: Re-adding an existing item with a different price retains original price."""
        self.order.add_item("prod-1", price=50.0, quantity=1)
        self.order.add_item("prod-1", price=99.0, quantity=1)
        self.assertEqual(self.order.items["prod-1"]["price"], 50.0)
        self.assertEqual(self.order.items["prod-1"]["qty"], 2)

    # --- Standard & Boundary Pricing / Discount Tests ---

    def test_total_price_calculation(self):
        """Test gross total price calculation before discounts."""
        self.order.add_item("prod-1", price=10.0, quantity=2) # $20
        self.order.add_item("prod-2", price=15.0, quantity=3) # $45
        self.assertEqual(self.order.total_price, 65.0)

    def test_apply_discount_regular_under_threshold(self):
        """Regular customer with total <= $100 gets no discount."""
        self.order.add_item("prod-1", price=50.0, quantity=1) # $50
        self.assertEqual(self.order.apply_discount(), 50.0)

    def test_apply_discount_regular_over_threshold(self):
        """Regular customer with total > $100 gets 10% discount."""
        self.order.add_item("prod-1", price=150.0, quantity=1) # $150
        self.assertEqual(self.order.apply_discount(), 135.0) # 150 * 0.9 = 135.0

    def test_apply_discount_vip_customer(self):
        """VIP customer gets 20% discount regardless of total."""
        vip_order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="vip@example.com",
            is_vip=True
        )
        vip_order.add_item("prod-1", price=50.0, quantity=1) # $50
        self.assertEqual(vip_order.apply_discount(), 40.0) # 50 * 0.8 = 40.0

    # --- CORNER CASE: Discount Boundary & Floating Point Tests ---

    def test_apply_discount_boundary_exact_100_dollars(self):
        """Corner Case: Total of exactly $100.00 gets NO discount (rule is > 100)."""
        self.order.add_item("prod-1", price=100.0, quantity=1)
        self.assertEqual(self.order.total_price, 100.0)
        self.assertEqual(self.order.apply_discount(), 100.0)

    def test_apply_discount_boundary_100_dollars_and_one_cent(self):
        """Corner Case: Total of $100.01 qualifies for 10% discount ($90.01 after rounding)."""
        self.order.add_item("prod-1", price=100.01, quantity=1)
        self.assertEqual(self.order.total_price, 100.01)
        # 100.01 * 0.9 = 90.009 -> rounded to 90.01
        self.assertEqual(self.order.apply_discount(), 90.01)

    def test_apply_discount_floating_point_rounding(self):
        """Corner Case: Verify precision rounding with odd amounts (e.g., $19.99 * 3 = $59.97)."""
        self.order.add_item("prod-1", price=19.99, quantity=3) # $59.97
        self.assertEqual(self.order.total_price, 59.97)
        self.assertEqual(self.order.apply_discount(), 59.97)

        # VIP test with precision rounding (59.97 * 0.8 = 47.976 -> 47.98)
        vip_order = Order(self.mock_inventory, self.mock_payment, "vip@test.com", is_vip=True)
        vip_order.add_item("prod-1", price=19.99, quantity=3)
        self.assertEqual(vip_order.apply_discount(), 47.98)

    # --- Standard & Corner Case Checkout Tests ---

    def test_checkout_empty_cart_raises_invalid_order_error(self):
        """Checkout on an empty cart raises InvalidOrderError."""
        with self.assertRaises(InvalidOrderError) as ctx:
            self.order.checkout()
        self.assertIn("Cannot checkout an empty cart", str(ctx.exception))

    def test_checkout_insufficient_stock_raises_inventory_shortage_error(self):
        """Checkout with insufficient stock raises InventoryShortageError."""
        self.order.add_item("prod-1", price=25.0, quantity=5)
        self.mock_inventory.get_stock.return_value = 2 # Only 2 in stock

        with self.assertRaises(InventoryShortageError) as ctx:
            self.order.checkout()
        
        self.assertIn("Not enough stock for prod-1", str(ctx.exception))
        self.mock_inventory.get_stock.assert_called_once_with("prod-1")
        self.mock_payment.charge.assert_not_called()

    def test_checkout_exact_stock_matches_requested_qty(self):
        """Corner Case: Stock available matches requested quantity exactly (e.g. 5 available, 5 requested)."""
        self.order.add_item("prod-1", price=50.0, quantity=5)
        self.mock_inventory.get_stock.return_value = 5 # Exact match
        self.mock_payment.charge.return_value = True

        result = self.order.checkout()
        self.assertEqual(result["status"], "success")
        self.mock_inventory.decrement_stock.assert_called_once_with("prod-1", 5)

    def test_checkout_multi_item_partial_shortage_aborts_checkout(self):
        """Corner Case: First item has stock, second item lacks stock -> raises exception without charging payment."""
        self.order.add_item("prod-1", price=20.0, quantity=1)
        self.order.add_item("prod-2", price=30.0, quantity=5)

        # Item 1 has 10 in stock, Item 2 has only 1 in stock
        def mock_stock_side_effect(pid):
            return 10 if pid == "prod-1" else 1

        self.mock_inventory.get_stock.side_effect = mock_stock_side_effect

        with self.assertRaises(InventoryShortageError) as ctx:
            self.order.checkout()

        self.assertIn("Not enough stock for prod-2", str(ctx.exception))
        self.mock_payment.charge.assert_not_called()
        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_payment_gateway_declined_raises_payment_failed_error(self):
        """Checkout when payment gateway declines charge raises PaymentFailedError."""
        self.order.add_item("prod-1", price=30.0, quantity=1)
        self.mock_inventory.get_stock.return_value = 10
        self.mock_payment.charge.return_value = False # Declined

        with self.assertRaises(PaymentFailedError) as ctx:
            self.order.checkout()

        self.assertIn("Transaction declined", str(ctx.exception))
        self.mock_payment.charge.assert_called_once_with(30.0, "USD")
        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_payment_returns_falsy_value(self):
        """Corner Case: Payment gateway returns None or 0 instead of False."""
        self.order.add_item("prod-1", price=30.0, quantity=1)
        self.mock_inventory.get_stock.return_value = 10
        self.mock_payment.charge.return_value = None # Falsy return

        with self.assertRaises(PaymentFailedError):
            self.order.checkout()

        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_payment_gateway_exception_raises_payment_failed_error(self):
        """Checkout when payment gateway throws network exception raises PaymentFailedError."""
        self.order.add_item("prod-1", price=30.0, quantity=1)
        self.mock_inventory.get_stock.return_value = 10
        self.mock_payment.charge.side_effect = RuntimeError("Payment service unavailable")

        with self.assertRaises(PaymentFailedError) as ctx:
            self.order.checkout()

        self.assertIn("Payment gateway error: Payment service unavailable", str(ctx.exception))
        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_success(self):
        """Successful checkout charges gateway, decrements stock, and updates order status."""
        self.order.add_item("prod-1", price=80.0, quantity=1) # $80
        self.order.add_item("prod-2", price=40.0, quantity=1) # $40 -> Gross $120
        # Discount: 10% off $120 = $108.0

        self.mock_inventory.get_stock.side_effect = lambda pid: 10
        self.mock_payment.charge.return_value = True

        result = self.order.checkout()

        self.assertEqual(result, {"status": "success", "charged_amount": 108.0})
        self.assertTrue(self.order.is_paid)
        self.assertEqual(self.order.status, "COMPLETED")

        self.mock_inventory.get_stock.assert_has_calls([call("prod-1"), call("prod-2")], any_order=True)
        self.mock_payment.charge.assert_called_once_with(108.0, "USD")
        self.mock_inventory.decrement_stock.assert_has_calls([call("prod-1", 1), call("prod-2", 1)], any_order=True)

if __name__ == '__main__':
    unittest.main()
