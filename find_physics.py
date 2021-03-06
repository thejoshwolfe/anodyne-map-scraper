#!/usr/bin/python3

import re
import sys

map_name = sys.argv[1]

#print("Paste the arg1.setTileProperties() calls now:")
text = sys.stdin.read()
pattern = (
  # simple version
  r'arg1\.setTileProperties\((\d+), (.*?)(?:, (.*?)(?:, (.*?)(?:, (.*?))?)?)?\)' + '|' +
  # for loop version
  r'loc1 = (\d+);\s+' +
  r'while \(loc1 < (\d+)\)\s+\{\s+' +
    r'arg1\.setTileProperties\(loc1, (.*?)(?:, (.*?)(?:, (.*?))?)?\);\s+' +
    r'\+\+loc1;\s+' +
  r'}'
)
matches = re.findall(pattern, text)
sanity_matches = re.findall('setTileProperties', text)
if len(matches) != len(sanity_matches):
  sys.exit("ERROR: regex didn't match everything")
#print("\n".join(repr(x) for x in matches));

conveyer_data = {
  "REDCAVE": {16: ">", 17: "v", 18: "<", 19: "^", 20: "w", 26: "w", 28: "w"},
  "TERMINAL": " ",
  "GO": {130: "w", 194: "w"}, # default leave it alone
  "APARTMENT": {206: "w", 231: "w"}, # default leave it alone
  "FIELDS": {250: "w", 270: ">", 271: "v", 272: "<", 273: "^"},
  "BEACH": " ",
  "HOTEL": {180: ">", 181: "v", 182: "<", 183: "^", 131: "w"},
  "CIRCUS": {110: "w", 111: ">", 112: "v", 113: "<", 114: "^"},
  "FOREST": {110: "w", 134: ">", 135: "v", 136: "<", 137: "^"},
  "WINDMILL": " ",
}
conveyer_data["DEBUG"] = conveyer_data["REDCAVE"]

conveyer_overrides = conveyer_data.get(map_name, {})

physics = {0: " "}
for match in matches:
  if match[0] != "":
    # simple version
    start = int(match[0])
    collision_flags = match[1]
    callback = match[2]
    entity_filter = match[3]
    end = start + int(match[4] or "1")
  else:
    # for loop version
    start = int(match[5])
    end = int(match[6])
    collision_flags = match[7]
    callback = match[8]
    entity_filter = match[9]

  if collision_flags == "org.flixel.FlxObject.NONE":
    char_code = " "
  elif collision_flags == "org.flixel.FlxObject.ANY":
    char_code = "#"
  elif collision_flags == "org.flixel.FlxObject.LEFT":
    char_code = "5"
  elif collision_flags == "org.flixel.FlxObject.UP":
    char_code = "6"
  elif collision_flags == "org.flixel.FlxObject.RIGHT":
    char_code = "7"
  elif collision_flags == "org.flixel.FlxObject.DOWN":
    char_code = "8"
  else:
    print("WARNING: unknown collision_flags: {}".format(repr(collision_flags)))
    continue

  if callback in ("", "null"):
    pass
  elif callback == "ladder":
    assert(char_code == " ")
    char_code = "l"
  elif callback == "data.TileData.slow":
    assert(char_code == " ")
    char_code = ","
  elif callback in ("hole", "data.TileData.hole"):
    assert(char_code == " ")
    char_code = "h"
  elif callback == "data.TileData.thin_left":
    assert(char_code == " ")
    char_code = "1"
  elif callback == "data.TileData.thin_up":
    assert(char_code == " ")
    char_code = "2"
  elif callback == "data.TileData.thin_right":
    assert(char_code == " ")
    char_code = "3"
  elif callback == "data.TileData.thin_down":
    assert(char_code == " ")
    char_code = "4"
  elif callback in ("data.TileData.conveyer", "conveyer"):
    assert(char_code == " ")
    if conveyer_overrides != " ":
      char_code = "w"
  elif callback in ("data.TileData.spike", "spike"):
    assert(char_code == " ")
    if map_name == "REDCAVE" and start == 31:
      # not it's not. it's jut air.
      char_code = " "
    else:
      char_code = "s"
  else:
    print("WARNING: unknown callback: {}".format(repr(callback)))
    continue

  if entity_filter not in ("", "null", "entity.player.Player"):
    print("WARNING: unknown entity_filter: {}".format(repr(entity_filter)))

  for i in range(start, end):
    physics[i] = char_code

# these override everything else
if conveyer_overrides != " ":
  for tile_index, char_code in conveyer_overrides.items():
    if physics.get(tile_index, "w") != "w": continue
    physics[tile_index] = char_code

print('"{}"'.format("".join(physics.get(i, "#") for i in range(max(physics.keys()) + 1))))
