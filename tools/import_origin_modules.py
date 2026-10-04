"""Import GT6's remaining origin modules without writing to the source checkout."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'gregtech6-master/gregtech6-master/src/main/java/gregtech/worldgen/center'
TARGET = ROOT / 'core/src/main/java/com/gregtech/gregtech/worldgen/center'


def source(name):
    raw = (SOURCE / (name + '.java')).read_text(encoding='utf-8')
    body = raw[raw.index('\t@Override\n\tpublic boolean generate('):]
    return raw, raw[:raw.index('package ')], body[body.index(' {'):]


def write(name, license, fields, body):
    text = license + 'package com.gregtech.gregtech.worldgen.center;\n'
    text += 'import static com.gregtech.gregtech.worldgen.center.OriginSupport.*;\n'
    text += '/** Original Gregorius Techneticies geometry; platform operations use OriginWorld. */\n'
    text += 'public final class ' + name + ' {\n' + fields + body
    (TARGET / (name + '.java')).write_text('\n'.join(line.rstrip() for line in text.splitlines()) + '\n', encoding='utf-8')


raw, license, body = source('WorldgenCenterBiomes')
body = '    public boolean generate(OriginWorld aWorld, OriginWorld.Chunk aChunk, int aMinX, int aMinZ, java.util.Random aRandom)' + body
biomes = {'icePlains': 'snowy_plains', 'coldTaiga': 'snowy_taiga', 'mesa': 'badlands', 'swampland': 'swamp'}
body = re.sub(r'Arrays.fill\(aChunk.getBiomeArray\(\), \(byte\)BiomeGenBase\.(\w+)\.biomeID\);',
              lambda m: 'aWorld.biome(aChunk, "' + biomes.get(m[1], m[1]) + '");', body)
body = re.sub(r'\s*BlockRiver.PLACEMENT_ALLOWED = [TF];', '', body)
body = re.sub(r'WD\.set\s*\(', 'set(', body)
# Only absolute underground fill starts at the modern world minimum. The source's
# relative height+1 clearing loops must keep their offset and clear modern mountains.
body = re.sub(r'int k = 1; k < (mHeight-\d+);', r'int k = aWorld.minY()+1; k < \1;', body)
body = re.sub(r'int k = (-?\d+); k < 64; k\+\+\) set\(aChunk, i, mHeight\+k,',
              r'int k = \1; k < aWorld.maxY()-mHeight; k++) set(aChunk, i, mHeight+k,', body)
# Modern coarse dirt replaces the optional Et Futurum dirt block (both source branches are retained).
body = body.replace('IL.EtFu_Dirt.exists()', 'T').replace('Block tBlock = IL.EtFu_Dirt.block();',
                                                       'OriginWorld.Block tBlock = Blocks.coarse_dirt;')
body = re.sub(r'new WorldGenTrees\(F, (.*?), (\d+), (\d+), [TF]\).generate\(aWorld, aRandom, (.*?), (.*?), (.*?)\);',
              r'aWorld.tree(\4, \5, \6, \2, \1, aRandom);', body)
body = body.replace('MultiTileEntityRegistry tRegistry = MultiTileEntityRegistry.getRegistry("gt.multitileentity");', '')
body = re.sub(r'if \(tRegistry != null\) tRegistry.mBlock.placeBlock\(aWorld, (.*?), (.*?), (.*?), SIDE_UNKNOWN, \(short\)(\d+), .*?, F, T\);',
              lambda m: 'aWorld.litter(' + ', '.join(m[i] for i in range(1, 5)) + ', '
              + ('true' if 'Items.flint' in m[0] else 'false') + ');', body)
write('SourceCenterBiomes', license, '''    private final int mHeight;
    private static final boolean GENERATE_STREETS=true, GENERATE_NEXUS=true, GENERATE_TESTING=true;
    public SourceCenterBiomes(int height) { mHeight=height; }
''', body)

raw, license, body = source('WorldgenTesting')
body = '    public boolean generate(OriginWorld aWorld, OriginWorld.Chunk aChunk, int aMinX, int aMinZ)' + body
body = re.sub(r'WD\.set\s*\(', 'set(', body)
body = body.replace('((BlockMetaType)BlocksGT.GlowGlass).mSlabs', 'BlocksGT.GLOW_GLASS_SLABS')
body = body.replace('((BlockMetaType)BlocksGT.CFoam).mSlabs', 'BlocksGT.FOAM_SLABS')
body = body.replace('int k = 1;', 'int k = aWorld.minY()+1;').replace('k < 256', 'k < aWorld.maxY()')
body = body.replace('MultiTileEntityRegistry tRegistry = MultiTileEntityRegistry.getRegistry("gt.multitileentity");', '')
start = body.index('\t\t\tItemStack[] tInventory')
end = body.index('};', start) + 2
inventory = body[start:end]
body = body[:start] + body[end:]
rows = []
for line in inventory.splitlines()[1:]:
    line = line.strip().split('//')[0].strip().lstrip(',').strip()
    if line and line != '};':
        rows.append(line)
(TARGET / 'OriginTestInventory.java').write_text(
    license + 'package com.gregtech.gregtech.worldgen.center;\n'
    '/** Original WorldgenTesting inventory slots, resolved by the native item adapter. */\n'
    'public final class OriginTestInventory { private OriginTestInventory() {}\n'
    'public static final java.util.List<String> ROWS=java.util.List.of(\n'
    + ',\n'.join(json.dumps(row) for row in rows) + '\n);\n}\n', encoding='utf-8')
body = re.sub(r'tRegistry.mBlock.placeBlock\(aWorld, (.*?), (.*?), (.*?), SIDE_UNKNOWN, \(short\)\s*(\d+), (.*?), T, T\);',
              lambda m: 'aWorld.tile(' + ', '.join(m[i] for i in range(1, 5)) + ', ' + json.dumps(m[5]) + ');', body)
body = re.sub(r'\s*TileEntity tTileEntity = WD.te\([^;]+;\s*if \(tTileEntity instanceof TileEntityBase06Covers\) .*?;',
              '\n            aWorld.drain(36, mHeight-4, -17, SIDE_Z_POS);', body)
write('SourceTesting', license, 'private final int mHeight; public SourceTesting(int height) {mHeight=height;}\n', body)

report = {'scope': 'Read-only original inputs to shared origin planners; native adapter validation recorded separately',
          'sources': [{'path': str(SOURCE / (name + '.java')),
                       'sha256': hashlib.sha256((SOURCE / (name + '.java')).read_bytes()).hexdigest()}
                      for name in ['WorldgenCenterBiomes', 'WorldgenTesting']],
          'test_inventory_slots': len(rows)}
(ROOT / 'docs/integration/verification/origin-modules-source-20261004.json').write_text(
    json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('Imported complete biome/test-building planners and', len(rows), 'source inventory slots')
