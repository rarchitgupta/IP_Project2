# Task Automation Scripts

Automated scripts for running Phase 5 experiments.

## Usage

All scripts follow the same pattern:

```bash
python3 tasks/task_X.py --host <hostname> --file <input-file> [options]
```

Common options:

- `--port 7735` - Server port (default: 7735)
- `--output results.txt` - Results file (default: taskX_results.txt)
- `--runs 5` - Runs per parameter (default: 5)

## Task Scripts

### task_1.py - Window Size Effect

```bash
python3 tasks/task_1.py --host 152.7.176.68 --file testfile_1mb.bin
```

Tests N ∈ {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024} with MSS=500, p=0.05.
Outputs timing data to `task1_results.txt`.

### task_2.py - MSS Effect

```bash
python3 tasks/task_2.py --host 152.7.176.68 --file testfile_1mb.bin
```

Tests MSS ∈ {100, 200, ..., 1000} bytes with N=64, p=0.05.
Outputs timing data to `task2_results.txt`.

### task_3.py - Loss Probability Effect

```bash
python3 tasks/task_3.py --host 152.7.176.68 --file testfile_1mb.bin
```

Tests p ∈ {0.01, 0.02, ..., 0.10} with N=64, MSS=500.
Outputs timing data to `task3_results.txt`.

## Prerequisites

Server must be running:

```bash
python3 src/server.py 7735 output.bin 0.05
```

Input file needed:

```bash
dd if=/dev/urandom of=testfile_1mb.bin bs=1M count=1
```
