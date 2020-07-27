from distutils.core import setup

setup(
    name='xmarievm',
    version='0.0.0',
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
    }
)
