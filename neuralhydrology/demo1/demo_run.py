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

    def execute(self) -> None:
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

        # print('Waiting 3 seconds')
        # time.sleep(3)
        self._run_training()
        self._run_testing()

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

    def _run_training(self):
        """"""
        pass

    def _run_testing(self):
        """"""
        pass

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
