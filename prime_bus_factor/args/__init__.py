from argparse import ArgumentDefaultsHelpFormatter
from typing import List

programName: str = "PRIME Bus Factor Calculator"
authorNames: List[str] = [
    "Nicholas M. Synovic",
    "Matthew Hyatt",
    "Oscar Yanek",
    "George K. Thiruvathukal",
]


class AlphabeticalOrderHelpFormatter(ArgumentDefaultsHelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=lambda x: x.dest)
        super(AlphabeticalOrderHelpFormatter, self).add_arguments(actions
