#!/bin/bash

# Used to run a single benchmark with our cpu
# Usage: ./run_gem5_simulation.sh -b <benchmark_name> -o <output_directory> -n <num_cpus>

# Default values (edit as needed)
CPU_TYPE="O3CPU"
MAX_INSTS=1000000000
L1I_SIZE="32kB"
L1D_SIZE="32kB"
L1D_ASSOC=8
L1I_ASSOC=8  
CACHELINE_SIZE=64
NUM_CPUS=1

# Parse arguments
while getopts "b:o:n:" opt; do
    case $opt in
        b) BENCHMARK="$OPTARG" ;;
        o) OUTDIR="$OPTARG" ;;
        n) NUM_CPUS="$OPTARG" ;;
        *) echo "Usage: $0 -b <benchmark_name> -o <output_directory> -n <num_cpus>"; exit 1 ;;
    esac
done

# Check if required arguments are provided
if [ -z "$BENCHMARK" ] || [ -z "$OUTDIR" ]; then
    echo "Error: Benchmark name and output directory are required."
    echo "Usage: $0 -b <benchmark_name> -o <output_directory> -n <num_cpus>"
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "$OUTDIR"

# Run the gem5 simulation
./build/ECE565-X86/gem5.opt \
    --outdir="$OUTDIR" \
    configs/spec/spec_se.py \
    -b "$BENCHMARK" \
    --cpu-type="$CPU_TYPE" \
    --maxinsts="$MAX_INSTS" \
    --caches \
    --num-cpus="$NUM_CPUS" \
    --l1i_size="$L1I_SIZE" \
    --l1i_assoc="$L1I_ASSOC" \
    --l1d_size="$L1D_SIZE" \
    --l1d_assoc="$L1D_ASSOC" \
    --cacheline_size="$CACHELINE_SIZE"

# Notify the user that the simulation is complete
echo "Simulation for benchmark '$BENCHMARK' with $NUM_CPUS CPU(s) completed."
echo "Output is in directory: $OUTDIR"
