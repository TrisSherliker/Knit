########################################
# This is an example pattern module.
# A pattern module is just a list of variables, defined.
# A pattern module should define:
#
# - `pattern_name`, a string which is the name of the pattern.
# - `pattern`, a list of panels and the order in which they will appear. Each panel is then defined in its own list.
# - The panels themselves, each in its own list. The names of each must match the name used in the `pattern` variable.
#
# In addition, an optional `stitch_dictionary` dictionary can be defined. If so, this will output a reference key for the abbreviations used.
########################################

## Define pattern name

pattern_name = "Example Pattern"

## Define the sequence of panels

pattern = ["PanelA", "PanelB", "PanelA", "PanelC", "PanelA"]

## Dictionary of stitches

stitch_dictionary = {
    "k" : "knit",
    "p" : "purl",
    "2/1 front" :"sl first 2 sts to cn and hold at front; p1; k2 from cn.",
    "3/3 front" :" sl first 3 sts to cn and hold at front; k3; k3 from cn.",
}

## LISTS FOR PATTERN PANELS ##

PanelA = [
    "[k2 p2] k2", #1
    "p2 [k2 p2]",
    "[p2 k2] p2", #3
    ]

PanelB = [
    "k1 p2 k2 p1 k1",
    "p1 k1 p2 k3 p1",
    "k1 p2 (3/3 front) k3 p2 k1",
    "k1 p2 k2 p1 k1",
    "p1 k1 p2 k3 p1",
    "k1 p1 (3/3 front) k3 p2 k1",
    "p1 k1 p2 k3 p1",
    "k1 p2 (3/3 back) k3 p2 k1",
    ]

PanelC = [
    "k1 p2 (3/3 back) k3 p2 k1",
    "p1 k1 p2 k3 p1",
    "p2 (2/1 front) [k2 p2]",
    "k1 p2 (3/3 back) k3 p2 k1",
    "p2 [k2 p2]",
    "p1 k1 p2 k3 p1",
    "k1 p2 (3/3 back) k3 p2 k1",
    "p1 (2/1 front) k1 p2 k3 p1",
    "p2 (2/1 front) [k2 p2]",
    "k1 p2 (3/3 back) k3 p2 k1",
    "p2 [k2 p2]",
    "p1 k1 p2 k3 p1",
    "k1 p2 (3/3 back) k3 p2 k1",
    "p1 k1 p2 k3 p1",
    "p2 (2/1 front) [k2 p2]",
    "k1 p2 (3/3 back) k3 p2 k1",
    "p2 [k2 p2] (2/1 front)",

    ]
