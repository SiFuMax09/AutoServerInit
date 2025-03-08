from setuptools import setup, find_packages

setup(
    name="autoserverinit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "paramiko>=3.4.0",
        "PyQt6>=6.6.1",
    ],
    entry_points={
        'console_scripts': [
            'serverinit=autoserverinit.main:main',
        ],
    },
    python_requires=">=3.6",
)
