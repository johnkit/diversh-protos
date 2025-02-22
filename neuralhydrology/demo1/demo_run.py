"""
This module provides a DemoRun class for performing neural hydrology modeling.

Uses container operations.
"""

import pathlib
import subprocess
import time

CONTAINER_NAME = 'demo1.run'
DEFAULT_ENGINE = 'docker'

class DemoRun:
    """A class for performing container-based hydrology operations.
    """
    def __init__(self,
            container_image: str,
            data_directory: str|pathlib.Path,
            engine: str=DEFAULT_ENGINE,
            verbose: bool=False,
            ):
        self.data_dir = data_directory
        self.image_name = container_image
        self.engine = engine
        self.verbose = verbose

    def is_image_available(self) -> bool|None:
        """Checks if image is in the container-engine store.

        Returns one of:
            * True if the image is available locally.
            * False otherwise
            * None on error
        """
        if self.verbose:
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

    def execute(self, basin_id: str, keep_container=False) -> None:
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
        self._check_for_container()
        self._start_container()

        run_id = self._run_training(basin_id)
        self._run_testing(run_id)

        if keep_container:
            print(f'Leaving container {CONTAINER_NAME} running')
        else:
            self._stop_container()

    def _check_for_container(self):
        """Checks for running container and stops it if found."""
        if self.verbose:
            print(f'Checking for extant "{CONTAINER_NAME}" container')

        command = f'{self.engine} ps -a -f name={CONTAINER_NAME} -q'
        result = self._run_command(command)

        if result.stdout:
            print(f'Found running "{CONTAINER_NAME}" container => shutting down ')
            self._stop_container()

    def _start_container(self):
        """Runs container in detached mode."""
        if self.verbose:
            print('Starting container...')
        command = f'{self.engine} run --gpus all --detach --restart always' + \
            f' --name {CONTAINER_NAME}' + \
            f' --mount type=bind,src={self.data_dir},dst=/data,readonly {self.image_name}' + \
            ' tail -f /dev/null'
        _result = self._run_command(command)

    def _run_training(self, basin_id: str) -> str:
        """"""
        command = self._create_nh_command('train', basin_id)
        if self.verbose:
            print(f'{command=}')

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
        print(f'return code {rc}')

        return 'run_1111_2222'

    def _run_testing(self, run_id: str):
        """"""
        print('Testing TBD')

    def _stop_container(self):
        """Stops container."""
        if self.verbose:
            print('Stopping container...')
        command = f'{self.engine} stop -t 5 {CONTAINER_NAME}'
        _result = self._run_command(command)
        command = f'{self.engine} rm {CONTAINER_NAME}'
        _result = self._run_command(command)

    def _run_command(self, command: str|list) -> None:
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

    def _create_nh_command(self, step: str, basin_id: str, run_id: str = None) -> list:
        """"""
        python_command = [
            'python', 'local_main.py',
            '--step', step,
            '--data_dir', '/data',
            '--experiments_dir', '/experiments',
            '--basin_id', basin_id,
        ]
        if run_id is not None:
            command += ['--run_id', run_id]

        run_command = [
            self.engine, 'run', '--rm', '-t', '--gpus', 'all',
            '--mount', f'type=bind,src={self.data_dir},dst=/data,readonly',
            'nh/demo1',
        ]
        return run_command + python_command
