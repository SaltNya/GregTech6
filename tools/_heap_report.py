import io
import re
import sys

path = 'build/heap-world.log'
lines = io.open(path, encoding='utf-8-sig', errors='replace').read().splitlines()


def inst(line, name):
    m = re.search(r'(\d+):\s+(\d+)\s+(\d+)\s+([\w.$]+)', line)
    for m in re.finditer(r'(\d+):\s+(\d+)\s+(\d+)\s+([\w.$]+)', line):
        if m.group(4).endswith(name):
            return int(m.group(2))
    return None


def used(line):
    m = re.search(r'used (\d+)K', line)
    return int(m.group(1)) // 1024 if m else None


samples = []
for l in lines:
    if l.startswith('[') and 'garbage-first' in l:
        samples.append({'ts': l[1:9], 'used': used(l)})
    elif l.startswith('[') and ':' in l:
        if samples:
            samples[-1].update({
                'chunk': inst(l, 'LevelChunk'),
                'ore': inst(l, 'OreBlockEntity'),
                'node': inst(l, 'HashMap$Node'),
                'stack': inst(l, 'ItemStack'),
                'tag': inst(l, 'CompoundTag'),
            })

print('samples: %d' % len(samples))
sys.stdout.write('%-8s %7s %7s %10s %10s %9s %8s\n' % ('time', 'usedMB', 'chunks', 'oreBE', 'BE/chunk', 'MapNode', 'ItemStack'))
for s in samples:
    ore, chunk = s.get('ore'), s.get('chunk')
    ratio = ('%.0f' % (ore / chunk)) if ore and chunk else '-'
    sys.stdout.write('%-8s %7s %7s %10s %10s %10s %8s\n' % (
        s['ts'], s.get('used'), chunk if chunk else '-', ore if ore else '-', ratio,
        s.get('node', '-'), s.get('stack', '-')))

if len(samples) >= 4:
    tail = samples[-4:]
    ores = [s.get('ore') for s in tail if s.get('ore')]
    chunks = [s.get('chunk') for s in tail if s.get('chunk')]
    useds = [s.get('used') for s in tail if s.get('used')]
    print('\nlast 4 samples: ore delta %s, chunk delta %s, used delta %s MB' % (
        (ores[-1] - ores[0]) if len(ores) > 1 else '-',
        (chunks[-1] - chunks[0]) if len(chunks) > 1 else '-',
        (useds[-1] - useds[0]) if len(useds) > 1 else '-'))
