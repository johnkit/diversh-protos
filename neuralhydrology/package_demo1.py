"""Script to build Demo1 install package in dist directory


To create tar file, be sure to remote any pyc files first.
Because I cannot figure out how to do that in tar, do this:

cd dist
rm -rf neuralhydrology_demo1/app/demo1/__pycache__/ && tar zcf neuralhydrology_demo1.tgz neuralhydrology_demo1/
"""

import os
import pathlib
import shutil
import tarfile

source_dir = pathlib.Path(__file__).parent
dist_dir = source_dir.parent / 'dist/neuralhydrology_demo1'
app_dir = dist_dir / 'app'

# Delete any existing tgz and app files
tgz_file = source_dir / 'dist/neuralhydrology_demo1.tgz'
tgz_file.unlink(missing_ok=True)
if app_dir.exists():
    shutil.rmtree(app_dir)

# Copy source files to app dir
app_dir.mkdir(parents=True, exist_ok=True)

filenames = ['demo1.py', 'plot_results.py']
for filename in filenames:
    from_path = source_dir / filename
    shutil.copy2(from_path, app_dir)

source_sub_dir = source_dir / 'demo1'
app_sub_dir = app_dir / 'demo1'
app_sub_dir.mkdir(parents=True, exist_ok=True)
filenames = ['__init__.py', 'args_utils.py', 'constants.py', 'demo_run.py', 'template.basin.yml']
for filename in filenames:
    from_path = source_sub_dir / filename
    shutil.copy2(from_path, app_sub_dir)

# Generate tgz file
dist_dir = source_dir.parent / 'dist'
os.chdir(dist_dir)
tgz_file = 'neuralhydrology_demo1.tgz'
with tarfile.open(tgz_file, 'w:gz') as tar:
    tar.add('neuralhydrology_demo1')
    tgz_path = dist_dir / tgz_file
    print(f'Wrote {tgz_path}')
