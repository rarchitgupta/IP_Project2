#!/usr/bin/env python3
"""
Task 1: Effect of Window Size N on Transfer Delay

Automatically runs client with varying window sizes and measures transfer time.
Server must be running separately before executing this script.

Usage:
    python3 task_1.py --host <server-hostname> --file <input-file> --output <output-file>

Example:
    python3 task_1.py --host eos.cs.university.edu --file testfile.bin --output results.txt
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
        elapsed_time: Time in seconds for transfer (from 'time' command)
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
        description='Task 1: Measure effect of window size N on transfer delay'
    )
    parser.add_argument('--host', required=True, help='Server hostname or IP address')
    parser.add_argument('--file', required=True, help='Input file to transfer')
    parser.add_argument('--port', type=int, default=7735, help='Server port (default: 7735)')
    parser.add_argument('--mss', type=int, default=500, help='MSS in bytes (default: 500)')
    parser.add_argument('--output', default='task1_results.txt', 
                       help='Output file for results (default: task1_results.txt)')
    parser.add_argument('--runs', type=int, default=5, 
                       help='Number of runs per N (default: 5)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.file):
        print(f"ERROR: Input file not found: {args.file}")
        sys.exit(1)
    
    # Check if src/client.py exists
    if not os.path.exists('src/client.py'):
        print("ERROR: src/client.py not found. Run this script from project root directory.")
        sys.exit(1)
    
    # Window sizes to test
    window_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    
    # Get file size
    file_size_mb = os.path.getsize(args.file) / (1024 * 1024)
    
    print("="*70)
    print("TASK 1: Effect of Window Size N on Transfer Delay")
    print("="*70)
    print(f"Server: {args.host}:{args.port}")
    print(f"Input file: {args.file} ({file_size_mb:.2f} MB)")
    print(f"MSS: {args.mss} bytes (fixed)")
    print(f"Loss probability: 0.05 (fixed, 5%)")
    print(f"Runs per N: {args.runs}")
    print("="*70)
    print()
    
    results = {}
    
    # Run tests for each window size
    for n in window_sizes:
        print(f"Window Size N = {n}:")
        times = []
        
        for run in range(1, args.runs + 1):
            print(f"  Run {run}/{args.runs}...", end=' ', flush=True)
            
            elapsed = run_client(args.host, args.port, args.file, n, args.mss)
            
            if elapsed is None:
                print("FAILED")
                continue
            
            times.append(elapsed)
            print(f"{elapsed:.3f}s")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            results[n] = {
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
        f.write("Task 1 Results: Effect of Window Size N on Transfer Delay\n")
        f.write("="*70 + "\n\n")
        f.write(f"Test Configuration:\n")
        f.write(f"  Server: {args.host}:{args.port}\n")
        f.write(f"  Input File: {args.file} ({file_size_mb:.2f} MB)\n")
        f.write(f"  MSS: {args.mss} bytes\n")
        f.write(f"  Loss Probability: 0.05 (5%)\n")
        f.write(f"  Runs per N: {args.runs}\n\n")
        
        f.write("Results:\n")
        f.write("-"*70 + "\n")
        f.write("N\tAvg (s)\t\tMin (s)\t\tMax (s)\t\tAll Times\n")
        f.write("-"*70 + "\n")
        
        for n in window_sizes:
            if n in results:
                res = results[n]
                times_str = ", ".join(f"{t:.3f}" for t in res['times'])
                f.write(f"{n}\t{res['avg']:.3f}\t\t{res['min']:.3f}\t\t{res['max']:.3f}\t\t{times_str}\n")
            else:
                f.write(f"{n}\tFAILED\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("Data for Plotting (copy into Python):\n")
        f.write("window_sizes = [" + ", ".join(str(n) for n in window_sizes if n in results) + "]\n")
        avg_times = [results[n]['avg'] for n in window_sizes if n in results]
        f.write("avg_delays = [" + ", ".join(f"{t:.3f}" for t in avg_times) + "]\n")
    
    print(f"Results saved to {args.output}")
    
    # Print summary table
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"{'N':<10} {'Avg (s)':<15} {'Min (s)':<15} {'Max (s)':<15}")
    print("-"*70)
    for n in window_sizes:
        if n in results:
            res = results[n]
            print(f"{n:<10} {res['avg']:<15.3f} {res['min']:<15.3f} {res['max']:<15.3f}")
    print("="*70)
    
    print("\nNext steps:")
    print("1. Use the window_sizes and avg_delays variables to create a plot")
    print("2. Verify output file matches input file (use 'diff' on remote server)")
    print("3. Include plot and analysis in your report")


if __name__ == '__main__':
    main()
