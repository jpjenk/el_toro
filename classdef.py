class Market():
    """Process and store share orders."""

    def __init__(self):
        """Define internal structures for object instance."""
        from collections import OrderedDict

        # The total shares available for each side of the ledger, bid "B"
        # and sale "S"
        self.shares = dict(B=0, S=0)

        # The running ledger of buy and sell order details
        self.orders = OrderedDict()

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
        from collections import OrderedDict

        # Add the order details as an n-tuple to the ledger dictionary
        self.orders[order_id] = (price, size, side)

        # Increase the shares available on the appropriate side
        self.shares[side] += size

        # Sort book into a list then recast as an ordered dictionary
        sorted_orders = sorted(self.orders.items(), key=lambda v: v[1])
        self.orders = OrderedDict(sorted_orders)

    def reduce(self, order_id, size):
        """Reduce shares from an existing order.

        :param order_id: Unique order identifier
        :param size: Number of shares
        :type order_id: str
        :type size: int

        """
        from collections import OrderedDict

        # Decrease the number of shares available on the appropriate side.
        # If an order is missing due to an earlier input message error,
        # the reduce order will fail gracefully.
        try:
            side = self.orders.get(order_id)[2]
            self.shares[side] -= size
        except TypeError as e:
            return

        # Remove the add order if the reduction order is the same size
        if self.orders.get(order_id)[1] <= size:
            self.orders.pop(order_id, None)

        # Decrease the share size of the add order if reduce order is smaller
        else:
            self.orders[order_id] = (self.orders.get(order_id)[0],
                                     self.orders.get(order_id)[1] - size,
                                     self.orders.get(order_id)[2])

        # Sort book into a list then recast as an ordered dictionary
        sorted_orders = sorted(self.orders.items(), key=lambda v: v[1])
        self.orders = OrderedDict(sorted_orders)

    def trade(self, target, action):
        """Calculate the expense or income incurred when buying or
        selling a specified number of shares.

        :param target: Number of shares to trade
        :param action: Type of trade to calculate, 'buy' or 'sell'
        :return total: Calculated expense or income
        :type target: int
        :type action: str
        :rtype total: float

        .. note::
            orders is a dictionary of tuples in the form,
            {order_id: (price, size, side),  ...}

            here it is reduced to sorted ledger side in the form,
            column = [(price, size), ...]

        """

        total = 0
        column = list()

        # Build a list of (price, size) tuples for the specified ledger side
        order_details = self.orders.values()
        side = 'S' if action == 'buy' else 'B'
        for order in order_details:
            if order[2] == side:
                column.append((order[0], order[1]))

        # Ledger column is sorted low-high, reverse this for sell pricing
        if action == 'sell':
            column = list(reversed(column))

        # Loop over sorted orders until target shares acquired
        for order in column:

            available_shares = order[1]
            price = order[0]

            debit_shares = min(available_shares, target)
            total = round(total + (price * debit_shares), 2)

            target = target - debit_shares

            if target == 0:
                break

        return total
