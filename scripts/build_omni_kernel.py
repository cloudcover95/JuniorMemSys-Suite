import os, shutil
from setuptools import setup
from Cython.Build import cythonize

core_dir = "junior_memsys_suite/core"
source = f"{core_dir}/omni_math.py"
target = f"{core_dir}/omni_math.pyx"

# If it's already a .pyx from a previous fail, we're good. 
# If it's a .py, we rename it for Cython.
if os.path.exists(source):
    shutil.move(source, target)

if os.path.exists(target):
    setup(
        ext_modules=cythonize(target, compiler_directives={'language_level': "3"}),
        script_args=['build_ext', '--inplace']
    )
else:
    print(f"CRITICAL ERROR: {target} not found for compilation.")
