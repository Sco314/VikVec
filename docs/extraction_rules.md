# Extraction Rules

- Identify scene islands first and isolate them as independent regions.
- Crop each region with a small amount of padding so the asset remains readable.
- Remove black or white background when the crop is intended to become a reusable asset.
- Mark screenshot crops as raster_reference_only when they are only being stored as references.
- Flag bad or occluded crops as rebuild_needed so they can be improved later.
