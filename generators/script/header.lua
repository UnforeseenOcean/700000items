Mod = RegisterMod("700000Items", 1)

VALID_DAMAGE_SOURCES = {
	[EntityType.ENTITY_TEAR] = true,
	[EntityType.ENTITY_LASER] = true,
	[EntityType.ENTITY_KNIFE] = true,
}

-- Tear flag list credit to /u/Snailic
-- Sweet list dude
TearFlag = {
	FLAG_NO_EFFECT = 0,
	FLAG_SPECTRAL = 1,
	FLAG_PIERCING = 1<<1,
	FLAG_HOMING = 1<<2,
	FLAG_SLOWING = 1<<3,
	FLAG_POISONING = 1<<4,
	FLAG_FREEZING = 1<<5,
	FLAG_COAL = 1<<6,
	FLAG_PARASITE = 1<<7,
	FLAG_MAGIC_MIRROR = 1<<8,
	FLAG_POLYPHEMUS = 1<<9,
	FLAG_WIGGLE_WORM = 1<<10,
	FLAG_UNK1 = 1<<11, --No noticeable effect
	FLAG_IPECAC = 1<<12,
	FLAG_CHARMING = 1<<13,
	FLAG_CONFUSING = 1<<14,
	FLAG_ENEMIES_DROP_HEARTS = 1<<15,
	FLAG_TINY_PLANET = 1<<16,
	FLAG_ANTI_GRAVITY = 1<<17,
	FLAG_CRICKETS_BODY = 1<<18,
	FLAG_RUBBER_CEMENT = 1<<19,
	FLAG_FEAR = 1<<20,
	FLAG_PROPTOSIS = 1<<21,
	FLAG_FIRE = 1<<22,
	FLAG_STRANGE_ATTRACTOR = 1<<23,
	FLAG_UNK2 = 1<<24, --Possible worm?
	FLAG_PULSE_WORM = 1<<25,
	FLAG_RING_WORM = 1<<26,
	FLAG_FLAT_WORM = 1<<27,
	FLAG_UNK3 = 1<<28, --Possible worm?
	FLAG_UNK4 = 1<<29, --Possible worm?
	FLAG_UNK5 = 1<<30, --Possible worm?
	FLAG_HOOK_WORM = 1<<31,
	FLAG_GODHEAD = 1<<32,
	FLAG_UNK6 = 1<<33, --No noticeable effect
	FLAG_UNK7 = 1<<34, --No noticeable effect
	FLAG_EXPLOSIVO = 1<<35,
	FLAG_CONTINUUM = 1<<36,
	FLAG_HOLY_LIGHT = 1<<37,
	FLAG_KEEPER_HEAD = 1<<38,
	FLAG_ENEMIES_DROP_BLACK_HEARTS = 1<<39,
	FLAG_ENEMIES_DROP_BLACK_HEARTS2 = 1<<40,
	FLAG_GODS_FLESH = 1<<41,
	FLAG_UNK8 = 1<<42, --No noticeable effect
	FLAG_TOXIC_LIQUID = 1<<43,
	FLAG_OUROBOROS_WORM = 1<<44,
	FLAG_GLAUCOMA = 1<<45,
	FLAG_BOOGERS = 1<<46,
	FLAG_PARASITOID = 1<<47,
	FLAG_UNK9 = 1<<48, --No noticeable effect
	FLAG_SPLIT = 1<<49,
	FLAG_DEADSHOT = 1<<50,
	FLAG_MIDAS = 1<<51,
	FLAG_EUTHANASIA = 1<<52,
	FLAG_JACOBS_LADDER = 1<<53,
	FLAG_LITTLE_HORN = 1<<54,
	FLAG_GHOST_PEPPER = 1<<55
}

--[[
Per-Item data, such as: stats, item variants, functionality, etc.
--]]
Mod.items = {} -- Item Data (indexable by name and id)
Mod.item_names = {} -- List of item names
Mod.item_ids = {} -- List of item ids (unordered)
Mod.cards = {} -- list of cards
Mod.pills = {} -- list of pills
Mod.trinkets = {} -- list of trinkets
Mod.familiars = {} -- list of familiars.
-- Keys are integers referring to Variant, and values are item def

function Mod:get_player_id(player)
	local game = Game()
	if type(player) == "number" then return player, Isaac.GetPlayer(player-1) end
	for i = 1, game:GetNumPlayers() do
		local p = game:GetPlayer(i-1)
		if p.Index == player.Index then
			return i, player
		end
	end
	error("No player with ID!")
end

-- call a callback for a specific player
function Mod:call_callbacks(player_id, func, ...)
	player_id, player = Mod:get_player_id(player_id)
	local item_ids = _get_player_items(player_id).list
	for item_id in pairs(item_ids) do
		local item_def = Mod.items[item_id]
		local item_func = item_def[func]
		if item_func then
			item_func(item_def, player, ...)
		end
	end
	for i = 1, player:GetMaxTrinkets() do
		local trinket_id = player:GetTrinket(i-1)
		local trinket_def = Mod.trinkets[trinket_id]
		if trinket_def then
			local trinket_func = trinket_def[func]
			if trinket_func then
				trinket_func(trinket_def, player, ...)
			end
		end
	end
end

function Mod:call_callbacks_all(func, ...)
	local game = Game()
	for i = 1, game:GetNumPlayers() do
		Mod:call_callbacks(i, func, ...)
	end
end

--[[
Global data, such as: damage taken, damage dealt, coins collected
--]]
Mod.args = {}
Mod.args.damage_taken = 0
Mod.args.damage_dealt = 0
Mod.args.room_changed = false
Mod.stats_permanant = {
	MaxFireDelay = 0,
	Damage = 0,
	MoveSpeed = 0,
	ShotSpeed = 0,
	Luck = 0,
	TearHeight = 0,
}

--[[
Utility functions
--]]

function _table_to_string(t)
	t_type = type(t)
	if t_type ~= "table" then
		if t_type == "string" then
			return ("%q"):format(t)
		end
		return tostring(t)
	end
	local ret = "{"
	for k,v in pairs(t) do
		ret = ret .. ("[%s] = %s,"):format(
			_table_to_string(k), _table_to_string(v))
	end
	ret = ret .. "}"
	return ret
end

function table_to_string(t)
	return _table_to_string(t)
end

function direction_to_vector(dir)
	if dir == Direction.LEFT then return Vector(-1, 0)
	elseif dir == Direction.RIGHT then return Vector(1, 0)
	elseif dir == Direction.UP then return Vector(0, -1)
	elseif dir == Direction.DOWN then return Vector(0, 1)
	else return Vector(0, 0) end
end

function save_output()
	t = {
		stats = Mod.stats_permanant,
	}
	out = table_to_string(t)
	Mod:SaveData(out)
end

function load_data()
	data = Mod:LoadData()
	t = load("return " .. data)()
	if t then
		if t.stats then
			Mod.stats_permanant = t.stats
		end
	end
end

function mod_reset()
	Mod:call_callbacks_all("reset")
	Mod.stats_permanant.MaxFireDelay = 0
	Mod.stats_permanant.Damage = 0
	Mod.stats_permanant.MoveSpeed = 0
	Mod.stats_permanant.ShotSpeed = 0
	Mod.stats_permanant.Luck = 0
	Mod.stats_permanant.TearHeight = 0
	save_output()
end

function random_choice(t)
	return t[math.random(#t)]
end

function get_size(entity)
	local as_npc = entity:ToNPC()
	local as_effect = entity:ToEffect()
	local as_knife = entity:ToKnife()
	local as_tear = entity:ToTear()
	local whatever = as_npc or as_effect or as_knife or as_tear
	local scale = whatever and whatever.Scale or 1
	return entity.SizeMulti * scale
end

function get_entity_distance_2(a, b)
	local a_size = get_size(a)
	local b_size = get_size(b)
	local a_pos = a.Position
	local b_pos = b.Position
	local x_diff = a_pos.X - b_pos.X
	local y_diff = a_pos.Y - b_pos.Y
	local sub_x = math.abs(a_size.X) + math.abs(b_size.X)
	local sub_y = math.abs(a_size.Y) + math.abs(b_size.Y)
	local x_diff_2 = math.max(0, x_diff^2 - sub_x^2)
	local y_diff_2 = math.max(0, y_diff^2 - sub_y^2)
	return x_diff_2 + y_diff_2
end

function get_entity_distance(a, b)
	return math.sqrt(get_entity_distance_2(a, b))
end

function are_entities_near(a, b, dis)
	return get_entity_distance_2(a, b) <= dis^2
end

function add_function_to_def(item_name, func_name, func)
	local item_def = Mod.items[item_name]
	if item_def[func_name] then
		local p_func = item_def[func_name]
		item_def[func_name] = function(...)
			p_func(...)
			func(...)
		end
	else
		item_def[func_name] = func
	end
end

function inf_norm(x, n)
	n = n or 1
	return x / (math.abs(x) + n)
end

function inf_norm_positive(x, n)
	return (inf_norm(x, n) + 1) / 2
end

_player_items = {}
function _get_player_items(id)
	if not _player_items[id] then
		_player_items[id] = {
			potential = {},
			list = {}
		}
	end
	return _player_items[id]
end

function _signal_refresh_cache(id)
	local player = type(id) == "number" and Isaac.GetPlayer(id) or id
	player:AddCacheFlags(CacheFlag.CACHE_ALL)
	player:EvaluateItems()
end

-- Completely refreshing the cache is a slow operation that may take a second
-- Use conservatively!
function _refresh_item_cache()
	local game = Game()
	for i = 1, game:GetNumPlayers() do
		local player_items = _get_player_items(i);
		local player = game:GetPlayer(i-1);
		-- player_items.list = {}
		player_items.potential = {}
		for _, item_id in pairs(Mod.item_ids) do
			if player:HasCollectible(item_id) and not player_items.list[item_id] then
				player_items.list[item_id] = true
				local item_def = Mod.items[item_id]
				if item_def.on_add then
					item_def:on_add(player)
				end
			end
		end
		_signal_refresh_cache(i-1)
	end
	Isaac.DebugString("Refreshed Item Cache")
end

--[[
Callback functions
--]]
Mod.callbacks = {}
Mod._cache_firedelay_need_update = false
function Mod.callbacks:evaluate_cache(player, flag)
	minimum_tears = math.min(player.MaxFireDelay, 5)
	Mod:call_callbacks(player, "evaluate_cache", flag)
	-- Special call is for effects with temporary stat upgrades.
	Mod:call_callbacks(player, "evaluate_cache_special", flag)

	-- calculate permanant stat upgrades
	if flag == CacheFlag.CACHE_DAMAGE then
		player.Damage = player.Damage + Mod.stats_permanant.Damage
	end
	if flag == CacheFlag.CACHE_SPEED then
		player.MoveSpeed = player.MoveSpeed + Mod.stats_permanant.MoveSpeed
	end
	if flag == CacheFlag.CACHE_LUCK then
		player.Luck = player.Luck + Mod.stats_permanant.Luck
	end
	if flag == CacheFlag.CACHE_RANGE then
		player.TearHeight = player.TearHeight + Mod.stats_permanant.TearHeight
	end
	if flag == CacheFlag.CACHE_SHOTSPEED then
		player.ShotSpeed = player.ShotSpeed + Mod.stats_permanant.ShotSpeed
	end
	if flag == CacheFlag.CACHE_FIREDELAY then
		player.MaxFireDelay = player.MaxFireDelay + Mod.stats_permanant.MaxFireDelay
	end

	player.MaxFireDelay = math.max(minimum_tears, player.MaxFireDelay)
end

local _room_id = -1
local _enemies = {}
local _killers = {}
local _timer = 0
local _timerf = 0
function Mod.callbacks:update()
	local game = Game()
	_timer = game:GetFrameCount()
	_timerf = _timer / 30

	if _timer == 1 then
		mod_reset()
	end

	Mod.args.room_changed = false
	-- refresh for room change
	local level = game:GetLevel()
	local room_id = level:GetCurrentRoomIndex()
	if _room_id ~= room_id then
		_room_id = room_id
		_refresh_item_cache()
		Mod.args.damage_taken = 0
		Mod.args.damage_dealt = 0
		Mod.args.room_changed = true
		Mod:call_callbacks_all("room_change")
		_enemies = {}
	end

	-- remove items that the player does not have
	for i = 1, game:GetNumPlayers() do
		local list = _get_player_items(i).list;
		local player = game:GetPlayer(i-1);
		local item_i = 1
		for item_id in pairs(list) do
			if not player:HasCollectible(item_id) then
				local item_def = Mod.items[item_id]
				if item_def.on_remove then
					item_def:on_remove(player)
				end
				list[item_id] = nil
				Isaac.DebugString(("Removed item %d!"):format(item_id))
				_signal_refresh_cache(i-1)
			end
		end
	end

	-- add items to list of potential items
	for _, entity in pairs(Isaac.GetRoomEntities()) do
		local item_id = entity.SubType
		if entity.Type == EntityType.ENTITY_PICKUP
		and entity.Variant == PickupVariant.PICKUP_COLLECTIBLE
		and Mod.items[item_id] then
			for i = 1, game:GetNumPlayers() do
				local player_items = _get_player_items(i)
				if player_items.list[item_id] == nil then
					if player_items.potential[item_id] == nil then
						Isaac.DebugString(("Added potential item %d!"):format(item_id))
					end
					player_items.potential[item_id] = 100
				end
			end
		end
	end

	-- track potential items and see if player picked them up
	for i = 1, game:GetNumPlayers() do
		local player_items = _get_player_items(i)
		local player = game:GetPlayer(i-1)
		for item_id in pairs(player_items.potential) do
			if player:HasCollectible(item_id) then
				player_items.list[item_id] = true
				player_items.potential[item_id] = nil
				Isaac.DebugString(("Added item %d!"):format(item_id))
				_signal_refresh_cache(i-1)
				local item_def = Mod.items[item_id]
				if item_def.on_pickup then
					item_def:on_pickup(player)
				end
				if item_def.on_add then
					item_def:on_add(player)
				end
			else
				player_items.potential[item_id] = player_items.potential[item_id] - 1
				if player_items.potential[item_id] <= 0 then
					player_items.potential[item_id] = nil
					Isaac.DebugString(("Removed potential item %d!"):format(item_id))
				end
			end
		end
	end

	-- add enemies to list
	for _, entity in pairs(Isaac.GetRoomEntities()) do
		if not _enemies[entity.Index] then
			-- Randomly replace trinkets as they spawn (50% chance)
			if entity.Type == EntityType.ENTITY_PICKUP
			and entity.Variant == PickupVariant.PICKUP_TRINKET
			and not Mod.args.room_changed then
				local entity = entity:ToPickup()
				if math.random() < 0.5 then
					trinket_name = random_choice(Mod.trinket_names)
					trinket_id = Isaac.GetTrinketIdByName(trinket_name)
					entity:Morph(EntityType.ENTITY_PICKUP,
						PickupVariant.PICKUP_TRINKET, trinket_id, true)
				end
			end
			_enemies[entity.Index] = entity
		end
	end

	-- check for dead enemies
	for id, entity in pairs(_enemies) do
		if not entity:Exists() then
			_enemies[id] = nil
			if entity:IsActiveEnemy(false) then
				local enemy = entity:ToNPC()
				Mod:call_callbacks(Isaac.GetPlayer(0), "enemy_died", enemy, _killers[id])
			end
			_killers[id] = nil
		end
	end

	Mod:call_callbacks_all("update", _timer, _timerf)
end

function Mod.callbacks:render()
	local game = Game()
	for i = 1, game:GetNumPlayers() do
		local list = _get_player_items(i).list;
		local pos = 0
		for item_i, item_v in pairs(list) do
			pos = pos + 1
			Isaac.RenderText(tostring(item_i), (i-1)*128, (pos-1)*16, 255, 255, 255, 255);
		end
	end
	Isaac.RenderText("Range: " .. tostring(Isaac.GetPlayer(0).TearHeight), 400, 0, 255, 255, 255, 255)
	for i, entity in pairs(Isaac.GetRoomEntities()) do
		if entity:ToPlayer() or entity:ToTear() or entity:ToNPC() then
			local size = get_size(entity)
			local pos = game:GetRoom():WorldToScreenPosition(entity.Position)
			Isaac.RenderText(("%.2f"):format(size.X), pos.X, pos.Y+ 0, 255, 255, 255, 255)
			Isaac.RenderText(("%.2f"):format(size.Y), pos.X, pos.Y+12, 255, 255, 255, 255)
			Isaac.RenderText(("%.2f"):format(entity.Mass), pos.X, pos.Y+24, 255, 255, 255, 255)
		end
	end
end

function Mod.callbacks:use_item(item, rng)
	local item_def = Mod.items[item]
	if item_def and item_def.on_usage then
		local ret = item_def:on_usage(Isaac.GetPlayer(0), rng)
		if ret == nil then ret = true end
		return ret
	end
end

function Mod.callbacks:player_take_damage(player, amount, ...)
	player = player:ToPlayer()
	Mod:call_callbacks(player, "player_take_damage", amount, ...)
	print("TOOK " .. tostring(amount) .. " DAMAGE!")
	Mod.args.damage_taken = Mod.args.damage_taken + amount
	print("NOW AT " .. tostring(Mod.args.damage_taken) .. " DAMAGE")
end

function Mod.callbacks:enemy_take_damage(enemy, amount, flag, source, ...)
	if not enemy:IsVulnerableEnemy() then return end
	_killers[enemy.Index] = _killers[enemy.Index] or {}
	if source then
		_killers[enemy.Index].Variant = source.Variant
		_killers[enemy.Index].Type = source.Type
		_killers[enemy.Index].SubType = source.SubType
	end
	Mod.args.damage_dealt = Mod.args.damage_dealt + amount
	Mod:call_callbacks(Isaac.GetPlayer(0), "enemy_take_damage",
		enemy, amount, flag, source, ...)
end

function Mod.callbacks:use_pill(pill_effect)
	Mod:call_callbacks(Isaac.GetPlayer(0), "take_pill", pill_effect)
	local func = Mod.pills[pill_effect]
	if func then
		func()
	else
		print("Error! Pill effect " .. tostring(pill_effect) .. " has no definition!")
	end
end

function Mod.callbacks:use_card(card)
	Mod:call_callbacks(Isaac.GetPlayer(0), "use_card", card)
	local func = Mod.cards[card]
	if func then
		func()
	else
		print("Error! Card " .. tostring(card) .. " has no definition!")
	end
end

function Mod.callbacks:familiar_init(familiar)
	local player = familiar.Player
	local def = Mod.familiars[familiar.Variant]
	if def and def.familiar_init then
		def:familiar_init(player, familiar)
	end
end

function Mod.callbacks:familiar_update(familiar)
	local player = familiar.Player
	local def = Mod.familiars[familiar.Variant]
	if def and def.familiar_update then
		def:familiar_update(player, familiar)
	end
end

Mod:AddCallback(ModCallbacks.MC_POST_UPDATE, Mod.callbacks.update)
Mod:AddCallback(ModCallbacks.MC_EVALUATE_CACHE, Mod.callbacks.evaluate_cache)
Mod:AddCallback(ModCallbacks.MC_USE_ITEM, Mod.callbacks.use_item)
Mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG, Mod.callbacks.player_take_damage, EntityType.ENTITY_PLAYER)
Mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG, Mod.callbacks.enemy_take_damage)
Mod:AddCallback(ModCallbacks.MC_USE_CARD, Mod.callbacks.use_card)
Mod:AddCallback(ModCallbacks.MC_USE_PILL, Mod.callbacks.use_pill)
Mod:AddCallback(ModCallbacks.MC_FAMILIAR_INIT, Mod.callbacks.familiar_init)
Mod:AddCallback(ModCallbacks.MC_FAMILIAR_UPDATE, Mod.callbacks.familiar_update)

--Uncomment for debug render
-- Mod:AddCallback(ModCallbacks.MC_POST_RENDER, Mod.callbacks.render)
