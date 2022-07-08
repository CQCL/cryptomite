import sys

from skbuild import setup


setup(
    zip_safe=False,
    packages=["extlib"],
    cmake_install_dir="extlib",
)
