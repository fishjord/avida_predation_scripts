#!/usr/bin/python

from PIL import Image
import argparse
import os
from random import randrange
import PIL
import sys

class RGB24ColorPalette:
    def __init__(self, allow_random):
        self.allow_random = allow_random
        self.colors = dict()
        self.colors["resources"] = dict()
        self.colors["forager_type"] = dict()

    def _get_random_color(self):
        if not self.allow_random:
            raise Exception("Random colors not allowed")

        return (randrange(0, 255), randrange(0, 255), randrange(0, 255))

    def get_color(self, color_type, idx):
        if color_type not in self.colors:
            raise Exception("Unknown color type '%s'" % color_type)

        if idx not in self.colors[color_type]:
            color = self._get_random_color()
            self.colors[color_type][idx] = color

        return self.colors[color_type][idx]

    def get_default_forager_color(self):
        return self.get_color("forager_type", 0)

def enumerate_grid_files(d):
    grid_map = {}
    width, height = -1, -1
    for f in os.listdir(d):
        if f.startswith("max_res_grid."):
            idx = 0
            if width == -1:
                height = 0
                for line in open(os.path.join(d, f)):
                    if line.strip() != "":
                        height += 1
                width = len(line.split())
        elif f.startswith("org_loc."):
            idx = 1

        update = int(f.split(".")[1])
        if update not in grid_map:
            grid_map[update] = [None, None]

        grid_map[update][idx] = os.path.join(d, f)

    return width, height, [grid_map[update] for update in sorted(grid_map.keys())]

def read_org_grid(org_file):
    stream = open(org_file)
    required_fields = {"org_id" : "id", "org_forage_target" : "forager_type", "av_cellx" : "x", "av_celly" : "y", "av_facing" : "facing"}
    field_map = {}

    headers = stream.readline().strip()
    if headers[0] != "#":
        raise IOError("No header at the top org file '%s'" % org_file)
    headers = headers[2:].split(",")

    for i in range(len(headers)):
        header = headers[i]
        if header in required_fields:
            field_map[i] = required_fields[header]

    if len(field_map) != len(required_fields):
        raise IOError("Didn't see all required fields in '%s' (expected %s, saw %s)" % (org_file, required_fields.keys(), field_map.values()))

    line = stream.readline()
    ret = []
    while line != "":
        lexemes = line.strip().split(",")
        if len(lexemes) == len(headers):
            values = {}
            for i in field_map:
                values[field_map[i]] = int(lexemes[i])

            ret.append(values)

        line = stream.readline()

    return ret

def create_org_image(palette, orgs, width, height):
    img = Image.new("RGB", (width, height), "white")
    data = img.load()

    for org in orgs:
        data[org["x"], org["y"]] = palette.get_color("forager_type", org["forager_type"])

    return img

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, help="Final frame width")
    parser.add_argument("--height", type=int, help="Final frame height")
    parser.add_argument("--color-def", help="Color definition file")
    parser.add_argument("--allow-random-colors", action="store_true", help="Allow the palette to select random colors for undefined resource/forager types")
    parser.add_argument("-c", action="store_true", help="Write frames to stdout instead of to image files")
    parser.add_argument("-f", "--format", default="png", help="Image output format")
    parser.add_argument("grid_dir", help="Grid dump directory path")

    args = parser.parse_args()

    palette = RGB24ColorPalette(args.allow_random_colors)
    width, height, grid_files = enumerate_grid_files(args.grid_dir)
    if width == -1 or height == -1:
        raise IOError("Couldn't determine the environment size from any resource files")

    frame = 0
    name_template = "frame_%06d." + args.format
    for res_grid, org_grid in grid_files:
        orgs = read_org_grid(org_grid)
        img = create_org_image(palette, orgs, width, height)
        img.save(name_template % frame)
        frame += 1

    print palette.colors

if __name__ == "__main__":
    main()
