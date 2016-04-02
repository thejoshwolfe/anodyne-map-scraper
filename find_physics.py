#!/usr/bin/python3

import re
import sys

#print("Paste the arg1.setTileProperties() calls now:")
text = sys.stdin.read()
simple_matches = re.findall(r'arg1\.setTileProperties\((\d+), (.*?)(?:, (.*?)(?:, (.*?)(?:, (.*?))?)?)?\)', text)
#print("\n".join(repr(x) for x in simple_matches));

physics = {0: " "}
for match in simple_matches:
  start = int(match[0])
  collision_flags = match[1]
  callback = match[2]
  entity_filter = match[3]
  run_length = int(match[4] or "1")

  if collision_flags == "org.flixel.FlxObject.NONE":
    char_code = " "
  elif collision_flags == "org.flixel.FlxObject.ANY":
    char_code = "#"
  else:
    print("WARNING: unknown collision_flags: {}".format(repr(collision_flags)))
    continue

  if callback in ("", "null"):
    pass
  elif callback in ("ladder",):
    assert(char_code == " ")
    char_code = "l"
  else:
    print("WARNING: unknown callback: {}".format(repr(callback)))
    continue

  for i in range(start, start + run_length):
    physics[i] = char_code

print('"{}"'.format("".join(physics.get(i, "#") for i in range(max(physics.keys())))))
