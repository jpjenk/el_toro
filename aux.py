def parse_args(args):
    """Error check the command line parameter."""
    import sys

    if len(args) == 1 or args[1] in ['-h', '--help']:
        print('Usage: pricer target-size < logfile\n')
        print('Trading logfile analyzer. Calculates', end=' ')
        print('expense and profit at the share target-size.')
        sys.exit()

    elif len(args) > 2:
        raise ValueError('Too many parameters')

    else:
        try:
            target = int(args[1])
        except ValueError as e:
            raise ValueError('Target-size must be an integer value')

    return target


def parse_log(line):
    """Decode log message line."""

    msg = line.split()

    if len(msg) == 6 and msg[1] == 'A':

        # Add order
        if msg[3] not in ['B', 'S']:
            raise ValueError('Order message is not a B or S')
        try:
            order = {'timestamp': int(msg[0]),
                     'order_type': msg[1],
                     'order_id': msg[2],
                     'side': msg[3],
                     'price': float(msg[4]),
                     'size': int(msg[5])}
            return order
        except ValueError as e:
            raise ValueError('Type error in message')

    elif len(msg) == 4 and msg[1] == 'R':

        # Reduce order
        try:
            order = {'timestamp': int(msg[0]),
                     'order_type': msg[1],
                     'order_id': msg[2],
                     'size': int(msg[3])}
            return order
        except ValueError as e:
            raise ValueError('Type error in message')

    else:
        raise ValueError('Incorrect message format')


def emit(ts, action, msg):
    """Print pricing message to stdout."""

    symbol = dict(sell='S', buy='B')

    if msg:
        print('{0:d} {1:s} {2:0.2f}'.format(ts, symbol[action], msg))

    else:
        print('{0:d} {1:s} NA'.format(ts, symbol[action]))
