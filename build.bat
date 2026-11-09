@echo off
REM ChronosMatch Cython Build Script
REM This script automates the compilation of engine.pyx into a C-extension

echo Cleaning previous build artifacts...
rmdir /S /Q build 2>nul

echo Compiling Cython matching engine...
python setup.py build_ext --inplace

echo Build complete!