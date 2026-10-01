# 双版本初期对齐：Native common tags 输入

现有 MaterialTagPack 已把 GregTech 自有条目写入 forge 与 c 两命名空间，MaterialEquivalence 的机器输入比较也已接受 c；但按 Source 保留的普通有序/无序 Ingredient JSON 仍引用 forge 标签。此前仅复制自有值到 c，外部模组追加到 c 的材料不会因此进入 forge 配方标签。这是 Native 标签边界差异，不是另建材料体系。

依据本机固定 NeoForge21.1.243 源码 Tags.java（c namespace，INGOTS_IRON=ingots/iron），现仅在 forge item/block 标签 JSON 序列化时加入同路径的可选 #c 引用。已有 aluminium/aluminum、quartz/nether_quartz、sulfur/sulphur、tungsten_steel/tungstensteel 别名双向匹配到 c，保留原自有值、replace=false 与配方身份。c 值在此之前已独立复制，序列化不会修改原 sets，生成的 c 标签不会引用 forge，也不会生成自引用闭环。不存在可选 c 标签时不要求它必须存在；其他模组或数据包自己声明的逆向循环不在本批证明范围。

只改1 Native Java。Core/Forge/资源文件和三个来源不改，一次集中compile 17s通过；没有新夹具、重复游戏或全资源打包。此前启动不覆盖这次 tag JSON 变化，外部物品真正合成、标签解析/reload及与第三方组合仍未实测；同路径/既有拼写兼容不代表所有模组或流体 schema 兼容。

整理旧账本：最近harvest-policy专服日志已观察多方块制作84 emitted/0 unresolved（早期记录38/46及77/7是历史状态），对应持久回执补实际计数。这只是生成/加载证据，不能推定结构、物料和完整生存链通过。启动中唯一 fusion_reactor_wall→machine casing 的替代仍保留：当前Forge与Native没有该独立注册定义，Source recipe表和fallback也有这个引用，未任意造一块Iridium墙来消除警告。

Git上传源码包仍固定8b47b7dc90；本批为其后续修改。旧d86cdfbcad模组包不含本批/实体id/采掘策略更改，最新源码构建方法仍见BUILDING.md。完整玩法、成品jar运行、独立存档重载和旧档继续未验证，完整三源目标active。
