# JADE Benchmark inputs
All benchmark inputs that can be freely redistributed and are used in [JADE](https://jade-a-nuclear-data-libraries-vv-tool.readthedocs.io/en/latest/) are stored in this repository.

The structure of the files is as follows:
```
jade_open_benchmarks
        |
        |------- exp_results
        |           |------------<benchmark name>
        |
        |------- inputs
                    |
                    |
                    |
                    |---<benchmark_name>
                    |            |
                    |            |-----<run name>
                    |            |        |------<code>
                    |            |                  |-----<benchmark input files>
                    |            |           
                    |            |----benchmark_metadata.json
                    |
                    |---<...>                            

```
If a new benchmark is added to this repository, it shall follow the same structure presented here, including a `benchmark_metada.json` file in the input folder as the example below:

```json
{
    "name": "ITER_1D",
    "version": {
        "mcnp": "1.0",
        "openmc": "1.0",
        "serpent": "1.0"
    }
}
```

The supported codes (at varying degrees of maturity) for JADE at the moment are `mcnp`, `openmc`, `serpent` and `d1s` (D1SUNED).

Whenever a pull request is filed to change one of these inputs, the benchmark version in the metadata MUST be modified as well. The semantic versioning for the benchmarks foresees only two change levels:
- **major**, if the retrocompatibility is not guaranteed. That is, results computed on previous version of the benchmark cannot be compared with the ones obtained from the new version.
- **minor**, all improvements to the benchmark that guarantee retrocompatibility for results comparison. These could be aestethic changes, performance improvement, addition of variance reduction or even tallies additions in some cases.