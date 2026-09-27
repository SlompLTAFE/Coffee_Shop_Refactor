class CoffeeShopError(Exception):
    """Base exception for all coffee shop errors."""
    pass


class OrderError(CoffeeShopError):
    """Base exception for order-related errors."""
    pass


class InvalidItemError(OrderError):
    """Raised when an item does not exist on the menu."""
    pass


class InvalidCustomizationError(OrderError):
    """Raised when a customization is not available."""
    pass

class PaymentError(CoffeeShopError):
    """Base exception for payment-related errors."""
    pass


class InsufficientPointsError(PaymentError):
    """Raised when loyalty points are insufficient for redemption."""
    pass