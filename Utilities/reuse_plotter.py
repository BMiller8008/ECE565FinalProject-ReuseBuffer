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
                        stats[key] = int(value)  # Assuming all data is integers
                    except ValueError:
                        pass  # Skip non-numeric values
    return stats

def add_value_labels(bars):
    """Add value labels on top of bars."""
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}',
                     ha='center', va='bottom', fontsize=9, color='black')

def plot_combined_bar(stats_sets, config_labels, benchmark_labels, title, ylabel):
    """Plot a combined bar graph with benchmarks grouped for each configuration."""
    x = np.arange(len(config_labels))
    num_benchmarks = len(benchmark_labels)
    bar_width = 0.8 / num_benchmarks  # Dynamically scale bar width
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Improved color scheme

    plt.figure(figsize=(14, 8))
    ax = plt.gca()

    for i, benchmark in enumerate(benchmark_labels):
        reused_values = [stats_set[benchmark].get('system.cpu.iew.reusedInsts', 0) for stats_set in stats_sets]
        bars = ax.bar(x - 0.4 + i * bar_width, reused_values, bar_width,
                      label=f'{benchmark} Total Reused', color=colors[i % len(colors)], edgecolor='black', alpha=0.85)
        add_value_labels(bars)

    ax.set_xticks(x)
    ax.set_xticklabels(config_labels, rotation=45, ha='right', fontsize=11)
    ax.set_yscale('log')  # Logarithmic scaling for large differences
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Reuse Buffer Entries', fontsize=13, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=13, labelpad=10)
    ax.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1), title="Benchmarks")
    ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    plt.tight_layout()
    plt.show()

def plot_individual_benchmark(stats_sets, config_labels, benchmark, title, ylabel):
    """Plot a bar graph for a single benchmark across configurations."""
    reused_values = [stats_set[benchmark].get('system.cpu.iew.reusedIntInsts', 0) for stats_set in stats_sets]
    float_values = [stats_set[benchmark].get('system.cpu.iew.reusedFloatInsts', 0) for stats_set in stats_sets]
    x = np.arange(len(config_labels))
    bar_width = 0.4

    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    bars1 = ax.bar(x - bar_width / 2, reused_values, bar_width, label='Reused Ints',
                   color='#1f77b4', edgecolor='black', alpha=0.85)
    add_value_labels(bars1)

    bars2 = ax.bar(x + bar_width / 2, float_values, bar_width, label='Reused Floats',
                   color='#2ca02c', edgecolor='black', alpha=0.85)
    add_value_labels(bars2)

    ax.set_xticks(x)
    ax.set_xticklabels(config_labels, rotation=45, ha='right', fontsize=11)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Reuse Buffer Entries', fontsize=13, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=13, labelpad=10)
    ax.legend(fontsize=10, loc='upper right', title="Instruction Type")
    ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    plt.tight_layout()
    plt.show()

def main():
    # Base directories for each configuration
    base_dirs = {
        "256": "Buffer_Benchmarks/1billionRB256/",
        "512": "Buffer_Benchmarks/1billionRB512/",
        "1024": "Buffer_Benchmarks/1billionRB1024/",
        "2048": "Buffer_Benchmarks/1billion2048/",
        "4096": "Buffer_Benchmarks/1billion4096/"
    }
    config_labels = list(base_dirs.keys())
    benchmarks = None

    # Collect stats for each configuration
    stats_sets = []
    for config, base_dir in base_dirs.items():
        files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
        if benchmarks is None:
            benchmarks = sorted(files)  # Use the first config to determine benchmark file names
        elif sorted(files) != benchmarks:
            raise ValueError(f"Benchmark files do not match for configuration {config}!")
        stats = {os.path.splitext(f)[0]: parse_stats_file(os.path.join(base_dir, f)) for f in files}
        stats_sets.append(stats)

    # Remove file extensions to create benchmark labels and exclude specrand benchmarks
    benchmark_labels = [os.path.splitext(f)[0] for f in benchmarks if "specrand" not in f]

    # Debugging: Print benchmarks and stats_sets to verify consistency
    print("Filtered Benchmarks:", benchmark_labels)
    print("Stats Sets Keys:", [list(stats.keys()) for stats in stats_sets])

    # Combined bar graph
    plot_combined_bar(stats_sets, config_labels, benchmark_labels,
                      'Reused Instructions for Different RB Configurations',
                      'Reused Instructions (Log Scale)')

    # Individual plots for each benchmark
    for benchmark in benchmark_labels:
        plot_individual_benchmark(stats_sets, config_labels, benchmark,
                                  f'Reused Instructions ({benchmark})',
                                  'Reused Instructions')

if __name__ == "__main__":
    main()
