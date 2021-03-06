from . import filepicker
from .stat import IsaacStats
from . import util
import os
import random
import glob

CONST_ACTIVE_ITEM_IDS = [
    # Only relevant items which wouldn't suck as an effect (e.g. no kamikaze)
    507, 486, 484, 421, 383, 394, 288, 287, 192, 175, 171,
    160, 145, 137, 123, 111, 107, 56, 45, 41, 39, 36, 35, 34
]

CONST_ITEM_PASSIVE_FILE = "generators/script/item_passive.lua"
CONST_ITEM_ACTIVE_FILE = "generators/script/item_active.lua"
CONST_ITEM_FAMILIAR_FILE = "generators/script/item_familiar.lua"
CONST_TRINKET_FILE = "generators/script/trinket.lua"
CONST_CARD_FILE = "generators/script/card.lua"
CONST_PILL_FILE = "generators/script/pill.lua"

CONST_TEARFLAGS = [
# "TearFlags.TEAR_BOMBERANG",
# "TearFlags.TEAR_WAIT", # antigrav (reset every frame)
# "TearFlags.TEAR_SAD_BOMB",
# "TearFlags.TEAR_BUTT_BOMB",
# "TearFlags.TEAR_GLITTER_BOMB",
# "TearFlags.TEAR_GISH", make enemy black
# "TearFlags.TEAR_SCATTER_BOMB",
# "TearFlags.TEAR_COIN_DROP",
# "TearFlags.TEAR_BLACK_HP_DROP",
# "TearFlags.TEAR_TRACTOR_BEAM",
# "TearFlags.TEAR_PERMANENT_CONFUSION",
# "TearFlags.TEAR_MIDAS",
# "TearFlags.TEAR_LUDOVICO",
    # List of tear effects which may be cool on a familiar or something
    "TearFlags.TEAR_SPECTRAL",
    "TearFlags.TEAR_PIERCING",
    "TearFlags.TEAR_HOMING",
    "TearFlags.TEAR_SLOW",
    "TearFlags.TEAR_POISON",
    "TearFlags.TEAR_FREEZE",
    "TearFlags.TEAR_SPLIT",
    "TearFlags.TEAR_GROW", #lump of coal
    "TearFlags.TEAR_PERSISTENT", # polyphemus
    "TearFlags.TEAR_WIGGLE",
    "TearFlags.TEAR_MIGAN", # create fly
    "TearFlags.TEAR_EXPLOSIVE",
    "TearFlags.TEAR_CHARM",
    "TearFlags.TEAR_CONFUSION",
    "TearFlags.TEAR_HP_DROP",
    "TearFlags.TEAR_ORBIT",
    "TearFlags.TEAR_QUADSPLIT",
    "TearFlags.TEAR_BOUNCE",
    "TearFlags.TEAR_FEAR",
    "TearFlags.TEAR_SHRINK",
    "TearFlags.TEAR_BURN",
    "TearFlags.TEAR_ATTRACTOR",
    "TearFlags.TEAR_KNOCKBACK",
    "TearFlags.TEAR_PULSE",
    "TearFlags.TEAR_SPIRAL",
    "TearFlags.TEAR_FLAT",
    "TearFlags.TEAR_SQUARE", # hook worm
    "TearFlags.TEAR_GLOW",
    "TearFlags.TEAR_STICKY",
    "TearFlags.TEAR_CONTINUUM",
    "TearFlags.TEAR_LIGHT_FROM_HEAVEN",
    "TearFlags.TEAR_GODS_FLESH",
    "TearFlags.TEAR_GREED_COIN",
    "TearFlags.TEAR_MYSTERIOUS_LIQUID_CREEP",
    "TearFlags.TEAR_BIG_SPIRAL", # ouroboros
    "TearFlags.TEAR_BOOGER",
    "TearFlags.TEAR_EGG",
    "TearFlags.TEAR_ACID",
    "TearFlags.TEAR_BONE",
    "TearFlags.TEAR_BELIAL",
    "TearFlags.TEAR_NEEDLE",
    "TearFlags.TEAR_JACOBS",
    "TearFlags.TEAR_HORN",
]

CONST_TEARFLAG_CHANCES = {
    "TearFlags.TEAR_HORN": 0.2,
    "TearFlags.TEAR_NEEDLE": 0.2,
    "TearFlags.TEAR_GODS_FLESH": 0.3,
    "TearFlags.TEAR_LIGHT_FROM_HEAVEN": 0.3,
    "TearFlags.TEAR_STICKY": 0.3,
    "TearFlags.TEAR_FEAR": 0.3,
    "TearFlags.TEAR_CHARM": 0.3,
    "TearFlags.TEAR_SLOW": 0.3,
    "TearFlags.TEAR_FREEZE": 0.3,
    "TearFlags.TEAR_CONFUSION": 0.4,
    "TearFlags.TEAR_POISON": 0.4,
    "TearFlags.TEAR_BOOGER": 0.4,
}

CONST_TEARFLAG_COLORS = {
    "TearFlags.TEAR_SPECTRAL":  (1.0, 1.0, 1.0, 0.7,   0,    0,    0),
    "TearFlags.TEAR_HOMING":    (0.8, 0.1, 1.0, 1.0,   0,    0,    0),
    "TearFlags.TEAR_SLOW":      (1.0, 1.0, 1.0, 1.0,  80,   80,   80),
    "TearFlags.TEAR_POISON":    (0.5, 1.0, 0.5, 1.0,   0,    0,    0),
    "TearFlags.TEAR_FREEZE":    (0.5, 0.5, 0.5, 1.0,   0,    0,    0),
    "TearFlags.TEAR_GROW":      (0.2, 0.2, 0.2, 1.0,   0,    0,    0),
    "TearFlags.TEAR_EXPLOSIVE": (0.2, 0.5, 0.2, 1.0,   0,    0,    0),
    "TearFlags.TEAR_CHARM":     (1.0, 0.5, 0.5, 1.0,   0,    0,    0),
    "TearFlags.TEAR_CONFUSION": (0.4, 0.4, 0.4, 1.0,   0,    0,    0),
    "TearFlags.TEAR_BOUNCE":    (0.9, 0.9, 0.9, 1.0,   0,    0,    0),
    "TearFlags.TEAR_LIGHT_FROM_HEAVEN": (0.9, 0.9, 1.0, 1.0,  10,   10,   20),
    "TearFlags.TEAR_GODS_FLESH":        (1.0, 0.9, 0.9, 1.0,   0,    0,    0),
    "TearFlags.TEAR_STRANGE_ATTRACTOR": (0.5, 0.5, 0.5, 1.0,  80,   80,   80),
}
CONST_TEARFLAG_VARIANTS = {
    "TearFlags.TEAR_FEAR": "TearVariant.DARK_MATTER",
    "TearFlags.TEAR_MYSTERIOUS_LIQUID_CREEP": "TearVariant.MYSTERIOUS",
    "TearFlags.TEAR_PIERCING": "TearVariant.CUPID_BLUE",
    "TearFlags.TEAR_GODS_FLESH": "TearVariant.GODS_FLESH",
    "TearFlags.TEAR_STICKY": "TearVariant.EXPLOSIVO",
    "TearFlags.TEAR_BOOGER": "TearVariant.BOOGER",
    "TearFlags.TEAR_EGG": "TearVariant.EGG",
    "TearFlags.TEAR_BONE": "TearVariant.BONE",
    "TearFlags.TEAR_HORN": "TearVariant.BLACK_TOOTH",
    "TearFlags.TEAR_NEEDLE": "TearVariant.NEEDLE",
}
CONST_EFFECT_TYPES_COMMON = [
    "EffectVariant.PLAYER_CREEP_WHITE",
    "EffectVariant.PLAYER_CREEP_BLACK",
    "EffectVariant.PLAYER_CREEP_RED",
    "EffectVariant.PLAYER_CREEP_GREEN",
]

CONST_EFFECT_TYPES_RARE = [
    "EffectVariant.HOT_BOMB_FIRE",
    "EffectVariant.MONSTROS_TOOTH",
    "EffectVariant.MOM_FOOT_STOMP",
    "EffectVariant.PLAYER_CREEP_LEMON_MISHAP",
    "EffectVariant.SHOCKWAVE",
    "EffectVariant.SHOCKWAVE_DIRECTIONAL",
    "EffectVariant.FIREWORKS",#Useless but kek
]

CONST_ENTITY_PICKUP = "EntityType.ENTITY_PICKUP"

CONST_PICKUP_VARIANTS = {
    "any": "PickupVariant.PICKUP_NULL",
    "heart": "PickupVariant.PICKUP_HEART",
    "coin": "PickupVariant.PICKUP_COIN",
    "key": "PickupVariant.PICKUP_KEY",
    "bomb": "PickupVariant.PICKUP_BOMB",
    "chest": "PickupVariant.PICKUP_CHEST",
    "sack": "PickupVariant.PICKUP_GRAB_BAG",
    "pill": "PickupVariant.PICKUP_PILL",
    "battery": "PickupVariant.PICKUP_LIL_BATTERY",
    "card": "PickupVariant.PICKUP_TAROTCARD",
    "trinket": "PickupVariant.PICKUP_TRINKET",
}
CONST_PICKUP_VARIANTS_LIST = list(CONST_PICKUP_VARIANTS.keys())

CONST_PICKUP_SUBTYPES = {
    # NOT a list of all subtypes!
    # This is only a selection of specific drops
    # "0" represents null sub-type, which spawns random drops
    "any": ["0"],
    "heart": ["0", "HeartSubType.HEART_FULL", "HeartSubType.HEART_SOUL",
        "HeartSubType.HEART_ETERNAL", "HeartSubType.HEART_BLACK",
        "HeartSubType.HEART_GOLDEN"],
    "coin": ["0", "CoinSubType.COIN_PENNY", "CoinSubType.COIN_STICKYNICKEL"],
    "key": ["0", "KeySubType.KEY_NORMAL", "KeySubType.KEY_CHARGED"],
    "bomb": ["0", "BombSubType.BOMB_NORMAL", "BombSubType.BOMB_TROLL"],
    "chest": ["0"],
    "sack": ["0"],
    "pill": ["0"],
    "battery": ["0"],
    "card": ["0"],
    "trinket": ["0"],
}

CONST_COLLECTIBLES = [
    # List of items that woudn't be totally broken or weird when
    # Added to and removed from the player at varying intervals
    "CollectibleType.COLLECTIBLE_DEAD_TOOTH",
    "CollectibleType.COLLECTIBLE_EYE_OF_BELIAL",
    "CollectibleType.COLLECTIBLE_JACOBS_LADDER",
    "CollectibleType.COLLECTIBLE_LARGE_ZIT",
    "CollectibleType.COLLECTIBLE_LEAD_PENCIL",
    "CollectibleType.COLLECTIBLE_LITTLE_HORN",
    "CollectibleType.COLLECTIBLE_SINUS_INFECTION",
    "CollectibleType.COLLECTIBLE_TRACTOR_BEAM",
    "CollectibleType.COLLECTIBLE_THE_WIZ",
    "CollectibleType.COLLECTIBLE_SCATTER_BOMBS",
    "CollectibleType.COLLECTIBLE_PUPULA_DUPLEX",
    "CollectibleType.COLLECTIBLE_NUMBER_TWO",
    "CollectibleType.COLLECTIBLE_NIGHT_LIGHT",
    "CollectibleType.COLLECTIBLE_KIDNEY_STONE",
    "CollectibleType.COLLECTIBLE_GLITTER_BOMBS",
    "CollectibleType.COLLECTIBLE_HEAD_OF_THE_KEEPER",
    "CollectibleType.COLLECTIBLE_EXPLOSIVO",
    "CollectibleType.COLLECTIBLE_EPIPHORA",
    # "CollectibleType.COLLECTIBLE_DEAD_EYE", Removed because it is kinda broken
    "CollectibleType.COLLECTIBLE_CONTINUUM",
    "CollectibleType.COLLECTIBLE_CIRCLE_OF_PROTECTION",
    "CollectibleType.COLLECTIBLE_BLACK_POWDER",
    "CollectibleType.COLLECTIBLE_WAFER",
    "CollectibleType.COLLECTIBLE_TREASURE_MAP",
    "CollectibleType.COLLECTIBLE_COMPASS",
    "CollectibleType.COLLECTIBLE_BLUE_MAP",
    "CollectibleType.COLLECTIBLE_TOUGH_LOVE",
    "CollectibleType.COLLECTIBLE_TINY_PLANET",
    "CollectibleType.COLLECTIBLE_TECHNOLOGY",
    # "CollectibleType.COLLECTIBLE_TECHNOLOGY_2", Also kinda broken
    "CollectibleType.COLLECTIBLE_TECH_X",
    "CollectibleType.COLLECTIBLE_STRANGE_ATTRACTOR",
    "CollectibleType.COLLECTIBLE_SPOON_BENDER",
    "CollectibleType.COLLECTIBLE_SOY_MILK",
    "CollectibleType.COLLECTIBLE_RUBBER_CEMENT",
    "CollectibleType.COLLECTIBLE_PROPTOSIS",
    "CollectibleType.COLLECTIBLE_PARASITE",
    "CollectibleType.COLLECTIBLE_OUIJA_BOARD",
    "CollectibleType.COLLECTIBLE_MY_REFLECTION",
    "CollectibleType.COLLECTIBLE_MONSTROS_LUNG",
    "CollectibleType.COLLECTIBLE_MOMS_KNIFE",
    "CollectibleType.COLLECTIBLE_MOMS_EYE",
    "CollectibleType.COLLECTIBLE_MIDAS_TOUCH",
    "CollectibleType.COLLECTIBLE_MAGNETO",
    "CollectibleType.COLLECTIBLE_LUMP_OF_COAL",
    "CollectibleType.COLLECTIBLE_LUDOVICO_TECHNIQUE",
    "CollectibleType.COLLECTIBLE_LOST_CONTACT",
    "CollectibleType.COLLECTIBLE_LOKIS_HORNS",
    "CollectibleType.COLLECTIBLE_LADDER",
    "CollectibleType.COLLECTIBLE_IPECAC",
    "CollectibleType.COLLECTIBLE_FIRE_MIND",
    "CollectibleType.COLLECTIBLE_EPIC_FETUS",
    "CollectibleType.COLLECTIBLE_DR_FETUS",
    "CollectibleType.COLLECTIBLE_CUPIDS_ARROW",
    "CollectibleType.COLLECTIBLE_CHOCOLATE_MILK",
    "CollectibleType.COLLECTIBLE_BRIMSTONE",
    "CollectibleType.COLLECTIBLE_ANTI_GRAVITY",
    "CollectibleType.COLLECTIBLE_20_20",
]

CONST_COLLECTIBLES_DISABLE_TIMER = [
    # Collectibles which just don't work when on a timer
    "CollectibleType.COLLECTIBLE_BRIMSTONE",
    "CollectibleType.COLLECTIBLE_CHOCOLATE_MILK",
    "CollectibleType.COLLECTIBLE_EPIC_FETUS",
    "CollectibleType.COLLECTIBLE_DR_FETUS",
    "CollectibleType.COLLECTIBLE_LADDER",
    "CollectibleType.COLLECTIBLE_LUDOVICO_TECHNIQUE",
    "CollectibleType.COLLECTIBLE_MONSTROS_LUNG",
    "CollectibleType.COLLECTIBLE_MOMS_KNIFE",
    "CollectibleType.COLLECTIBLE_TECH_X",
    "CollectibleType.COLLECTIBLE_TECHNOLOGY",
    "CollectibleType.COLLECTIBLE_TREASURE_MAP",
    "CollectibleType.COLLECTIBLE_COMPASS",
]

# Collectibles which may be used on a timer
CONST_COLLECTIBLES_TIMER = [x for x in CONST_COLLECTIBLES
    if x not in CONST_COLLECTIBLES_DISABLE_TIMER]

def choose_random_active():
    return random.choice(CONST_ACTIVE_ITEM_IDS)

def choose_random_effect_common():
    return random.choice(CONST_EFFECT_TYPES_COMMON)

def choose_random_effect_rare():
    return random.choice(CONST_EFFECT_TYPES_RARE)

def choose_random_collectible(is_timer):
    if is_timer:
        return random.choice(CONST_COLLECTIBLES_TIMER)
    else:
        return random.choice(CONST_COLLECTIBLES)

def choose_random_tearflag():
    return random.choice(CONST_TEARFLAGS)

def get_tearflag_chance(flagname):
    if flagname in CONST_TEARFLAG_CHANCES:
        return CONST_TEARFLAG_CHANCES[flagname]
    return 1

def get_tearflag_color(flagname):
    if flagname in CONST_TEARFLAG_COLORS:
        return "Color({})".format(",".join([str(x) for x in CONST_TEARFLAG_COLORS[flagname]]))

def get_tearflag_variant(flagname):
    if flagname in CONST_TEARFLAG_VARIANTS:
        return CONST_TEARFLAG_VARIANTS[flagname]

def id_to_descriptors(item_id):
    if "." in item_id:
        item_id = item_id.rsplit(".")[1]
    return [x.title() for x in item_id.split("_")[1:]]

def does_effect_need_velocity(name):
    return name == "EffectVariant.SHOCKWAVE_DIRECTIONAL"

def choose_random_pickup_subtype(name):
    if name in CONST_PICKUP_SUBTYPES:
        if random.random() < 0.50:
            return "0"
        else:
            return random.choice(CONST_PICKUP_SUBTYPES[name])
    else:
        return "0"

def choose_random_pickup(genstate):
    choices, weights = [], []
    for name in CONST_PICKUP_VARIANTS_LIST:
        choices.append(name)
        weights.append(1+genstate.get_hint("pickup-{}".format(name)))
    return util.choice_weights(choices, weights)

def get_pickup_name(name):
    return CONST_PICKUP_VARIANTS[name]

def load_file(fname, genstate):
    with open(fname, 'r') as fh:
        return load_string(fh.read(), genstate, fname)

def load_string(string, genstate, fname):
    sb = ScriptBuilder(genstate);
    sb.parse_file_to_output(fname);
    return sb

def generate_item_active(genstate):
    return load_file(CONST_ITEM_ACTIVE_FILE, genstate)

def generate_item_passive(genstate):
    return load_file(CONST_ITEM_PASSIVE_FILE, genstate)

def generate_item_familiar(genstate):
    return load_file(CONST_ITEM_FAMILIAR_FILE, genstate)

def generate_card_effect(genstate):
    return load_file(CONST_CARD_FILE, genstate)

def generate_pill_effect(genstate):
    return load_file(CONST_PILL_FILE, genstate)

def generate_trinket(genstate):
    return load_file(CONST_TRINKET_FILE, genstate)

CONST_PYTHON_BEGIN = "python[["
CONST_PYTHON_END = "]]"
CONST_PYTHON_BEGIN_LEN = len(CONST_PYTHON_BEGIN)
CONST_PYTHON_END_LEN = len(CONST_PYTHON_END)
CONST_GEN_PATH = "generators/script/"

class ScriptBuilder:
    def __init__(self, genstate):
        self.output = []
        self.buffer = ""
        self.data = {}
        self.genstate = genstate
        self.allow_random = True
    def set_allow_random(self, value):
        self.allow_random = value
    def inc_var(self, name, acc):
        if not name in self.data:
            self.data[name] = 0
        self.data[name] += acc
    def set_var(self, name, value):
        self.data[name] = value
    def get_var(self, name):
        if name in self.data:
            return self.data[name]
    def get_var_default(self, name, other):
        if name in self.data:
            return self.data[name]
        else:
            return other
    def parse_file(self, fname):
        with open(fname, 'r') as fh:
            self.parse(fh.read(), fname)
    def parse_file_to_output(self, fname):
        self.parse_file(fname)
        self.write_effect(self.buffer)
        self.buffer = ""
    def parse(self, string, fname):
        self.buffer = ""
        while len(string) > 0:
            if CONST_PYTHON_BEGIN in string and CONST_PYTHON_END in string:
                # Find positions
                python_pos_start = string.find(CONST_PYTHON_BEGIN)
                python_pos_end = string.find(CONST_PYTHON_END)
                # Get string splits
                append_string = string[:python_pos_start]
                python_string = string[python_pos_start+CONST_PYTHON_BEGIN_LEN:python_pos_end]
                string = string[python_pos_end+CONST_PYTHON_END_LEN:]
                # Append strings
                self.write(append_string)
                try:
                    exec(python_string, globals(), {
                        "gen": self
                    })
                except Exception as err:
                    print(err)
                    print("Occurred in file {}!".format(fname))
            else:
                self.write(string)
                string = ""
    def parse_to_output(self, string, fname):
        self.parse(string, fname)
        self.write_effect(self.buffer)
        self.buffer = ""
    def write(self, string):
        self.buffer += str(string)
    def get_hint(self, name):
        return self.genstate.get_hint(name)
    def add_hint(self, name, value):
        self.genstate.add_hint(name, value)
    def writeln(self, string):
        self.buffer += str(string) + "\n"
    def write_effect(self, string):
        self.output.append(str(string))
    def include(self, fname, exclude=[]):
        if os.path.isfile(fname):
            # result = load_file(fname, self.genstate)
            # self.writeln(result.get_output())
            # for key, value in result.data.items():
            #     self.set_var(key, value)
            pbuffer = self.buffer
            self.parse_file(fname)
            self.buffer = pbuffer + self.buffer
            return filepicker.path_to_name(fname)
        elif os.path.isdir(fname):
            picker = filepicker.get_path(fname)
            filedef = picker.choose_random_with_hint(\
                self.genstate, exclude=exclude)
            path = filedef.get_path()
            return self.include(path)
        else:
            base_dir = os.path.dirname(fname)
            if not base_dir.startswith(CONST_GEN_PATH):
                return self.include(os.path.join(CONST_GEN_PATH, fname), exclude)
            else:
                raise Exception("Not a file or directory!" + fname)
    def chance(self, base_chance, luck_scale, min_chance):
        if self.allow_random:
            self.writeln("if math.random()*math.max({}, {}-{}*player.Luck) > 1 then return end".format(\
                min_chance, base_chance, luck_scale));
    def get_output(self):
        return ",".join(self.output)
