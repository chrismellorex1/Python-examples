import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis

import UserInfo

# Define Regional overrides of Product Definition settings and
# default values of additional Regional Definition settings
#  ( This Definition section must be before the Class definition)

#***** THIS NEXT LINE IS REQUIRED *****
Definition = {}

#####################################################
# Override VariableList if desired
#
#VariableList = [
#        (("Include Previous Discussion?", "includePrevDisc") , "No", "radio",
#            ["Yes","No"]),
#        ]
# NC Definitions:
# Definition statements must start in column 1

### Regional settings of baseline options: ###

#Definition["displayName"] = "MIM_NC"
# product name
Definition["productName"] = "Tropical Weather Discussion"
# Location of WFO - city st
Definition["wfoCityState"] = "National Hurricane Center Miami FL"
# What string to use after forecaster name. Use "" if none wanted.
Definition["signature"] = "OCEAN PREDICTION CENTER."
# Area Dictionary -- Descriptive information about zones
Definition["areaDictionary"] = "AreaDictionary"
# hazardSampingThreshold  (%cov, #points)
Definition["hazardSamplingThreshold"] = (0, 1)
# Max line length for warning formatting
Definition["lineLength"] = 66
# file to save output to.
#Definition["outputFile"] = "{prddir}/TEXT/MIM_NFD.txt"
Definition["topicDividers"] = [
                ("seas", ".SEAS..."),
                ("etsurge", ".EXTRATROPICAL STORM SURGE GUIDANCE..."),
                          ]
Definition["debug"] = 0
# Definition["notice"] = "NOTE: ON OCTOBER 31, 2013...OPC MADE A CHANGE TO THIS MARINE WEATHER DISCUSSION. " + \
#         "CONFIDENCE LEVELS FOR EACH INDIVIDUAL WARNING HEADLINE ARE NO LONGER SPECIFIED BY ZONE...BUT " + \
#         "ARE DISCUSSED IN THE BODY OF THE PRODUCT. FOR COMMENTS...PLEASE GO TO " + \
#         "HTTP://WWW.OPC.NCEP.NOAA.GOV/FEEDBACK.PHP\n/ALL LOWER CASE LETTERS/\n"


### New Regional Definitions not in the baseline ###

# END NC definitions
############################################################

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the above Definition = {} line
# plus following class definition and the __init__ method with only
# the "pass" line in it.

class TWD_NC_Overrides:
    """Class NNN_FILETYPE - Version: IFPS"""

    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Add methods here making sure to indent inside the class statement
    # NC MIM Overrides ------------------------

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in MIM_NC_Overrides")
