# 共享材料物品定义与Neo注册

2026-09-30；在704fbb785d之后的隔离分支实施。core新增 `api.material.MaterialItemDefinitions`，从原saltnya Loader_Items提取107个显式候选前缀的顺序，保留每前缀sortedMaterials、隐藏/非canonical/不合法过滤、plate/WoodTreated例外，以及base ID→base_id后缀→碰撞失败策略。没有第二份材料目录或演示材料。

Forge `loaders/a/Loader_Items` 消费这份定义，实际构造与绑定仍在平台：coin仍用CoinItem，其他用MaterialItem。其后GTTechnological、GTMultiItems、GTFoodItems、GTFuelRods段与原import逐字节一致。定义移入core后显式core输入即可保持注册顺序，不能改成遍历无序map或所有PrefixRegistry条目。

Neo在材料presence绑定、完整init/role之后，向模组事件总线接 `registry.GTItems.ITEMS` 的DeferredRegister.Items。所有原定义均创建实际 `item.MaterialItem`，prefix/material绑定表只存共享对象与平台holder；getObject/getStack/getCreativeStack保持原包名及lookup语义。正式ID由共享prefix和canonical material名称生成，因此铜锡青铜锭及tiny煤灰沿原命名，不能使用Cu/Sn符号或DarkAsh别名再注册第二个ID。不存在stack NBT材料payload。

原注册提交只交付物品注册/身份/getStack；后续共享模型资源、Neo模型别名与颜色源码已接入，详见 `P2_MATERIAL_ITEM_VISUALS.md`，该视觉批次未编译、未测试或运行。语言资源与完整tooltip、coin放置/renderer等特殊行为仍pending。Neo普通coin材料物品不代表原CoinItem游戏行为已移植。原版统一/组成由主线单独接入，未改ItemMaterialRegistry/ItemComposition或相关loader；共同机器、工具、配方和存档验收继续推进。

来源blob/SHA及取舍见 `core/provenance/material-item-extraction.json`。原作者历史/适用许可仍未决，未更改原授权。已做一次源比对，确认107候选顺序及Forge后续注册段保持；此次没有新增合约、运行javac、Gradle、成品打包或游戏。主线阶段末统一构建/关键玩法/视觉验证通过后再补实际证据，不能用queued日志算运行完成。
