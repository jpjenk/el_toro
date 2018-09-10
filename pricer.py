#!/usr/bin/env python3
"""Traded shares log file analyzer."""

import sys
import aux
from classdef import Market


if __name__ == '__main__':

    # Two sided ledger book
    book = Market()

    # Tracks the value of the last issued sell (income) or buy (expense)
    last_price = dict(sell=0, buy=0)

    # Tracks whether a price has been issued or has been invalidates
    standing_price = dict(sell=False, buy=False)

    # Maps a sell or buy action to the correct side of the leger
    side = dict(sell='B', buy='S')

    # Exit if runtime argument error or help requested
    try:
        target = aux.parse_args(sys.argv)
    except ValueError as e:
        print(e.args[0])
        sys.exit()

    for line in sys.stdin:

        # Read message from logfile, skip if there are formatting errors
        try:
            order = aux.parse_log(line)
        except ValueError as e:
            sys.stderr.write('{0:s}: {1:s}\n'.format(e.args[0], line))
            continue

        # Modify the book based on incomming message
        if order['order_type'] == 'A':
            book.add(side=order['side'],
                     order_id=order['order_id'],
                     price=order['price'],
                     size=order['size'])

        elif order['order_type'] == 'R':
            book.reduce(order_id=order['order_id'],
                        size=order['size'])

        # Run pricing logic for both sides of the ledger
        for action in ['sell', 'buy']:

            if standing_price[action]:

                # Update existing pricing message if change
                if book.shares[side[action]] >= target:
                    total = book.trade(target=target, action=action)
                    if total != last_price[action]:
                        last_price[action] = total
                        aux.emit(ts=order['timestamp'],
                                 action=action,
                                 msg=total)

                # Cancel pricing, sale or buy no longer possible
                else:
                    aux.emit(ts=order['timestamp'],
                             action=action,
                             msg=None)
                    standing_price[action] = False

            elif not standing_price[action]:

                # Resume pricing availability
                if book.shares[side[action]] >= target:
                    total = book.trade(target=target, action=action)
                    standing_price[action] = True
                    last_price[action] = total
                    aux.emit(ts=order['timestamp'],
                             action=action,
                             msg=total)
