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
    standing_buy = False
    last_buy = 0

    target = aux.parse_args(sys.argv)
    if not target:
        sys.exit()

    for line in sys.stdin:

        order = parse_log(line)

        if not order:
            sys.stderr.write('Message error: {0:s}\n'.format(line))
            continue

        if order['order_type'] == 'A':
            book.add(side=order['side'],
                     order_id=order['order_id'],
                     price=order['price'],
                     size=order['size'])

        elif order['order_type'] == 'R':
            book.reduce(order_id=order['order_id'],
                        size=order['size'])

        if standing_sell:
            if book.shares['B'] >= target:
                total = book.trade(target=target, buy=False)
                if total != last_sell:
                    print('{0:d} S {1:0.2f}'
                          .format(order['timestamp'], total))
                    last_sell = total
            else:
                print('{0:d} S NA'.format(order['timestamp']))
                last_sell = 0
                standing_sell = False

        elif not standing_sell:
            if book.shares['B'] >= target:
                total = book.trade(target=target, buy=False)
                print('{0:d} S {1:0.2f}'
                      .format(order['timestamp'], total))
                standing_sell = True
                last_sell = total

        if standing_buy:
            if book.shares['S'] >= target:
                total = book.trade(target=target, buy=True)
                if total != last_buy:
                    print('{0:d} B {1:0.2f}'
                          .format(order['timestamp'], total))
                    last_buy = total
            else:
                print('{0:d} B NA'.format(order['timestamp']))
                last_buy = 0
                standing_buy = False

        elif not standing_buy:
            if book.shares['S'] >= target:
                total = book.trade(target=target, buy=True)
                print('{0:d} B {1:0.2f}'
                      .format(order['timestamp'], total))
                standing_buy = True
                last_buy = total




        #  if book.shares['S'] >= target:
        #      pass
        #      #  total = book.trade(target=target, buy=True)
        #      #  print('{0:d} B {1:0.2f}'.format(order['timestamp'], total))
        #  else:
        #      pass
