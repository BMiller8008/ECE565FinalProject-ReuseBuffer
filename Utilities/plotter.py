import os
import matplotlib.pyplot as plt
import numpy as np

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

def add_value_labels(bars):
    """Add value labels on top of bars."""
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}',
                 ha='center', va='bottom', fontsize=8)

def plot_grouped_bar_comparison(stat_key, stats1, stats2, labels, title, ylabel):
    """Plot grouped bar graphs comparing statistics between two sets of data."""
    values1 = [stats.get(stat_key, 0) for stats in stats1]
    values2 = [stats.get(stat_key, 0) for stats in stats2]

    # X-axis positions
    x = np.arange(len(labels))
    bar_width = 0.35

    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(x - bar_width / 2, values1, bar_width, label='O3 CPU', color='blue', alpha=0.7)
    bars2 = plt.bar(x + bar_width / 2, values2, bar_width, label='Modified CPU', color='orange', alpha=0.7)

    # Add value labels to bars
    add_value_labels(bars1)
    add_value_labels(bars2)

    plt.xticks(x, labels, rotation=45, ha='right')
    plt.title(title)
    plt.xlabel('Benchmark')
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def main(base_dir1, files1, base_dir2, files2):
    stats_set1 = [parse_stats_file(os.path.join(base_dir1, f)) for f in files1]
    stats_set2 = [parse_stats_file(os.path.join(base_dir2, f)) for f in files2]

    # Labels for the x-axis
    labels = [os.path.basename(f) for f in files1]

    # Plot IPC comparison
    plot_grouped_bar_comparison('system.cpu.ipc', stats_set1, stats_set2, labels,
                                'IPC Comparison (Base: O3 CPU)', 'IPC')

    # Plot execution time comparison
    plot_grouped_bar_comparison('simSeconds', stats_set1, stats_set2, labels,
                                'Execution Time Comparison (Base: O3 CPU)', 'Time (s)')

    # Plot CPI comparison
    plot_grouped_bar_comparison('system.cpu.cpi', stats_set1, stats_set2, labels,
                                'CPI Comparison (Base: O3 CPU)', 'CPI')


if __name__ == "__main__":
    base_dir1 = "Base_Benchmarks/Single_Core/"
    files1 = ["astar.txt", "deepsjeng_s.txt", "lbm.txt", "milc.txt"]
    base_dir2 = "Buffer_Benchmarks/1billionRB1024/"
    files2 = ["astarstats.txt", "deepsjengstats.txt", "lbmstats.txt", 'milcstats.txt']

    main(base_dir1, files1, base_dir2, files2)
