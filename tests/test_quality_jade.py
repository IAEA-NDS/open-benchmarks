import json
import os
from pathlib import Path
import pandas as pd
import re
from f4enix import Input

rmode_pat = re.compile(r"RMODE", re.IGNORECASE)

ROOT = Path("jade_open_benchmarks")


def test_metadata():
    for folder in os.listdir(ROOT / "inputs"):
        path_folder = ROOT / "inputs" / folder
        if not path_folder.is_dir():
            continue
        with open(path_folder / "benchmark_metadata.json") as f:
            data = json.load(f)
        assert data["name"] == folder

        # check internal structure
        ref_set_flag = False
        for subrun in os.listdir(path_folder):
            if subrun == "benchmark_metadata.json":
                continue

            codes = os.listdir(path_folder / subrun)
            if not ref_set_flag:
                ref_codes = codes
                ref_set_flag = True
                continue

            # check that in all subrun the same codes are implemented
            assert codes == ref_codes, f"Subrun {subrun}"

        # check that the version is specified for each code
        for code in ref_codes:
            assert data["version"][code]


def test_error_relative():
    absolute_errors = []

    # these are exceptions where the rel error is indeed above 1
    manually_checked = ["Tiara-BC", "FNS-TOF"]

    for folder in os.listdir(ROOT / "exp_results"):
        if folder in manually_checked:
            continue
        for file in os.listdir(ROOT / "exp_results" / folder):
            file = ROOT / "exp_results" / folder / file
            df = pd.read_csv(file)
            if df["Error"].max() > 1:
                absolute_errors.append(folder)
                print(
                    f"Absolute error found in {file}: max error = {df['Error'].max()}"
                )
    absolute_errors = list(set(absolute_errors))
    assert len(absolute_errors) == 0, f"Folders with absolute errors: {absolute_errors}"


def test_no_RMODE_card():
    for file in mcnp_input_paths_generator():
        with open(file) as f:
            for line in f:
                if rmode_pat.match(line):
                    raise AssertionError(f"RMODE card found in {file}")


def test_f4enix_readability():
    """test that all MCNP input files can be read by f4enix"""
    for file in mcnp_input_paths_generator():
        _ = Input.from_input(file)


def test_exp_data_naming_consistency():
    """test that all files in exp_results have a corresponding input file with the
    same name"""
    known_exceptions = ["Oktavian_Pb"]
    for folder in os.listdir(Path(ROOT, "exp_results")):
        path_folder = Path(ROOT, "exp_results", folder)
        for file in os.listdir(path_folder):
            name = file.split(" ")[0]
            if name in known_exceptions:
                continue
            assert Path(ROOT, "inputs", folder, name).exists(), (
                f"File {file} in {folder} does not match any input file"
            )


def test_mcnp_filename_matches_subrun():
    """Test that MCNP input file names match their parent subrun folder names."""
    for folder in os.listdir(ROOT / "inputs"):
        folder_path = ROOT / "inputs" / folder
        if not folder_path.is_dir():
            continue
        for subrun in os.listdir(folder_path):
            subrun_path = folder_path / subrun
            if not subrun_path.is_dir():
                continue
            for code in os.listdir(subrun_path):
                if code != "mcnp":
                    continue
                mcnp_path = subrun_path / code
                # Get all .i files in the mcnp directory
                i_files = list(mcnp_path.glob("*.i"))
                assert len(i_files) == 1, (
                    f"Expected exactly 1 .i file in {mcnp_path}, found {len(i_files)}"
                )

                expected_filename = f"{subrun}.i"
                actual_filename = i_files[0].name
                assert actual_filename == expected_filename, (
                    f"File name mismatch in {mcnp_path}: expected '{expected_filename}', found '{actual_filename}'"
                )


def test_prdmp_card_settings():
    """Test that all MCNP input files have a suitable PRDMP card
    settings should be explicit, mctal file needs to be printed and dump frequency
    cannot be too low."""
    for file in mcnp_input_paths_generator():
        found = False
        with open(file) as f:
            for line in f:
                if line.strip().upper().startswith("PRDMP"):
                    prdmp_values = re.split(r"\s+", line.strip())
                    # force card to be in explicit
                    found = True
                    break
        if not found:
            raise AssertionError(f"PRDMP card not found in {file}")
        else:
            assert len(prdmp_values) == 6, f"PRDMP card not explicit in {file}, {line}"
            assert prdmp_values[1].upper() == "J"  # NDP
            assert float(prdmp_values[2]) >= 5e7 or float(prdmp_values[2]) < -60  # NDM
            assert int(prdmp_values[3]) > 0  # MCT
            assert int(prdmp_values[4]) in [1, 2]  # NDMP no more than 2 dumps in runtpe
            try:
                DDMP = int(prdmp_values[5])
            except ValueError:
                DDMP = float(prdmp_values[5])

            assert DDMP == 0 or DDMP >= 5e7  # DMMP


def mcnp_input_paths_generator():
    for folder in os.listdir(Path(ROOT, "inputs")):
        folder_path = Path(ROOT, "inputs", folder)
        if not folder_path.is_dir():
            continue
        for subrun in os.listdir(folder_path):
            subrun_path = folder_path / subrun
            if not subrun_path.is_dir():
                continue
            for code in os.listdir(subrun_path):
                if code != "mcnp":
                    continue

                yield subrun_path / code / f"{subrun}.i"
