#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from core import __main__

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="Export JSON")
    parser.add_argument("--csv", help="Export CSV")
    parser.add_argument("--quiet", action="store_true")
    args, unknown = parser.parse_known_args()

    result = __main__.main_with_result(unknown)

    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2))

    if args.csv:
        Path(args.csv).write_text(result['csv'])

    if not args.quiet:
        print(result['summary'])
