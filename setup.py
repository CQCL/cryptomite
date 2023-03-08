import sys

from skbuild import setup


setup(
    zip_safe=False,
    packages=["cryptomite"],
    cmake_install_dir="cryptomite",
)
