#!/bin/bash

# Usage: ./run_all_benchmarks_parallel.sh -o <output_base_dir> -n <num_cpus> -t <num_threads>
# Example: ./run_all_benchmarks_parallel.sh -o ./RESULTS -n 4 -t 4

# Default values
OUTPUT_BASE_DIR="./RESULTS"
NUM_CPUS=1
NUM_THREADS=1  # Number of parallel simulations

# Parse arguments
while getopts "o:n:t:" opt; do
    case $opt in
        o) OUTPUT_BASE_DIR="$OPTARG" ;;
        n) NUM_CPUS="$OPTARG" ;;
        t) NUM_THREADS="$OPTARG" ;;
        *) echo "Usage: $0 -o <output_base_dir> -n <num_cpus> -t <num_threads>"; exit 1 ;;
    esac
done

# Check required arguments
if [ -z "$OUTPUT_BASE_DIR" ] || [ -z "$NUM_THREADS" ]; then
    echo "Error: Output base directory and number of threads are required."
    echo "Usage: $0 -o <output_base_dir> -n <num_cpus> -t <num_threads>"
    exit 1
fi

# List of benchmarks to run
BENCHMARKS=(
    bwaves_s
    cactuBSSN_s
    lbm_s
    wrf_s
    cam4_s
    pop2_s
    imagick_s
    nab_s
    fotonik3d_s
    rom_s
    specrand_fs
    perlbench_s
    gcc_s
    mcf_s
    omnetpp_s
    xalancbmk_s
    x264_s
    deepsjeng_s
    leela_s
    exchange2_s
    xz_s
    specrand_is
    bwaves_r
    cactuBSSN_r
    lbm_r
)

# Function to run a benchmark
run_benchmark() {
    local BENCHMARK="$1"
    local OUTPUT_DIR="$OUTPUT_BASE_DIR/$BENCHMARK"

    mkdir -p "$OUTPUT_DIR"  # Ensure the output directory exists
    echo "Starting benchmark: $BENCHMARK (Output: $OUTPUT_DIR)"
    ./runner.sh -b "$BENCHMARK" -o "$OUTPUT_DIR" -n "$NUM_CPUS"
    if [ $? -ne 0 ]; then
        echo "Error running benchmark: $BENCHMARK"
    else
        echo "Completed benchmark: $BENCHMARK"
    fi
}

# Run benchmarks in parallel
echo "Running benchmarks in parallel with $NUM_THREADS threads..."
THREADS=0

for BENCHMARK in "${BENCHMARKS[@]}"; do
    run_benchmark "$BENCHMARK" &  # Run the benchmark in the background
    ((THREADS++))

    # Wait for all threads to complete if reaching the thread limit
    if (( THREADS >= NUM_THREADS )); then
        wait
        THREADS=0
    fi
done

# Wait for any remaining background jobs to finish
wait

echo "All benchmarks completed."
