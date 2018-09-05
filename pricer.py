#!/usr/bin/env python3
"""Traded shares log file analyzer."""

import sys


def parse_args(args):
    """Error check the command line parameter."""

    if len(args) == 1 or args[1] in ['-h', '--help']:
        print('Traded shares log file analyzer')
        print('  usage: pricer [target-size]\n')
        print('  where target-size is an integer representing ')
        print('  the volume threshold for buying and selling shares.')
        sys.exit()
    elif len(args) > 2:
        print('Too many parameters')
        sys.exit()
    else:
        try:
            target = int(args[1])
        except ValueError as e:
            print('Target-size must be an integer value')
            sys.exit()

    return target


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

    target = parse_args(sys.argv)

    for line in sys.stdin:
        order = parse_log(line)
