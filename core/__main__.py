#!/usr/bin/env python3
import argparse
import time
from .detect import Detector
from .mtr import run_mtr
from .analyzer import analyze_path


def main():
    parser = argparse.ArgumentParser(description="Ploss: Packet Loss Detector")
    parser.add_argument("target", help="Target IP")
    parser.add_argument("--watch", action="store_true", help="Live monitoring")
    parser.add_argument("--mtr", action="store_true", help="per hop analysis")
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--json", help="Export JSON analysis")
    parser.add_argument("--csv", help="Export CSV hops")
    args = parser.parse_args()

    if args.mtr:
        hops = run_mtr(args.target)
        if hops:
            print("\nTraceroute Hops:")
            for hop in hops:
                status = "BAD" if hop['loss'] > 10 else "OK"
                print(f"{status} Hop {hop['hop']}: {hop['loss']:.1f}% -> {hop['host']} (avg: {hop['avg']} ms)")
        
        # Analysis only if hops exist
        analysis = analyze_path(hops)
        print(f"\nAnalysis:")
        print(f"Total Hops: {analysis['total_hops']}")
        print(f"Total Loss: {analysis['total_loss']:.1f}%")
        print(f"Average Latency: {analysis['average_latency']:.1f} ms")
        print(f"Worst Latency: {analysis['worst_latency']:.1f} ms")
        print(f"Bottleneck: Hop {analysis['bottleneck']['hop']} ({analysis['bottleneck']['host']}) with {analysis['bottleneck']['loss']:.1f}% loss")
        print(f"Next: {analysis['suggestion']}")

        if args.json and hops:
            import json
            data = {'hops': hops, 'analysis': analysis, 'timestamp':time.strftime("%Y-%m-%d %H:%M:%S")}
            with open(args.json, 'w') as f:
                json.dump(data, f, indent=2)
                print(f"\nJSON saved: {args.json}")

        if args.csv and hops:
            import csv
            with open(args.csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames= hops[0].keys())
                writer.writeheader()
                writer.writerows(hops)
                print(f"\nCSV saved: {args.csv}")

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