"""
This script uses the demo1 container image to train and test neuralhyrology models.

On turtleland4, use venv ~/.py3-venv/neuralhydrology
"""

import argparse
import pathlib
import sys

from demo1.args_utils import add_standard_arguments, validate_inputs
from demo1.demo_run import DemoRun

# Container image constants
#[registry-hostname]/[username/organization-name]/[image-name]:[tag]
IMAGE_REGISTRY_USER = 'ghcr.io/johnkit'
IMAGE_NAME = 'neuralhydrology/demo1:1.0.0'

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

    image = IMAGE_NAME if args.local_image_build else f'{IMAGE_REGISTRY_USER}/{IMAGE_NAME}'
    runner = DemoRun(image, args.data_dir, verbose=args.verbose)
    if not runner.is_image_available():
        print()
        if args.local_image_build:
            print(f'Container image not found: {image}')
        else:
            print('Container image not found')
            print(f'In a terminal run `docker pull {image}` and rerun this script')
        sys.exit(1)

    print(f'Container image was found: {image}')
    runner.execute(
        args.basin_id,
        pathlib.Path(args.experiments_dir),
        epochs=args.training_epochs,
        keep_container=args.keep_container,
        )

if __name__ == '__main__':
    main()
