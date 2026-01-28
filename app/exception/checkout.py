class CartItemError(Exception):
    pass

class PaymentFailedError(CartItemError):
    pass

class PaymentError(CartItemError):
    pass

class OrderError(CartItemError):
    pass

class InsufficientStockError(CartItemError):
    pass

class PaymentAmountMismatch(CartItemError):
    pass

class AddressIdError(CartItemError):
    pass

class RazorpayPaymentFailed(CartItemError):
    pass