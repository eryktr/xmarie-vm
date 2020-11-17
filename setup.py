import setuptools
from distutils.core import setup

setup(
    name='xmarievm',
    version='1.8.0',
    description='Virtual machine to run XMARIE code',
    author='eryktr',
    install_requires=[
        'ply==3.11',
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'mypy',
        ]
    },
    packages=setuptools.find_namespace_packages(include=('xmarievm', 'xmarievm.*')),
)
