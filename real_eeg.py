import os
import wget
import mne
import numpy as np


BASE_URL = "https://physionet.org/files/eegmmidb/1.0.0/"


FILES = [

    "S001/S001R01.edf",
    "S001/S001R03.edf"

]


RAW_DIR = "data/raw"


def download_dataset():

    os.makedirs(
        RAW_DIR,
        exist_ok=True
    )

    for file in FILES:

        filename = os.path.basename(file)

        output = os.path.join(
            RAW_DIR,
            filename
        )

        if not os.path.exists(output):

            print(f"Downloading {filename}")

            wget.download(
                BASE_URL + file,
                output
            )

            print()


def preprocess_raw(raw):

    raw.filter(
        1.,
        45.,
        verbose=False
    )

    raw.notch_filter(
        50.,
        verbose=False
    )

    raw.set_eeg_reference(
        'average',
        verbose=False
    )

    return raw


def load_rest_data():

    file = os.path.join(
        RAW_DIR,
        "S001R01.edf"
    )

    raw = mne.io.read_raw_edf(
        file,
        preload=True,
        verbose=False
    )

    raw = preprocess_raw(raw)

    return raw


def load_task_data():

    file = os.path.join(
        RAW_DIR,
        "S001R03.edf"
    )

    raw = mne.io.read_raw_edf(
        file,
        preload=True,
        verbose=False
    )

    raw = preprocess_raw(raw)

    return raw


def extract_signal(raw):

    data = raw.get_data()

    signal = np.mean(
        data,
        axis=0
    )

    return signal