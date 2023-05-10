from argparse import ArgumentParser, Namespace
from importlib.metadata import version

import prime_bus_factor.args as argVars

def getArgs()   ->  Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=argVars.programName,
        usage="To calculate the bus factor value per bin of a repository."
        epilog=f"Authors: {', '.join(argVars.authorNames)}",
        formatter_class=argVars.AlphabeticalOrderHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Commits JSON file. DEFAULT: ./commits_loc.json",
        default="commits_loc.json",
    )
    parser.add_argument(
        "-b",
        "--bin",
        help="Bin containing the number of days between computed bus factor values. DEFAULT: 1",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file. DEFAULT: ./bus_factor.json",
        type=str,
        default="bus_factor.json",
    )
    parser.add_argument(
        "-a",
        "--alpha",
        help="The percent change of the code base a developer needs to contribute in a time interval . DEFAULT: 0.8",
        type=float,
        default=0.8,
    )
     parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{argVars.programName}: {version(distribution_name='prime-bus-factor')}",
    )
    return parser.parse_args()
