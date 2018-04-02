from setuptools import setup, find_packages

setup(
    name="sudoku_solver",
    version="0.1",
    description="A sudoku solver using CSP techniques",
    url="https://github.com/andrewhalle/sudoku_solver",
    author="Andrew Halle",
    author_email="ahalle@berkeley.edu",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sudoku_solver = sudoku_solver.gui:main"
        ]
    }
)
