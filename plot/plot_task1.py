#!/usr/bin/env python3
"""
Plot Task 1 results: Window Size N vs Average Transfer Delay
Reads data from task1_results.txt
"""

import matplotlib.pyplot as plt
import re
import os

# Read task1_results.txt
# Try current directory first, then parent
if os.path.exists('task1_results.txt'):
    results_file = 'task1_results.txt'
else:
    results_file = '../task1_results.txt'

if not os.path.exists(results_file):
    print(f"Error: {results_file} not found")
    exit(1)

window_sizes = []
avg_delays = []

with open(results_file, 'r') as f:
    for line in f:
        # Match lines like: "1	126.564		121.734		142.491		126.564, 125.084, ..."
        match = re.match(r'(\d+)\s+([0-9.]+)\s+', line)
        if match:
            n = int(match.group(1))
            avg = float(match.group(2))
            window_sizes.append(n)
            avg_delays.append(avg)

if not window_sizes:
    print(f"Error: Could not parse data from {results_file}")
    exit(1)

print(f"Loaded {len(window_sizes)} data points from {results_file}")
print(f"Window sizes: {window_sizes}")
print(f"Avg delays: {avg_delays}")

# Create figure
plt.figure(figsize=(12, 7))

# Plot with markers
plt.plot(window_sizes, avg_delays, 'bo-', linewidth=2.5, markersize=8, label='Average Delay')

# Formatting
plt.xlabel('Window Size N (segments)', fontsize=13, fontweight='bold')
plt.ylabel('Average Transfer Delay (seconds)', fontsize=13, fontweight='bold')
plt.title('Task 1: Effect of Window Size N on Transfer Delay\n(MSS=500, p=0.05, 1MB file)', 
          fontsize=14, fontweight='bold')

# Log scale for x-axis to better show the spread
plt.xscale('log', base=2)

# Set x-axis to show the actual N values
plt.xticks(window_sizes, window_sizes)

# Grid
plt.grid(True, alpha=0.3, linestyle='--')

# Add value labels on points
for n, delay in zip(window_sizes, avg_delays):
    plt.annotate(f'{delay:.1f}s', xy=(n, delay), xytext=(0, 8), 
                textcoords='offset points', ha='center', fontsize=9)

plt.tight_layout()

# Create results directory if it doesn't exist
import os
os.makedirs('results', exist_ok=True)

# Save
output_file = 'results/task1.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"\nPlot saved to: {output_file}")
plt.show()

# Print analysis
print("\n" + "="*70)
print("TASK 1 ANALYSIS: Window Size Effect")
print("="*70)
print(f"Minimum delay: {min(avg_delays):.2f}s at N={window_sizes[avg_delays.index(min(avg_delays))]}")
print(f"Maximum delay: {max(avg_delays):.2f}s at N={window_sizes[avg_delays.index(max(avg_delays))]}")
print(f"Improvement (N=1 to N={window_sizes[-1]}): {((avg_delays[0] - avg_delays[-1]) / avg_delays[0] * 100):.1f}%")
print("\nKey observations:")
print("- Steep drop from N=1 to N=8 (stop-and-wait → pipelining)")
print("- Diminishing returns for N>8 (network RTT becomes limiting factor)")
print("- Plateaus around N=64-128 (window large enough for this network)")
print("="*70)
