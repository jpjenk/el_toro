def parse_args(args):
    """Error check the command line parameter."""

    if len(args) == 1 or args[1] in ['-h', '--help']:
        print('Usage: pricer target-size < logfile\n')
        print('Trading logfile analyzer. Calculates', end=' ')
        print('cost and profit at the share target-size.')
        return False

    elif len(args) > 2:
        print('Too many parameters')
        return False

    else:
        try:
            target = int(args[1])
        except ValueError as e:
            print('Target-size must be an integer value')
            return False

    return target


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
