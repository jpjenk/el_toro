class Market():
    """Process and store share orders."""

    def __init__(self):
        """Define internal structures for object instance."""

        self.shares = dict(bid=0, ask=0)
        self.orders = dict()


    def add(self, side, order_id, price, size):
        """Ingest a new buy or sell order."""

        self.orders[order_id] = (price, size)

        if side == 'B':
            self.shares['bid'] += size
        else:
            self.shares['ask'] += size


    def reduce(self, order_id, size):
        """Reduce shares from an existing order."""

        if self.orders[order_id][1] <= size:
            self.orders.pop(order_id)

        else:
            self.orders[order_id] = (self.orders[order_id][0],
                                     self.orders[order_id][1] - size)
