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
- **Suggest** — Practical next steps based on patterns

## Status

Early prototype