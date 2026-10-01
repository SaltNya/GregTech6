"""Java identifier migration shared by the import tools and framework migration.

Only Java identifiers are changed; registry strings and GT6 source comments stay
verbatim. Short names are accepted only as upstream importer input; emitted Java uses full names.
"""
from modular_materials import replace_identifiers

DATA_NAMES = {
    'MT': 'ImportedMaterialData',
    'CS': 'GregTechConstants', 'FL': 'RegisteredFluids', 'FM': 'FuelRecipeMaps',
    'RM': 'MachineRecipeMaps', 'OP': 'MaterialPrefixes', 'TD': 'GregTechTags',
    'MD': 'ModReferences', 'OD': 'OreDictionaryNames', 'IL': 'ItemReferences',
    'LH': 'TranslationKeys', 'BI': 'BlockIcons', 'TC': 'AspectReferences',
    'AM': 'AntimatterMaterials', 'ANY': 'MaterialGroups',
}

def readable_java(text):
    return replace_identifiers(text, DATA_NAMES)
