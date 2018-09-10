#!/usr/bin/env python3
"""Traded shares log file analyzer."""

import sys
import aux
from classdef import Market


if __name__ == '__main__':

    book = Market()
    last_sell = 0
    last_buy = 0
    last_ts = 0
    standing = dict(sell=False, buy=False)

    target = aux.parse_args(sys.argv)
    if not target:
        sys.exit()

    for line in sys.stdin:

        order = aux.parse_log(line)

        # Skip if log message has formatting errors
        if not order:
            sys.stderr.write('Message error: {0:s}\n'.format(line))
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

        # Run pricing logic if all simultaneous messages recieved
        ts = order['timestamp']

        if standing['sell']:
            if book.shares['B'] >= target:
                total = book.trade(target=target, action='sell')
                if total != last_sell:
                    last_sell = total
                    print('{0:d} S {1:0.2f}'.format(ts, total))
            else:
                print('{0:d} S NA'.format(ts))
                standing['sell'] = False

        elif not standing['sell']:
            if book.shares['B'] >= target:
                total = book.trade(target=target, action='sell')
                standing['sell'] = True
                last_sell = total
                print('{0:d} S {1:0.2f}'.format(ts, total))

        if standing['buy']:
            if book.shares['S'] >= target:
                total = book.trade(target=target, action='buy')
                if total != last_buy:
                    last_buy = total
                    print('{0:d} B {1:0.2f}'.format(ts, total))
            else:
                standing['buy'] = False
                print('{0:d} B NA'.format(ts))

        elif not standing['buy']:
            if book.shares['S'] >= target:
                total = book.trade(target=target, action='buy')
                standing['buy'] = True
                last_buy = total
                print('{0:d} B {1:0.2f}'.format(ts, total))
