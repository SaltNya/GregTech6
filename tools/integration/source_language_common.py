"""Shared lexical/material spelling rules for read-only original language importers."""
import re

STRING = r'"(?:\\.|[^"\\])*"'


def material_key(name):
    internal = re.sub(r"[ \-'/]", '', name)
    return 'gt.material.' + internal[:1].upper() + internal[1:]
