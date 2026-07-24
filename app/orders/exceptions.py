class OrderException(Exception):
    def __init__(self, order_id: str):
        self.order_id = order_id

class OrderNotFound(OrderException):
    pass


class InvalidOrderTransition(OrderException):
    pass


class OrderAlreadyPaid(InvalidOrderTransition):
    pass


class CancelledOrderCannotBePaid(InvalidOrderTransition):
    pass


class ShippedOrderCannotBePaid(InvalidOrderTransition):
    pass