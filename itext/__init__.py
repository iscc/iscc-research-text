# -*- coding: utf-8 -*-
import os
import click
from os.path import join, basename

__version__ = "0.1.0"
APP_NAME = "iscc-text-research"
APP_DIR = click.get_app_dir(APP_NAME, roaming=False)
UNPAYWALL_URL = (
    "https://unpaywall-data-snapshots.s3-us-west-2.amazonaws.com/"
    "unpaywall_snapshot_2021-07-02T151134.jsonl.gz"
)
UNPAYWALL_SIZE = 27353738031
UNPAYWALL_FILE = join(APP_DIR, basename(UNPAYWALL_URL))

os.makedirs(APP_DIR, exist_ok=True)
