import argparse
import os
import time

parser = argparse.ArgumentParser(
    description="Appends additional keyboard layout shortcuts to kitty.conf"
)
parser.add_argument(
    "--config",
    type=str,
    dest="config",
    help="Config file to edit. If not provided, \
          will be used default location: ~/.config/kitty/kitty.conf",
)
parser.add_argument(
    "--map",
    type=str,
    dest="mapfile",
    help="Map file with two lines: existing and additional layout. \
          If not provided, default latin to cyrillic map will be used",
)
parser.add_argument(
    "--skip-macos",
    dest="skip_macos",
    action="store_true",
    help="Macos shortcuts will be skipped",
)
parser.add_argument(
    "--uncomment",
    dest="uncomment",
    action="store_true",
    help="Commented lines with suitable settings \
          will be uncommented",
)
parser.add_argument(
    "--no-backup",
    dest="backup",
    action="store_false",
    help="No backup file will be created",
)

args = parser.parse_args()

if args.config:
    config_file_path = os.path.expanduser(args.config)
else:
    config_file_path = os.path.expanduser(r"~/.config/kitty/kitty.conf")

config_directory, config_file_name = os.path.split(config_file_path)

if args.mapfile:
    with open(args.mapfile) as f:
        lines = f.readlines()
    line1 = lines[0].strip()
    line2 = lines[1].strip()
    map_dict = dict(zip(line1, line2))
else:
    map_dict = dict(
        zip(
            r"qwertyuiop[]\asdfghjkl;'zxcvbnm,./",
            r"йцукенгшщзхъ\фывапролджэячсмитьбю."
        )
    )

mac_os_keys = ["opt", "cmd"]

# read config file all lines
with open(config_file_path) as f:
    lines = f.readlines()
# for each line search mapping line and add additional line with mapping
new_lines = []
for line in lines:
    # if line doesn't contain map
    if "map " not in line:
        new_lines.append(line)
        continue
    # if line contains map but starts with #::
    if line.startswith("#:"):
        new_lines.append(line)
        continue
    # if line contains map for macos
    if args.skip_macos and any(key in line for key in mac_os_keys):
        new_lines.append(line)
        continue
    # line contains map the first thing is to find mapping parts
    line_parts = line.split(" ")
    map_part_index = line_parts.index("map")
    keys_part_index = map_part_index + 1
    keys_list = line_parts[keys_part_index].split("+")
    # for each key in keys list find mapping
    new_keys_list = []
    for key in keys_list:
        if key not in map_dict:
            new_keys_list.append(key)
            continue
        new_keys_list.append(map_dict[key])
    # create new line with new keys list
    new_keys_part = "+".join(new_keys_list)
    new_line = ""
    for i, part in enumerate(line_parts):
        if i == keys_part_index:
            new_line += new_keys_part
        else:
            new_line += part
        new_line += " "
    new_line = new_line[:-1]
    # remove comment from line and new line if it exists
    if args.uncomment and line.startswith("#"):
        line = line[1:].strip() + "\n"
        new_line = new_line[1:].strip() + "\n"
    # append initial line and a new one, if it is not fully equal
    new_lines.append(line)
    if line != new_line:
        new_lines.append(new_line)
# create backup
if args.backup:
    with open(os.path.join(
        config_directory, f"{config_file_name}.{time.time()}.backup"), "w"
    ) as f:
        f.writelines(new_lines)
# write new config file
with open(config_file_path, "w") as f:
    f.writelines(new_lines)
