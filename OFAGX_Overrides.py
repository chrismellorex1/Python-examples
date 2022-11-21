import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis


#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class OFAGX_Overrides:
    def __init__(self):
        pass

    def _Text1(self):
        self.debug_print("Debug: _Text1 in MIM")
        #productDescription = ".FORECAST DISCUSSION: MAJOR FEATURES/WINDS/SEAS/SIGNIFICANT\n" \
        #                   + ".WEATHER FOR THE " + self._longProductDesc + "\n\n"
        productDescription = ""
        return productDescription

       #### ***THIS SECTION CONTROLS PREVIOUS VERSION***

    def _Text2(self):
        self.debug_print("Debug: _Text2 in MIM")
        # Include the previous MIM is requested
        previousMIM = ""

        if self._includePrevDisc != "No - blank MIM":
            self.debug_print("Debug: including previous discussion")
            #  Try to get previous MIM
            previousMIM = self.getPreviousProduct(self._textdbPil, "")
            # This gets the entire products, so grab just part without header
            #if self._debug: print "looking for :" + self._longProductDesc +"\n"
            #previousMIM = previousMIM.partition(self._longProductDesc)[2]
            previousMIM = previousMIM.partition("....")[0]
            # remove the warning section too if it's headered correctly
            previousMIM = previousMIM.partition("....")[0]
#            previousMIM = self.endline(previousMIM, linelength=66, breakStr=" ")

            #  add a line and note to separate the two.
            if self._includePrevDisc == "Yes - update - both forecaster names":
                self.debug_print("Debug: Adding PREVIOUS DISCUSSION line")
                previousMIM = "\n\n-----------------------------------------------------------------\n" \
                    + "PREVIOUS DISCUSSION..." + previousMIM
        else:
            self.debug_print("Debug: NOT including previous discussion")
        return  previousMIM #+ "\n"

    def generateForecast(self, argDict):
        self.debug_print("Debug: generateForecast in MIM")
        # Generate Text Phrases for a list of edit areas

        # Get variables
        error = self._getVariables(argDict)
        if error is not None:
            return error

        # Get the areaList -- derived from defaultEditAreas
        self._areaList = argDict["editAreas"]
        #self._areaList = self.getAreaList(argDict)
        if not self._areaList:
            return "WARNING -- No Edit Areas Specified to Generate Product."

        error = self._determineTimeRanges(argDict)
        if error is not None:
            return error

        # Initialize the output string
        fcst = self._preProcessProduct("", argDict)

        # add the header for the Warning section
        fcst = fcst

        # Generate the warnings for each edit area in the list
        #for editArea, areaLabel in self._areaList:
            # add pz5 or 6 area label
        #    fcst = self._preProcessArea(fcst, areaLabel, argDict)
            # add hazard
        #    fcst = self._makeProduct(fcst, editArea, areaLabel, argDict)
#             fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)

        fcst = self._postProcessProduct(fcst, argDict)
        fcst = fcst.replace("HURRICANE", "HURRICANE WARNING")
        fcst = fcst.replace("TROPICAL STORM", "TROPICAL STORM WARNING")
        fcst = fcst.replace("HURRICANE WARNING FORCE", "HURRICANE FORCE WIND WARNING")
        fcst = fcst.replace("STORM", "STORM WARNING")
        fcst = fcst.replace("GALE", "GALE WARNING")
        #fcst = string.replace(fcst, "HURRICANE FORCE WIND WARNING POSSIBLE", "HURRICANE FORCE CONDITIONS POSSIBLE")
        fcst = fcst.replace("STORM WARNING POSSIBLE", "STORM CONDITIONS POSSIBLE")
        fcst = fcst.replace("GALE WARNING POSSIBLE", "GALE CONDITIONS POSSIBLE")
        fcst = fcst.replace("TROPICAL STORM WARNING WARNING", "TROPICAL STORM WARNING")
        fcst = fcst.replace("HURRICANE FORCE WIND WARNING POSSIBLE", "HURRICANE FORCE WINDS POSSIBLE")
        fcst = fcst.replace("TROPICAL STORM WARNING POSSIBLE", "TROPICAL STORM CONDITIONS POSSIBLE")
        fcst = fcst.replace("HURRICANE WARNING POSSIBLE", "HURRICANE CONDITIONS POSSIBLE")
        fcst = fcst.replace("SMALL CRAFT ADVISORY", "NONE")
        fcst = fcst.replace("NONE FOR WINDS", "NONE")
        fcst = fcst.replace("GALE FORCE WARNING WINDS", "GALE FORCE WINDS")
        fcst = fcst.replace("NATIONAL HURRICANE WARNING CENTER", "NATIONAL HURRICANE CENTER")
        #fcst = string.replace(fcst, "AM PDT", "UTC")
        #fcst = string.replace(fcst, "PM PDT", "UTC")
        return fcst

    def allowedHazards(self):

        allActions = ["NEW", "EXA", "EXB", "EXT", "CAN", "CON", "EXP"]
        tropicalActions = ["NEW", "EXA", "EXB", "EXT", "UPG", "CAN", "CON",
          "EXP"]
        marineActions = ["NEW", "EXA", "EXB", "EXT", "CON"]
        return [
            ('HU.W', tropicalActions, 'Tropical'),     # HURRICANE WARNING
            ('TY.W', tropicalActions, 'Tropical'),     # TYPHOON WARNING
            ('TR.W', tropicalActions, 'Tropical'),     # TROPICAL STORM WARNING
            ('HF.W', marineActions, 'Marine'),       # HURRICANE FORCE WIND WARNING
            ('SR.W', marineActions, 'Marine'),       # STORM WARNING
            ('GL.W', marineActions, 'Marine'),       # GALE WARNING
            ('SE.W', marineActions, 'Marine'),       # HAZARDOUS SEAS
            ('UP.W', allActions, 'IceAccr'),                        # HEAVY FREEZING SPRAY WARNING

             # added by J. Lewitsky/NHC on 02/12/11 for expected wording
            ('GCE', marineActions, 'Marine'),
            ('SCE', marineActions, 'Marine'),
            ('HFE', marineActions, 'Marine'),
            ('TRE', tropicalActions, 'Tropical'),
            ('HUE', tropicalActions, 'Tropical'),

            ('GL.A', marineActions, 'Marine'),
            ('SR.A', marineActions, 'Marine'),
            ('HF.A', marineActions, 'Marine'),
##            ('GL.O', marineActions, 'Local'),
            ('MF.Y', allActions, 'Fog'),                            # DENSE FOG ADVISORY
            ('MS.Y', allActions, 'Smoke'),                          # DENSE SMOKE ADVISORY
##            ('UP.Y', allActions, 'IceAccr'),                        # HEAVY FREEZING SPRAY ADVISORY
            ('MH.Y', allActions, 'Ashfall')                        # VOLCANIC ASHFALL ADVISORY
            ]

    def DAY(self):
        return 7 + self.daylight()
    def NIGHT(self):
        return 19 + self.daylight()
