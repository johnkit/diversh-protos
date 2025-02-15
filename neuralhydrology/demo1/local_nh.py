"""Runs neural hydrology demos in local file system."""

import argparse
import os
import pathlib

from neuralhydrology import nh_run

class LocalNH:
    def __init__(self, args: argparse.Namespace):
        """Calling code responsible for argument checking."""
        self.args = args
        self.scratch_dir = pathlib.Path(self.args.experiments_root_dir) / '.scratch'

    def run(self) -> bool:
        """"""
        # Set up experiment directory as cwd
        exp_dir = pathlib.Path(self.args.experiments_root_dir) / self.args.basin_id
        exp_dir.mkdir(exist_ok=True)
        os.chdir(exp_dir)

        # Generate basin.txt file
        txt_path = self.scratch_dir / 'basin.txt'
        with open(txt_path, 'w') as fp:
            fp.write(self.args.basin_id)

        # Run the step
        if self.args.step == 'train':
            self.run_training()
        elif self.args.step == 'test':
            self.run_testing()
        else:
            raise NotImplementedError(f'Unrecognized step {self.args.step}')

    def run_training(self) -> bool:
        # raise NotImplementedError(f'Todo {__class__}.run_training()')
        yml_path = self.scratch_dir / 'basin.yml'
        retval = nh_run.start_run(yml_path)
        return retval


    def run_testing(self) -> bool:
        raise NotImplementedError(f'Todo {__class__}.run_testing()')
