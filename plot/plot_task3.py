#!/usr/bin/env python3
"""
Plot Task 3 results: Loss Probability p vs Average Transfer Delay
Reads data from task3_results.txt
"""

import matplotlib.pyplot as plt
import re
import os

# Read task3_results.txt
# Try current directory first, then parent
if os.path.exists('task3_results.txt'):
    results_file = 'task3_results.txt'
else:
    results_file = '../task3_results.txt'

if not os.path.exists(results_file):
    print(f"Error: {results_file} not found in current or parent directory")
    exit(1)

loss_probs = []
avg_delays = []

with open(results_file, 'r') as f:
    for line in f:
        # Match lines like: "0.01	45.234		42.123		48.567		45.234, 43.456, ..."
        match = re.match(r'([0-9.]+)\s+([0-9.]+)\s+', line)
        if match:
            p = float(match.group(1))
            avg = float(match.group(2))
            loss_probs.append(p)
            avg_delays.append(avg)

if not loss_probs:
    print(f"Error: Could not parse data from {results_file}")
    exit(1)

print(f"Loaded {len(loss_probs)} data points from {results_file}")
print(f"Loss probabilities: {loss_probs}")
print(f"Avg delays: {avg_delays}")

# Create figure
plt.figure(figsize=(12, 7))

# Plot with markers
plt.plot(loss_probs, avg_delays, 'ro-', linewidth=2.5, markersize=8, label='Average Delay')

# Formatting
plt.xlabel('Loss Probability p', fontsize=13, fontweight='bold')
plt.ylabel('Average Transfer Delay (seconds)', fontsize=13, fontweight='bold')
plt.title('Task 3: Effect of Loss Probability p on Transfer Delay\n(N=64, MSS=500, 1MB file)', 
          fontsize=14, fontweight='bold')

# Grid
plt.grid(True, alpha=0.3, linestyle='--')

# Add value labels on points
for p, delay in zip(loss_probs, avg_delays):
    plt.annotate(f'{delay:.1f}s', xy=(p, delay), xytext=(0, 8), 
                textcoords='offset points', ha='center', fontsize=9)

plt.tight_layout()

# Create results directory if it doesn't exist
import os
os.makedirs('results', exist_ok=True)

# Save
output_file = 'results/task3.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"\nPlot saved to: {output_file}")
plt.show()

# Print analysis
print("\n" + "="*70)
print("TASK 3 ANALYSIS: Loss Probability Effect")
print("="*70)
print(f"Minimum delay: {min(avg_delays):.2f}s at p={loss_probs[avg_delays.index(min(avg_delays))]:.2f}")
print(f"Maximum delay: {max(avg_delays):.2f}s at p={loss_probs[avg_delays.index(max(avg_delays))]:.2f}")
print(f"Increase (p=0.01 to p=0.10): {((avg_delays[-1] - avg_delays[0]) / avg_delays[0] * 100):.1f}%")

# Calculate expected retransmission rates
print("\nExpected retransmission impact:")
print("With N=64, MSS=500 → ~2000 segments for 1MB file")
total_segments = 1_000_000 // 500
for p in loss_probs:
    expected_losses = total_segments * p
    print(f"  p={p:.2f}: ~{expected_losses:.0f} loss events expected")

print("="*70)
