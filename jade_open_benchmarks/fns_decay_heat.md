# FNS iron decay heat, 1996 five-minute irradiation

This initial `FNS-DecayHeat` case contains the JAEA Fusion Neutronics Source
(FNS) iron experiment from the 1996 campaign, distributed by the IAEA through
[CoNDERC](https://www-nds.iaea.org/conderc/). It requires the ACTINV scalar code
target introduced in [JADE PR #549](https://github.com/JADE-V-V/JADE/pull/549).
It is distinct from the FNS time-of-flight benchmark.

## JADE files

- Input: `inputs/FNS-DecayHeat/Fe-1996-5min/actinv/spec.json`.
- Version: `inputs/FNS-DecayHeat/benchmark_metadata.json`, ACTINV `1.0.0`.
- Measurements: `exp_results/FNS-DecayHeat/Fe-1996-5min Decay heat.csv`.

The input describes one gram of elemental iron (`FE: 100` weight percent), a
300-second irradiation at a total neutron flux of `1.116e10 n/cm²/s`, and the
original inline 709-group FISPACT spectrum in its original group order. The
spectrum is normalized to the total flux specified by the source input deck.
No neutron transport calculation is needed.

Each of the 20 measured cooling times is a schedule endpoint. Cooling steps
have zero flux, and their positive incremental durations are derived from the
published decimal-minute measurements. The older FISPACT deck's rounded
whole-second cooling increments are not used. The ACTINV output therefore has
21 endpoints, including the end of irradiation at 300 seconds.

The CSV columns are:

| Column | Meaning |
| --- | --- |
| `time` | Seconds after shutdown, published minutes multiplied by 60. |
| `Value` | Published decay heat in microW/g. |
| `Error` | Published absolute error divided by the measured heat. |

No measurement is omitted or interpolated. The published error magnitude is
preserved; no confidence level or covariance is assumed. The comparison is
calculated/measured decay heat. ACTINV supplies zero Monte Carlo sampling error;
the resulting C/E error represents the reported measurement error, not total
predictive uncertainty.

The portable `catalog:` activation and decay references are defaults for
standalone ACTINV use. JADE replaces them with the library and decay files
selected in its configuration. Activation and decay libraries are installed
separately and are not included in this benchmark package.

## Source and changes

The source is the IAEA CoNDERC
[`fns.zip` archive](https://www-nds.iaea.org/conderc/fusion/files/fns.zip),
SHA-256 `ba1dd6cb150a4aa3e0d81461054aec7d415ef19d946aba8b9886b31de218252d`.
The relevant original members are:

| Member under `fns/Fe/` | SHA-256 |
| --- | --- |
| `1996exp_5min.exp` | `4eb4635d1d70498f691284d396d2a9276beb8ff161e1f568d1622256c80b6c64` |
| `1996exp_5min_fluxes` | `6c2a23393bd71bc5ac957ee53ca6b6ea747b8b0ed87d19361053f37505937d66` |
| `TENDL-2017_1996exp_5min.i` | `fdb943333dd293cdda057fad49df8bf152000cf3f48fa64b12afd54a57eda071` |
| `total_1996exp_5min.pdf` | `d6ea06aadbf0fc9c2ad91452b32e8e0e64afe692c5624d07ccd03fb1673bb876` |

The source plot identifies heat in microW/g and time after irradiation in
minutes. Changes for JADE are conversion of the input to ACTINV JSON, exact
measurement-time schedule endpoints, conversion of minutes to seconds, and
conversion of absolute measurement errors to relative errors. The spectrum,
material, source-deck total flux, irradiation duration and measured heat values
are retained. This package follows this repository's existing CoNDERC
attribution and [CC BY 4.0 license](../LICENSE).
