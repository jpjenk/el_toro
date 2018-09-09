#!/usr/bin/env python3
"""Traded shares log file analyzer."""

import sys
import aux
from classdef import Market


def parse_log(line):
    """Decode log message line."""
    msg = line.split()

    if len(msg) == 6 and msg[1] == 'A':
        # Add order
        if msg[3] not in ['B', 'S']:
            return False
        try:
            order = {'timestamp': int(msg[0]),
                     'order_type': msg[1],
                     'order_id': msg[2],
                     'side': msg[3],
                     'price': float(msg[4]),
                     'size': int(msg[5])}
            return order
        except ValueError as e:
            return False

    elif len(msg) == 4 and msg[1] == 'R':
        # Reduce order
        try:
            order = {'timestamp': int(msg[0]),
                     'order_type': msg[1],
                     'order_id': msg[2],
                     'size': int(msg[3])}
            return order
        except ValueError as e:
            return False

    else:
        # Message is incorrectly formatted
        return False


if __name__ == '__main__':

    book = Market()
    standing_sell = False
    last_sell = 0
    sell_msg = None
    standing_buy = False
    last_buy = 0
    buy_msg = None
    last_ts = 0

    target = aux.parse_args(sys.argv)
    if not target:
        sys.exit()

    for line in sys.stdin:

        order = parse_log(line)

        # Skip if log message has formatting errors
        if not order:
            print('parse error')
            sys.exit()
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

        if standing_sell:
            if book.shares['B'] >= target:
                total = book.trade(target=target, buy=False)
                if total != last_sell:
                    last_sell = total
                    print('{0:d} S {1:0.2f}'.format(ts, total))
            else:
                print('{0:d} S NA'.format(ts))
                #  last_sell = 0
                standing_sell = False

        elif not standing_sell:
            if book.shares['B'] >= target:
                total = book.trade(target=target, buy=False)
                standing_sell = True
                last_sell = total
                print('{0:d} S {1:0.2f}'.format(ts, total))

        if standing_buy:
            if book.shares['S'] >= target:
                total = book.trade(target=target, buy=True)
                #  print(last_buy, total)
                if total != last_buy:
                    last_buy = total
                    print('{0:d} B {1:0.2f}'.format(ts, total))
            else:
                #  last_buy = 0
                standing_buy = False
                print('{0:d} B NA'.format(ts))

        elif not standing_buy:
            if book.shares['S'] >= target:
                total = book.trade(target=target, buy=True)
                standing_buy = True
                last_buy = total
                print('{0:d} B {1:0.2f}'.format(ts, total))
