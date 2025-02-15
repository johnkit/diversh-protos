"""Runs neural hydrology demos in local file system."""

import argparse

class LocalNH:
    def __init__(self, args: argparse.Namespace):
        """Calling code responsible for argument checking."""
        self.args = args

    def run(self) -> bool:
        if self.args.step == 'train':
            self.run_training()
        elif self.args.step == 'test':
            self.run_testing()
        else:
            raise NotImplementedError(f'Unrecognized step {self.args.step}')

    def run_training(self) -> bool:
        raise NotImplementedError(f'Todo {__class__}.run_training()')

    def run_testing(self) -> bool:
        raise NotImplementedError(f'Todo {__class__}.run_testing()')
