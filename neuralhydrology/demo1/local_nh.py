"""Runs neural hydrology demos in local file system."""

import argparse
import os
import pathlib
import pickle

# Hard coded number of epochs; must must config.yaml file
EPOCHS = 50

from neuralhydrology import nh_run

class LocalNH:
    def __init__(self, args: argparse.Namespace):
        """Calling code responsible for argument checking."""
        self.args = args
        self.scratch_dir = pathlib.Path(self.args.experiments_root_dir) / '.scratch'

    def run_training(self) -> str:
        """Runs training based on passed in configuration.

        Returns run_id
        """
        # Set up experiment directory as cwd
        basin_dir = pathlib.Path(self.args.experiments_root_dir) / self.args.basin_id
        basin_dir.mkdir(exist_ok=True)
        os.chdir(basin_dir)

        # Generate basin.txt file
        txt_path = self.scratch_dir / 'basin.txt'
        with open(txt_path, 'w') as fp:
            fp.write(self.args.basin_id)

        # yml file already set up
        # Todo generate yml file here
        yml_path = self.scratch_dir / 'basin.yml'
        nh_run.start_run(yml_path)
        # ?Also run validation?

        # Todo get run id
        return 'todo run_id'

    def run_testing(self) -> dict:
        """"""
        exp_dir = pathlib.Path(self.args.experiments_root_dir)
        run_dir = exp_dir / self.args.basin_id / 'runs' / self.args.run_id
        # print(f'{run_dir=}')
        nh_run.eval_run(run_dir, 'test')

        # Get the results file and return dataset
        eps = f'{EPOCHS:03d}'
        results_path = run_dir / f'test/model_epoch{eps}/test_results.p'
        with open(results_path, 'rb') as fp:
            file_dict = pickle.load(fp)
            basin_dict = file_dict.get(self.args.basin_id, {})
            oned_dict = basin_dict.get('1D', {})
            return oned_dict

        # If we reached here, didn't get the results data
        return dict()
