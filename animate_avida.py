#!/usr/bin/python

import argparse
import os
from random import randrange
import sys
import numpy

class RGB24ColorPalette:
    def __init__(self, allow_random):
        self.allow_random = allow_random
        self.colors = dict()
        self.colors["resources"] = dict()
        self.colors["forager_type"] = dict()

    def from_stream(self, stream):
        line = stream.readline()
        while line != "":
            lexemes = line.strip().split("\t")
            if line[0] != "#" and len(lexemes) == 3:
                i = int(lexemes[1])
                color = self._color_from_string(lexemes[2])
                if lexemes[0] == "resource":
                    self.colors["resources"][i] = self._get_color_gradiant(color)
                elif lexemes[0] == "forager_type":
                    self.colors["forager_type"][i] = color

            line = stream.readline()

    def __repr__(self):
        s = "#RGB24ColorPalette\n"
        for resource in self.colors["resources"]:
            s += "resource\t%s\t%s\n" % (resource, "#%02x%02x%02x".upper() % self._unpack_color(self.colors["resources"][resource][-1]))
        for ft in self.colors["forager_type"]:
            s += "forager_type\t%s\t%s\n" % (ft, "#%02x%02x%02x".upper() % self._unpack_color(self.colors["forager_type"][ft]))

        return s

    def _unpack_color(self, color):
        b = (color) & 0xff
        g = (color >> 8) & 0xff
        r = (color >> 16) & 0xff

        return (r, g, b)

    def _get_color_gradiant(self, color, steps = 100):
        r, g, b = self._unpack_color(color)
        ret = []
        for i in range(steps):
            ratio = i / float(steps)
            ret.append(self._pack_color(int(r * ratio), int(g * ratio), int(b * ratio)))

        return ret

    def _pack_color(self, r, g, b):
        ret = r
        ret = ret << 8 | g
        ret = ret << 8 | b

        return ret

    def _color_from_string(self, s):
        if s[0] != "#" or len(s) != 7:
            raise Exception("Invalid color format '%s'" % s)

        return self._pack_color(int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))

    def _get_random_color(self):
        if not self.allow_random:
            raise Exception("Random colors not allowed")

        return self._pack_color(randrange(0, 255), randrange(0, 255), randrange(0, 255))

    def get_resource_color(self, idx, scale = 1):
        resources = self.colors["resources"]
        if idx not in resources:
            color = self._get_random_color()
            resources[idx] = self._get_color_gradiant(color)

        return resources[idx][int(max(min(1, scale), 0) * (len(resources[idx]) - 1))]

    def get_ft_color(self, idx):
        ft = self.colors["forager_type"]
        if idx not in ft:
            color = self._get_random_color()
            ft[idx] = color

        return ft[idx]

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

def read_max_res(res_file):
    ret = []
    for line in open(res_file):
        if line.strip() == "":
            continue
        lexemes = line.strip().split()
        ret.append([])
        for x in lexemes:
            ret[-1].append(float(x))

    return ret

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

def create_image(palette, resources, orgs, width, height, scaling_factor, img_buf):
    final_width = width * scaling_factor
    final_height = height * scaling_factor

    for x in range(height):
        for y in range(width):
            for xi in range(scaling_factor):
                for yi in range(scaling_factor):
                    img_buf[(x * scaling_factor + xi) * final_width + (y * scaling_factor) + yi] = palette.get_resource_color(1, resources[x][y])

    for org in orgs:
        for xi in range(scaling_factor):
            for yi in range(scaling_factor):
                img_buf[(org["x"] * scaling_factor + xi) * final_width + (org["y"] * scaling_factor) + yi] = palette.get_ft_color(org["forager_type"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1, help="Image scaling factor")
    parser.add_argument("--color-def", dest="color_def", help="Color definition file")
    parser.add_argument("--allow-random-colors", action="store_true", help="Allow the palette to select random colors for undefined resource/forager types")
    parser.add_argument("-c", dest="to_stdout", action="store_true", help="Write frames to stdout instead of to image files")
    parser.add_argument("grid_dir", help="Grid dump directory path")

    args = parser.parse_args()

    palette = RGB24ColorPalette(args.allow_random_colors)
    if args.color_def:
        palette.from_stream(open(args.color_def))

    width, height, grid_files = enumerate_grid_files(args.grid_dir)
    if width == -1 or height == -1:
        raise IOError("Couldn't determine the environment size from any resource files")

    print >>sys.stderr, "Avida grid size: %dx%d, image size: %dx%d" % (width, height, width * args.scale, height * args.scale)

    frame = 0
    name_template = "frame_%06d.xrgb32"
    img_buf = numpy.zeros((width * args.scale) * (height * args.scale), dtype=numpy.int32)
    for res_grid, org_grid in grid_files:
        grid = read_max_res(res_grid)
        orgs = read_org_grid(org_grid)

        create_image(palette, grid, orgs, width, height, args.scale, img_buf)

        if args.to_stdout:
            img_buf.tofile(sys.stdout)
        else:
            out = open(name_template % frame, "w")
            img_buf.tofile(out)
            out.close()
        frame += 1

    print >>sys.stderr, palette

if __name__ == "__main__":
    main()
