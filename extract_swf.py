#!/usr/bin/env python3

import os
import subprocess
import shutil
import re

tmp_dir = ".tmp"

def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("ffdec", metavar="ffdec.exe", help="the ffdec executable")
  parser.add_argument("swf", metavar="Anodyne.swf")
  parser.add_argument("-f", "--force", action="store_true")
  parser.add_argument("-o", "--output", default="Anodyne_1.509")
  args = parser.parse_args()

  if args.force or not os.path.isdir(tmp_dir):
    if os.path.isdir(tmp_dir):
      shutil.rmtree(tmp_dir)
    subprocess.check_call(["progress", args.ffdec, "-export", "all", tmp_dir, args.swf])

  if args.force and os.path.exists(args.output):
    shutil.rmtree(args.output)

  if args.force or not os.path.exists(args.output):
    os.rename(os.path.join(tmp_dir, "scripts"), args.output)

  for dir in os.listdir(tmp_dir):
    if dir in ("sprites", "texts", "frames", "shapes"):
      shutil.rmtree(os.path.join(tmp_dir, dir))
      continue
    for file in os.listdir(os.path.join(tmp_dir, dir)):
      if file in ("154.png", "177.mp3", "158.mp3"):
        os.remove(os.path.join(tmp_dir, dir, file))
        continue
      prefix_part, name = file.split("_", 1)
      assert([c for c in prefix_part if c not in "01234596789"] == [])
      # undo "/" -> "." transformation, but don't replace too many "."s.
      name, ext = name.rsplit(".", 1)
      name_start = re.search("[^.a-z]", name).start()
      name = name[:name_start].replace(".", "/") + name[name_start:]
      name = name + "." + ext
      os.rename(os.path.join(tmp_dir, dir, file), os.path.join(args.output, name))
    os.rmdir(os.path.join(tmp_dir, dir))
  os.rmdir(tmp_dir)

if __name__ == "__main__":
  main()
