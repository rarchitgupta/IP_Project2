# Task 1: Effect of Window Size N on Transfer Delay

## Quick Summary

Measure how window size N affects transfer delay. Fix MSS=500, p=0.05, vary N from 1 to 1024.

## Before You Start

### On Remote Server (EOS/Campus)

```bash
cd project_2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create test file (at least 1 MB)
dd if=/dev/urandom of=testfile.bin bs=1M count=5

# Get hostname
hostname
```

### On Local Client (Your Laptop)

```bash
cd project_2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create same test file
dd if=/dev/urandom of=testfile.bin bs=1M count=5

# Measure RTT to server
ping -c 10 <remote-hostname>
# Record the average RTT shown
```

## Running Task 1

### Step 1: Start Server on Remote Machine

Open a terminal on the remote machine and run:

```bash
python3 src/server.py 7735 output.bin 0.05
```

This will show "Server listening on port 7735" and occasional "Packet loss, sequence number = X" messages.

### Step 2: Run Client on Local Machine for Each N Value

For each N in: **1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024**

Run this 5 times and record the **real** time each time:

```bash
time python3 src/client.py <REMOTE_HOSTNAME> 7735 testfile.bin <N> 500
```

Example for N=1:

```bash
time python3 src/client.py eos.cs.university.edu 7735 testfile.bin 1 500
```

The output will show:

```
real    0m14.523s    ← Record this value
user    0m0.234s
sys     0m0.156s
```

### Step 3: Record All Timings

Create a table with all 11 N values and 5 measurements each:

```
N=1:     Run1=14.5s  Run2=14.6s  Run3=14.5s  Run4=14.7s  Run5=14.6s  → Average = 14.58s
N=2:     Run1=7.3s   Run2=7.4s   Run3=7.2s   Run4=7.3s   Run5=7.4s   → Average = 7.32s
N=4:     ...
...
N=1024:  ...
```

### Step 4: Verify File Integrity

After all tests complete, verify files match on remote machine:

```bash
diff testfile.bin output.bin && echo "✓ Files match"
```

## Plotting

Use this code to create your plot:

```bash
python3 << 'EOF'
import matplotlib.pyplot as plt

# Your data (replace with actual averages)
N_values = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
avg_delays = [14.58, 7.32, 3.89, 2.14, 1.23, 0.89, 0.76, 0.73, 0.72, 0.71, 0.71]

plt.figure(figsize=(10, 6))
plt.plot(N_values, avg_delays, marker='o', linewidth=2, markersize=8, label='Avg Delay')
plt.xlabel('Window Size (N)', fontsize=12)
plt.ylabel('Average Transfer Delay (seconds)', fontsize=12)
plt.title('Task 1: Effect of Window Size N on Transfer Delay\n(MSS=500 bytes, p=0.05)', fontsize=14)
plt.xscale('log', base=2)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('task1_plot.png', dpi=150)
print("Plot saved as: task1_plot.png")
EOF
```

## Report Contents

1. **File size used**: (e.g., 5 MB)
2. **Remote machine**: (hostname and network location)
3. **RTT measurement**: (from ping output)
4. **Data table**: All 11 N values with 5 timings + average
5. **Plot**: Window size vs average delay (with clear labels)
6. **Analysis**:
   - How does N affect delay?
   - Why does performance improve with N?
   - At what point do you see diminishing returns?
   - What's the curve shape and why?
   - Why is N=1 slower than N=2?

## Expected Results

- **N=1** (stop-and-wait): Slowest (waits for each ACK)
- **N=2-32**: Rapid improvement (pipelining effect)
- **N=64-512**: Plateaus (diminishing returns)
- **N=1024**: Almost no improvement over N=512

## Troubleshooting

**"Connection refused"**: Server not running on remote machine or wrong hostname/port

**"Timeout, sequence number = ..."**: Normal with 5% loss. More timeouts = more packet loss.

**File sizes don't match**: Check network connectivity, increase file size if transfer is too fast to measure accurately

**Highly variable timings**: Normal. That's why you run 5 times and average them.
