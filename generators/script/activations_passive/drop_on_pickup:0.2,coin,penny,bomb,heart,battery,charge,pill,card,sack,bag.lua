python[[gen.genstate.add_descriptors(["Sack", "Squeeze"])]]
on_pickup = function(self, player)
    local pos = player.Position
    local num = python[[gen.writeln("{}".format(random.randint(1, 3)))]]
    for i = 1, num do
        local pickup, subtype = python[[
pickup = choose_random_pickup()
subtype = choose_random_pickup_subtype(pickup)
pickup_name = get_pickup_name(pickup)
gen.writeln("{}, {}".format(pickup_name, subtype))
gen.genstate.add_descriptor(pickup.title())
        ]]
        local pos = Isaac.GetFreeNearPosition(pos, 1)
        Isaac.Spawn(EntityType.ENTITY_PICKUP, pickup, subtype, pos, Vector(0, 0), nil)
    end
end