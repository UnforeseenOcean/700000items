python[[gen.inc_var("value", 1)]]
python[[gen.chance(8, 1, 1)]]
do
    local id = python[[
gen.writeln("{}".format(choose_random_effect_rare()))
    ]]
    local entity = Isaac.Spawn(EntityType.ENTITY_EFFECT, id, 0, pos, Vector(0,0), nil)
    -- local effect = entity:ToEffect()
    -- effect:SetDamageSource(EntityType.ENTITY_PLAYER)
    -- effect.LifeSpan = 30
end