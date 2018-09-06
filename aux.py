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
