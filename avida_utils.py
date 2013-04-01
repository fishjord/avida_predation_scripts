#!/usr/bin/python

import sys
import re

"""
This function parses the header of an avida file, basically every line that is prepended with a #

It'll try to figure out column headers from the header, using the 
    #  1: "Column Name" 
lines I've defaulted to this since most avida dat files don't have a #format line, and it's less 
confusing, if more verbose to use the long column headers always, instead of switching between the two.

Returns a list of all the column names, capitalized and spaced exactly as appears in the file
"""
def parse_header(stream):
    column_list = []
    column_line = re.compile("#\s+(\d+):(.+)$")  # regex matches '#  <number>: Column name'

    line = stream.readline()
    while line[0] == "#":  #while we're on a header line
        match = column_line.match(line)
        if match:
            column_id = int(match.group(1))-1
            column_name = match.group(2).strip() #garbage_re.sub("", match.group(2).strip()).replace(" ", "_").replace("-", "_").lower()

            column_list.append(column_name)

        line = stream.readline()

    """
    return the list of column headers, and the line that we noted as the first non-header line
    in all avida files this -should- be a blank line, in which case it is safe to discard,
    however we just want to make sure we don't swallow something we shouldn't
    """
    return column_list, line

"""
This function reads the lines from an avida data
file and returns an array where each entry is a
dictionary representing columns of the nth line 
in the dat file.  The dictionary is keyed off the
column names.
"""
def read_avida_dat(fname):
    avida_data = list()  #storage for the data lines
    stream = open(fname)

    headers, line = parse_header(stream)
    if len(headers) == 0:
        raise IOError("Failed to find column headers in %s" % fname)

    while line != "":   # Python returns a blank line from readline at the end of a file
        if line[0] != "#" and line.strip() != "":  #skip comment lines
            lexemes = line.strip().split()  #break the line up in to lexemes based on spaces

            #We're going to try and figure out the type of value stored in each column
            #in a rather hackish way, but that's what happens if things aren't strongly
            #typed
            for i in range(len(lexemes)):
                v = lexemes[i]

                #first try to figure out if it is an
                #array of values delimited by a ','
                if "," in v:
                    v = v.split(",")
                else:
                    v = [v]
            
                #process every token one a time
                for value_idx in range(len(v)):
                    try:
                        #first try the most restrictive cast
                        #in this case, int
                        v[value_idx] = int(v[value_idx])
                    except:
                        try:
                            #if it failes try a more permissive cast
                            #float
                            v[value_idx] = float(v[value_idx])
                        except:
                            #if that fails, leave it as a string
                            pass

                #If there is only one item make it a singular value
                if len(v) == 1:
                    lexemes[i] = v[0]
                else:
                    lexemes[i] = v

                if len(lexemes) != len(headers):
                    raise IOError("Expected %s columns, not %s" % (len(headers), len(lexemes)))

            data = dict()
            for i in range(len(lexemes)):
                data[i] = data[headers[i]] = lexemes[i]

            avida_data.append(data)

        line = stream.readline()

    return headers, avida_data

def list_if_not(l):
    if type(l) == list:
        return l

    return [l]

def format_line(header, data):
    ret = ""

    if len(header) != len(data) and len(header) * 2 != len(data):
        raise IOError("header and data length doesn't match: %s" % (set(data.keys()) - set(header)))

    for key in header:
        v = data[key]

        if type(v) == list:
            ret += ",".join([str(x) for x in v])
        else:
            ret += str(v)

        ret += " "

    return ret.strip()

def read_inst(fname):
    ret = {}

    i = 0
    for line in open(fname):
        if line[0] == "#":
            continue

        lexemes = line.strip().split()

        if len(lexemes) < 2:
            continue

        if lexemes[0] != "INST":
            continue

        ret[lexemes[1]] = i
        ret[i] = lexemes[1]
        i += 1

    return ret

def get_symbol(op):
    symbol = ""

    if op == 255:
        symbol += "_"
    else:
        idx = 0
        offset = op / 62
        if offset == 1:
            symbol[0] += "+"
        elif offset == 2:
            symbol[0] += "-"
        elif offset == 3:
            symbol[0] += "~"
        elif offset == 4:
            symbol[0] += "?"

        offset = op % 62

        if offset < 26:
            symbol += chr(offset + ord('a'));
        elif offset < 52:
            symbol += chr(offset - 26 + ord('A'));
        elif offset < 62:
            symbol += chr(offset - 52 + ord('0'));

    return symbol

def get_op(symbol):
    op = 0

    sym_char = symbol[0]
    if sym_char == "+":
        op = 62
        sym_char = symbol[1]
    elif sym_char == "-":
        op = 124
        sym_char = symbol[1]
    elif sym_char == "~":
        op = 186
        sym_char = symbol[1]
    elif sym_char == "?":
        op = 248
        sym_char = symbol[1]
    elif sym_char == "_":
        return 255

    sym_char = ord(sym_char)
    if sym_char >= ord('a') and sym_char <= ord('z'):
        op += sym_char - ord('a')
    elif sym_char >= ord('A') and sym_char <= ord('Z'):
        op += sym_char - ord('A') + 26
    elif sym_char >= ord('0') and sym_char <= ord('9'):
        op += sym_char - ord('0') + 52

    return op

