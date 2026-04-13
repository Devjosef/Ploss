#!/usr/bin/env python3
import argparse
import time
from .detect import Detector

def main():
    parser = argparse.ArgumentParser(description="Ploss: Packet Loss Detector")
    parser.add_argument("target", help="Target Ip")
    parser.add_argument("--watch", action="store_true", help="Live monitoring")
    parser.add_argument("--interval", type=float, default=3.0)
    args = parser.parse_args()

    d = Detector()
    if args.watch:
        print(f"Monitoring loss {args.target}...")
        try:
            while True:
                d.probe(args.target)
                print(f"\r{d.status()}", end="")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        for _ in range(30):
            d.probe(args.target)
        print(d.status())

if __name__ == "__main__":
    main()