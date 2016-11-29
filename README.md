# Anodyne Map Scraper

This program reads a decompilation of Anodyne.swf and outputs maps as .png files.

This program was originally created by Joseph Landry. www.josephlandry.com

Anodyne is a video game created by [Sean HTCH](https://twitter.com/sean_htch) and [Joni Kittaka](https://twitter.com/jonikitsu).
http://www.anodynegame.com/

## How to use this program

Prerequisites:

* Purchase Anodyne
* Some skill at using the command line
* Python 3
* ffdec.exe - a flash decompiler - tested with version 9.0.0
* Tested on Linux and Windows+Cygwin

When you purchase Anodyne, you will get a file called `Anodyne.swf` somewhere.
If you bought it through Steam on 64-bit Windows, the file is located here:

```
C:\Program Files (x86)\Steam\steamapps\common\Anodyne\Anodyne.swf
```

Decompile the swf using the command line.
From this project's directory:

```
python3 extract_swf.py PATH/TO/ffdec.exe PATH/TO/Anodyne.swf
```

Make sure you got the submodules updated. With git, do this:

```
git submodule init
git submodule update
```

Without git, you can just download [simplepng.py](https://raw.githubusercontent.com/thejoshwolfe/simplepng.py/master/simplepng.py)
and put it in this directory at `simplepng.py/simplepng.py`.

Now you can build the maps:

```
python3 buildmap2.py
```

The default output location is `maps/`.

Try running either of the above `.py` scripts with `--help` for more detailed options
such as adding grid lines or rendering only the physics instead of the appearance.

## Example maps

Map of the Nexus:
![nexus](http://vignette3.wikia.nocookie.net/anodyne/images/c/c5/Nexus_HiddenAreas.png/revision/latest?cb=20160408213319)

Map of the Nexus showing the physics collisions of tiles and objects:
![nexus physics](http://vignette1.wikia.nocookie.net/anodyne/images/7/77/NEXUS_p.png/revision/latest?cb=20160518032003)
