import com.gregtech.gregtech.api.material.GTMaterial;
import com.gregtech.gregtech.api.material.GTMaterialRegistry;
import com.gregtech.gregtech.api.mod.ModData;
import com.gregtech.gregtech.data.SourceBlockProperties;
import com.gregtech.gregtech.data.FluidCatalog;
import com.gregtech.gregtech.data.generated.GT6Materials;
import com.gregtech.gregtech.content.fluid.FluidDefinitions;
import com.gregtech.gregtech.content.machine.BasicMachineCatalog;
import java.util.Locale;

/** Development-only identity export. Run with the compiled shared core, never ship in the mod. */
class LanguageIdentities {
    public static void main(String[] args) throws ReflectiveOperationException {
        ModData.bindPresence(id -> id.equals("minecraft") || id.equals("gregtech"));
        GTMaterialRegistry.setLogSink((warning, message) -> {});
        GTMaterialRegistry.init();
        FluidDefinitions.prepare();
        SourceBlockProperties.blocks().forEach((path, p) -> row("block.gregtech." + path,
                "gt.multitileentity." + p.sourceId(), ""));
        for (var p : BasicMachineCatalog.specifications())
            SourceBlockProperties.basic(p.machineName(), p.tier()).ifPresent(s -> row(
                    "block.gregtech." + p.id(), "gt.multitileentity." + s.sourceId(), ""));
        for (var m : GTMaterialRegistry.allMaterials())
            row(m.getTranslationKey(), "gt.material." + m.getName(), m.getDisplayNameFallback());
        for (var holder : GT6Materials.class.getDeclaredClasses()) for (var field : holder.getFields()) {
            if (field.getType() != GTMaterial.class) continue;
            var material = (GTMaterial) field.get(null);
            row("material.gregtech." + field.getName().toLowerCase(Locale.ROOT),
                    "gt.material." + material.getName(), material.getDisplayNameFallback());
        }
        FluidCatalog.all().values().stream().distinct().forEach(f -> row(
                "fluid_type.gregtech." + FluidCatalog.sanitizePath(f.registryName()),
                "fluid." + f.registryName(), ""));
        com.gregtech.gregtech.api.prefix.PrefixRegistry.ensurePrefixesLoaded();
        for (var p : com.gregtech.gregtech.api.prefix.PrefixRegistry.all()) if (!p.isHiddenFromCreative())
            row("item.gregtech.tab_icon_" + p.getRegistryName(), "oredict.prefix." + p.getName(), p.getDisplayName());
        com.gregtech.gregtech.api.prefix.BlockPrefixRegistry.ensurePrefixesLoaded();
        for (var p : com.gregtech.gregtech.api.prefix.BlockPrefixRegistry.all()) if (!p.isPartialCrate())
            row("item.gregtech.tab_icon_block_" + p.getRegistryName(), "oredict.prefix." + p.getName(), p.getDisplayName());
    }
    private static void row(String key, String original, String fallback) {
        if ((key + original + fallback).matches("(?s).*[\\t\\r\\n].*"))
            throw new IllegalStateException("Identity export cannot contain TSV controls");
        System.out.println(key + "\t" + original + "\t" + fallback);
    }
}
