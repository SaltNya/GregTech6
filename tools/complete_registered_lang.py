"""Complete audited registered names with explicit Chinese family terminology; never copy English as Chinese."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
r=ROOT/'src/main/resources/assets/gregtech/lang'
e=json.loads((r/'en_us.json').read_text(encoding='utf-8'));z=json.loads((r/'zh_cn.json').read_text(encoding='utf-8'))
missing=json.loads((ROOT/'docs/localization-runtime-missing.json').read_text(encoding='utf-8'))
# Registry names with templates elsewhere are aliases, not independently translated content.
terms=dict(line.split('=',1) for line in """
advanced_button=高级按钮
advanced_crafting_table=高级工作台
bathing_pot=浸洗盆
bumbliary=大黄蜂巢
cap_nozzle=喷嘴盖
cfoam=建筑泡沫
charging_crafting_table=充电工作台
coin_mold=硬币模具
coin_pile=硬币堆
bedrock_drill=基岩钻机
coke_oven=焦炉
cryo_distillation=低温蒸馏塔
heat_exchanger=热交换器
fusion_reactor=聚变反应堆
implosion_compressor=聚爆压缩机
large_crucible=大型坩埚
large_gas_turbine=大型燃气轮机
lightning_rod=避雷针
logistics_core=物流核心
long_dist_endpoint_fluid=远距离流体端点
long_dist_endpoint_item=远距离物品端点
long_dist_pipe=远距离管道
loot_crate=战利品箱
diggable_clay=黏土沉积层
diggable_peat=泥炭沉积层
extender_advanced=高级扩展器
extender_basic=基础扩展器
extender_elite=精英扩展器
extender_wireless=无线扩展器
filter_fluids=流体过滤器
filter_items=物品过滤器
filter_items_fluids=物品与流体过滤器
fluid_barometer_gas_cylinder=带压力表气瓶
fluid_cup=杯子
fluid_funnel=漏斗
fluid_jug=壶
fluid_measuring_pot=量杯
fluid_thermos=保温瓶
glass_glow=发光玻璃
greg_lantern=格雷灯笼
ingot_pile=锭堆
juicer=榨汁器
laser_fiber_wire=激光光纤
panel_asphalt=沥青面板
panel_cfoam=建筑泡沫面板
panel_colored_black=黑色面板
panel_colored_gray=灰色面板
panel_concrete=混凝土面板
panel_wood=木面板
plant_pot=花盆
plate_gem_pile=宝石板堆
plate_pile=板堆
railroad=铁轨
reactor_casing=反应堆外壳
reactor_core_2x2=2×2反应堆核心
sandwich_block=三明治
sap_bag=树液收集袋
scaffold=脚手架
spike_fancy=花式尖刺
spike_metal=金属尖刺
spike_sharp=锋利尖刺
spike_steel=钢尖刺
spike_super=超级尖刺
tank_3x3=3×3储罐主控
tank_5x5=5×5储罐主控
tank_wall=储罐壁
tank_wall_dense=致密储罐壁
sensor_bucketometer=流量计
sensor_chronometer=计时器
sensor_geiger=盖革计数器
sensor_gibblometer=压力计
sensor_kilobucketometer=千桶流量计
sensor_laserometer=激光功率计
sensor_luminometer=照度计
sensor_playercounter=玩家计数器
sensor_stackometer=物品堆计数器
sensor_tachometer=转速计
sensor_thermometer=温度计
sensor_weightometric=称重计
cover_conveyor=传送带覆盖板
cover_pump=泵覆盖板
cover_redstone_repeater=红石中继器覆盖板
cover_redstone_torch=红石火把覆盖板
cover_robot_arm=机械臂覆盖板
cover_tag_selector=标签选择器覆盖板
electric_chainsaw=电动链锯
electric_drill=电钻
electric_screwdriver=电动螺丝刀
electric_wrench=电动扳手
fuel_rod_am_243=镅-243燃料棒
fuel_rod_mox=混合氧化物燃料棒
fuel_rod_naquadah=硅岩燃料棒
blackstone=黑石
electron=电子
hexorium=六方晶
neutrino=中微子
neutron=中子
photon=光子
porcelain=瓷
proton=质子
quartz=石英
heliumplasma=氦等离子体
nitrogenplasma=氮等离子体
liquid_medium_oil=中质原油
mcguffium=麦高芬
nitrofuel=硝基燃料
uuamplifier=UU增幅剂
""".strip().splitlines())
materials={'stainless':'不锈钢','tungstensteel':'钨钢','wood':'木','galvanized':'镀锌钢','alnico':'铝镍钴','ferrite':'铁氧体','blue_mahoe':'蓝马槿','white_mahoe':'白马槿','ebony':'乌木','pine':'松木','maple':'枫木','rainbowood':'彩虹木','rubber':'橡胶木','willow':'柳木'}
for k,v in z.items():
 if k.startswith('material.gregtech.'):
  name=k.split('.',2)[2];materials.setdefault(name,v)
def material(s):return materials.get(s) or materials.get(s.replace('_',''))
colors=dict(zip('black blue brown cyan gray green lightblue lightgray lime magenta orange pink purple red white yellow'.split(),'黑 蓝 棕 青 灰 绿 淡蓝 淡灰 黄绿 品红 橙 粉红 紫 红 白 黄'.split()))
families={'auto_hammer':'自动锤','auto_igniter':'自动点火器','axle':'传动轴','bars':'栏杆','gearbox':'齿轮箱','rotation_transformer':'旋转变速器','rotational_pump':'旋转泵','engine_diesel':'柴油引擎','magnet':'磁铁','magnet_electromagnetic':'电磁铁','beam':'横梁','log':'原木','leaves':'树叶','planks':'木板','sapling':'树苗'}
levels={'battery':'电池','co2_laser':'二氧化碳激光器','electric_cooler':'电制冷器','electric_heater':'电加热器','flux_laser':'通量激光器','laser_absorber':'激光吸收器'}
anyterms={'aventurine':'东陵石','garnet':'石榴石','ashes':'灰烬','coal/carbon':'煤或碳','defaultwood':'普通木材','flour':'面粉','flourorgrains':'面粉或谷物','grains':'谷物','hardplastic':'硬塑料','ironorsteel':'铁或钢','ironsteel':'铁或钢','magicalwood':'魔法木材','magiciron':'魔法铁','metal':'金属','normalwood':'普通木材','silicondioxide':'二氧化硅','thaumiccrystal':'神秘水晶','treatedwood':'防腐木','untreatedwood':'未处理木材','woodorplastic':'木材或塑料'}
def translated(k):
 name=k.split('.',2)[2]
 for prefix in ['item.gregtech.','block.gregtech.','fluid.gregtech.','fluid_type.gregtech.']:
  other=prefix+name
  if other!=k and other in z:return z[other]
 if name in terms:return terms[name]
 if name.startswith('any'):
  tail=name[3:];base=anyterms.get(tail) or material(tail)
  if base:return '任意'+base
 if name.startswith('cfoam.'):
  return ('私人' if '.owned.' in name else '')+colors[name.split('.')[-1]]+'色建筑泡沫'
 if name.startswith('dye'):
  tail=name.removeprefix('dye').strip('.')
  bits=tail.split('.');c=colors.get(bits[-1]);family={'chemical':'化学','flower':'植物','watermixed':'水混合'}.get(bits[0],'')
  if c:return family+c+'色染料'
 if name.startswith('tab_icon_'):
  tail=name[len('tab_icon_'):]
  keys=['item.gregtech.'+tail,'block.gregtech.'+tail.removeprefix('block_'),'itemGroup.gregtech.'+tail]
  for key in keys:
   if key in z:return z[key].replace('%s','').strip()+'（分类图标）'
  if tail in ['tools','stones']:return {'tools':'工具','stones':'石材'}[tail]+'（分类图标）'
 if name.startswith('burning_box_'):
  kind,rest=name[len('burning_box_'):].split('_',1);dense=rest.startswith('dense_');rest=rest.removeprefix('dense_');m=material(rest)
  if m:return ('致密' if dense else '')+m+{'fluidbed':'流化床','gas':'气体','liquid':'液体'}[kind]+'燃烧室'
 for ending,word in [('_main','主控'),('_wall','结构壁')]:
  if name.endswith(ending) and name[:-len(ending)] in terms:return terms[name[:-len(ending)]]+word
 for family,word in sorted(families.items(),key=lambda x:-len(x[0])):
  if name.startswith(family+'_'):
   rest=name[len(family)+1:];suffix=''
   if family=='axle' and rest[-1:].isdigit():rest,n=rest.rsplit('_',1);suffix='（'+n+'级）'
   m=material(rest)
   if m:return m+word+suffix
 for family,word in levels.items():
  if name.startswith(family+'_'):return word+'（'+name[len(family)+1:].upper()+'）'
 return None
remaining=[]
for entry in missing:
 language,key=entry.split(':',1);target=e if language=='en_us' else z
 if key in target:continue
 if language=='en_us':
  name=key.split('.',2)[2];target[key]=re.sub(r'([a-z])([A-Z])',r'\1 \2',name).replace('_',' ').replace('.',' ').title()
 else:
  value=translated(key)
  if value:target[key]=value
  else:remaining.append(key)
for n,d in [('en_us',e),('zh_cn',z)]: (r/(n+'.json')).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print('Unresolved Chinese:',len(remaining));print('\n'.join(remaining))

from sync_standard_chinese import sync
sync()
