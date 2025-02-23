"""
This script uses the demo1 container image to train and test neuralhyrology models.
"""

import argparse
import pathlib
import sys

from demo1.args_utils import add_standard_arguments, validate_inputs
from demo1.demo_run import DemoRun

# Container image constants
#[registry-hostname]/[username/organization-name]/[image-name]:[tag]
IMAGE_REGISTRY_USER = 'ghcr.io/johnkit'
IMAGE_NAME = 'nh/demo1:latest'

# Optional filename for command line args
ARGS_FILENAME = '.args.txt'

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=f'Note: You can also put arguments in {ARGS_FILENAME} file',
        fromfile_prefix_chars='@')
    add_standard_arguments(parser)
    parser.add_argument('-l', '--local_image_build', action='store_true',
        help='use locally built docker image')
    parser.add_argument('-k', '--keep_container', action='store_true',
        help='keep container running (dont stop)')

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

    # name_tag = f'{IMAGE_NAME}:{IMAGE_TAG}'
    runner = DemoRun(IMAGE_NAME, args.data_dir, verbose=args.verbose)
    if not runner.is_image_available():
        if args.local_image_build:
            print(f'container image not available: {IMAGE_NAME}')
            sys.exit(1)
        else:
            print('Future: add code to fetch image')
            sys.exit(1)

    print('Image was found!')
    runner.execute(
        args.basin_id,
        pathlib.Path(args.experiments_dir),
        epochs=args.training_epochs,
        keep_container=args.keep_container,
        )

if __name__ == '__main__':
    main()
