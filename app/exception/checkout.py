class CartItemError(Exception):
    pass

class PaymentFailedError(CartItemError):
    pass

class InsufficientStockError(CartItemError):
    pass

class PaymentAmountMismatch(CartItemError):
    pass

class AddressIdError(CartItemError):
    pass