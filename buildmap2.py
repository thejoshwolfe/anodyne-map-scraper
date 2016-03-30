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
import itertools
from xml import sax

def read_layer(filename):
  f = open(filename, "r")
  map_reader = csv.reader(f, delimiter=",")
  map = []
  for row in map_reader:
    map.append(row)
  f.close()
  return map


def read_tileset(filename, fade=False):
  with open(filename, "rb") as f:
    image = simplepng.read_png(f)
  if fade:
    # apply semitransparency by clearing the msb of the alpha channel
    for i in range(len(image.data)):
      image.data[i] &= 0xffffff7f
  return image

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
      if self.current_map_name == "TRAIN":
        # for some reason the entities for CELL are filed under TRAIN
        self.current_map_name = "CELL"
    else:
      self.objects_by_map_name[self.current_map_name].append({
        "name": name,
        "x": int(float(attrs["x"])),
        "y": int(float(attrs["y"])),
        "frame": int(attrs["frame"]),
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

sprite_paths = {
  "Slime": "Anodyne/src/entity/enemy/bedroom/Slime_Slime_Sprite.png",
  "SinglePushBlock": "Anodyne/src/entity/gadget/SinglePushBlock_C_PUSH_BLOCKS.png",
  "Door": [
    "Anodyne/src/entity/gadget/Door_embed_nexus_cardgem.png",
    "Anodyne/src/entity/gadget/Door_Nexus_door_overlay_embed.png",
    "Anodyne/src/entity/gadget/Door_Sprite_nexus_door.png",
    "Anodyne/src/entity/gadget/Door_Door_Sprites.png",
    "Anodyne/src/entity/gadget/Door_Nexus_door_previews_embed.png",
  ],
  "Wall_Laser": "???",
  "Eye_Light": "Anodyne/src/entity/decoration/Eye_Light_Eye_Light_Sprite.png",
  "Mover": "Anodyne/src/entity/enemy/redcave/Mover_mover_sprite.png",
  "KeyBlock": "Anodyne/src/entity/gadget/KeyBlock_C_KEYBLOCK_SPRITE.png",
  "Hole": "Anodyne/src/entity/gadget/Hole_C_HOLE_SPRITE.png",
  "Gate": "Anodyne/src/entity/gadget/Gate_C_GATE_SPRITES.png",
  "Treasure": "Anodyne/src/entity/gadget/Treasure_S_TREASURE_SPRITE.png",
  "CrackedTile": "Anodyne/src/entity/gadget/CrackedTile_C_CRACKED_TILES.png",
  "Button": "Anodyne/src/entity/gadget/Button_S_BUTTON.png",
  "Sun_Guy": "Anodyne/src/entity/enemy/bedroom/Sun_Guy_C_SUN_GUY.png",
  "Dust": "Anodyne/src/entity/gadget/Dust_DUST_SPRITE.png",
  "Shieldy": "Anodyne/src/entity/enemy/bedroom/Shieldy_SPRITE_SHIELDY.png",
  "Pew_Laser": "Anodyne/src/entity/enemy/bedroom/Pew_Laser_PEW_LASER.png",
  "Annoyer": "Anodyne/src/entity/enemy/bedroom/Annoyer_S_ANNOYER_SPRITE.png",
  "Console": "Anodyne/src/entity/gadget/Console_sprite_console.png",
  "Follower_Bro": "Anodyne/src/entity/enemy/etc/Follower_Bro_sprite_follower.png",
  "Sadbro": "Anodyne/src/entity/enemy/etc/Sadbro_sadman_sprite.png",
  "Red_Walker": "Anodyne/src/entity/enemy/etc/Red_Walker_sprite_redwalker.png",
  "Four_Shooter": "Anodyne/src/entity/enemy/redcave/Four_Shooter_four_shooter_sprite.png",
  "Slasher": "Anodyne/src/entity/enemy/redcave/Slasher_slasher_sprite.png",
  "On_Off_Laser": "Anodyne/src/entity/enemy/redcave/On_Off_Laser_on_off_shooter_sprite.png",
  "Red_Pillar": [
    "Anodyne/src/entity/interactive/Red_Pillar_red_pillar_ripple_sprite.png",
    "Anodyne/src/entity/interactive/Red_Pillar_red_pillar_sprite.png",
  ],
  "Solid_Sprite": [
    "Anodyne/src/entity/decoration/Solid_Sprite_red_cave_left_sprite.png",
    "Anodyne/src/entity/decoration/Solid_Sprite_trees_sprites.png",
  ],
  "Big_Door": "Anodyne/src/entity/gadget/Big_Door_big_door_sprite.png",
  "Fisherman": "???",
  "Jump_Trigger": "Anodyne/src/entity/gadget/Jump_Trigger_spring_pad_sprite.png",
  "NPC": [
    "Anodyne/src/entity/interactive/NPC_key_sparkle_embed.png",
    "Anodyne/src/entity/interactive/NPC_embed_trade_npcs.png",
    "Anodyne/src/entity/interactive/NPC_embed_hotel_npcs.png",
    "Anodyne/src/entity/interactive/NPC_embed_cube_kings.png",
    "Anodyne/src/entity/interactive/NPC_embed_cell_bodies.png",
    "Anodyne/src/entity/interactive/NPC_embed_geoms.png",
    "Anodyne/src/entity/interactive/NPC_embed_nexus_pad.png",
    "Anodyne/src/entity/interactive/NPC_embed_windmill_blade.png",
    "Anodyne/src/entity/interactive/NPC_embed_randoms.png",
    "Anodyne/src/entity/interactive/NPC_note_rock.png",
    "Anodyne/src/entity/interactive/NPC_embed_smoke_red.png",
    "Anodyne/src/entity/interactive/NPC_npc_spritesheet.png",
  ],
  "Red_Boss": [
    "Anodyne/src/entity/enemy/redcave/Red_Boss_red_boss_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Red_Boss_ripple_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Red_Boss_big_wave_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Red_Boss_bullet_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Red_Boss_tentacle_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Red_Boss_red_boss_alternate_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Red_Boss_small_wave_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Red_Boss_warning_sprite.png",
  ],
  "Propelled": "Anodyne/src/entity/gadget/Propelled_moving_platform_sprite.png",
  "Stop_Marker": "???",
  "Person": "Anodyne/src/entity/enemy/crowd/Person_person_sprite.png",
  "Rotator": "Anodyne/src/entity/enemy/crowd/Rotator_rotator_sprite.png",
  "Frog": "Anodyne/src/entity/enemy/crowd/Frog_frog_sprite.png",
  "Dog": "Anodyne/src/entity/enemy/crowd/Dog_dog_sprite.png",
  "WallBoss": [
    "Anodyne/src/entity/enemy/crowd/WallBoss_wall_sprite.png",
    "Anodyne/src/entity/enemy/crowd/WallBoss_bullet_sprite.png",
    "Anodyne/src/entity/enemy/crowd/WallBoss_l_hand_sprite.png",
    "Anodyne/src/entity/enemy/crowd/WallBoss_r_hand_sprite.png",
    "Anodyne/src/entity/enemy/crowd/WallBoss_face_sprite.png",
    "Anodyne/src/entity/enemy/crowd/WallBoss_laser_sprite.png",
  ],
  "Pillar_Switch": "Anodyne/src/entity/gadget/Pillar_Switch_pillar_switch_sprite.png",
  "Switch_Pillar": "Anodyne/src/entity/gadget/Switch_Pillar_switch_pillar_sprite.png",
  "Silverfish": "Anodyne/src/entity/enemy/apartment/Silverfish_silverfish_sprite.png",
  "Rat": "Anodyne/src/entity/enemy/apartment/Rat_rat_sprite.png",
  "Teleguy": "Anodyne/src/entity/enemy/apartment/Teleguy_teleguy_sprite.png",
  "Dash_Trap": "Anodyne/src/entity/enemy/apartment/Dash_Trap_dash_trap_sprite.png",
  "Gasguy": "Anodyne/src/entity/enemy/apartment/Gasguy_gas_guy_sprite.png",
  "Terminal_Gate": "???",
  "Dustmaid": "Anodyne/src/entity/enemy/hotel/Dustmaid_dustmaid_sprite.png",
  "Splitboss": "Anodyne/src/entity/enemy/apartment/Splitboss_splitboss_sprite.png",
  "Nonsolid": [
    "Anodyne/src/entity/decoration/Nonsolid_grass_REDSEA_sprite.png",
    "Anodyne/src/entity/decoration/Nonsolid_rail_sprite.png",
    "Anodyne/src/entity/decoration/Nonsolid_rail_CROWD_sprite.png",
    "Anodyne/src/entity/decoration/Nonsolid_rail_NEXUS_sprite.png",
    "Anodyne/src/entity/decoration/Nonsolid_grass_1_sprite.png",
  ],
  "Steam_Pipe": "Anodyne/src/entity/enemy/hotel/Steam_Pipe_steam_pipe_sprite.png",
  "Burst_Plant": "Anodyne/src/entity/enemy/hotel/Burst_Plant_burst_plant_sprite.png",
  "Dash_Pad": "Anodyne/src/entity/gadget/Dash_Pad_dash_pad_sprite.png",
  "Elevator": "Anodyne/src/entity/interactive/Elevator_Elevator_Sprite.png",
  "Eye_Boss": [
    "Anodyne/src/entity/enemy/hotel/Eye_Boss_eye_boss_water_sprite.png",
    "Anodyne/src/entity/enemy/hotel/Eye_Boss_eye_boss_bullet_sprite.png",
    "Anodyne/src/entity/enemy/hotel/Eye_Boss_eye_boss_splash_sprite.png",
  ],
  "HealthPickup": [
    "Anodyne/src/entity/player/HealthPickup_embed_Big_health.png",
    "Anodyne/src/entity/player/HealthPickup_S_SMALL_HEALTH.png",
  ],
  "Contort": "Anodyne/src/entity/enemy/circus/Contort_contort_big_sprite.png",
  "Lion": "Anodyne/src/entity/enemy/circus/Lion_lion_sprite.png",
  "Fire_Pillar": "Anodyne/src/entity/enemy/circus/Fire_Pillar_fire_pillar_base_sprite.png",
  "Sage": "Anodyne/src/entity/interactive/npc/Sage_sage_sprite.png",
  "Mitra": "Anodyne/src/entity/interactive/npc/Mitra_mitra_sprite.png",
  #"Mitra": [
  #  "Anodyne/src/entity/interactive/npc/Mitra_mitra_sprite.png",
  #  "Anodyne/src/entity/interactive/npc/Mitra_bike_sprite.png",
  #  "Anodyne/src/entity/interactive/npc/Mitra_mitra_on_bike_sprite.png",
  #],
  "Health_Cicada": "Anodyne/src/entity/interactive/Health_Cicada_health_cicada_embed.png",
  "Dungeon_Statue": "Anodyne/src/entity/interactive/Dungeon_Statue_statue_bedroom_embed.png",
  "Chaser": "Anodyne/src/entity/enemy/etc/Chaser_embed_chaser_sprite.png",
  "Space_Face": "???",
  "Go_Detector": "???",
  "Sage_Boss": [
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_sage_attacks.png",
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_long_dust.png",
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_sage_boss.png",
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_sage_long_attacks.png",
  ],
  "Shadow_Briar": "Anodyne/src/entity/interactive/npc/Shadow_Briar_embed_briar.png",
  "Trade_NPC": "Anodyne/src/entity/interactive/npc/Trade_NPC_embed_dame_trade_npc.png",
  "Forest_NPC": "Anodyne/src/entity/interactive/npc/Forest_NPC_embed_forest_npcs.png",
  "Redsea_NPC": "Anodyne/src/entity/interactive/npc/Redsea_NPC_embed_redsea_npcs.png",
  "Happy_NPC": "Anodyne/src/entity/interactive/npc/Happy_NPC_embed_happy_npcs.png",
  "Space_NPC": "Anodyne/src/entity/interactive/npc/Space_NPC_embed_space_npc.png",
  "Huge_Fucking_Stag": "Anodyne/src/entity/interactive/npc/Huge_Fucking_Stag_embed_stag.png",
  "Black_Thing": "???",
  "Suburb_Walker": [
    "Anodyne/src/entity/enemy/suburb/Suburb_Walker_embed_suburb_walker.png",
    "Anodyne/src/entity/enemy/suburb/Suburb_Walker_embed_suburb_folk.png",
    "Anodyne/src/entity/enemy/suburb/Suburb_Walker_embed_suburb_killer.png",
  ],
}
sprites = {}
def load_sprites():
  for sprite_name in sprite_paths:
    if type(sprite_paths[sprite_name]) == str and sprite_paths[sprite_name] != "???":
      sprites[sprite_name] = read_tileset(sprite_paths[sprite_name])
  sprites["nonsolid_rail_sprite"] = read_tileset("Anodyne/src/entity/decoration/Nonsolid_rail_sprite.png")
  sprites["nonsolid_rail_crowd"] = read_tileset("Anodyne/src/entity/decoration/Nonsolid_rail_CROWD_sprite.png")
  sprites["npc_cell_bodies"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_cell_bodies.png")
  sprites["npc_rock"] = read_tileset("Anodyne/src/entity/interactive/NPC_note_rock.png")
  sprites["door_portal"] = read_tileset("Anodyne/src/entity/gadget/Door_White_Portal_Sprite.png")
  sprites["nexus_pad"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_nexus_pad.png")
  sprites["beach_npcs"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_beach_npcs.png")
  sprites["whirlpool"] = read_tileset("Anodyne/src/entity/gadget/Door_Whirlpool_Door_Sprite.png")
  sprites["npc_sage_statue"] = read_tileset("Anodyne/src/entity/interactive/NPC_sage_statue.png")
  sprites["big_key"] = read_tileset("Anodyne/src/entity/interactive/NPC_key_green_embed.png")
  sprites["windmill_console"] = read_tileset("Anodyne/src/entity/gadget/Console_embed_windmill_inside.png")
  sprites["windmill_shell"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_windmill_shell.png")
  sprites["big_gate"] = read_tileset("Anodyne/src/entity/gadget/KeyBlock_green_gate_embed.png")
  sprites["checkpoint"] = read_tileset("Anodyne/src/entity/gadget/Checkpoint_checkpoint_sprite.png")
  sprites["Spike_Roller_V"] = read_tileset("Anodyne/src/entity/enemy/crowd/Spike_Roller_Spike_Roller_Sprite.png")
  sprites["Spike_Roller_H"] = read_tileset("Anodyne/src/entity/enemy/crowd/Spike_Roller_Spike_Roller_Sprite_H.png")
  sprites["Spike_Roller_V_S"] = read_tileset("Anodyne/src/entity/enemy/crowd/Spike_Roller_vert_shadow_sprite.png", fade=True)
  sprites["Spike_Roller_H_S"] = read_tileset("Anodyne/src/entity/enemy/crowd/Spike_Roller_hori_shadow_sprite.png", fade=True)
  sprites["npc_snowman"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_blue_npcs.png")
  sprites["circus_folks_arthur"] = read_tileset("Anodyne/src/entity/enemy/circus/Circus_Folks_arthur_sprite.png")
  sprites["circus_folks_javiera"] = read_tileset("Anodyne/src/entity/enemy/circus/Circus_Folks_javiera_sprite.png")
  sprites["circus_folks_both"] = read_tileset("Anodyne/src/entity/enemy/circus/Circus_Folks_both_sprite.png")
  sprites["npc_golem"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_cliff_npcs.png")
  sprites["biofilm"] = read_tileset("Anodyne/src/entity/interactive/NPC_npc_biofilm.png")
  sprites["wall_boss_wall"] = read_tileset("Anodyne/src/entity/enemy/crowd/WallBoss_wall_sprite.png")
  sprites["wall_boss_mouth"] = read_tileset("Anodyne/src/entity/enemy/crowd/WallBoss_face_sprite.png")
  sprites["wall_boss_hand"] = read_tileset("Anodyne/src/entity/enemy/crowd/WallBoss_l_hand_sprite.png")

warning_set = set()
def render_entities(image, entities, map_name):
  did_anything = False

  # get all the Dust first, since it can go away to fule a Propelled
  dust_entities  = [entity for entity in entities if entity["name"] == "Dust"]
  other_entities = [entity for entity in entities if entity["name"] != "Dust"]

  def consume_dust_at(x, y):
    for i, dust in enumerate(dust_entities):
      if dust["x"] == x and dust["y"] == y:
        del dust_entities[i]
        return True
    return False

  # chain lets us delete from dust_entities and then not iterate over them
  for entity in itertools.chain(other_entities, dust_entities):
    entity_name = entity["name"]
    x = entity["x"]
    y = entity["y"]
    if x < 0 or y < 0:
      print("WARNING: ignoring out of bounds entity: {}, {}".format(x, y))
      continue
    frame = entity["frame"]
    sx = 0
    sy = 0
    width = 16
    height = 16
    sprite = sprites.get(entity_name, None)
    sprite2 = None
    is_boi = map_name == "REDCAVE" and y > 1000
    if entity_name == "Switch_Pillar":
      sx = frame * 16
    elif entity_name == "Silverfish":
      sy = 16
      if frame == 0: # left
        sx = 32
        sy = 16
        # TODO: horizontal flip
      elif frame == 1: # down
        sy = 16
      elif frame == 2: # right
        sx = 32
        sy = 16
      elif frame == 3: # up
        sy = 32
      else:
        print("WARNING: what Silverfish direction is this: {}".format(frame))
    elif entity_name in ("Pew_Laser", "Steam_Pipe"):
      sx = (frame & 3) * 16
    elif entity_name == "On_Off_Laser":
      if frame == 0:
        sy = 16 # up
      elif frame == 1:
        pass # right
        # TODO: rotate left
      elif frame == 2:
        pass # down
      elif frame == 3:
        pass # left
        # TODO: rotate right
      else:
        print("WARNING: what On_Off_Laser direction is this: {}".format(frame))
    elif entity_name == "Dash_Trap":
      sy = 16
      if is_boi:
        sx = 32
    elif entity_name in ("Gasguy", "Teleguy", "Sun_Guy", "Dustmaid"):
      height = 24
    elif entity_name == "Slasher":
      width = 24
      height = 24
    elif entity_name == "Splitboss":
      width = 24
      height = 32
    elif entity_name == "Contort":
      height = 32
    elif entity_name == "Lion":
      width = 32
      height = 32
    elif entity_name == "Red_Walker":
      width = 32
      height = 48
    elif entity_name == "Huge_Fucking_Stag":
      width = 64
      height = 80
    elif entity_name == "Fire_Pillar":
      y += 16
    elif entity_name == "Redsea_NPC":
      sy = frame * 16 // 10
    elif entity_name == "Circus_Folks":
      if frame == 0:
        # arthur
        sprite = sprites["circus_folks_arthur"]
        y -= 7 * 16
        sy = 64
      elif frame == 1:
        # javiera
        sprite = sprites["circus_folks_javiera"]
      elif frame == 2:
        # both?
        sprite = sprites["circus_folks_both"]
        y -= 64
        height = 32
      else: unreachable()
    elif entity_name == "KeyBlock":
      if frame == 0:
        pass # small key block
      elif frame in (1, 2, 3):
        # large key gate
        sprite = sprites["big_gate"]
        width = 32
        if frame == 1:
          sy = 7 * 16
        elif frame == 2:
          sy = 0
        elif frame == 3:
          sy = 6 * 16
      elif frame == 4:
        # card gate
        sprite = sprites["big_gate"]
        width = 32
        if map_name == "OVERWORLD":
          sy = 8 * 16
        elif map_name == "BEACH":
          sy = 9 * 16
        elif map_name == "SUBURB":
          sy = 10 * 16
        elif map_name == "CELL":
          sy = 13 * 16
        elif map_name == "TERMINAL":
          sy = 14 * 16
        elif map_name == "NEXUS":
          sy = 15 * 16
        elif map_name == "BLANK":
          # there are 2 here
          if y == 864:
            sy = 11 * 16
          else:
            sy = 16 * 16
        else:
          print("WARNING: ignoring card gate in map: {}".format(map_name))
          continue
      else:
        print("WARNING: ignoring KeyBlock frame: {}".format(frame))
        continue
    elif entity_name == "Nonsolid":
      nonsolid_type = entity["type"]
      if nonsolid_type == "Rail_1":
        sprite = sprites["nonsolid_rail_sprite"]
      elif nonsolid_type == "Rail_CROWD":
        sprite = sprites["nonsolid_rail_crowd"]
      else:
        print("WARNING: what nonsolid type is this: {}".format(nonsolid_type))
    elif entity_name == "Jump_Trigger":
      if map_name in ("APARTMENT", "CLIFF", "BEACH", "CROWD"):
        # jump triggers are invisible in these maps
        continue
      elif map_name == "HOTEL":
        if entity["type"] != "1":
          # only type=1 is visible
          continue
    elif entity_name == "Gate":
      if map_name == "BLANK":
        sy = 32
    elif entity_name == "Console":
      if map_name == "WINDMILL":
        sprite = sprites["windmill_console"]
        sprite2 = sprites["windmill_shell"]
        width = 48
        height = 48
    elif entity_name == "Propelled":
      if (frame & 1) == 0:
        sy = 16
      if consume_dust_at(x, y):
        sx = 16
    elif entity_name == "Shadow_Briar":
      sy = 32
      if frame in (0, 2, 3, 4):
        pass # face down
      elif frame == 1:
        sx = 64 # face up
      else:
        print("WARNING: ignoring Shadow_Briar frame: {}".format(frame))
        continue
    elif entity_name == "Chaser":
      height = 32
      sy = 32
      if frame == 0:
        sx = 32
    elif entity_name == "Treasure":
      if map_name == "CELL":
        sy = 32
    elif entity_name == "Rat":
      if map_name == "CELL":
        sy = 16
    elif entity_name == "Dash_Pad":
      sy = 16
      sx = frame * 16
    elif entity_name == "Spike_Roller":
      if frame in (0, 3):
        sprite = sprites["Spike_Roller_H_S"]
        width = 128
      elif frame in (1, 2):
        sprite = sprites["Spike_Roller_V_S"]
        height = 128
      elif frame in (4, 7):
        sprite = sprites["Spike_Roller_H"]
        width = 128
      elif frame in (5, 6):
        sprite = sprites["Spike_Roller_V"]
        height = 128
      else:
        print("WARNING: ignoring Spike_Roller frame: {}".format(frame))
        continue
    elif entity_name == "Button":
      if map_name == "REDCAVE":
        sy = 32
      elif map_name == "CELL":
        sy = 64
      else:
        sy = 16
    elif entity_name in ("Hole", "CrackedTile"):
      if map_name == "BEDROOM":
        pass
      elif map_name == "REDCAVE":
        sx = 32
      elif map_name == "CIRCUS":
        sx = 32
        sy = 16
      else:
        print("WARNING: ignoring {} in map: {}".format(entity_name, map_name))
        continue
    elif entity_name == "Dungeon_Statue":
      width = 32
      height = 48
      if map_name == "BEDROOM":
        pass
      elif map_name == "REDCAVE":
        sx = 32
      elif map_name == "CROWD":
        sx = 64
      else: unreachable()
    elif entity_name == "NPC":
      npc_type = entity["type"]
      if npc_type == "Cell_Body":
        sprite = sprites["npc_cell_bodies"]
        if frame == 0:
          pass
        elif frame == 2:
          sx = 32
        elif frame == 4:
          sy = 16
        elif frame == 6:
          sx = 32
          sy = 16
        else:
          print("WARNING: ignoring npc cell body frame: {}".format(frame))
          continue
      elif npc_type == "rock":
        sprite = sprites["npc_rock"]
        if map_name == "CELL":
          sx = 16
      elif npc_type == "statue":
        sprite = sprites["npc_sage_statue"]
      elif npc_type == "big_key":
        sprite = sprites["big_key"]
        if map_name == "BEDROOM":
          sy = 0
        elif map_name == "REDCAVE":
          sy = 16
        elif map_name == "CROWD":
          sy = 32
        else: unreachable()
      elif npc_type == "generic":
        if map_name == "BEACH":
          if frame == 7:
            # Hews the lobster
            sprite = sprites["beach_npcs"]
          elif frame == 16:
            sprite = sprites["Trade_NPC"]
            sx = 96
            sy = 128
        elif map_name == "WINDMILL":
          # don't bother rendering the windmill blades
          continue
        elif map_name == "BLUE":
          sprite = sprites["npc_snowman"]
        elif map_name == "HAPPY":
          # invisible NPC that talks to you at the save point
          continue
        elif map_name == "CELL":
          sprite = sprites["npc_cell_bodies"]
          sy = 32
        elif map_name == "CLIFF":
          if frame == 7:
            sprite = sprites["npc_golem"]
          elif frame == 6:
            sprite = sprites["Dog"]
          else: unreachable()
        else:
          print("WARNING: ignoring generic npc in map: {}".format(map_name))
          continue
      elif npc_type == "biofilm":
        sprite = sprites["biofilm"]
        width = 32
        height = 32
      else:
        print("WARNING: ignoring npc type: {}".format(npc_type))
        continue
    elif entity_name == "Happy_NPC":
      if frame == 18:
        continue # briar walking along a trough thing
      if frame in (0,1,3):
        sy = 16 # male
    elif entity_name == "Fisherman":
      sprite = sprites["beach_npcs"]
      sy = 16
    elif entity_name == "Person":
      # there's information to rotate the persons,
      # but they rotate themselves randomly before you can see it in game,
      # so whatever
      pass
    elif entity_name == "Health_Cicada":
      if map_name == "CELL":
        sy = 32
    elif entity_name == "Annoyer":
      if map_name == "CELL":
        sy = 16
      elif frame == 0:
        sy = 0
      elif frame == 2:
        sy = 32
      elif frame == 8:
        sx = 32
        sy = 16
    elif entity_name == "Slime":
      if is_boi:
        sx = 32
    elif entity_name == "Frog":
      if is_boi:
        sy = 32
    elif entity_name == "Door":
      door_type = entity["type"]
      if door_type in ("1", "5", "6", "8", "9", "10", "11", "12", "14", "15"):
        continue # invisible
      elif door_type == "4":
        sprite = sprites["door_portal"]
        if map_name == "CELL":
          sy = 16
      elif door_type == "7":
        sprite = sprites["whirlpool"]
      elif door_type == "16":
        sprite = sprites["nexus_pad"]
        width = 32
        height = 32
        if map_name == "CELL":
          sy = 32
      else:
        print("WARNING: ignoring door type: {}".format(door_type))
        continue
    elif entity_name in ("solid_tile", "Water_Anim"):
      continue # invisible
    elif entity_name == "Solid_Sprite":
      solid_type = entity["type"]
      if solid_type in ("blocker", "vblock"):
        continue # invisible
      else:
        print("WARNING: ignoring Solid_Sprite type: {}".format(solid_type))
        continue
    elif entity_name in (
        "Pillar_Switch", "Dog", "Shieldy", "Rotator", "Dust",
        "Burst_Plant", "Four_Shooter", "Eye_Light",
      ):
      pass # simple
    elif entity_name == "Stop_Marker":
      continue # invisible
    elif entity_name == "Event":
      if frame == 2:
        sprite = sprites["checkpoint"]
        if map_name == "CELL":
          sy = 16
      else:
        continue # invisible
    elif entity_name in sprites:
      if entity_name not in warning_set:
        warning_set.add(entity_name)
        print("default rendering sprite: {}".format(entity_name))

    if entity_name == "WallBoss":
      # special case for all these sprites
      image.paste(sprites["wall_boss_wall"], dx=1440, dy=960, width=160, height=32)
      image.paste(sprites["wall_boss_mouth"], sx=16, dx=1504, dy=960, width=32, height=32)
      image.paste(sprites["wall_boss_hand"], dx=1456, dy=992, width=32, height=32)
      # TODO: horizontal flip
      image.paste(sprites["wall_boss_hand"], dx=1552, dy=992, width=32, height=32)
      did_anything = True
    elif sprite != None:
      image.paste(sprite, sx=sx, sy=sy, dx=x, dy=y, width=width, height=height)
      did_anything = True
      if sprite2 != None:
        image.paste(sprite2, sx=sx, sy=sy, dx=x, dy=y, width=width, height=height)
    else:
      if entity_name not in warning_set:
        warning_set.add(entity_name)
        print("WARNING: ignoring entity: {}".format(entity_name))
  return did_anything

def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("map_name", nargs="*")
  parser.add_argument("-s", "--separate", action="store_true")
  args = parser.parse_args()

  # read registry XML file that contains entity information
  objects_by_map_name = read_registry()
  load_sprites()

  if not os.path.exists("maps"):
    os.makedirs("maps")

  for mapfile in mapfiles:
    map_name = mapfile["map_name"]
    if args.map_name and map_name not in args.map_name:
      continue
    print("Processing: " + map_name)

    # build initial map image
    layers = generate_map_image(mapfile)
    # draw the supported entities on the maps
    entity_layer = simplepng.ImageBuffer(layers[0].width, layers[0].height)
    if render_entities(entity_layer, objects_by_map_name[map_name], map_name):
      layers[2] = entity_layer

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
