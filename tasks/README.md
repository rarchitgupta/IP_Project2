# Task Scripts

Automated scripts for running experiments.

## Task 1: Window Size Effect

Run client transfers with varying window sizes (N=1,2,4,...,1024) and measure timing.

**Prerequisites:**

- Server running on remote machine: `python3 src/server.py 7735 output.bin 0.05`
- Input file (≥1 MB) prepared on local machine

**Usage:**

```bash
cd ..  # Go to project root
python3 tasks/task_1.py --host <remote-hostname> --file <input-file>
```

**Example:**

```bash
python3 tasks/task_1.py --host eos.cs.university.edu --file testfile.bin
```

**Options:**

```
--host <hostname>      Server hostname or IP (required)
--file <filename>      Input file to transfer (required)
--port <port>         Server port (default: 7735)
--mss <bytes>         MSS value (default: 500)
--output <filename>   Output results file (default: task1_results.txt)
--runs <n>            Runs per window size (default: 5)
```

**Output:**

- Console output with live progress
- Results file (task1_results.txt) with:
  - Full timing data for all N values
  - Average/min/max times
  - Python code ready for plotting

**Example output file:**

```
Task 1 Results: Effect of Window Size N on Transfer Delay
...
N       Avg (s)         Min (s)         Max (s)         All Times
1       14.523          14.489          14.712          14.523, 14.601, ...
2       7.452           7.234           7.823           7.452, 7.501, ...
...
```
