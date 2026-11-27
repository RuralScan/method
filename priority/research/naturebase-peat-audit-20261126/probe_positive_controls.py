"""Locate one positive native cell per raster; not a global accuracy test."""
import argparse
import json
from pathlib import Path

import numpy as np
import rasterio

parser = argparse.ArgumentParser()
parser.add_argument("restoration")
parser.add_argument("management")
parser.add_argument("output")
args = parser.parse_args()
results = {}
for prefix, path in [("wet_per", args.restoration), ("wet_ipm", args.management)]:
    with rasterio.open(path) as dataset:
        for _, window in dataset.block_windows(1):
            values = dataset.read(1, window=window, masked=True)
            positions = np.argwhere((values > 0).filled(False))
            if not len(positions):
                continue
            local_row, local_col = positions[0]
            row = int(window.row_off + local_row)
            col = int(window.col_off + local_col)
            lon, lat = dataset.xy(row, col)
            results[prefix] = {"lon": lon, "lat": lat,
                               "value": float(values[local_row, local_col]),
                               "row": row, "col": col}
            break
        else:
            results[prefix] = None
Path(args.output).write_text(json.dumps(results, indent=2) + "\n")
