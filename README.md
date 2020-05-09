# OoTR Mystery Settings

This is a python script to be used with the [Ocarina of Time Randomizer](https://github.com/TestRunnerSRL/OoT-Randomizer). Its purpose is to randomize more settings than the built-in `Randomize Main Rule Settings` will and customize how often each option will get selected via a simple json file.

## How to

- Take MysterySettings.py and put it into the main folder of an OoTR repo (forks work just the same).
- Run MysterySettings.py once to create `mystery-weights.json`. This file will contain all settings and their corresponding options with default weights of 1.
- Customize the weights to your liking. For each setting, the chance for each individual option will be `[value for this option] / [sum of values for all options for this setting]`.
  - For example

    ```json
      "open_door_of_time": {
          "true": 2,
          "false": 1
      },
    ```

    will result in `open_door_of_time` being `true` 2/3 of the time and `false` 1/3 of the time.
- Run MysterySettings.py again and it will read `mystery-weights.json` to create `mystery-plando.json`. This file will contain the selected settings, so do not look inside to avoid spoilers.
- Run Gui.py from the OoTR repo:
  - At the top of the first tab `ROM Options` check `Enable Plandomizer (Optional)`.
  - Select `mystery-plando.json` you just created for `Plandomizer File` right below it.
  - Generate your seed and enjoy the mystery :D
- You can "save" different weights by keeping the customized `mystery-weights.json`. The script will always read from a file with that name in the same folder.

## Limitations

Right now it is not possible to randomize certain things with this script:

- Excluded Locations
- Enabled Tricks
- Starting Equipment
- Starting Songs
- Starting Items

When generating your seed, the randomizer will instead chose whatever you have selected in the GUI for those 5 lists.
