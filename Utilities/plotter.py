import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

def parse_stats_file(file_path):
    """Parse a gem5 stats file and return relevant statistics as a dictionary."""
    stats = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "::" not in line:
                parts = line.split()
                if len(parts) >= 2:
                    key, value = parts[0], parts[1]
                    try:
                        stats[key] = float(value)
                    except ValueError:
                        pass  # Skip non-numeric values
    return stats

def add_value_labels(bars, percentages=False):
    """Add value labels on top of bars."""
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            label = f'{height:.2f}%' if percentages else f'{height:.2f}'
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, label,
                     ha='center', va='bottom', fontsize=8)

def plot_grouped_bar_comparison(stat_key, stats1, stats2, labels, title, ylabel):
    """Plot grouped bar graphs comparing statistics between two sets of data."""
    values1 = [stats.get(stat_key, 0) for stats in stats1]
    values2 = [stats.get(stat_key, 0) for stats in stats2]

    # X-axis positions
    x = np.arange(len(labels))
    bar_width = 0.35
    colors = cm.tab20.colors  # Use a colormap

    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(x - bar_width / 2, values1, bar_width, label='O3 CPU', color=colors[0], alpha=0.85)
    bars2 = plt.bar(x + bar_width / 2, values2, bar_width, label='Modified CPU', color=colors[1], alpha=0.85)

    # Add value labels to bars
    add_value_labels(bars1)
    add_value_labels(bars2)

    plt.xticks(x, labels, rotation=45, ha='right', fontsize=10)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Benchmark', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_stacked_bar_comparison(stats, labels, title):
    """Plot stacked bar graphs showing percentages of reused float and int instructions."""
    reused_floats = [stats.get('system.cpu.iew.reusedFloatInsts', 0) for stats in stats]
    reused_ints = [stats.get('system.cpu.iew.reusedIntInsts', 0) for stats in stats]
    total_reused = [f + i for f, i in zip(reused_floats, reused_ints)]

    # Calculate percentages
    percentages_floats = [f / t * 100 if t > 0 else 0 for f, t in zip(reused_floats, total_reused)]
    percentages_ints = [i / t * 100 if t > 0 else 0 for i, t in zip(reused_ints, total_reused)]

    x = np.arange(len(labels))
    bar_width = 0.6
    colors = cm.tab10.colors  # Use a colormap

    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(x, percentages_floats, bar_width, label='Reused Float Instructions', color=colors[2])
    bars2 = plt.bar(x, percentages_ints, bar_width, bottom=percentages_floats, label='Reused Int Instructions', color=colors[3])

    plt.xticks(x, labels, rotation=45, ha='right', fontsize=10)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Benchmark', fontsize=12)
    plt.ylabel('Percentage of Reused Instructions (%)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_modified_cpu_only(stat_key, stats, labels, title, ylabel):
    """Plot bar graphs for statistics specific to the modified CPU."""
    values = [stats.get(stat_key, 0) for stats in stats]

    # X-axis positions
    x = np.arange(len(labels))
    bar_width = 0.6
    colors = cm.tab20.colors  # Use a colormap

    plt.figure(figsize=(10, 6))
    bars = plt.bar(x, values, bar_width, label='Modified CPU', color=colors[4], alpha=0.85)

    # Add value labels to bars
    add_value_labels(bars)

    plt.xticks(x, labels, rotation=45, ha='right', fontsize=10)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Benchmark', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main(base_dir1, files1, base_dir2, files2):
    stats_set1 = [parse_stats_file(os.path.join(base_dir1, f)) for f in files1]
    stats_set2 = [parse_stats_file(os.path.join(base_dir2, f)) for f in files2]

    # Labels for the x-axis without `.txt`
    labels = [os.path.basename(f).replace('.txt', '') for f in files1]
    reuse_labels = [os.path.basename(f).replace('.txt', '') for f in files2]

    # Plot IPC comparison
    plot_grouped_bar_comparison('system.cpu.ipc', stats_set1, stats_set2, labels,
                                'IPC Comparison (Base: O3 CPU)', 'IPC')

    # Plot execution time comparison
    plot_grouped_bar_comparison('simSeconds', stats_set1, stats_set2, labels,
                                'Execution Time Comparison (Base: O3 CPU)', 'Time (s)')

    # Plot CPI comparison
    plot_grouped_bar_comparison('system.cpu.cpi', stats_set1, stats_set2, labels,
                                'CPI Comparison (Base: O3 CPU)', 'CPI')

    # Plot stacked bar comparison for reused instructions
    plot_stacked_bar_comparison(stats_set2, reuse_labels, 'Reused Instruction Breakdown')

    # Plot reused instructions (modified CPU only)
    plot_modified_cpu_only('system.cpu.iew.reusedInsts', stats_set2, reuse_labels,
                           'Total Reused Instructions', 'Reused Instructions')
    plot_modified_cpu_only('system.cpu.iew.reusedFloatInsts', stats_set2, reuse_labels,
                           'Reused Floating-Point Instructions', 'Reused Float Instructions')
    plot_modified_cpu_only('system.cpu.iew.reusedIntInsts', stats_set2, reuse_labels,
                           'Reused Integer Instructions', 'Reused Int Instructions')

if __name__ == "__main__":
    base_dir1 = "Base_Benchmarks/Single_Core/"
    files1 = ["astar.txt", "deepsjeng_s.txt", "lbm.txt", "milc.txt", "specrand_is.txt", "specrand_fs.txt"]
    base_dir2 = "Buffer_Benchmarks/1billionRB1024/"
    files2 = ["astarstats.txt", "deepsjengstats.txt", "lbmstats.txt", 'milcstats.txt', 'specrand_isstats.txt', 'specrand_fsstats.txt']

    main(base_dir1, files1, base_dir2, files2)
