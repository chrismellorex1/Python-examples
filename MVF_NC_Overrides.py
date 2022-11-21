import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis



# Define Regional overrides of Product Definition settings and
# default values of additional Regional Definition settings
#  ( This Definition section must be before the Class definition)

#***** THIS NEXT LINE IS REQUIRED *****
Definition = {}

#####################################################
# Override VariableList if desired
#
#VariableList = []
# Taken from MVF definitions file. Variable list commented out there.
# Add check mark list of working buoys.
# First set of buoys are those defaulted to working
# Forecaster can check or uncheck as needed.
# Update this list as buoys come online/go offline.
# F.Achorn 01/27/11
VariableList = [
         (("Forecaster Number", "forecasterNumber"), 99, "alphaNumeric"),
         (("Tropical Storm", "tropicalStorm"), "no", "radio", ["no", "yes"]),
         (("Buoys Reporting Winds", "workingWindsBuoys"),
          ["41010", "42003", "42001", "42002"], "check",
          ["41010", "42003", "42001", "42002"]),
         (("Buoys Reporting Seas", "workingSeasBuoys"),
          ["41010", "42003", "42001", "42002"], "check",
          ["41010", "42003", "42001", "42002"])
        ]
#
# NC Definitions:
# Definition statements must start in column 1

### Regional settings of baseline options: ###

#Definition["displayName"] = "MVF_NC"

### New Regional Definitions not in the baseline ###

# END NC definitions
############################################################

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the above Definition = {} line
# plus following class definition and the __init__ method with only
# the "pass" line in it.

class MVF_NC_Overrides:
    """Class NNN_FILETYPE - Version: IFPS"""

    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Add methods here making sure to indent inside the class statement
    # NC MVF Overrides ------------------------

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in MVF_NC_Overrides")

# Taken from MVF.TextProduct
# remove "SC" as a warning cat.
# F.Achorn 01/27/11
    def _warningStatus(self, statDict, argDict):
        self.debug_print("Debug: _warningStatus in MVF_NC_Overrides")
        # Return a warning status
        wind = self.getStats(statDict, "Wind")

        # Need to use total or 'combined' seas
        waves = self.getStats(statDict, "WaveHeight")  # fixed

        if wind is None:
            return "NO"
        mag, dir = wind

        #non-tropical
        if self._tropicalStorm == 0:
            if mag < 25 and waves < 5:
                return "NO"
            elif mag < 34:                     # gales start at 34 kts
                return "NO"
            elif mag < 48:                     # storms start at 48 kts
                return "GL"
            elif mag < 63:
                return "ST"
            else:
                return "HF"
        #tropical
        else:
            if mag < 25 and waves < 5:
                return "NO"
            elif mag < 34:                     # gales start at 34 kts
                return "NO"
            elif mag < 63:                     # TS/HR winds
                return "TS"
            else:
                return "HR"

# Taken from MVF.TextProduct
# Write out standard 99s if buoy not working
# e.g.
#     %%F02 46005 18/NO/9999/99/06/NO/9999/99
# F.Achorn 01/27/11
    def _makeProduct(self, fcst, editArea, areaLabel, argDict):
        self.debug_print("Debug: _makeProduct in MVF_NC_Overrides")
        statList = self.getStatList(self._sampler, self._getAnalysisList(),\
                                    self._timeRangeList, editArea)

        fcst += "%%F"
        fcst += self._forecasterNumber
        fcst += " " + areaLabel + " "

        index = 0
        for statDict in statList:

            fcst += self._timeRangeList[index][1] + "/"

            # Warning Status
            str = self._warningStatus(statDict, argDict)
            fcst += str + "/"

            # if the buoy is listed in the workingBuoys array, forecast as normal.
            if areaLabel in self._workingWindsBuoys:

                # Wind direction and speed : ddff
                str = self._windDirSpeed(statDict, argDict)
                fcst += str + "/"
            else:
                # Wind direction and speed : ddff
                str = "9999"
                fcst += str + "/"

            # if the buoy is listed in the workingBuoys array, forecast as normal.
            if areaLabel in self._workingSeasBuoys:
                # Wave Height
                str = self._sigWaveHeight(statDict, argDict)
                fcst += str + "/"
            else:
                # Wave Height
                str = "99"
                fcst += str + "/"

            index += 1
        return fcst
