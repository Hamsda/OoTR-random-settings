from SettingsList import setting_infos, get_settings_from_tab
from StartingItems import inventory, songs, equipment
import json
import random


FILE_WEIGHTS = "mystery-weights.json"
FILE_PLANDO = "mystery-plando.json"


def getChoicesFromType(setting):
    dictionary = dict()
    if setting.gui_type == "SearchBox":
        pass
    elif setting.gui_type == "CheckBox":
        dictionary[True] = 1
        dictionary[False] = 1
    else:
        for key in setting.choices:
            dictionary[key] = 1
    return dictionary


def castStringsToType(string):
    try:
        if string == "true":
            return True
        elif string == "false":
            return False
        else:
            return int(string)
    except ValueError:
        return string


settings_list = list()
settings_list.extend(list(get_settings_from_tab("main_tab"))[1:])
settings_list.extend(list(get_settings_from_tab("detailed_tab")))
settings_list.extend(list(get_settings_from_tab("starting_tab")))
settings_list.extend(list(get_settings_from_tab("other_tab")))

weighted_settings = {}
try:
    with open(FILE_WEIGHTS, "r") as fp:
        weighted_settings = json.load(fp)
    print("weights loaded")

    chosen_settings = {}
    for setting, options in weighted_settings.items():
        if options:
            chosen_settings[setting] = castStringsToType(random.choices(population=list(options.keys()), weights=list(options.values()), k=1)[0])
    print("settings chosen")

    output = {}
    output["settings"] = chosen_settings
    with open(FILE_PLANDO, "w") as fp:
        json.dump(output, fp, indent=4)
    print("plando file created")

except IOError:
    print("no weights found")
    for info in setting_infos:
        if info.name in settings_list:
            weighted_settings[info.name] = getChoicesFromType(info)
    with open(FILE_WEIGHTS, "w") as fp:
        json.dump(weighted_settings, fp, indent=4)
    print("default weights file created")

