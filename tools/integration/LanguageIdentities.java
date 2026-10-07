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
        for (var field : com.gregtech.gregtech.data.ImportedMaterialData.class.getFields()) {
            if (field.getType() != GTMaterial.class) continue;
            var material = (GTMaterial) field.get(null);
            row("@symbol.MT." + field.getName(), material.getName(), "");
        }
        row("@symbol.MT.Wood", GT6Materials.Woods.Wood.getName(), "");
        row("@symbol.MT.WoodTreated", GT6Materials.Woods.WoodTreated.getName(), "");
        for (var pipe : com.gregtech.gregtech.content.transport.fluid.FluidTransportDefinitions.pipes())
            row("block.gregtech." + pipe.id(), "@pipe.fluid." + pipe.material().getName()
                    + "." + pipe.size().name(), "");
        for (var mat : com.gregtech.gregtech.content.transport.ItemPipeCatalog.ITEM_PIPE_MATS)
            for (var size : com.gregtech.gregtech.api.machine.ItemPipeSpec.ItemPipeSize.values())
                row("block.gregtech.item_pipe_" + size.name().toLowerCase(Locale.ROOT) + "_" + mat.idSuffix(),
                        "@pipe.item." + mat.material().getName() + "." + size.name(), "");
        for (var p : com.gregtech.gregtech.content.tool.AutomaticToolRules.ALL)
            row("block.gregtech." + p.id(), "gt.multitileentity."
                    + ((p.igniter() ? 15010 : 15000) + p.quality()), "");
        for (var p : com.gregtech.gregtech.content.logistics.ExtenderSpec.values())
            row("block.gregtech." + p.id, "gt.multitileentity." + p.originalId, "");
        for (var p : com.gregtech.gregtech.content.transport.fluid.CheapWoodBarrelCatalog.ENTRIES)
            row("block.gregtech." + p.id(), "gt.multitileentity." + p.sourceId(), "");
        for (var p : com.gregtech.gregtech.api.fluid.PortableFluidContainerSpec.values())
            if (p.shapeId().equals("cell")) row("block.gregtech.fluid_" + p.id(),
                    "@cell." + p.material().getName(), "");
        for (var p : com.gregtech.gregtech.content.transport.TrackCatalog.MATERIALS)
            for (String variant : new String[]{"", "booster", "detector"})
                row("block.gregtech.track_" + (variant.isEmpty() ? "" : variant + "_") + p.slug(),
                        "gt.block.rail." + (variant.isEmpty() ? "" : variant + ".") + p.slug(), "");
        var colors = com.gregtech.gregtech.worldgen.SurfaceFloraRules.GLOWTUS_COLOURS;
        for (int i = 0; i < colors.size(); i++)
            row("block.gregtech.glowtus_" + colors.get(i), "gt.block.lilypad.glowtus." + i, "");
        for (var p : com.gregtech.gregtech.content.logistics.LongDistanceCatalog.ALL) {
            if (p.sourceLine()) row("block.gregtech." + p.id(),
                    (p.kind().equals("WIRE") ? "gt.block.longdistwire.01." : "gt.block.longdistpipe.01.")
                            + p.sourceMeta(), "");
            else if (p.kind().equals("TRANSFORMER")) {
                int tier = 4;
                for (long voltage = 2048; voltage < p.voltage(); voltage *= 4) tier++;
                row("block.gregtech." + p.id(), "gt.multitileentity." + (10060 + tier), "");
            }
        }
        row("block.gregtech.fluid_jug", "gt.multitileentity.32740", "");
        row("block.gregtech.fluid_cup", "gt.multitileentity.32739", "");
        row("block.gregtech.fluid_measuring_pot", "gt.multitileentity.32738", "");
        row("block.gregtech.fluid_measuring_pot_stainless_steel", "gt.multitileentity.32743", "");
        row("block.gregtech.fluid_thermos", "gt.multitileentity.32737", "");
        row("block.gregtech.fluid_barometer_gas_cylinder", "gt.multitileentity.32055", "");
        row("block.gregtech.fluid_barometer_gas_cylinder_stainless_steel", "gt.multitileentity.32056", "");
        // Loader_MultiTileEntities' literal wood-barrel and metal-drum registrations.
        for (String binding : new String[]{"wood_barrel_treated|32714", "wood_barrel_skyroot|32019",
                "wood_barrel_livingwood|32010", "wood_barrel_dreamwood|32009", "wood_barrel_shimmerwood|32016",
                "wood_barrel_ironwood|32734", "wood_barrel_greatwood|32017", "wood_barrel_silverwood|32018",
                "drum_invar|32064", "drum_desh|32070", "drum_syrmorite|32020", "drum_efrine|32093",
                "drum_thaumium|32022", "drum_manasteel|32023", "drum_tungsten_alloy|32090", "drum_netherite|32087",
                "drum_void_metal|32063", "drum_tantalum_hafnium_carbide|32083", "drum_gaia_spirit|32024",
                "drum_adamantium|32719", "drum_draconium|32021", "drum_awakened_draconium|32066", "drum_infinity|32067"}) {
            String[] parts = binding.split("\\|");
            row("block.gregtech." + parts[0], "gt.multitileentity." + parts[1], "");
        }
        row("block.gregtech.asphalt", "gt.block.asphalt.0", "");
        row("block.gregtech.railroad", "gt.block.rail.road", "");
        for (var tool : com.gregtech.gregtech.api.tool.ToolDefinition.values()) {
            row("item.gregtech.tool." + tool.id(), "gt.metatool.01." + tool.gt6Id(), "");
            row(tool.translationKey(), "gt.metatool.01." + tool.gt6Id(), "");
        }
        for (var tool : com.gregtech.gregtech.content.tool.ElectricToolCatalog.ALL)
            row("item.gregtech." + tool.id(), "@tool." + tool.original(), "");
        String[] components = {"electric_motor", "electric_pump", "electric_conveyor", "electric_piston",
                "robot_arm", "force_field_emitter", "signal_emitter", "sensor"};
        String[] tiers = {"ulv", "lv", "mv", "hv", "ev", "iv", "luv", "zpm", "uv", "puv1"};
        // MultiItemTechnological's 0..9 loop. The port-only XV rows have no source number.
        for (int c = 0; c < components.length; c++) for (int tier = 0; tier < tiers.length; tier++)
            row("item.gregtech.compact_" + components[c] + "_" + tiers[tier],
                    "gt.multiitem.technological." + (12000 + c * 20 + tier), "");
        for (var battery : com.gregtech.gregtech.content.energy.ChemicalBatterySpec.all()) {
            int sourceId = 14000 + battery.chemistry().ordinal() * 10 + battery.tier();
            row("block.gregtech." + battery.id(), "gt.multitileentity." + sourceId, "");
            if (battery.chemistry() == com.gregtech.gregtech.content.energy.ChemicalBatterySpec.Chemistry.LITHIUM_COBALT)
                row("block.gregtech.battery_eu_" + battery.voltage(), "gt.multitileentity." + sourceId, "");
        }
        // Original A/B metadata order differs from WoodSpecies enum order.
        String[] treeSpecies = {"rubber", "maple", "willow", "blue_mahoe", "hazel", "cinnamon", "coconut", "rainbowood"};
        for (int i = 0; i < treeSpecies.length; i++) {
            for (String kind : new String[]{"sapling", "leaves", "planks"})
                row("block.gregtech." + kind + "_" + treeSpecies[i], "gt.block." + kind + "." + i, "");
            for (String kind : new String[]{"log", "beam"})
                row("block.gregtech." + kind + "_" + treeSpecies[i], "gt.block." + kind + "." + (i < 4 ? "a" : "b") + "." + (i % 4), "");
        }
        for (String kind : new String[]{"sapling", "leaves", "planks", "log", "beam"}) {
            String suffix = switch(kind) { case "sapling", "leaves" -> ".cd"; case "planks" -> "2"; default -> ".c"; };
            row("block.gregtech." + kind + "_bluespruce", "gt.block." + kind + suffix + ".0", "");
            row("block.gregtech." + kind + "_bluemahoe", "gt.block." + kind + (kind.equals("log") || kind.equals("beam") ? ".a.3" : ".3"), "");
        }
        String[] fallen = {"dry", "rotten", "mossy", "frozen"};
        for (int i = 0; i < fallen.length; i++) {
            row("block.gregtech.log_" + fallen[i], "gt.block.log.1." + i, "");
            row("block.gregtech.planks_" + fallen[i], "gt.block.planks." + (12 + i), "");
        }
        row("block.gregtech.planks_compressed", "gt.block.planks.8", "");
        row("block.gregtech.planks_wood", "gt.block.planks.9", "");
        row("block.gregtech.planks_treated", "gt.block.planks.10", "");
        row("block.gregtech.slab_bluespruce", "gt.block.planks2.slab.0.0", "");
        for (var flower : com.gregtech.gregtech.content.plant.BedrockFlowers.ALL)
            row("block.gregtech." + flower.id(), "gt.block.flower."
                    + Character.toLowerCase(flower.family()) + "." + flower.meta(), "");
        String[][] beams = {{"oak", "spruce", "birch", "jungle"},
                {"acacia", "darkoak", "rubberwood", "wood"},
                {"greatwood", "silverwood", "skyroot", "darkwood"}};
        for (int group = 0; group < beams.length; group++) for (int meta = 0; meta < 4; meta++)
            row("block.gregtech.beam_" + beams[group][meta], "gt.block.beam." + (group + 1) + "." + meta, "");
        row("block.gregtech.fluid_measuring_pot_tungsten", "gt.multitileentity.32744", "");
        row("block.gregtech.fluid_measuring_pot_tantalum_hafnium_carbide", "gt.multitileentity.32077", "");
        row("block.gregtech.fluid_barometer_gas_cylinder_tungsten", "gt.multitileentity.32057", "");
        row("block.gregtech.fluid_barometer_gas_cylinder_tantalum_hafnium_carbide", "gt.multitileentity.32078", "");
        row("block.gregtech.fluid_funnel", "gt.multitileentity.32723", "");
        row("block.gregtech.fluid_funnel_stainless_steel", "gt.multitileentity.32725", "");
        row("block.gregtech.loot_crate", "gt.multitileentity.32110", "");
        row("block.gregtech.bumble_hive", "gt.multitileentity.32755", "");
        for (var color : colors)
            row("block.gregtech.bumble_hive_" + color, "gt.multitileentity.32755", "");
        for (var spring : com.gregtech.gregtech.worldgen.FluidSpringRules.SPRINGS)
            row("block.gregtech." + com.gregtech.gregtech.worldgen.FluidSpringRules.blockPath(spring),
                    "gt.multitileentity.32763", "");
        row("block.gregtech.bottle_crate", "gt.multitileentity.8762", "");
        // Every original plank index uses the same generic name. Modern woods
        // reuse this family name; 8700 is not a fabricated per-wood source ID.
        for (var wood : com.gregtech.gregtech.content.storage.BottleCrateVariants.WOODS)
            row("block.gregtech." + wood.id(), "gt.multitileentity.8700", "");
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
