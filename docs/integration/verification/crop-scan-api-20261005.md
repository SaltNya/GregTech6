# Issue 13: addon crop scanning

An addon can implement `com.gregtech.gregtech.api.crop.CropScanSource` on its crop block entity without an IC2 dependency. Return `CropScanData` with the name, attributes, discoverer, growth/gain/resistance, fertilizer/water/WeedEX, nutrients/humidity/air and current scan level. Return null when no crop is present. `setCropScanLevel` records discovery at level 4. Existing IC2 reflection remains the fallback. Both native scanner adapters use this shared reader.

The original scanner formatter and 32768/512 discovery/repeat costs are preserved. The shared contract checks passed (2465 assertions, 30 groups total). A third-party addon installation has not been tested.

Source hash, author and license: [source record](crop-scan-api-20261005.json).
