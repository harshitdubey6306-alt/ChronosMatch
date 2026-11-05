"""
ChronosMatch Cython Build Configuration
This setup script compiles the engine.pyx file into a C-extension.
By building the engine natively, it allows the matching logic to 
execute at C-level speeds and bypass Python's standard overhead.
"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("engine.pyx")
)