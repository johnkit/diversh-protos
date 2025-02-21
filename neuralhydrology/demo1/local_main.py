"""
This script uses the BasinNH class to train and test neuralhyrology models.
"""

import argparse
import pathlib
import sys

# Optional filename for command line args
ARGS_FILENAME = '.args.txt'

from args_utils import add_standard_arguments, validate_inputs

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=f'Note: You can also put arguments in {ARGS_FILENAME} file',
        fromfile_prefix_chars='@')
    add_standard_arguments(parser)

    # Include ARGS_FILENAME if present
    file_args = [f'@{ARGS_FILENAME}'] if pathlib.Path(ARGS_FILENAME).exists() else []
    args = parser.parse_args(sys.argv[1:] + file_args)
    # print(args)

    try:
        validate_inputs(args)
    except Exception as e:
        print(f'Error: {e}')
        print('Exiting')
        sys.exit(2)

    # Ask if user is ready
    if not args.yes:
        reply = input(f'Ready to proceed with {args.step} step [y/N]? ')
        if not reply or reply[0] not in ['y', 'Y']:
            print('Exiting')
            sys.exit(0)

    # Import BasinNH here, just so that we run argparse without the delay
    print('Importing BasinNH')
    from basin_nh import BasinNH

    nh = BasinNH(args)
    if args.step == 'train':
        run_id: str = nh.run_training()
        print(f'Training returned {run_id=}')
    elif args.step == 'test':
        results_ds = nh.run_testing()
        print('Testing returned dataset:')
        print(results_ds)
    else:
        print(f'Unrecognized step argument {args.step}')


if __name__ == '__main__':
    main()
