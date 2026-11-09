# ChronosMatch System Architecture

## Design Philosophy
ChronosMatch is engineered to bypass the Python Global Interpreter Lock (GIL) and standard dynamic typing overhead to achieve sub-microsecond latency in order matching.

## Core Components
1. **Data Firehose (`writer.py`):** Simulates an exchange feed by packing raw C-struct limit orders into a 10MB memory-mapped (`mmap`) ring buffer.
2. **Matching Engine (`engine.pyx`):** A Cython-compiled limit order book utilizing static typing and contiguous C-arrays for maximum execution speed.
3. **Zero-Copy IPC:** The engine reads the physical memory addresses written by the firehose directly, completely eliminating network latency and data serialization.