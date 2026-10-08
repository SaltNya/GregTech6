"""Verify the original creative-tab naming path before reading its arguments."""
import re

from generate_machine_material_data import masked
from source_language_common import STRING


def creative_name_sources(original):
    snippets = {
        'gregapi/item/CreativeTab.java': (
            'LH.add("itemGroup."+aName,aLocal);',),
        'gregapi/block/multitileentity/MultiTileEntityRegistry.java': (
            'new CreativeTab(mNameInternal+"."+aClassContainer.mCreativeTabID,aCategoricalName,Item.getItemFromBlock(mBlock),aClassContainer.mCreativeTabID)',),
        'gregapi/item/prefixitem/PrefixItem.java': (
            'new CreativeTab(mPrefix.mNameInternal,mPrefix.mNameCategory,this,W)',),
        'gregapi/oredict/OreDictPrefix.java': (
            'mNameCategory=aCategoryName;',),
    }
    files = [original / 'src/main/java' / path for path in snippets]
    if not any(path.exists() for path in files):
        return []  # Minimal fixtures without a creative-tab subsystem.
    for path, required in zip(files, snippets.values()):
        if not path.exists():
            raise ValueError('Missing original creative naming source: ' + str(path))
        raw = ''.join(re.findall(STRING + r'|\S', masked(path.read_text(encoding='utf-8'))))
        if any(''.join(re.findall(STRING + r'|\S', snippet)) not in raw for snippet in required):
            raise ValueError('Unsupported original creative naming formula: ' + str(path))
    return files
