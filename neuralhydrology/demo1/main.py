"""Run neuralhyrology in local environment"""

print('Loading')

import argparse
import pathlib
import string
import sys

from local_nh import LocalNH

# Optional filename for command line args
ARGS_FILENAME = '.args.txt'


def validate_inputs(args):
        # Check that data_dir exists
    camels_path = pathlib.Path(args.data_dir)
    if not camels_path.exists():
        raise FileNotFoundError(f'data_dir not found: {camels_path}')

    # Check for valid basin_id
    if len(args.basin_id) != 8:
        raise ValueError(f'Invalid basin id {args.basin_id} - must be 8 digits')

    if args.step == 'test' and args.run_id is None:
        raise ValueError('No run_id argument. Must be provided for test step')

    # Check for basin_id in camels (data_dir); streamflow file should be sufficient
    pattern = f'usgs_streamflow/*/{args.basin_id}*.txt'
    matches = camels_path.glob(pattern)
    try:
        first_match = next(matches)
    except StopIteration:
        raise FileNotFoundError(f'Unable to find base {args.basin_id} in CAMELS data')

    # Make sure experiments_dir exists
    exp_root_dir = pathlib.Path(args.experiments_root_dir)
    scratch_dir = exp_root_dir / '.scratch'
    if not exp_root_dir.exists():
        if not args.yes:
            print(f'experiments root path {exp_root_dir} does not exist')
            reply = input('OK to create [y/N]? ')
            if not reply or reply[0] not in ['y', 'Y']:
                print('Exiting')
                sys.exit(0)
        print(f'Creating {exp_root_dir}')
        # Create .scratch folder too
        scratch_dir.mkdir(parents=True)

    # Generate basin.yml from template
    this_dir = pathlib.Path(__file__).parent
    template_path = this_dir / 'template.basin.yml'
    template = None
    with open(template_path) as fp:
        template_string = fp.read()
        template = string.Template(template_string)
    if template is None:
        raise RuntimeError(f'Failed to read yml tempalte {template_path}')
    basin_txt_path = scratch_dir / 'basin.txt'
    template_dict = dict(
        basin_txt_file=basin_txt_path.resolve(),
        data_dir=camels_path.resolve()
        )
    yml = template.substitute(template_dict)

    # Write basin.yml to scratch folder
    yml_path = scratch_dir / 'basin.yml'
    with open(yml_path, 'wt') as fp:
        fp.write(yml)

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=f'Note: You can also put arguments in {ARGS_FILENAME} file',
        fromfile_prefix_chars='@')

    parser.add_argument('-s', '--step',
        required=True, choices=['train', 'test'], help='Required: select train or test')
    parser.add_argument('-d', '--data_dir', required=True, help='Path to CAMELS_US dataset')
    parser.add_argument('-e', '--experiments_root_dir', required=True,
        help='Required: root path for output data')
    parser.add_argument('-b', '--basin_id', required=True, help='Basin id')
    parser.add_argument('-r', '--run_id',
        help='Run id for model (required for test step, not used for training)')
    parser.add_argument('-y', '--yes', action='store_true', help='Run without confirmation')

    # Include ARGS_FILENAME if present
    file_args = [f'@{ARGS_FILENAME}' if pathlib.Path(ARGS_FILENAME).exists() else []]
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

    nh = LocalNH(args)
    retval = nh.run()
    print(f'run() returned {retval}')


if __name__ == '__main__':
    print('Starting execution')
    main()
