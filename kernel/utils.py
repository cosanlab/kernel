import h5py
from mne.io import read_raw_snirf
import numpy as np
import pandas as pd


def load_snirf_file(snirf_file, drop_bad_channels=True):
    """Helper function to load Kernel SNIRF files"""

    raw = read_raw_snirf(snirf_file)
    raw.load_data()

    raw._data *= 1e-6  # Kernel Recommended unit scaling

    if drop_bad_channels:  # drop bad channels that are full of nans
        idx_drop = np.where(np.any(np.isnan(raw._data), axis=1))[0]
        raw = raw.drop_channels(np.array(raw.info["ch_names"])[idx_drop])

    return raw


def extract_stimulus_data(snirf_file):
    """helper function to extract stimulus file information from SNIRF HDF5 container"""

    with h5py.File(snirf_file, "r") as file:
        stim_data = {}
        for stim in [x for x in file["nirs"] if "stim" in x]:
            stim_data[file["nirs"][stim]["name"][()].decode("utf-8")] = pd.DataFrame(
                file["nirs"]["stim1"]["data"][()],
                columns=[
                    col.decode("UTF-8") for col in file["nirs"][stim]["dataLabels"]
                ],
            )
    return stim_data


def get_optodes(snirf_file):
    """extract information about source and detector optode names and mni coordinates"""
    probe_keys = [
        ("detectorLabels", str),
        ("sourceLabels", str),
        ("sourcePos3D", float),
        ("detectorPos3D", float),
    ]
    with h5py.File(snirf_file, "r") as file:
        probe_data = {
            key: np.array(file["nirs"]["probe"][key]).astype(dtype)
            for key, dtype in probe_keys
        }
    return probe_data
