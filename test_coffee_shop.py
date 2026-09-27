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

    


if __name__ == "__main__":
    unittest.main()
