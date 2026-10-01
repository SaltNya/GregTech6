"""Record a 60-second creative-inventory reproduction with the JDK's local tools.

Usage: python tools/capture_client_memory.py --pid GAME_JAVA_PID
Start this with the game running, then open and scroll the creative inventory.
No forced GC, heap dump, game settings changes or network upload is performed.
"""
import argparse
import datetime
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_jcmd():
    executable = shutil.which('jcmd')
    if executable:
        return executable
    settings = subprocess.run(['java', '-XshowSettings:properties', '-version'], capture_output=True, text=True)
    match = re.search(r'java.home\s*=\s*(.+)', settings.stderr)
    if match:
        for filename in ('jcmd.exe', 'jcmd'):
            executable = Path(match.group(1).strip()) / 'bin' / filename
            if executable.is_file():
                return str(executable)
    raise SystemExit('JDK jcmd was not found. Install/configure a JDK, rather than a JRE.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', required=True, type=int)
    parser.add_argument('--seconds', type=int, default=60)
    args = parser.parse_args()
    if args.pid <= 0 or not 10 <= args.seconds <= 300:
        parser.error('Use a positive game PID and a duration of 10..300 seconds.')
    directory = ROOT / 'build/memory' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    directory.mkdir(parents=True, exist_ok=True)
    executable = find_jcmd()
    for command in ('VM.flags', 'GC.heap_info'):
        result = subprocess.run([executable, str(args.pid), command], capture_output=True, text=True)
        (directory / (command + '.txt')).write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            raise SystemExit(f'Cannot inspect game PID {args.pid}: {result.stderr or result.stdout}')
    recording = directory / 'creative-scroll.jfr'
    result = subprocess.run([executable, str(args.pid), 'JFR.start', 'name=gt6-creative-scroll',
                             'settings=profile', f'duration={args.seconds}s', f'filename={recording}'],
                            capture_output=True, text=True)
    (directory / 'recording.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
    print(result.stdout or result.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)
    print(f'Scroll the creative inventory now. Recording finishes automatically after {args.seconds} seconds: {recording}')


if __name__ == '__main__':
    main()
