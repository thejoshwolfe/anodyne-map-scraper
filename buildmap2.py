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
    "Anodyne/src/entity/gadget/Door_White_Portal_Sprite.png",
    "Anodyne/src/entity/gadget/Door_Door_Sprites.png",
    "Anodyne/src/entity/gadget/Door_Nexus_door_previews_embed.png",
    "Anodyne/src/entity/gadget/Door_Whirlpool_Door_Sprite.png",
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
  "Sun_Guy": [
    "Anodyne/src/entity/enemy/bedroom/Sun_Guy_C_SUN_GUY.png",
    "Anodyne/src/entity/enemy/bedroom/Sun_Guy_C_SUN_GUY_WAVE.png",
    "Anodyne/src/entity/enemy/bedroom/Sun_Guy_C_LIGHT_ORB.png",
  ],
  "Dust": "Anodyne/src/entity/gadget/Dust_DUST_SPRITE.png",
  "Shieldy": "Anodyne/src/entity/enemy/bedroom/Shieldy_SPRITE_SHIELDY.png",
  "Pew_Laser": [
    "Anodyne/src/entity/enemy/bedroom/Pew_Laser_PEW_LASER_BULLET.png",
    "Anodyne/src/entity/enemy/bedroom/Pew_Laser_PEW_LASER.png",
  ],
  "Annoyer": "Anodyne/src/entity/enemy/bedroom/Annoyer_S_ANNOYER_SPRITE.png",
  "Console": [
    "Anodyne/src/entity/gadget/Console_embed_windmill_inside.png",
    "Anodyne/src/entity/gadget/Console_sprite_console.png",
  ],
  "Follower_Bro": "Anodyne/src/entity/enemy/etc/Follower_Bro_sprite_follower.png",
  "Sadbro": "Anodyne/src/entity/enemy/etc/Sadbro_sadman_sprite.png",
  "Red_Walker": "Anodyne/src/entity/enemy/etc/Red_Walker_sprite_redwalker.png",
  "Four_Shooter": [
    "Anodyne/src/entity/enemy/redcave/Four_Shooter_four_shooter_bullet_sprite.png",
    "Anodyne/src/entity/enemy/redcave/Four_Shooter_four_shooter_sprite.png",
  ],
  "Slasher": "Anodyne/src/entity/enemy/redcave/Slasher_slasher_sprite.png",
  "On_Off_Laser": [
    "Anodyne/src/entity/enemy/redcave/On_Off_Laser_v_on_off_sprite.png",
    "Anodyne/src/entity/enemy/redcave/On_Off_Laser_h_on_off_sprite.png",
    "Anodyne/src/entity/enemy/redcave/On_Off_Laser_on_off_shooter_sprite.png",
  ],
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
    "Anodyne/src/entity/interactive/NPC_embed_beach_npcs.png",
    "Anodyne/src/entity/interactive/NPC_embed_cliff_npcs.png",
    "Anodyne/src/entity/interactive/NPC_embed_nexus_pad.png",
    "Anodyne/src/entity/interactive/NPC_embed_windmill_blade.png",
    "Anodyne/src/entity/interactive/NPC_embed_randoms.png",
    "Anodyne/src/entity/interactive/NPC_sage_statue.png",
    "Anodyne/src/entity/interactive/NPC_embed_windmill_shell.png",
    "Anodyne/src/entity/interactive/NPC_key_green_embed.png",
    "Anodyne/src/entity/interactive/NPC_note_rock.png",
    "Anodyne/src/entity/interactive/NPC_npc_biofilm.png",
    "Anodyne/src/entity/interactive/NPC_embed_smoke_red.png",
    "Anodyne/src/entity/interactive/NPC_embed_blue_npcs.png",
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
  "Spike_Roller": [
    "Anodyne/src/entity/enemy/crowd/Spike_Roller_Spike_Roller_Sprite_H.png",
    "Anodyne/src/entity/enemy/crowd/Spike_Roller_vert_shadow_sprite.png",
    "Anodyne/src/entity/enemy/crowd/Spike_Roller_hori_shadow_sprite.png",
    "Anodyne/src/entity/enemy/crowd/Spike_Roller_Spike_Roller_Sprite.png",
  ],
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
  "Steam_Pipe": [
    "Anodyne/src/entity/enemy/hotel/Steam_Pipe_steam_sprite.png",
    "Anodyne/src/entity/enemy/hotel/Steam_Pipe_steam_pipe_sprite.png",
  ],
  "Burst_Plant": [
    "Anodyne/src/entity/enemy/hotel/Burst_Plant_burst_plant_bullet_sprite.png",
    "Anodyne/src/entity/enemy/hotel/Burst_Plant_burst_plant_sprite.png",
  ],
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
  "Circus_Folks": [
    "Anodyne/src/entity/enemy/circus/Circus_Folks_javiera_juggle_sprite.png",
    "Anodyne/src/entity/enemy/circus/Circus_Folks_both_sprite.png",
    "Anodyne/src/entity/enemy/circus/Circus_Folks_shockwave_sprite.png",
    "Anodyne/src/entity/enemy/circus/Circus_Folks_javiera_sprite.png",
    "Anodyne/src/entity/enemy/circus/Circus_Folks_arthur_sprite.png",
  ],
  "Fire_Pillar": [
    "Anodyne/src/entity/enemy/circus/Fire_Pillar_fire_pillar_base_sprite.png",
    "Anodyne/src/entity/enemy/circus/Fire_Pillar_fire_pillar_sprite.png",
  ],
  "Sage": "Anodyne/src/entity/interactive/npc/Sage_sage_sprite.png",
  "Mitra": [
    "Anodyne/src/entity/interactive/npc/Mitra_mitra_sprite.png",
    "Anodyne/src/entity/interactive/npc/Mitra_bike_sprite.png",
    "Anodyne/src/entity/interactive/npc/Mitra_mitra_on_bike_sprite.png",
  ],
  "Health_Cicada": "Anodyne/src/entity/interactive/Health_Cicada_health_cicada_embed.png",
  "Dungeon_Statue": "Anodyne/src/entity/interactive/Dungeon_Statue_statue_bedroom_embed.png",
  "Chaser": "Anodyne/src/entity/enemy/etc/Chaser_embed_chaser_sprite.png",
  "Space_Face": "???",
  "Water_Anim": "???",
  "Go_Detector": "???",
  "Sage_Boss": [
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_sage_attacks.png",
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_long_dust.png",
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_sage_boss.png",
    "Anodyne/src/entity/enemy/etc/Sage_Boss_embed_sage_long_attacks.png",
  ],
  "Shadow_Briar": [
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_mist.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_ground_thorn.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_thorn_bullet.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_happy_thorn.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_ice_crystal.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_body_thorn.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_briar_core.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_overhang.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_ice_explosion.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_dust_explosion.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_blue_thorn.png",
    "Anodyne/src/entity/enemy/etc/Briar_Boss_embed_fire_eye.png",
  ],
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
  sprites["npc_cell_bodies"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_cell_bodies.png")
  sprites["npc_rock"] = read_tileset("Anodyne/src/entity/interactive/NPC_note_rock.png")
  sprites["door_portal"] = read_tileset("Anodyne/src/entity/gadget/Door_White_Portal_Sprite.png")
  sprites["nexus_pad"] = read_tileset("Anodyne/src/entity/interactive/NPC_embed_nexus_pad.png")

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
    frame = entity["frame"]
    sx = 0
    sy = 0
    width = 16
    height = 16
    sprite = sprites.get(entity_name, None)
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
    elif entity_name == "Dash_Trap":
      sy = 16
      if is_boi:
        sx = 32
    elif entity_name in ("Gasguy", "Teleguy"):
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
    elif entity_name == "Redsea_NPC":
      sy = frame * 16 // 10
    elif entity_name == "KeyBlock":
      if frame == 0: # small key block
        pass
      else:
        print("WARNING: ignoring KeyBlock frame: {}".format(frame))
        continue
    elif entity_name == "Nonsolid":
      if entity["type"] == "Rail_1":
        sprite = sprites["nonsolid_rail_sprite"]
      else:
        print("WARNING: what nonsolid type is this: {}".format(entity["type"]))
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
    elif entity_name == "Propelled":
      if (frame & 1) == 0:
        sy = 16
      if consume_dust_at(x, y):
        sx = 16
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
    elif entity_name == "Button":
      if map_name == "REDCAVE":
        sy = 32
      elif map_name == "CELL":
        sy = 64
      else:
        sy = 16
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
      else:
        print("WARNING: ignoring npc type: {}".format(npc_type))
        continue
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
      if door_type in ("1", "5", "10"):
        continue # invisible
      elif door_type == "4":
        sprite = sprites["door_portal"]
        if map_name == "CELL":
          sy = 16
      elif door_type == "16":
        sprite = sprites["nexus_pad"]
        width = 32
        height = 32
        if map_name == "CELL":
          sy = 32
      else:
        print("WARNING: ignoring door type: {}".format(door_type))
        continue
    elif entity_name == "Solid_Sprite":
      solid_type = entity["type"]
      if solid_type == "blocker":
        continue # invisible
      else:
        print("WARNING: ignoring Solid_Sprite type: {}".format(solid_type))
        continue
    elif entity_name in ("Pillar_Switch", "Dog", "Shieldy", "Rotator", "Dust"):
      pass # simple
    elif entity_name in ("Stop_Marker", "Event"):
      continue # invisible
    elif entity_name in sprites:
      if entity_name not in warning_set:
        warning_set.add(entity_name)
        print("default rendering sprite: {}".format(entity_name))
    if sprite != None:
      image.paste(sprite, sx=sx, sy=sy, dx=x, dy=y, width=width, height=height)
      did_anything = True
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
