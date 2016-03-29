#!/usr/bin/python3
#
# www.josephlandry.com
#
# buildmap.py
#
# Builds map images from Anodyne game source files.
#
# Anodyne game: http://www.anodynegame.com/
#
# The source folder should be in ./Anodyne/src/
# The map images will be outputted to ./maps/ in PNG format.
#

import os
import csv
import simplepng
from collections import defaultdict
from xml import sax

def read_layer(filename):
  f = open(filename, "r")
  map_reader = csv.reader(f, delimiter=",")
  map = []
  for row in map_reader:
    map.append(row)
  f.close()
  return map


def read_tileset(filename):
  with open(filename, "rb") as f:
    return simplepng.read_png(f)

def paint_with_layer(image, layer, tileset):
  y_blocks = len(layer)
  x_blocks = len(layer[0])
  found_anything = False
  for y in range(y_blocks):
    for x in range(x_blocks):
      tile_index = int(layer[y][x])
      if tile_index == 0: continue
      found_anything = True
      tile_y = tile_index // (tileset.width // 16)
      tile_x = tile_index % (tileset.width // 16)
      image.paste(tileset, sx=tile_x*16, sy=tile_y*16, dx=x*16, dy=y*16, width=16, height=16)
  return found_anything


def generate_map_image(map):
  layer_images = [None, None, None, None]
  tileset = read_tileset(map["tileset"])
  width = None
  height = None
  for i, layerfile in enumerate(map["layers"]):
    layer = read_layer(layerfile)
    if width == None:
      width = len(layer[0]) * 16
      height = len(layer) * 16
    image = simplepng.ImageBuffer(width, height)
    if paint_with_layer(image, layer, tileset):
      if i == 2: i = 3 # leave space for the entities layer
      layer_images[i] = image
  return layer_images

class RegistryHandler(sax.ContentHandler):
  def __init__(self):
    super().__init__()
    self.current_map_name = ""
    self.objects_by_map_name = defaultdict(list)
  def startElement(self, name, attrs):
    if name == "root":
      pass
    elif name == "map":
      self.current_map_name = attrs["name"]
    else:
      self.objects_by_map_name[self.current_map_name].append({
        "name": name,
        "x": int(float(attrs["x"])),
        "y": int(float(attrs["y"])),
        "frame": attrs["frame"],
        "type": attrs.get("type", None),
      })
  def endElement(self, name):
    pass

def read_registry():
  parser = sax.make_parser()
  handler = RegistryHandler()
  parser.setContentHandler( handler )
  parser.parse( 'Anodyne/src/global/Registry_EmbedXML.dat')
  return handler.objects_by_map_name



mapfiles = [
  {
    "map_name": "APARTMENT",
    "tileset": "Anodyne/src/data/TileData__Apartment_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_APARTMENT_BG.dat", "Anodyne/src/data/CSV_Data_APARTMENT_BG2.dat", "Anodyne/src/data/CSV_Data_APARTMENT_FG.dat"]
  },
  {
    "map_name": "BEACH",
    "tileset": "Anodyne/src/data/TileData__Beach_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_BEACH_BG.dat"]
  },
  {
    "map_name": "BEDROOM",
    "tileset": "Anodyne/src/data/TileData__Bedroom_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_BEDROOM_BG.dat"]
  },
  {
    "map_name": "BLANK",
    "tileset": "Anodyne/src/data/TileData_Blank_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_BLANK_BG.dat"]
  },
  {
    "map_name": "BLUE",
    "tileset": "Anodyne/src/data/TileData_Blue_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_BLUE_BG.dat", "Anodyne/src/data/CSV_Data_BLUE_BG2.dat"]
  },
  {
    "map_name": "CELL",
    "tileset": "Anodyne/src/data/TileData_Cell_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_CELL_BG.dat"]
  },
  {
    "map_name": "CIRCUS",
    "tileset": "Anodyne/src/data/TileData__Circus_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_CIRCUS_BG.dat", "Anodyne/src/data/CSV_Data_CIRCUS_FG.dat"]
  },
  {
    "map_name": "CLIFF",
    "tileset": "Anodyne/src/data/TileData_Cliff_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_CLIFF_BG.dat", "Anodyne/src/data/CSV_Data_CLIFF_BG2.dat"]
  },
  {
    "map_name": "CROWD",
    "tileset": "Anodyne/src/data/TileData__Crowd_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_CROWD_BG.dat", "Anodyne/src/data/CSV_Data_CROWD_BG2.dat"]
  },
  {
    "map_name": "DEBUG",
    "tileset": "Anodyne/src/data/TileData_Debug_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_DEBUG_BG.dat", "Anodyne/src/data/CSV_Data_DEBUG_BG2.dat", "Anodyne/src/data/CSV_Data_DEBUG_FG.dat"]
  },
  {
    "map_name": "DRAWER",
    "tileset": "Anodyne/src/data/TileData_BlackWhite_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_DRAWER_BG.dat"]
  },
  {
    "map_name": "FIELDS",
    "tileset": "Anodyne/src/data/TileData__Fields_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_FIELDS_BG.dat", "Anodyne/src/data/CSV_Data_FIELDS_FG.dat"]
  },
  {
    "map_name": "FOREST",
    "tileset": "Anodyne/src/data/TileData_Forest_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_FOREST_BG.dat", "Anodyne/src/data/CSV_Data_FOREST_BG2.dat", "Anodyne/src/data/CSV_Data_FOREST_FG.dat"]
  },
  {
    "map_name": "GO",
    "tileset": "Anodyne/src/data/TileData_Go_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_GO_BG.dat", "Anodyne/src/data/CSV_Data_GO_BG2.dat"]
  },
  {
    "map_name": "HAPPY",
    "tileset": "Anodyne/src/data/TileData_Happy_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_HAPPY_BG.dat", "Anodyne/src/data/CSV_Data_HAPPY_BG2.dat"]
  },
  {
    "map_name": "HOTEL",
    "tileset": "Anodyne/src/data/TileData__Hotel_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_HOTEL_BG.dat", "Anodyne/src/data/CSV_Data_HOTEL_BG2.dat", "Anodyne/src/data/CSV_Data_HOTEL_FG.dat"]
  },
  {
    "map_name": "NEXUS",
    "tileset": "Anodyne/src/data/TileData__Nexus_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_NEXUS_BG.dat", "Anodyne/src/data/CSV_Data_NEXUS_FG.dat"]
  },
  {
    "map_name": "OVERWORLD",
    "tileset": "Anodyne/src/data/TileData__Overworld_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_OVERWORLD_BG.dat", "Anodyne/src/data/CSV_Data_OVERWORLD_BG2.dat"]
  },
  {
    "map_name": "REDCAVE",
    "tileset": "Anodyne/src/data/TileData_REDCAVE_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_REDCAVE_BG.dat", "Anodyne/src/data/CSV_Data_REDCAVE_BG2.dat"]
  },
  {
    "map_name": "REDSEA",
    "tileset": "Anodyne/src/data/TileData_Red_Sea_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_REDSEA_BG.dat", "Anodyne/src/data/CSV_Data_REDSEA_FG.dat"]
  },
  {
    "map_name": "SPACE",
    "tileset": "Anodyne/src/data/TileData_Space_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_SPACE_BG.dat", "Anodyne/src/data/CSV_Data_SPACE_BG2.dat", "Anodyne/src/data/CSV_Data_SPACE_FG.dat"]
  },
  {
    "map_name": "STREET",
    "tileset": "Anodyne/src/data/TileData__Street_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_STREET_BG.dat", "Anodyne/src/data/CSV_Data_STREET_BG2.dat", "Anodyne/src/data/CSV_Data_STREET_FG.dat"]
  },
  {
    "map_name": "SUBURB",
    "tileset": "Anodyne/src/data/TileData_Suburb_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_SUBURB_BG.dat"]
  },
  {
    "map_name": "TERMINAL",
    "tileset": "Anodyne/src/data/TileData_Terminal_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_TERMINAL_BG.dat", "Anodyne/src/data/CSV_Data_TERMINAL_BG2.dat"]
  },
  {
    "map_name": "WINDMILL",
    "tileset": "Anodyne/src/data/TileData__Windmill_Tiles.png",
    "layers": ["Anodyne/src/data/CSV_Data_WINDMILL_BG.dat", "Anodyne/src/data/CSV_Data_WINDMILL_BG2.dat"]
  }
]

entities = {
  "Treasure": { "image": "Anodyne/src/entity/gadget/Treasure_S_TREASURE_SPRITE.png", "tile_index": 1}
}

def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("map_name", nargs="*")
  parser.add_argument("-s", "--separate", action="store_true")
  args = parser.parse_args()

  # read registry XML file that contains entity information
  objects_by_map_name = read_registry()
  treasure_tiles = read_tileset("Anodyne/src/entity/gadget/Treasure_S_TREASURE_SPRITE.png");

  if not os.path.exists("maps"):
    os.makedirs("maps")

  warning_set = set()
  for mapfile in mapfiles:
    map_name = mapfile["map_name"]
    if args.map_name and map_name not in args.map_name:
      continue
    print("Processing: " + map_name)

    # build initial map image
    layers = generate_map_image(mapfile)
    # draw the supported entites on the maps
    for entity in objects_by_map_name[map_name]:
      entity_name = entity["name"]
      x = entity["x"]
      y = entity["y"]
      width = 16
      height = 16
      if entity_name == "Treasure":
        sprite = treasure_tiles
      else:
        if entity_name not in warning_set:
          print("WARNING: ignoring entity: {}".format(entity_name))
          warning_set.add(entity_name)
        continue
      if layers[2] == None:
        layers[2] = simplepng.ImageBuffer(layers[0].width, layers[0].height)
      layers[2].paste(sprite, sx=0, sy=0, dx=x, dy=y, width=width, height=height)

    # save images
    file_name_base = "maps/" + map_name
    if args.separate:
      for i, layer in enumerate(layers):
        if layer == None: continue
        with open("{}_{}.png".format(file_name_base, i), "wb") as f:
          simplepng.write_png(f, layer)
    else:
      # add everything to layer[0]
      for layer in layers[1:]:
        if layer == None: continue
        layers[0].paste(layer)
      with open(file_name_base + ".png", "wb") as f:
        simplepng.write_png(f, layers[0])

if __name__ == "__main__":
  main()
