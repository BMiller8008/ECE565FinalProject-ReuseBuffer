# ECE565FinalProject-ReuseBuffer

Purdue ECE565 Final Project

This project implements the ReuseBuffer, a buffer design aimed at improving CPU performance through the efficient reuse of intermediate computation results. Our implementation is based on the design and techniques outlined in the following research paper:

https://ieeexplore.ieee.org/document/604688

Project Overview:
The ReuseBuffer is an exciting new way to make processors more efficient by reducing repetitive calculations. It works by holding onto intermediate results so they can be reused later, cutting down on unnecessary cycles and saving power.

Objective:
We’re aiming to see how practical the ReuseBuffer really is and measure how much it can improve performance. To test this, we’ve implemented the ReuseBuffer concept within the gem5 O3CPU model. This model, part of the widely-used gem5 simulator, is perfect for experimenting with out-of-order CPU behaviors and testing performance optimizations like ours.

Implementation Details:
Simulator: We’re using the gem5 simulation environment to build and test our ReuseBuffer.
CPU Model: Our focus is on the O3CPU, which can simulate out-of-order execution, making it ideal for evaluating advanced scheduling and speculation techniques.To simulate a modern processor, both out I and D caches were 32kB with 8-way associativity.

Modifications: We’ve made specific modifications to the O3CPU model to add the ReuseBuffer, enabling it to keep track of intermediate results so they can be dynamically reused in future instructions. These changed occured in the IEW stage of the O3 pipeline.

Evaluation:

We will be using the following SPEC2017 benchmarks to evaluate performance before and after the reuse buffer is added to the O3CPU:
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
