"""Import the complete GT6 origin structures into the shared, game-independent placement planner.

Geometry and ordering come directly from the read-only original files. Only platform operations,
beacon effect writes, the world-bottom boundary and old chunk-loading probes are adapted.
"""
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'gregtech6-master/gregtech6-master/src/main/java/gregtech/worldgen/center'
TARGET = ROOT / 'core/src/main/java/com/gregtech/gregtech/worldgen/center'


def import_class(name):
    path = SOURCE / (name + '.java')
    original = path.read_text(encoding='utf-8')
    body = original[original.index('\t@Override\n\tpublic boolean generate('):]
    signature_end = body.index(' {')
    if name == 'WorldgenNexus':
        body = '''    public boolean generate(OriginWorld aWorld, OriginWorld.Chunk aChunk,
                            int aMinX, int aMinZ, java.util.Random aRandom)''' + body[signature_end:]
        body = body.replace('RNGSUS', 'aRandom')
        fields = '''    public final int mHeight;
    private final boolean GENERATE_STREETS;
    public SourceNexus(int height, boolean streets) { mHeight=height; GENERATE_STREETS=streets; }
'''
        target_name = 'SourceNexus'
    else:
        body = '''    public boolean generate(OriginWorld aWorld, int aMinX, int aMinZ,
                            int aMaxX, int aMaxZ, java.util.Set<String> aBiomeNames)''' + body[signature_end:]
        fields = '''    public final int mHeight;
    private final boolean GENERATE_BEACON, GENERATE_BIOMES, GENERATE_NEXUS, GENERATE_TESTING;
    public SourceStreets(int height, boolean beacon, boolean biomes, boolean nexus, boolean testing) {
        mHeight=height; GENERATE_BEACON=beacon; GENERATE_BIOMES=biomes;
        GENERATE_NEXUS=nexus; GENERATE_TESTING=testing;
    }
'''
        target_name = 'SourceStreets'
        # Beacon block placement and effects are one platform operation instead of 1.7.10 NBT APIs.
        body = body.replace('\t\t\t\t\tTileEntity tTileEntity;\n', '')
        pattern = r'WD\.set\(aWorld,\s*([^,]+),\s*([^,]+),\s*([^,]+), Blocks\.beacon, 0, 3\);\s*tTileEntity = WD\.te\(aWorld,[^;]+;\s*if \(tTileEntity instanceof TileEntityBeacon\) \{.*?setInteger\("Primary", Potion\.(\w+)\.id\);.*?setInteger\("Secondary", Potion\.(\w+)\.id\);.*?tTileEntity\.readFromNBT\(tNBT\);\s*\}'
        effects={'moveSpeed':'speed','digSpeed':'haste','damageBoost':'strength','resistance':'resistance','regeneration':'regeneration'}
        body, count = re.subn(pattern,lambda m:f'aWorld.beacon({m[1]}, {m[2]}, {m[3]}, "{effects[m[4]]}", "{effects[m[5]]}");',body,flags=re.S)
        assert count == 4, count
        body = body.replace('new HashSetNoNulls<>', 'new java.util.HashSet<>')
        body = body.replace('BIOMES_INFINITE_WATER.contains(tName)', 'aWorld.isInfiniteWaterBiome(tName)')
    body = re.sub(r'for \(EntityLivingBase tEntity : .*?tEntity\.setDead\(\);',
                  lambda m:'aWorld.clearNonPlayerEntities('+re.search(r'getBoundingBox\((.*?)\)',m[0]).group(1)+');', body)
    body = re.sub(r'\bWorld aWorld','OriginWorld aWorld',body).replace('BiomeGenBase tBiome', 'OriginWorld.Biome tBiome')
    body = body.replace('printStackTrace(ERR)', 'printStackTrace(System.err)')
    body = body.replace('tBiome.biomeName', 'tBiome.biomeName()')
    body = body.replace('aWorld.provider.worldChunkMgr.getBiomeGenAt', 'aWorld.getBiomeGenForCoords')
    body = body.replace('UT.Code.stringValidate', 'text').replace('UT.Code.inside', 'inside')
    body = body.replace('WD.sign(aWorld,', 'aWorld.sign(')
    for fn in ('set','block','opq','anywater','even'):
        body = body.replace('WD.'+fn+'(',fn+'(')
    body = body.replace('((BlockMetaType)BlocksGT.CFoam).mSlabs', 'BlocksGT.FOAM_SLABS')
    body = body.replace('(Block)BlocksGT.RailRoad', 'BlocksGT.RailRoad')
    body = body.replace('Block tBlock', 'OriginWorld.Block tBlock')
    body = body.replace('tBlock.getMaterial().isLiquid()', 'tBlock.liquid()')
    body = body.replace('tBlock.getMaterial() != Material.wood', '!tBlock.wood()')
    body = re.sub(r'tBlock\.isWood\([^)]*\)', 'tBlock.wood()', body)
    body = re.sub(r'tBlock\.isLeaves\([^)]*\)', 'tBlock.leaves()', body)
    # The literal source floor y=0 becomes the actual modern world bottom, preserving bedrock.
    body = re.sub(r'\b(int [jk] = )1(; [jk] < mHeight)', r'\1aWorld.minY()+1\2', body)
    body = re.sub(r'for \([^)]*\)',lambda m:re.sub(r'\b([jk]) > 0',r'\1 > aWorld.minY()',m[0]),body)
    # Bridge footing condition offsets have the same relative relation to the world floor.
    body = re.sub(r'k>\s*([+-]?\d+)',lambda m:'k>aWorld.minY()+('+m[1]+')',body)
    # These four out-of-chunk y=255 writes existed solely to force-load distant old chunks.
    body = re.sub(r'^\s*aWorld\.setBlock\([^\n]*, 255, [^\n]*\);\n','\n',body,flags=re.M)
    for forbidden in ('WD.','UT.','TileEntity','EntityLivingBase','BiomeGenBase','Material.','AxisAlignedBB','aWorld.provider'):
        assert forbidden not in body, (name, forbidden)
    header = original[:original.index('package ')]
    content = header + '''package com.gregtech.gregtech.worldgen.center;

import static com.gregtech.gregtech.worldgen.center.OriginSupport.*;

/** Original GT6 geometry, adapted by tools/import_origin_worldgen.py; platform effects use OriginWorld.
 * @author Gregorius Techneticies (original geometry)
 */
public final class ''' + target_name + ' {\n' + fields + body
    content = '\n'.join(line.rstrip() for line in content.splitlines())+'\n'
    (TARGET / (target_name + '.java')).write_text(content,encoding='utf-8')
    return {'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'target':str(TARGET/(target_name+'.java'))}


if __name__ == '__main__':
    TARGET.mkdir(parents=True,exist_ok=True)
    records=[import_class(name) for name in ('WorldgenNexus','WorldgenStreets')]
    cs_path = SOURCE.parents[2] / 'gregapi/data/CS.java'
    cs = cs_path.read_text(encoding='utf-8')
    line = next(line for line in cs.splitlines() if 'BIOMES_INFINITE_WATER = ' in line)
    names = re.findall(r'"([^"]+)"', line) + ['Ocean', 'Frozen Ocean', 'Deep Ocean', 'Beach', 'Cold Beach', 'Stone Beach', 'Mushroom Island Shore', 'River', 'Frozen River']
    names = sorted({re.sub(r'[^a-z0-9]', '', name.lower()) for name in names})
    literal = ',\n            '.join('"'+name+'"' for name in names)
    (TARGET/'OriginBiomeNames.java').write_text('''package com.gregtech.gregtech.worldgen.center;
/** Original CS.BIOMES_INFINITE_WATER names. Modern native biome tags are checked separately. */
public final class OriginBiomeNames {
    private OriginBiomeNames() {}
    private static final java.util.Set<String> WATER = java.util.Set.of(
            '''+literal+''');
    public static boolean water(String path) {
        return WATER.contains(path.toLowerCase(java.util.Locale.ROOT).replaceAll("[^a-z0-9]", ""));
    }
}
''', encoding='utf-8')
    records.append({'source':str(cs_path.relative_to(ROOT.parent)), 'source_sha256':hashlib.sha256(cs_path.read_bytes()).hexdigest(), 'scope':'CS.BIOMES_INFINITE_WATER exact normalized names'})
    receipt=ROOT/'docs/integration/verification/origin-worldgen-source-20261004.json'
    receipt.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Imported complete Nexus and streets source planners with original copyright headers.')
