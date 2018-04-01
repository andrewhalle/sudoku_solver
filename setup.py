from setuptools import setup, find_packages

setup(
    name="sudoku_solver",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sudoku_solver = sudoku_solver.gui:main"
        ]
    }
)
