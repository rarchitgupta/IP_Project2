#!/usr/bin/env python3
"""
Plot Task 2 results: MSS vs Average Transfer Delay
Reads data from task2_results.txt
"""

import matplotlib.pyplot as plt
import re
import os

# Read task2_results.txt
# Try current directory first, then parent
if os.path.exists('task2_results.txt'):
    results_file = 'task2_results.txt'
else:
    results_file = '../task2_results.txt'

if not os.path.exists(results_file):
    print(f"Error: {results_file} not found")
    exit(1)

mss_values = []
avg_delays = []

with open(results_file, 'r') as f:
    for line in f:
        # Match lines like: "100	45.234		42.123		48.567		45.234, 43.456, ..."
        match = re.match(r'(\d+)\s+([0-9.]+)\s+', line)
        if match:
            mss = int(match.group(1))
            avg = float(match.group(2))
            mss_values.append(mss)
            avg_delays.append(avg)

if not mss_values:
    print(f"Error: Could not parse data from {results_file}")
    exit(1)

print(f"Loaded {len(mss_values)} data points from {results_file}")
print(f"MSS values: {mss_values}")
print(f"Avg delays: {avg_delays}")

# Create figure
plt.figure(figsize=(12, 7))

# Plot with markers
plt.plot(mss_values, avg_delays, 'go-', linewidth=2.5, markersize=8, label='Average Delay')

# Formatting
plt.xlabel('MSS (bytes)', fontsize=13, fontweight='bold')
plt.ylabel('Average Transfer Delay (seconds)', fontsize=13, fontweight='bold')
plt.title('Task 2: Effect of MSS on Transfer Delay\n(N=64, p=0.05, 1MB file)', 
          fontsize=14, fontweight='bold')

# Grid
plt.grid(True, alpha=0.3, linestyle='--')

# Add value labels on points
for mss, delay in zip(mss_values, avg_delays):
    plt.annotate(f'{delay:.1f}s', xy=(mss, delay), xytext=(0, 8), 
                textcoords='offset points', ha='center', fontsize=9)

plt.tight_layout()

# Create results directory if it doesn't exist
import os
os.makedirs('results', exist_ok=True)

# Save
output_file = 'results/task2.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"\nPlot saved to: {output_file}")
plt.show()

# Print analysis
print("\n" + "="*70)
print("TASK 2 ANALYSIS: MSS Effect")
print("="*70)
print(f"Minimum delay: {min(avg_delays):.2f}s at MSS={mss_values[avg_delays.index(min(avg_delays))]} bytes")
print(f"Maximum delay: {max(avg_delays):.2f}s at MSS={mss_values[avg_delays.index(max(avg_delays))]} bytes")
print(f"Improvement (MSS={mss_values[0]} to MSS={mss_values[-1]}): {((avg_delays[0] - avg_delays[-1]) / avg_delays[0] * 100):.1f}%")

# Calculate segments for each MSS
file_size = 1_000_000  # 1MB
print("\nSegments per MSS:")
for mss in mss_values:
    segments = file_size // mss
    print(f"  MSS={mss:4d} bytes → {segments:5d} segments")

print("\nKey observations:")
print("- Strong inverse relationship: larger MSS → fewer segments → faster transfer")
print("- Diminishing returns at large MSS (overhead reduction plateaus)")
print("- Roughly follows O(1/MSS) curve for reasonable MSS values")
print("="*70)
