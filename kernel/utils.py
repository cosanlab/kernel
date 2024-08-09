import os
import h5py
from mne.io import read_raw_snirf
import numpy as np
import pandas as pd
import kernel


def get_resource_path():
    """Get path to feat resource directory."""
    return os.path.join(kernel.__path__[0], "resources")


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
                file["nirs"][stim]["data"][()],
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


def pick_channels_from_distance_mne_epochs(
    snirf_file, epochs, min_distance=None, max_distance=None
):
    """
    Pick Channels based on Source-Detector Distance for mne.Epochs object instance

    Args:
        min_distance (int): minimum distance (mm) between source and detector. None indicates no bound
        max_distance (int): maximum distance (mm) between source and detector. None indicates no bound

    Returns:
        idx_channels (np.array): index to each channel to retain
    """

    # Get information about each optode
    probe_data = get_optodes(snirf_file)

    # Access the Source-Detector distance for each channel
    idx_sources = np.array(
        [int(ch.split("_")[0][1:]) - 1 for ch in epochs.info["ch_names"]]
    )
    idx_detectors = np.array(
        [int(ch.split("_")[1].split(" ")[0][1:]) - 1 for ch in epochs.info["ch_names"]]
    )
    source_positions = np.array(probe_data["sourcePos3D"])[idx_sources]
    detector_positions = np.array(probe_data["detectorPos3D"])[idx_detectors]
    sds = np.sqrt(np.sum((source_positions - detector_positions) ** 2, axis=1))

    # find index of source-detector distances between min_distance and max_distance
    if min_distance is None:
        if max_distance is None:
            idx_channels = np.flatnonzero(sds)
        else:
            idx_channels = np.flatnonzero(sds < max_distance)
    else:
        if max_distance is None:
            idx_channels = np.flatnonzero(sds > min_distance)
        else:
            idx_channels = np.flatnonzero((sds > min_distance) & (sds < max_distance))

    return idx_channels
