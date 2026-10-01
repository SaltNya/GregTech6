"""Prepare resources through Gradle, preserving its incremental output snapshots.

Do not write build/resources/main outside Gradle. runGameTestServer now uses its
normal resource dependency; -x processResources is no longer needed.
"""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    result=subprocess.run([str(ROOT/'gradlew.bat'),'processResources','--offline','--console=plain'],cwd=ROOT)
    if result.returncode:raise SystemExit(result.returncode)

if __name__=='__main__':main()
