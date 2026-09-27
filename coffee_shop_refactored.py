from coffee_shop_exceptions import InsufficientPointsError, InvalidCustomizationError


class MenuItem:
    """Represents a menu item and its price."""
    
    SIZE_MULTIPLIERS = {"small": 1.0, "medium": 1.3, "large": 1.6}
    
    MILK_SURCHARGES = {
        "whole": 0.0,
        "skim": 0.0,
        "oat": 0.50,
        "almond": 0.50,
        "none": 0.0
    }

    EXTRA_SHOT_PRICE = 1.00
    WHIPPED_CREAM_PRICE = 0.75
    
    def __init__(self, name, base_price, available_sizes: list[str]) -> None:
        """Initializes menu item
        
        Args:
            name: The name of the menu item.
            base_price: The base price of the menu item.
            available_sizes: A list of available sizes for the menu item.
        """
        
        self.name = name
        self.base_price = base_price
        self.available_sizes = available_sizes

    def calculate_price(self, size: str) -> float:
        """Calculate the price of the item for a given size.

        Args:
            size: Drink size.

        Returns:
            The calculated price.

        Raises:
            InvalidCustomizationError: If the size is not available.
        """
        if size not in self.available_sizes:
            raise InvalidCustomizationError(
                f"Size '{size}' not available for {self.name}."
            )

        return self.base_price * self.SIZE_MULTIPLIERS[size]
    
    def calculate_customized_price(
        self,
        size: str,
        milk_type: str = "whole",
        extra_shot: bool = False,
        whipped_cream: bool = False
    ) -> float:
        """Calculate the price including customizations.

        Args:
            size: Drink size.
            milk_type: Type of milk.
            extra_shot: Whether to add an extra shot.
            whipped_cream: Whether to add whipped cream.

        Returns:
            The final customized price.

        Raises:
            InvalidCustomizationError: If the size or milk type is invalid.
        """
        price = self.calculate_price(size)

        if milk_type not in self.MILK_SURCHARGES:
            raise InvalidCustomizationError(
                f"Milk type '{milk_type}' is not available."
            )

        price += self.MILK_SURCHARGES[milk_type]

        if extra_shot:
            price += self.EXTRA_SHOT_PRICE

        if whipped_cream:
            price += self.WHIPPED_CREAM_PRICE

        return price
    
class Customer:
    """A coffee shop customer."""

    def __init__(self, name: str, member: bool = False) -> None:
        """Initialize a customer.

        Args:
            name: The customer's name.
            member: Whether the customer is a member.
        """
        self.name = name
        self.member = member   
        
class OrderItem:
    """Represent a customized item in an order."""

    def __init__(
        self,
        menu_item: MenuItem,
        size: str,
        milk_type: str = "whole",
        extra_shot: bool = False,
        whipped_cream: bool = False
    ) -> None:
        """Initialize an order item.

        Args:
            menu_item: The menu item being ordered.
            size: The selected size.
            milk_type: The selected milk type.
            extra_shot: Whether an extra shot was added.
            whipped_cream: Whether whipped cream was added.
        """
        self.menu_item = menu_item
        self.size = size
        self.milk_type = milk_type
        self.extra_shot = extra_shot
        self.whipped_cream = whipped_cream
        self.is_free = False

    def price(self) -> float:
        """Calculate the price of this customized item.

        Returns:
            The customized item price, or 0 if the item is free.
        """
        if self.is_free:
            return 0.0

        return self.menu_item.calculate_customized_price(
            self.size,
            self.milk_type,
            self.extra_shot,
            self.whipped_cream
        )
    
class LoyaltyProgram:
    """Manage customer loyalty points."""

    def __init__(self) -> None:
        """Initialize the loyalty program."""
        self.accounts: dict[str, int] = {}
        self.points_per_dollar = 1
        self.free_drink_points = 100
    
    def earn_points(self, customer: Customer, amount: float) -> int:
        """Award loyalty points based on the amount spent.

        Args:
            customer: The customer earning points.
            amount: The amount spent.

        Returns:
            The number of points earned.
        """
        points = int(amount * self.points_per_dollar)

        if customer.name not in self.accounts:
            self.accounts[customer.name] = 0

        self.accounts[customer.name] += points

        return points   
    
    def redeem_points(self, customer: Customer, points_to_redeem: int) -> None:
        """Redeem loyalty points from a customer's account.

        Args:
            customer: The customer redeeming points.
            points_to_redeem: Number of points to redeem.

        Raises:
            InsufficientPointsError: If the customer does not have enough points.
        """
        current_points = self.accounts.get(customer.name, 0)

        if current_points < points_to_redeem:
            raise InsufficientPointsError(
                f"{customer.name} has {current_points} points, "
                f"but {points_to_redeem} are required."
            )

        self.accounts[customer.name] -= points_to_redeem
    
class Order:
    """Represent a customer's coffee order."""

    MEMBER_DISCOUNT = 0.10

    def __init__(
        self,
        customer: Customer,
        staff_order: bool = False
    ) -> None:
        """Initialize an order.

        Args:
            customer: The customer placing the order.
            staff_order: Whether the order is a staff order.
        """
        self.customer = customer
        self.staff_order = staff_order
        self.items: list[OrderItem] = []
        
    def add_item(self, order_item: OrderItem) -> None:
        """Add a customized item to the order.

        Args:
            order_item: The customized item to add.
        """
        self.items.append(order_item)

    def total(self) -> float:
        """Calculate the order total.

        Returns:
            The total price of the order, including any member discount.
        """
        if self.staff_order:
            return 0.0

        total = sum(item.price() for item in self.items)

        if self.customer.member:
            total *= 1 - self.MEMBER_DISCOUNT

        return total
    
    def earn_loyalty_points(self, loyalty_program: LoyaltyProgram) -> int:
        """Award loyalty points for this order.

        Args:
            loyalty_program: The loyalty program to award points through.

        Returns:
            The number of points earned.
        """
        order_total = self.total()
        return loyalty_program.earn_points(self.customer, order_total)
    
    def redeem_free_drink(
        self,
        loyalty_program: LoyaltyProgram,
        order_item: OrderItem
    ) -> None:
        """Redeem loyalty points for a free small drink.

        Args:
            loyalty_program: The loyalty program used for redemption.
            order_item: The order item being made free.

        Raises:
            InvalidCustomizationError: If the drink is not small.
            InsufficientPointsError: If the customer lacks enough points.
        """
        if order_item.size != "small":
            raise InvalidCustomizationError(
                "Free drinks must be small size."
            )

        loyalty_program.redeem_points(
            self.customer,
            loyalty_program.free_drink_points
        )
        order_item.is_free = True
    
class SalesTracker:
    """Track completed coffee shop orders and sales."""

    def __init__(self) -> None:
        """Initialize the sales tracker."""
        self.orders: list[Order] = []

    def record_order(self, order: Order) -> None:
        """Record a completed order.

        Args:
            order: The completed order to record.
        """
        self.orders.append(order)

    def order_count(self) -> int:
        """Return the number of recorded orders.

        Returns:
            The total number of recorded orders.
        """
        return len(self.orders)

    def total_sales(self) -> float:
        """Calculate total sales from recorded orders.

        Returns:
            The total sales amount.
        """
        return sum(order.total() for order in self.orders)

    def average_order(self) -> float:
        """Calculate the average order value.

        Returns:
            The average order value, or 0 if there are no orders.
        """
        if not self.orders:
            return 0.0

        return self.total_sales() / self.order_count()
    
class DailySalesReport:
    """Generate reports from tracked coffee shop orders."""

    def __init__(self, tracker: SalesTracker) -> None:
        """Initialize the daily sales report.

        Args:
            tracker: The sales tracker containing completed orders.
        """
        self.tracker = tracker

    def generate_report(self) -> str:
        """Generate a text summary of daily sales.

        Returns:
            A formatted sales report.
        """
        return (
            f"Orders: {self.tracker.order_count()}\n"
            f"Sales: ${self.tracker.total_sales():.2f}\n"
            f"Average order: ${self.tracker.average_order():.2f}"
        )

    def save_to_file(self, filename: str) -> None:
        """Save the daily sales report to a file.

        Args:
            filename: The file to save the report to.
        """
        with open(filename, "a") as file:
            file.write(self.generate_report() + "\n")
    
