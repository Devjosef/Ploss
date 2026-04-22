# Ploss
**Packet loss detector and debugger**

## Overview

Networks are unreliable. Packets get lost in transmission. Debugging the *where* and *why* is hard and convoluted.

Ploss detects packet loss, localizes it to specific hops/segments, then suggests next steps. When you know exactly *where* it went wrong, fixing it becomes much easier.

## The Problem
Packet loss is sporadic and hard to reproduce:

- Loss only happens under certain conditions (like load)
- Could be one bad router, cable, or ISP segment
- Simple pings miss bursty or path-specific issues

## What Ploss Does

- **Detect** — Continuous probes catch sporadic loss
- **Localize** — Per-hop visibility shows exactly where packets drop
- **Document** - JSON/CSV exports for ISP support tickets
- **Suggest** — Practical next steps based on patterns

## Current Status
Per-hop loss detection by mtr parsing
Smart bottleneck analysis
JSON/CSV ISP evidence export
Live monitoring using the (--watch) command
Cross-platform (macOS/linux)

## Quick Start

ploss 8.8.8.8                   # Basic loss test
ploss 8.8.8.8 --mtr             # Traceroute + analysis  
ploss 8.8.8.8 --mtr --json=proof.json --csv=hops.csv  # ISP evidence
ploss 8.8.8.8 --watch           # Live monitoring


## Installation
pip install ploss
# or from source
pip install git+https://github.com/Devjosef/Ploss

## Scaling Directions (PLANNED)
**Cloud Targets**
ploss aws-ec2.eu-north.... --mtr
ploss gcp-cloud.eu

## Multi-target (PLANNED)
ploss --targets google,github,aws --mtr

## Agent mode (PLANNED)
ploss-agent --server central-monitor.com