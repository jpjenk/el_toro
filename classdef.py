class Market():
    """Process and store share orders."""

    def __init__(self):
        """Define internal structures for object instance."""

        # The total shares available for each side of the ledger, bid "B"
        # and sale "S"
        self.shares = dict(B=0, S=0)

        # The running ledger of buy and sell order details
        self.orders = dict()

    def add(self, side, order_id, price, size):
        """Ingest a new buy or sell order.

        :param side: Either bid "B" or sell "S"
        :param order_id: Unique order identifier
        :param price: Price offered or asked for a share
        :param size: Number of shares
        :type side: str
        :type order_id: str
        :type price: float
        :type size: int

        """

        # Add the order details as an n-tuple to the ledger dictionary
        self.orders[order_id] = (price, size, side)

        # Increase the shares available on the appropriate side
        self.shares[side] += size

    def reduce(self, order_id, size):
        """Reduce shares from an existing order.

        :param order_id: Unique order identifier
        :param size: Number of shares
        :type order_id: str
        :type size: int

        """

        # Decrease the number of shares available on the appropriate side
        side = self.orders.get(order_id)[2]
        self.shares[side] -= size

        # Remove the add order if the reduction order is the same size 
        if self.orders.get(order_id)[1] <= size:
            self.orders.pop(order_id, None)

        # Decrease the share size of the add order if reduce order is smaller
        else:
            self.orders[order_id] = (self.orders.get(order_id)[0],
                                     self.orders.get(order_id)[1] - size,
                                     self.orders.get(order_id)[2])
