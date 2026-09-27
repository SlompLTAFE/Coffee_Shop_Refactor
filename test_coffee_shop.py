import unittest

from coffee_shop_refactored import (
    MenuItem,
    Order,
    OrderItem,
    Customer,
    LoyaltyProgram,
    SalesTracker,
)
from coffee_shop_exceptions import (
InvalidCustomizationError,
InsufficientPointsError,
)

class TestCoffeeShop(unittest.TestCase):


    def setUp(self):
        """Set up test fixtures."""
        self.latte = MenuItem(
            "Latte",
            4.50,
            ["small", "medium", "large"]
        )
        self.customer = Customer("Alice", member=True)
        self.loyalty = LoyaltyProgram()

    def test_menu_item_pricing_small(self):
        """Test MenuItem calculates small drink price correctly."""
        price = self.latte.calculate_price("small")

        self.assertEqual(price, 4.50)

    def test_menu_item_pricing_medium_oat_milk(self):
        """Test medium latte with oat milk calculates correctly."""
        price = self.latte.calculate_customized_price(
            "medium",
            milk_type="oat"
        )

        self.assertAlmostEqual(price, 6.35)

    def test_menu_item_pricing_invalid_size(self):
        """Test MenuItem raises exception for invalid size."""
        with self.assertRaises(InvalidCustomizationError):
            self.latte.calculate_price("extra-large")

    def test_menu_item_invalid_milk(self):
        """Test MenuItem raises exception for invalid milk."""
        with self.assertRaises(InvalidCustomizationError):
            self.latte.calculate_customized_price(
                "small",
                milk_type="soy"
            )

    def test_order_total_with_multiple_items(self):
        """Test Order calculates total correctly."""
        customer = Customer("Bob")
        order = Order(customer)

        latte = OrderItem(self.latte, "small")
        second_latte = OrderItem(self.latte, "small")

        order.add_item(latte)
        order.add_item(second_latte)

        self.assertEqual(order.total(), 9.00)

    def test_member_discount_applied(self):
        """Test member discount is 10%."""
        order = Order(self.customer)

        latte = OrderItem(self.latte, "small")
        order.add_item(latte)

        self.assertEqual(order.total(), 4.05)

    def test_loyalty_points_earned(self):
        """Test loyalty points: $1 = 1 point."""
        customer = Customer("Bob")
        order = Order(customer)

        latte = OrderItem(self.latte, "small")
        order.add_item(latte)

        points = order.earn_loyalty_points(self.loyalty)

        self.assertEqual(points, 4)
        self.assertEqual(self.loyalty.accounts["Bob"], 4)

    def test_redeem_points_insufficient(self):
        """Test redeeming with insufficient points raises exception."""
        with self.assertRaises(InsufficientPointsError):
            self.loyalty.redeem_points(
                self.customer,
                points_to_redeem=100
            )

    def test_free_drink_redemption(self):
        """Test 100 points can redeem a free small drink."""
        self.loyalty.earn_points(self.customer, 100)

        order = Order(self.customer)
        drink = OrderItem(self.latte, "small")
        order.add_item(drink)

        order.redeem_free_drink(self.loyalty, drink)

        self.assertEqual(drink.price(), 0.0)
        self.assertEqual(self.loyalty.accounts["Alice"], 0)

    def test_free_drink_must_be_small(self):
        """Test free drink redemption rejects non-small drinks."""
        self.loyalty.earn_points(self.customer, 100)

        order = Order(self.customer)
        drink = OrderItem(self.latte, "medium")
        order.add_item(drink)

        with self.assertRaises(InvalidCustomizationError):
            order.redeem_free_drink(self.loyalty, drink)

    def test_staff_order_is_free(self):
        """Test staff orders have a total of zero."""
        staff_customer = Customer("Staff")
        order = Order(staff_customer, staff_order=True)

        drink = OrderItem(self.latte, "large")
        order.add_item(drink)

        self.assertEqual(order.total(), 0.0)

    def test_staff_order_is_tracked(self):
        """Test staff orders are still recorded by SalesTracker."""

        staff_customer = Customer("Staff")
        order = Order(staff_customer, staff_order=True)

        drink = OrderItem(self.latte, "small")
        order.add_item(drink)

        tracker = SalesTracker()
        tracker.record_order(order)

        self.assertEqual(tracker.order_count(), 1)
        self.assertEqual(tracker.total_sales(), 0.0)

    def test_sales_tracker_total_sales(self):
        """Test SalesTracker calculates total sales."""
        customer = Customer("Bob")
        order = Order(customer)

        latte = OrderItem(self.latte, "small")
        order.add_item(latte)

        tracker = SalesTracker()
        tracker.record_order(order)

        self.assertEqual(tracker.total_sales(), 4.50)

    def test_sales_tracker_average_order(self):
        """Test SalesTracker calculates average order value."""
        customer = Customer("Bob")

        first_order = Order(customer)
        first_order.add_item(OrderItem(self.latte, "small"))

        second_order = Order(customer)
        second_order.add_item(OrderItem(self.latte, "medium"))

        tracker = SalesTracker()
        tracker.record_order(first_order)
        tracker.record_order(second_order)

        expected_average = (4.50 + 5.85) / 2

        self.assertAlmostEqual(tracker.average_order(), expected_average)

if __name__ == "__main__":
    unittest.main()
