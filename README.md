# Open benchmarks for FENDL V&V

The objective of this repository is to compile
transport code input files, reference output,
and associated experimental data, adopting a systematic
directory structure to facilitate interfacing V&V systems
with it.

:warning: **This is a work in progress repository**
users should be aware that significant changes could be made to the structures and/or the files until a more stable stage for the project is reached.

## Description of contents
- [jade_open_benchmarks](./jade_open_benchmarks) contains all template inputs of the benchmarks that are freely distributed and that can be used in [JADE](https://jade-a-nuclear-data-libraries-vv-tool.readthedocs.io/en/latest/). A complete description of the benchmarks can be found in the [specific JADE documentation seciton](https://jade-a-nuclear-data-libraries-vv-tool.readthedocs.io/en/latest/usage/benchmarks.html). Part of the computational inputs, reference otputs and experimental data have been adopted from the [CoNDERC project](https://nds.iaea.org/conderc). Some of the inputs may have been modified if mistakes in the input files have been discovered or due to JADE specific needs. Technical solutions to synchronize this repository with CoNDERC will be investigated in the future. Additional details on how the repo is structured and how to upload or modify the inputs is provided [here](./jade_open_benchmarks/jade_benchmarks.md).
