from SettingsList import logic_tricks, setting_infos, get_settings_from_tab
from LocationList import location_table
from StartingItems import inventory, songs, equipment
import json
import sys
import random as R

##################################
# if any of the EXCLUDE options are set to True, the corresponding setting will not be randomized via plando
# instead the value selected in the GUI will be used for seed generation
# should you exclude an entire tab, none of the settings will be randomized

EXCLUDE_MAIN_TAB = False
# rainbow bridge requirement will still be randomized, just without skull tokens as an option
EXCLUDE_BRIDGETOKENS = True
EXCLUDE_TRIFORCE_HUNT = False
EXCLUDE_ONE_MAJOR_PER_DUNGEON = True
# a value between 0 and 12 inclusive guarantees that number of MQ dungeons, any other value will turn on random MQ
NUM_MASTER_QUEST = 0
EXCLUDE_ENTRANCE_RANDO = False

EXCLUDE_DETAILED_TAB = True
# an integer used to weight the probability of adding any specific trick
NUM_EXPECTED_TRICKS = 0
# an integer used to weight the probability of excluded locations
NUM_EXCLUDED_LOCATIONS = 0

EXCLUDE_STARTING_TAB = False
NUM_STARTING_HEARTS = 3
# an integer used to weight the probability of each item to be included from the corresponding list
# these lists are fairly small, so the variance can be pretty high
NUM_STARTING_INVENTORY = {
    "starting_equipment": 0,
    "starting_items": 0,
    "starting_songs": 0
}

EXCLUDE_OTHER_TAB = False
# all 3 hint settings: clearer, requirement, distribution
EXCLUDE_HINTS = False
# both ice trap settings: appearance, number
EXCLUDE_ICE_TRAPS = True
EXCLUDE_ITEM_POOL = True
EXCLUDE_DAMAGE_MULT = True
##################################


def populateTricks():
    weight = NUM_EXPECTED_TRICKS / len(logic_tricks)
    tricks = []
    for _, v in logic_tricks.items():
        if R.random() <= weight:
            tricks.append(v['name'])

    return tricks


def populateLocationExclusions():
    # prune the raw list of locations to only those that give items
    TYPES_NOT_INCLUDED = ['Event', 'Drop', 'Boss', 'GossipStone']
    refined_locations = []
    for k, v in location_table.items():
        if ((v[0] in TYPES_NOT_INCLUDED) or (v[0] == 'Shop' and k[-1] in ['1', '2', '3', '4'])):
            continue
        else:
            refined_locations.append(k)

    weight = NUM_EXCLUDED_LOCATIONS / len(refined_locations)
    excluded_locations = []
    for l in refined_locations:
        if R.random() <= weight:
            excluded_locations.append(l)

    return excluded_locations


def populateStartingItems(setting_name):
    item_list = []
    if setting_name == "starting_equipment":
        item_list = equipment
    elif setting_name == "starting_items":
        item_list = inventory
    elif setting_name == "starting_songs":
        item_list = songs
    else:
        return []

    weight = NUM_STARTING_INVENTORY[setting_name] / len(item_list)
    result = []
    for item in item_list:
        if R.random() <= weight:
            result.append(item)

    return result


def getRandomFromType(setting):
    if setting.gui_type == 'Checkbutton':
        return R.random() <= 0.5
    elif setting.gui_type == 'Combobox':
        s = list(setting.choices.keys())
        if setting.name == 'bridge' and EXCLUDE_BRIDGETOKENS:
            s.remove('tokens')
        return R.choice(s)
    elif setting.gui_type == 'Scale':
        if setting.name == "starting_hearts":
            return NUM_STARTING_HEARTS
        else:
            s = list(setting.choices.keys())
            s.sort()
            return R.randint(s[0], s[-1])
    elif setting.gui_type == 'SearchBox':
        if setting.name == 'disabled_locations':
            return populateLocationExclusions()
        elif setting.name == 'allowed_tricks':
            return populateTricks()
        else:
            return populateStartingItems(setting.name)
    else:
        return setting.default


settings_to_randomize = list()
if not EXCLUDE_MAIN_TAB:
    settings_to_randomize.extend(list(get_settings_from_tab('main_tab'))[1:])
if not EXCLUDE_DETAILED_TAB:
    settings_to_randomize.extend(list(get_settings_from_tab('detailed_tab')))
if not EXCLUDE_STARTING_TAB:
    settings_to_randomize.extend(list(get_settings_from_tab('starting_tab')))
if not EXCLUDE_OTHER_TAB:
    settings_to_randomize.extend(list(get_settings_from_tab('other_tab')))


dont_randomize = {
    "logic_rules",
    "fast_chests",
    "text_shuffle",
    "ocarina_songs",
    "useful_cutscenes",
    "mq_dungeons_random",
    "mq_dungeons",
}
if EXCLUDE_ONE_MAJOR_PER_DUNGEON:
    dont_randomize.add("one_item_per_dungeon")
if EXCLUDE_DAMAGE_MULT:
    dont_randomize.add("damage_multiplier")
if EXCLUDE_ENTRANCE_RANDO:
    dont_randomize.add("entrance_shuffle")
if EXCLUDE_TRIFORCE_HUNT:
    dont_randomize.add("triforce_hunt")
if EXCLUDE_HINTS:
    dont_randomize.add("clearer_hints")
    dont_randomize.add("hints")
    dont_randomize.add("hint_dist")
if EXCLUDE_ICE_TRAPS:
    dont_randomize.add("ice_trap_appearance")
    dont_randomize.add("junk_ice_traps")
if EXCLUDE_ITEM_POOL:
    dont_randomize.add("item_pool_value")


chosen_settings = {}
for info in setting_infos:
    if info.name in settings_to_randomize and info.name not in dont_randomize:
        chosen_settings[info.name] = getRandomFromType(info)
        print(info.name + ' - ' + info.gui_type +
              ' : ' + str(chosen_settings[info.name]))


# either fix MQ or turn on the built in random function
if NUM_MASTER_QUEST >= 0 and NUM_MASTER_QUEST <= 12:
    chosen_settings["mq_dungeons_random"] = False
    chosen_settings["mq_dungeons"] = NUM_MASTER_QUEST
else:
    chosen_settings["mq_dungeons_random"] = True


output = {}
output['settings'] = chosen_settings
with open('rand-settings.json', 'w') as fp:
    json.dump(output, fp, indent=4)
