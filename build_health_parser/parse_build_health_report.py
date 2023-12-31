#!/usr/bin/python3

import argparse
import sys
from pathlib import Path
from typing import Sequence

from fix_advice import parse_lines


def main(args: Sequence[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "build_health_report",
        nargs=1,
        type=str,
        help="Path to build health report file",
    )
    parser.add_argument(
        "--gradle_root",
        default=".",
        type=str,
        help="Path to gradle root directory",
    )
    parser.add_argument(
        "--output",
        action="store",
        type=argparse.FileType("a"),
        default=sys.stdout,
        help="Path to gradle root directory",
    )
    args = parser.parse_args(args=args)

    build_health_report = Path(args.build_health_report[0])
    gradle_root = Path(args.gradle_root)
    output = args.output

    with build_health_report.open() as f:
        with output:
            for fix_advice in parse_lines(gradle_root, iter(f.readlines())):
                output.write(fix_advice.to_errorformat() + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
