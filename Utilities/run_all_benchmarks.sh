#!/bin/bash

# Usage: ./run_all_benchmarks_parallel.sh -o <output_base_dir> -n <num_cpus>
# Example: ./run_all_benchmarks_parallel.sh -o ./RESULTS -n 4

# Default values
OUTPUT_BASE_DIR="./Benchmark_RESULTS"
NUM_CPUS=1

# Parse arguments
while getopts "o:n:" opt; do
    case $opt in
        o) OUTPUT_BASE_DIR="$OPTARG" ;;
        n) NUM_CPUS="$OPTARG" ;;
        *) echo "Usage: $0 -o <output_base_dir> -n <num_cpus>"; exit 1 ;;
    esac
done

# Check required arguments
if [ -z "$OUTPUT_BASE_DIR" ] || [ -z "$NUM_CPUS" ]; then
    echo "Error: Output base directory and number of CPUs are required."
    echo "Usage: $0 -o <output_base_dir> -n <num_cpus>"
    exit 1
fi

# List of benchmarks to run
BENCHMARKS=(
    bwaves_s
    wrf_s
    cam4_s
    nab_s
    fotonik3d_s
    specrand_fs
    mcf_s
    x264_s
    deepsjeng_s
    leela_s
    exchange2_s
    xz_s
    specrand_is
    sjeng
    astar
    milc
    namd
    leslie3d
    lbm
)

# Function to run a benchmark
run_benchmark() {
    local BENCHMARK="$1"
    local OUTPUT_DIR="$OUTPUT_BASE_DIR/$BENCHMARK"

    mkdir -p "$OUTPUT_DIR"  # Ensure the output directory exists
    echo "Starting benchmark: $BENCHMARK (Output: $OUTPUT_DIR)"
    ./runner.sh -b "$BENCHMARK" -o "$OUTPUT_DIR" -n "$NUM_CPUS" &> "$OUTPUT_DIR/log.txt"
    if [ $? -ne 0 ]; then
        echo "Error running benchmark: $BENCHMARK" >> "$OUTPUT_DIR/log.txt"
    else
        echo "Completed benchmark: $BENCHMARK" >> "$OUTPUT_DIR/log.txt"
    fi
}

# Run all benchmarks simultaneously
echo "Running all benchmarks in parallel..."
for BENCHMARK in "${BENCHMARKS[@]}"; do
    run_benchmark "$BENCHMARK" &
done

# Wait for all jobs to complete
wait

echo "All benchmarks completed."
