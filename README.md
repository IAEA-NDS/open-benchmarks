# Open benchmarks for FENDL V&V

The purpose of this repository is to compile
transport code input files, reference output,
and associated experimental data, adopting a systematic
directory structure to facilitate interfacing V&V systems
with it.

:warning: **This is a work in progress repository**
users should be aware that significant changes could be made to the structures and/or the files until a more stable stage for the project is reached.

## Description of contents

- [jade_open_benchmarks](./jade_open_benchmarks) contains all template inputs of the benchmarks that are freely distributed and that can be used in [JADE](https://jade-a-nuclear-data-libraries-vv-tool.readthedocs.io/en/latest/). A complete description of the benchmarks can be found in the [specific JADE documentation section](https://jade-a-nuclear-data-libraries-vv-tool.readthedocs.io/en/latest/usage/benchmarks.html). Additional details on how the repo is structured and how to upload or modify the inputs are provided [here](./jade_open_benchmarks/jade_benchmarks.md).

## License

All data (including input files, reference output and experimental data) in this repository are distributed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/deed.en) license.
See the `LICENSE` file for details on terms and conditions. 

## Related projects

- Part of the computational inputs, reference otputs and experimental data have been adopted from the [CoNDERC project](https://nds.iaea.org/conderc). Some of the inputs may have been modified if mistakes in the input files have been discovered or due to JADE specific needs. Technical solutions to synchronize this repository with CoNDERC will be investigated in the future. 


# Developers notes

## Git Large Files System (LFS)
This repository makes use of [git lfs](https://git-lfs.com/) an extension of ``git`` which allows to deal more effectively with large files. This is necessary to deal with weight windows file which can be quite heavy and not exactly git-friendly.
To take advantage of git-lfs, developers should:
1) Install the git lfs ectension from the website
2) activate it through ``git lfs install`` (to be run only once per user account)

Additional files to be tracked with lfs system can be added with ``git lfs track "<some regex>"`` where the admissible regex are the same as for the ``.gitignore`` file. To check which files are currently tracked via lfs one can run ``git lfs ls-files``. 
