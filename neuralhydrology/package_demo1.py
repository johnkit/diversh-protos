"""Script to build Demo1 install package in dist directory"""

import pathlib
import shutil

source_dir = pathlib.Path(__file__).parent
dist_dir = source_dir.parent / 'dist'
app_dir = dist_dir / 'app'

# Copy source files to app dir
app_dir.mkdir(parents=True, exist_ok=True)

from_path = source_dir / 'demo1.py'
shutil.copy2(from_path, app_dir)

source_sub_dir = source_dir / 'demo1'
app_sub_dir = app_dir / 'demo1'
app_sub_dir.mkdir(parents=True, exist_ok=True)
filenames = ['__init__.py', 'args_utils.py', 'constants.py', 'demo_run.py', 'template.basin.yml']
for filename in filenames:
    from_path = source_sub_dir / filename
    shutil.copy2(from_path, app_sub_dir)
