#!/usr/bin/python3

import subprocess
import re

src_dir = "Anodyne/src/"

png_file_names = subprocess.check_output(["find", src_dir, "-name", "*.png"]).decode("utf8").strip().split("\n")

with open(src_dir + "helper/SpriteFactory.as") as f:
  sprite_factory_source = f.read()

if_regex = re.compile(r'if \(loc6 == "(.+?)"')
constructor_regex = re.compile(r' = new (entity\..+?)\(')

if_match = if_regex.search(sprite_factory_source)
index = if_match.start() + 1
while True:
  name = if_match.group(1)
  if_match = if_regex.search(sprite_factory_source, index)
  if if_match == None:
    break
  constructor_match = constructor_regex.search(sprite_factory_source, index, if_match.start())
  if constructor_match != None:
    class_name = constructor_match.group(1)
    # find likely images
    likely_images = [x for x in png_file_names if x.startswith(src_dir + class_name.replace(".", "/"))]
    if len(likely_images) == 1:
      print('  "{}": "{}",'.format(name, likely_images[0]))
    elif len(likely_images) == 0:
      print('  "{}": "???",'.format(name))
    else:
      print('  "{}": [\n{}  ],'.format(name, "".join('    "{}",\n'.format(x) for x in likely_images)))
  index = if_match.start() + 1
