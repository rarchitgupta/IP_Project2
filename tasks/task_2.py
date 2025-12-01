#!/usr/bin/env python3
"""
Task 2: Effect of MSS on Transfer Delay

Automatically runs client with varying MSS values and measures transfer time.
Window size N and loss probability are fixed.
Server must be running separately before executing this script.

Usage:
    python3 task_2.py --host <server-hostname> --file <input-file> --output <output-file>

Example:
    python3 task_2.py --host 152.7.176.68 --file testfile_1mb.bin --output task2_results.txt
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path


def run_client(host, port, input_file, window_size, mss):
    """
    Run client and measure transfer time.
    
    Returns:
        elapsed_time: Time in seconds for transfer
    """
    cmd = [
        'python3',
        'src/client.py',
        host,
        str(port),
        input_file,
        str(window_size),
        str(mss)
    ]
    
    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        elapsed = time.time() - start
        
        if result.returncode != 0:
            print(f"  ERROR: Client failed with return code {result.returncode}")
            return None
        
        return elapsed
    except subprocess.TimeoutExpired:
        print(f"  ERROR: Transfer timed out after 300 seconds")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Task 2: Measure effect of MSS on transfer delay'
    )
    parser.add_argument('--host', required=True, help='Server hostname or IP address')
    parser.add_argument('--file', required=True, help='Input file to transfer')
    parser.add_argument('--port', type=int, default=7735, help='Server port (default: 7735)')
    parser.add_argument('--window', type=int, default=64, help='Window size N (default: 64)')
    parser.add_argument('--output', default='task2_results.txt', 
                       help='Output file for results (default: task2_results.txt)')
    parser.add_argument('--runs', type=int, default=5, 
                       help='Number of runs per MSS (default: 5)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.file):
        print(f"ERROR: Input file not found: {args.file}")
        sys.exit(1)
    
    # Check if src/client.py exists
    if not os.path.exists('src/client.py'):
        print("ERROR: src/client.py not found. Run this script from project root directory.")
        sys.exit(1)
    
    # MSS values to test
    mss_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    
    # Get file size
    file_size_mb = os.path.getsize(args.file) / (1024 * 1024)
    
    print("="*70)
    print("TASK 2: Effect of MSS on Transfer Delay")
    print("="*70)
    print(f"Server: {args.host}:{args.port}")
    print(f"Input file: {args.file} ({file_size_mb:.2f} MB)")
    print(f"Window size: {args.window} (fixed)")
    print(f"Loss probability: 0.05 (fixed, 5%)")
    print(f"Runs per MSS: {args.runs}")
    print("="*70)
    print()
    
    results = {}
    
    # Run tests for each MSS value
    for mss in mss_values:
        print(f"MSS = {mss}:")
        times = []
        
        for run in range(1, args.runs + 1):
            print(f"  Run {run}/{args.runs}...", end=' ', flush=True)
            
            elapsed = run_client(args.host, args.port, args.file, args.window, mss)
            
            if elapsed is None:
                print("FAILED")
                continue
            
            times.append(elapsed)
            print(f"{elapsed:.3f}s")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            results[mss] = {
                'times': times,
                'avg': avg_time,
                'min': min_time,
                'max': max_time
            }
            print(f"  Average: {avg_time:.3f}s (min: {min_time:.3f}s, max: {max_time:.3f}s)")
        else:
            print(f"  All runs failed!")
        
        print()
    
    # Write results to output file
    print(f"Writing results to {args.output}...")
    with open(args.output, 'w') as f:
        f.write("Task 2 Results: Effect of MSS on Transfer Delay\n")
        f.write("="*70 + "\n\n")
        f.write(f"Test Configuration:\n")
        f.write(f"  Server: {args.host}:{args.port}\n")
        f.write(f"  Input File: {args.file} ({file_size_mb:.2f} MB)\n")
        f.write(f"  Window Size: {args.window}\n")
        f.write(f"  Loss Probability: 0.05 (5%)\n")
        f.write(f"  Runs per MSS: {args.runs}\n\n")
        
        f.write("Results:\n")
        f.write("-"*70 + "\n")
        f.write("MSS\tAvg (s)\t\tMin (s)\t\tMax (s)\t\tAll Times\n")
        f.write("-"*70 + "\n")
        
        for mss in mss_values:
            if mss in results:
                res = results[mss]
                times_str = ", ".join(f"{t:.3f}" for t in res['times'])
                f.write(f"{mss}\t{res['avg']:.3f}\t\t{res['min']:.3f}\t\t{res['max']:.3f}\t\t{times_str}\n")
            else:
                f.write(f"{mss}\tFAILED\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("Data for Plotting (copy into Python):\n")
        f.write("mss_values = [" + ", ".join(str(m) for m in mss_values if m in results) + "]\n")
        avg_times = [results[m]['avg'] for m in mss_values if m in results]
        f.write("avg_delays = [" + ", ".join(f"{t:.3f}" for t in avg_times) + "]\n")
        f.write("\n# Plotting code:\n")
        f.write("import matplotlib.pyplot as plt\n")
        f.write("plt.figure(figsize=(10, 6))\n")
        f.write("plt.plot(mss_values, avg_delays, 'go-', linewidth=2, markersize=8)\n")
        f.write("plt.xlabel('MSS (bytes)', fontsize=12)\n")
        f.write("plt.ylabel('Average Delay (seconds)', fontsize=12)\n")
        f.write(f"plt.title('Task 2: Effect of MSS on Transfer Delay (N={args.window}, p=0.05)', fontsize=14)\n")
        f.write("plt.grid(True, alpha=0.3)\n")
        f.write("plt.tight_layout()\n")
        f.write("plt.savefig('task2_plot.png', dpi=150)\n")
        f.write("plt.show()\n")
    
    print(f"Results saved to {args.output}")
    
    # Print summary table
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"{'MSS':<10} {'Avg (s)':<15} {'Min (s)':<15} {'Max (s)':<15}")
    print("-"*70)
    for mss in mss_values:
        if mss in results:
            res = results[mss]
            print(f"{mss:<10} {res['avg']:<15.3f} {res['min']:<15.3f} {res['max']:<15.3f}")
    print("="*70)
    
    print("\nNext steps:")
    print("1. Use the mss_values and avg_delays variables to create a plot")
    print("2. Verify output file matches input file (use 'diff' on remote server)")
    print("3. Include plot and analysis in your report")


if __name__ == '__main__':
    main()
