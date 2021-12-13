# -*- coding: utf-8 -*-
"""Library of utility functions for the project"""
from pathlib import Path
import json_lines
import itext
from loguru import logger as log
import urllib.request
from alive_progress import alive_bar
from typing import Generator


def reader():
    # type: () -> Generator[dict, None, None]
    """Returns a generator object that yields rows from the unpaywall dataset"""
    path = download_dataset()
    with json_lines.open(path.as_posix()) as f:
        for item in f:
            yield item


def download_dataset():
    # type: () -> Path
    """Downloads dataset if not available and returns local file path"""

    # Check if we already have the dataset
    path = Path(itext.UNPAYWALL_FILE)
    exists = path.exists() and path.stat().st_size == itext.UNPAYWALL_SIZE
    if exists:
        log.info(f"dataset at {path}")
        return path

    # Streaming download with progress bar
    log.info(f"downloading from {itext.UNPAYWALL_URL}")
    log.info(f"downloading to   {itext.UNPAYWALL_FILE}")
    with path.open("wb") as outfile:
        with urllib.request.urlopen(itext.UNPAYWALL_URL) as stream:
            with alive_bar(itext.UNPAYWALL_SIZE, title="Unpaywall Download") as bar:
                data = stream.read(250000)
                while data:
                    outfile.write(data)
                    bar(250000)
                    data = stream.read(250000)
    return path


if __name__ == "__main__":
    download_dataset()
