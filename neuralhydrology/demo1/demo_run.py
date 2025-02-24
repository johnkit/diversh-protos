"""
This module provides a DemoRun class for performing neural hydrology modeling.

Uses container operations.
"""

import pathlib
import subprocess
import tempfile

from .constants import RUN_ID_FILENAME

CONTAINER_NAME = 'demo1.run'
DEFAULT_ENGINE = 'docker'

class DemoRun:
    """A class for performing container-based hydrology operations.
    """
    def __init__(self,
            image_name: str,
            data_directory: str|pathlib.Path,
            engine: str=DEFAULT_ENGINE,
            verbose: bool=False,
            ):
        self.data_dir = data_directory
        self.image_name = image_name
        self.engine = engine
        self.verbose = verbose

    def is_image_available(self) -> bool|None:
        """Checks if image is in the container-engine store.

        Returns one of:
            * True if the image is available locally.
            * False otherwise
            * None on error
        """
        print(f'Checking for docker image {self.image_name}')
        try:
            result = subprocess.run(
                [self.engine, 'inspect', self.image_name],
                capture_output=True,
                text=True,
                check=False,  # Important: Do not raise exception on non-zero exit code
            )
            if result.returncode == 0:
                return True  # image found
            elif result.returncode == 1:
                return False
            else:
                print(f'Error inspecting image: {result.stderr}')
                return None
        except FileNotFoundError:
            print(f'Error: {self.engine} command not found')
            return None
        except Exception as e:
            print(f'Unexpected error occurred: {e}')
            return None

    def execute(self,
            basin_id: str,
            host_experiments_dir: pathlib.Path | str,
            epochs: int|None = None,
            keep_container=False) -> None:
        """"
        Carries out full model train & test:
        * Check for image
        * Check for and stop extant container
        * Start container
        * Run training
        * Run testing
        * Copy results
        * Stop the container

        Note: caller is responsible for making image available
        """
        # Future: ?check for image and pull if needed
        try:
            self._check_for_container()
            self._start_container()

            self._run_training(basin_id, epochs=epochs)
            run_id = self._get_run_id()
            self._run_testing(basin_id, run_id)
            self._copy_run_directory(basin_id, run_id, host_experiments_dir)
        except Exception:
            raise
        finally:
            if keep_container:
                print(f'Leaving container {CONTAINER_NAME} running')
            else:
                self._stop_container()

    def _check_for_container(self):
        """Checks for running container and stops it if found."""
        print(f'Checking for extant "{CONTAINER_NAME}" container')

        command = f'{self.engine} ps -a -f name={CONTAINER_NAME} -q'
        result = self._run_command(command)

        if result.stdout:
            print(f'Found running "{CONTAINER_NAME}" container => shutting down ')
            self._stop_container()

    def _start_container(self):
        """Runs container in detached mode."""
        print('Starting container...')
        command = f'{self.engine} run --gpus all --detach --restart always' + \
            f' --name {CONTAINER_NAME}' + \
            f' --mount type=bind,src={self.data_dir},dst=/data,readonly {self.image_name}' + \
            ' tail -f /dev/null'
        _result = self._run_command(command)

    def _run_training(self, basin_id: str, epochs: int = None):
        """Invokes the BasinNH.run_training method in the container."""
        print('Begin training sequence...')

        command = self._create_nh_command('train', basin_id, epochs=epochs)
        if self.verbose:
            print(f'{command=}')

        rc = self._run_command_with_output(command)
        if rc != 0:
            raise RuntimeError(f'Error: return code {rc}')

    def _get_run_id(self) -> str|None:
        """Gets run_id from from container file designated for this.

        This code hinges on the BasinNH.run_training() code in the container
        writing a file to the /experiments/.scratch directory. We should
        probably using a shared config file to keep the host and container
        in sync.
        """
        print('Retrieving last run_id from container...')

        # Training code in container writes run_id to file in scratch directory
        with tempfile.TemporaryDirectory() as temp_dir:
            src_file = f'/experiments/.scratch/{RUN_ID_FILENAME}'
            command = f'{self.engine} cp {CONTAINER_NAME}:{src_file} {temp_dir}'
            result = self._run_command(command)
            if result.returncode != 0:
                raise RuntimeError('Error: failed to retrieve run_id from container')

            run_id = None
            dst_path = pathlib.Path(temp_dir) / RUN_ID_FILENAME
            with open(dst_path) as fp:
                content = fp.read()
                if content.startswith('run_'):
                    run_id = content

        return run_id

    def _run_testing(self, basin_id: str, run_id: str):
        """Invokes the BasinNH.run_testing method in the container."""
        print(f'Begin testing sequence, {basin_id=}, {run_id=}...')

        command = self._create_nh_command('test', basin_id, run_id=run_id)
        if self.verbose:
            print(f'{command=}')

        rc = self._run_command_with_output(command)
        if rc != 0:
            raise RuntimeError(f'Error: return code {rc}')

    def _copy_run_directory(self,
                basin_id: str,
                run_id: str,
                host_experiments_dir: pathlib.Path):
        """Copies run directory to from container to host."""
        print(f'Copying run directory to host...')

        # Make sure runs dir is on host machine
        host_dir = host_experiments_dir / f'{basin_id}/runs'
        host_dir.mkdir(parents=True, exist_ok=True)

        run_dir = f'/experiments/{basin_id}/runs/{run_id}'
        command = f'{self.engine} cp {CONTAINER_NAME}:{run_dir} {str(host_dir)}'
        _result = self._run_command(command)

        host_run_dir = host_dir / run_id
        print(f'Wrote {host_run_dir}')

    def _stop_container(self):
        """Stops container."""
        print('Stopping container...')
        command = f'{self.engine} stop -t 5 {CONTAINER_NAME}'
        _result = self._run_command(command)
        command = f'{self.engine} rm {CONTAINER_NAME}'
        _result = self._run_command(command)

    def _run_command(self, command: str|list) -> subprocess.CompletedProcess:
        """"""
        cmd = command.split() if isinstance(command, str) else command
        result = None
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # print(f'{result=}')
        except subprocess.CalledProcessError as e:
            (f'Error: subprocess.run command failed with exit code {e.returncode}')
            raise
        except Exception:
            raise

        if self.verbose:
            print(f'{result=}')
        return result

    def _run_command_with_output(self, command: str | list) -> int:
        cmd = command.split() if isinstance(command, str) else command
        # Run process and capture live messages
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        rc = process.poll()
        return rc

    def _create_nh_command(self,
                step: str, basin_id: str, run_id: str = None, epochs: int = None) -> list:
        """"""
        python_command = [
            'python', 'local_main.py',
            '--step', step,
            '--data_dir', '/data',
            '--experiments_dir', '/experiments',
            '--basin_id', basin_id,
        ]
        if epochs:
            python_command += ['--training_epochs', str(epochs)]
        if run_id:
            python_command += ['--run_id', run_id]

        run_command = [self.engine, 'exec','-t', CONTAINER_NAME]
        return run_command + python_command
