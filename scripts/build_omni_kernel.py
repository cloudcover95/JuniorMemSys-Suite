# scripts/build_omni_kernel.py
from setuptools import setup
from Cython.Build import cythonize
import os, shutil

source = "jcllc_mem_sys/core/omni_math.py"
target = "jcllc_mem_sys/core/omni_math.pyx"

if os.path.exists(source):
    shutil.move(source, target)

setup(
    ext_modules=cythonize(target, compiler_directives={'language_level': "3"})
)
