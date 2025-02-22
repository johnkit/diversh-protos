"""
This module defines the BasinNH class, which is used for training and testing
LSTM networks to model single watershed basin. It is a light wrapper around
the Google neural hydrology package.

The neural nydrology package uses the CAMEL-US dataset for historical weather
and streamflow records. It writes results to an experiments directory specified
in the input arguments.
"""

import argparse
import os
import pathlib
import pickle
import string

import xarray as xr

# Hard coded number of epochs; must match config.yaml file used for training
EPOCHS = 50

from neuralhydrology import nh_run

class BasinNH:
    """A class for running Google neural hydrology code for a single basin.
    """
    def __init__(self, args: argparse.Namespace):
        """
        Initializes a BasinNH object.

        Input args must include the following
        * data_dir - the root of the CAMELS-US dataset
        * experiments_dir - which must already exist
        * basin_id - 8 digit id of one entry in CAMELS-US
        * run_id - folder where model is stored (only required for testing steps)

        Note: The calling code responsible for argument checking.
        """
        self.args = args
        self.scratch_dir = pathlib.Path(self.args.experiments_dir) / '.scratch'

    def run_training(self) -> str:
        """Runs training based on passed in configuration.

        Returns run_id (or None)
        """
        # Set up experiment directory as cwd
        basin_dir = pathlib.Path(self.args.experiments_dir) / self.args.basin_id
        basin_dir.mkdir(exist_ok=True)
        os.chdir(basin_dir)

        # Generate basin.txt file
        txt_path = self.scratch_dir / 'basin.txt'
        with open(txt_path, 'w') as fp:
            fp.write(self.args.basin_id)

        # Generate basin.yml
        yml_path = self.scratch_dir / 'basin.yml'
        self._generate_config_file(yml_path)

        # Because nh generates the run directory internally, we don't have access to
        # the directory name used for the run. For now, we will infer the run_id by
        # finding the latest run directory in the basin directory.
        # We do this before and after training, to make sure that a new run directory
        # was in fact created.
        parent_dir = basin_dir / 'runs'
        last_run_id = self._get_latest_run_id(parent_dir)

        # Call start_run() which does training and validation
        nh_run.start_run(yml_path)

        # Get latest run_id which *should* be different than last_run_id
        next_run_id = self._get_latest_run_id(parent_dir)
        run_id = next_run_id if next_run_id != last_run_id else None
        return run_id

    def run_testing(self, write_nc: bool = True) -> xr.Dataset:
        """"""
        exp_dir = pathlib.Path(self.args.experiments_dir)
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

        # Sanity check
        if not oned_dict:
            return None

        # Add NSE as attribute on xaray
        xr_dataset = oned_dict.get('xr')
        nse = oned_dict.get('NSE')
        atts = dict(
            NSE=nse,
            basin=self.args.basin_id,
            run=self.args.run_id,
        )
        ds = xr_dataset.assign_attrs(atts)

        if write_nc:
            rel_path = f'test/model_epoch{eps}/test_results.nc'
            nc_path = run_dir / rel_path
            ds.to_netcdf(nc_path)

            head_path = f'{self.args.basin_id}/runs/{self.args.run_id}'
            print(f' Wrote {head_path}/{rel_path}')

        return ds

    def _generate_config_file(self, yml_path: pathlib.Path) -> None:
        """Generates basin.yml from template"""
        # Load the template file
        this_dir = pathlib.Path(__file__).parent
        template_path = this_dir / 'template.basin.yml'

        template = None
        with open(template_path) as fp:
            template_string = fp.read()
            template = string.Template(template_string)
        if template is None:
            raise RuntimeError(f'Failed to read yml tempalte {template_path}')
        basin_txt_path = self.scratch_dir / 'basin.txt'

        data_dir = pathlib.Path(self.args.data_dir).resolve()
        template_dict = dict(
            basin_txt_file=basin_txt_path.resolve(),
            data_dir=data_dir,
            )
        yml = template.substitute(template_dict)

        # Write basin.yml to scratch folder
        with open(yml_path, 'wt') as fp:
            fp.write(yml)

    def _get_latest_run_id(self, parent_dir: pathlib.Path) -> str | None:
        """Returns the most recent run_id in parent_dir."""
        if not parent_dir.is_dir():
            return None

        run_dirs = \
            [d for d in parent_dir.iterdir() if d.is_dir() and d.name.startswith('run_')]
        if not run_dirs:
            return None

        latest_dir = max(run_dirs, key=os.path.getctime)
        return latest_dir.name
