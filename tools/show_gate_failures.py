"""Prints every failed GameTest of the last gate run, in one go.

The gate log is UTF-8 and its failures are one line each, so the discipline this tool encodes is
simple: **read all of them before touching any code**. A red list is rarely one problem - the §108
rounds went 10 red -> 4 red -> 5 red, and in the second round two of the four were the same root cause
(the entity query limitation) while two were unrelated. Classify first:

  * a wrong test expectation (the GT6 source disagrees with the assertion),
  * an environment limitation (a test chunk's entity sections are HIDDEN, a mock player has no
    network channel, ...),
  * a seed-dependent existing test (terrain where the test expected air),
  * a real implementation bug - the only class that should change production code.

Usage:
  python tools/show_gate_failures.py [--log build/gametest.log] [--context 3]
"""

import argparse
import io
import re
import sys

FAIL = re.compile(r"LogTestReporter\]: (?P<message>.*)$")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="build/gametest.log")
    parser.add_argument("--context", type=int, default=0,
                        help="also print this many log lines around each failure")
    args = parser.parse_args()

    try:
        lines = io.open(args.log, encoding="utf-8", errors="replace").read().splitlines()
    except FileNotFoundError:
        print("no gate log at %s" % args.log)
        return 1

    failures = [(i, FAIL.search(line).group("message")) for i, line in enumerate(lines)
                if FAIL.search(line)]
    for index, message in failures:
        # The gate log is UTF-8 with mojibake in it, and this prints to whatever console the caller
        # has - a Windows console in a GBK code page raises UnicodeEncodeError on the replacement
        # character alone. Escaping to ASCII keeps the diagnostic readable instead of crashing on it.
        print(ascii(message[:400]))
        if args.context:
            for j in range(max(0, index - args.context), min(len(lines), index + args.context + 1)):
                print("    | " + ascii(lines[j][:190]))
        print("-" * 100)

    counts = [line for line in lines if "required tests" in line or "GAME TESTS COMPLETE" in line
              or "tests are now running" in line]
    for line in counts:
        print(ascii(line[:190]))
    print("%d failures in %d log lines" % (len(failures), len(lines)))
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
