from setuptools import setup, find_packages

setup(
    name='ptrack',
    version='0.1.0',
    description='A simple CLI utility for asthetically tracking progress when copying or moving files.',
    author='Connor Etherington',
    author_email='connor@concise.cc',
    packages=find_packages(),
    install_requires=[
        'rich',
        'argparse',
        'argcomplete',
    ],
    entry_points={
        'console_scripts': [
            'ptc=ptrack.main:copy',
            'ptm=ptrack.main:move',
            'ptrack=ptrack.main:main',
        ]
    }
)
