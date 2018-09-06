#!/usr/bin/env python3
"""Traded shares log file analyzer."""

import sys
import aux

def parse_log(line):
    """Decode log message line."""
    msg = line.split()

    if len(msg) == 6 and msg[1] == 'A':
        # Add order
        if msg[3] not in ['B', 'S']:
            print('Message skipped: Side value error')
            return None
        try:
            order = {'timestamp': int(msg[0]),
                     'order_type': msg[1],
                     'order_id': msg[2],
                     'side': msg[3],
                     'price': float(msg[4]),
                     'size': int(msg[5])}
            return order
        except ValueError as e:
            print(e)
            return None

    elif len(msg) == 4 and msg[1] == 'R':
        # Reduce order
        try:
            order = {'timestamp': int(msg[0]),
                     'order_type': msg[1],
                     'order_id': msg[2],
                     'size': int(msg[3])}
            return order
        except ValueError as e:
            print(e)
            return None

    else:
        # Message is incorrectly formatted
        return None


if __name__ == '__main__':

    target = aux.parse_args(sys.argv)
    if not target:
        sys.exit()

    for line in sys.stdin:
        order = parse_log(line)
