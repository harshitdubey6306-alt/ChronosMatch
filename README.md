# ChronosMatch: High-Frequency Trading Engine

ChronosMatch is a low-latency High-Frequency Trading (HFT) matching engine built in Python and Cython. It is designed to bypass standard Python bottlenecks to achieve sub-microsecond latency.

## Core Architecture
* **Cython Limit Order Book:** Order book state is maintained in native C-arrays to prevent Python Garbage Collection pauses.
* **Zero-Copy IPC (mmap):** Bypasses the Global Interpreter Lock (GIL) by allowing independent Python processes to communicate instantly via a shared RAM memory map using raw C-struct binary bytes.
* **Live Concurrency:** Features a dual-terminal pipeline where a continuous data firehose writes orders to memory, and the Cython engine reads and matches them in real-time.
* **Terminal Visualization:** Utilizes the `Rich` library to render a live UI displaying throughput and the Bid/Ask spread at 10 frames per second without blocking the matching engine.

## Benchmarks
* **Throughput:** Processed 100,000 orders in 0.39 seconds.