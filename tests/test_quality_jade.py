import json
import os
from pathlib import Path
import pandas as pd
import re

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
                file = subrun_path / code / f"{subrun}.i"
                with open(file) as f:
                    for line in f:
                        if rmode_pat.match(line):
                            raise AssertionError(f"RMODE card found in {file}")


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
