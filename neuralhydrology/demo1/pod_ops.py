"""
This module provides a PodOps class for performing container operations.

Parts of this class are hard-coded to match the nh/demo1 docker image.
The implementation is brute force, running a separate subprocess for each method.
"""

import pathlib
import subprocess

# Default parameters that will move to application script
DEFAULT_ENGINE = 'docker'
LOCAL_IMAGE = 'nh/demo1:latest'
GITHUB_IMAGE_URl = None


class PodOps:
    """A class for performing container-based operations.
    """
    def __init__(self,
            data_directory: str|pathlib.Path,
            image:str=LOCAL_IMAGE,
            engine:str=DEFAULT_ENGINE
            ):
        self.data_dir = data_directory
        self.image_name = image
        self.engine = engine

    def is_image_available(self) -> bool|None:
        """Checks if image is in the container-engine store.

        Returns one of:
            * True if the image is available locally.
            * False otherwise
            * None on error
        """
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

    def pull_image(self, quiet=False) -> bool|None:
        """Pulls the container image

        Args:
            image_name: The name of the Docker image.
            quiet: If True, suppresses output unless an error occurs.

        Returns:
            True if the image was pulled successfully, False otherwise.  Returns None on error.
        """
        raise NotImplementedError
        try:
            command = [self.engine, "pull", self.image_name]
            if quiet:
                command.append("--quiet") # Add quiet option.

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,  # Important: Do not raise exception on non-zero exit code
            )

            if result.returncode == 0:
                if not quiet:
                    print(result.stdout)
                return True
            else:
                print(f'Error pulling image {self.image_name}:\n{result.stderr}')
                return False
        except FileNotFoundError:
            print("Error: docker command not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def run_nh_training(self, basin_id: str, dry_run: bool = False):
        """"""
        # if step not in ['train', 'test']:
        #     raise ValueError(f'Unrecognized nh step {step}; must be train or test')

        # Todo refactor this
        nh_command = self._nh_command('train', basin_id)
        run_command: list = self._container_command(nh_command)

        if dry_run:
            print()
            print(' '.join(run_command))
            return

        # Todo call run_container_command
        return

    def _nh_command(self, step: str, basin_id: str, run_id: str = None) -> list:
        """"""
        command = [
            'python', 'local_main.py',
            '--step', step,
            '--data_dir', '/data',
            '--experiments_root_dir', '/experiments',
            '--basin_id', basin_id,
        ]
        if run_id is not None:
            command += ['--run_id', run_id]

        return command

    def _container_command(self, nh_command: list) -> list:
        """"""
        run_command = [
            self.engine, 'run', '--rm', '-it', '--gpus all',
            '--mount', f'type=bind,src={self.data_dir},dst=/data,readonly',
            'nh/demo1',
        ]
        return run_command + nh_command

    def run_container_command(self, command, volumes=None, detach=False, interactive=False, tty=False, user=None):
        """Runs train or test step in a container.

        Args:
            command: The command to execute inside the container (can be a string or a list).
            volumes: A list of volume mappings (e.g., ["/host_path:/container_path"]). Defaults to None.
            ports: A list of port mappings (e.g., ["8080:80"]). Defaults to None.
            detach: If True, runs the container in detached mode. Defaults to False.
            interactive: If True, runs the container in interactive mode. Defaults to False.
            tty: If True, allocates a pseudo-TTY connected to stdin of the container. Defaults to False.
            user: The username or UID to run the container as. Defaults to None.

        Returns:
            If detach is False:
                A CompletedProcess object (containing stdout, stderr, and return code).
            If detach is True:
                The container ID (string).
            Returns None on error.
        """
        try:
            docker_command = ["docker", "run"]

            if volumes:
                for volume in volumes:
                    docker_command.extend(["-v", volume])

            if ports:
                for port in ports:
                    docker_command.extend(["-p", port])

            if detach:
                docker_command.append("-d")

            if interactive:
                docker_command.append("-i")

            if tty:
                docker_command.append("-t")

            if user:
                docker_command.extend(["-u", user])

            docker_command.append(image_name)

            if isinstance(command, list):  # Handle both string and list commands
                docker_command.extend(command)
            elif isinstance(command, str):
                docker_command.extend(command.split()) # Splits the command by space
            else:
                print("Error: Command must be a string or a list.")
                return None


            if detach:
                result = subprocess.run(
                    docker_command,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    container_id = result.stdout.strip()
                    return container_id
                else:
                    print(f"Error starting container in detached mode:\n{result.stderr}")
                    return None
            else:
                result = subprocess.run(
                    docker_command,
                    capture_output=True,
                    text=True,
                    check=False # Do not raise exception on non-zero exit code
                )
                return result # Return the completed process object

        except FileNotFoundError:
            print("Error: docker command not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

if __name__ == '__main__':
    # Hack in a quick test
    data_dir = '/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2'
    pod_ops = PodOps(data_dir)
    avail = pod_ops.is_image_available()
    print(f'container image {avail=}')
    if avail:
        pod_ops.run_nh_training('02450250', dry_run=True)
    print('finis')
