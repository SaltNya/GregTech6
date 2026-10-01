# CI material snapshot repair and version 0.0.0

Failed run: https://github.com/SaltNya/GregTech6/actions/runs/36901215336

Both platform annotations report the same material snapshot assertion; the required-builds job then fails because its dependencies failed. The exact assertion was reproduced locally with `:core:materialBehaviorContracts` before changing its baseline.

## Cause and correction

The catalog snapshot includes `GTMaterial.getSourceMod().name`. The authorized rename changed `ModReferences.GT.name` from `GregTech` to `GregTech 6 Community Edition`, invalidating the pinned definitions and post-init fingerprints. Restoring only that display name in an ignored, temporary probe recovered both exact original fingerprints. Counts and all other observed fields remain preserved. See `core/provenance/community-material-baseline.json`.

The test keeps its full observation and uses the verified Community Edition fingerprints. No assertions or material fields were removed. The Forge CI task is now `:build`, so its matrix job targets the root Forge project instead of selecting build tasks across all subprojects.

The current source also retained calls to the missing shared `MoldCastingRules`; that previously implemented class was restored verbatim from the preserved integration snapshot, with its provenance recorded separately.

The user requested version `0.0.0` and both final platform JARs. Both platforms consume the root version property. Build commands and current artifact names are recorded in `docs/work/BUILDING.md`.

## Validation scope

Local pre-fix material task: failed with the same CI assertion.

Name-only differential probe: both original SHA-256 fingerprints recovered exactly.

Post-fix material task: passed, 6,154 assertions. Forge Java compilation: passed.

Remote confirmation: the user pushed commit `dbd38be949378aca72ea0174501a95c6d7c1f547`. Run https://github.com/SaltNya/GregTech6/actions/runs/36903728760 completed successfully in 4m 43s, including both platform jobs and the required-builds aggregate. Two packaging reports were produced. No remote push or workflow dispatch was performed by the agent.

Final local build and packaging results are recorded after the build finishes. No new client/server startup, gameplay or world reload is claimed by this change.
