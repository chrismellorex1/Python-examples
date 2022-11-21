import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis

import UserInfo
HideTool = 1
#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class MIM_NEW_NH2_Overrides:
    def __init__(self):
        pass

    def _Text1(self):
        self.debug_print("Debug: _Text1 in MIM")
        #productDescription = ".FORECAST DISCUSSION: MAJOR FEATURES/WINDS/SEAS/SIGNIFICANT\n" \
        #                   + ".WEATHER FOR THE " + self._longProductDesc + "\n\n"
#         productDescription = "MARINE WEATHER DISCUSSION FOR THE GULF OF MEXICO...CARIBBEAN\n" \
#         "SEA AND TROPICAL N ATLANTIC FROM 07N TO 19N BETWEEN 55W AND\n" \
#         "64W...AND THE SW N ATLANTIC INCLUDING THE BAHAMAS."
#         return productDescription

        productDescription = "Marine Weather Discussion for the Gulf of Mexico, Caribbean Sea,\n" \
        "and Tropical North Atlantic from 07N to 19N between 55W and 64W\n" \
        "and the Southwest North Atlantic including the Bahamas\n\n"
        return productDescription

    #Modified from OFF base
    def _Text2(self):
        self.debug_print("Debug: _Text2 in OFF_NH2_Overrides")

        #  Try to get Synopsis from previous CWF
        productID = "MIAOFFNT4"
        synopsis = self.getPreviousProduct(productID, "SYNOPSIS")
        #  Clean up the previous synopsis
        synopsis = re.sub(r'\n', r' ', synopsis)
        synopsis = re.sub(r'  ', r' ', synopsis)
        #synopsis = self._synopsisHeading + synopsis
        synopsis = self.endline(synopsis, linelength=65, breakStr=" ")

        return "...GULF OF MEXICO...\n\n" + synopsis + "\n"

    def _Text3(self):

        productID = "MIAOFFNT3"
        synopsis = self.getPreviousProduct(productID, "SYNOPSIS")
        #  Clean up the previous synopsis
        synopsis = re.sub(r'\n', r' ', synopsis)
        synopsis = re.sub(r'  ', r' ', synopsis)
        #synopsis = self._synopsisHeading + synopsis
        synopsis = self.endline(synopsis, linelength=65, breakStr=" ")

        return"...CARIBBEAN SEA AND TROPICAL N ATLANTIC FROM 07N TO 19N BETWEEN 55W AND 64W...\n\n" + \
              synopsis + "\n"

    def _Text4(self):
        synopsis2 = ""
        productID = "MIAOFFNT3"
        # Can't just search for "SYNOPSIS"
        # It will only return the first one it finds
        entire_product = self.getPreviousProduct(productID).strip()
        # get just the second synopsis
        # split the product on the synopsisHeading (.SYNOPSIS...)
        # then split on "$$" and grab everything before the $$ at the end of the synopsis
        synopsis2 = entire_product.split(self._definition["synopsisHeading"])[2].split("$$")[0]

        #  Clean up the previous synopsis
        synopsis2 = re.sub(r'\n', r' ', synopsis2)
        #synopsis2 = self._synopsisHeading + synopsis2
        synopsis2 = self.endline(synopsis2, linelength=65, breakStr=" ")

        return "...SW N ATLANTIC INCLUDING THE BAHAMAS...\n\n" + synopsis2 + "\n$$\n\n"

    # F.Achorn/OPC    09/23/13    Add in topic dividers
    def _preProcessProduct(self, fcst, argDict):
        self.debug_print("Debug: _preProcessProduct in MIM")
        # Add product headers
        if self._areaName:
             productName = self._productName.strip() + " FOR " + \
                           self._areaName.strip()
        else:
             productName = self._productName.strip()

        issuedByString = self.getIssuedByString()

        fcst =  fcst + self._wmoID + " " + self._fullStationID + " " + \
               self._ddhhmmTime + "\n" + self._pil + "\n\n" +\
               productName + "\n" +\
               "NWS " + self._wfoCityState + \
               "\n" + issuedByString + self._timeLabel + "\n\n"

        fcst += self._Text1()
        try:
            text2 = self._Text2(argDict["host"])
        except:
            text2 = self._Text2()

        try:
            text3 = self._Text3(argDict["host"])
        except:
            text3 = self._Text3()

        try:
            text4 = self._Text4(argDict["host"])
        except:
            text4 = self._Text4()

        fcst += text2 + text3 + text4

        # Add in any topic dividers

#         if self._includePrevDisc == "No - blank MIM":
#             for topic in self._topicDividers:
#                 self.debug_print("DEBUG: Adding "+topic[0] + " topic divider")
#                 fcst = fcst + topic[1] + "\n\n\n"
        return fcst

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
        fcst += ".WARNINGS...Any changes impacting coastal NWS offices will be\n" \
                    + "coordinated through AWIPS II Collaboration Chat, or by telephone:\n"

        # Generate the warnings for each edit area in the list
        for editArea, areaLabel in self._areaList:
            # add pz5 or 6 area label
            fcst = self._preProcessArea(fcst, areaLabel, argDict)
            # add hazard
            fcst = self._makeProduct(fcst, editArea, areaLabel, argDict)
#             fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)

        fcst = self._postProcessProduct(fcst, argDict)
        #fcst = string.replace(fcst, "HURRICANE", "HURRICANE WARNING") #commented out 09/03/16 ERA
        #fcst = string.replace(fcst, "TROPICAL STORM", "TROPICAL STORM WARNING")
        fcst = fcst.replace("HURRICANE WARNING FORCE", "HURRICANE FORCE WIND WARNING")
        #fcst = string.replace(fcst, "STORM", "STORM WARNING") commented out to get rid of "warning" wording ERA 06/18/16
        #fcst = string.replace(fcst, "GALE", "GALE WARNING") #commented out 09/03/16 ERA
        #fcst = string.replace(fcst, "HURRICANE FORCE WIND WARNING POSSIBLE", "HURRICANE FORCE CONDITIONS POSSIBLE")
        fcst = fcst.replace("STORM WARNING POSSIBLE", "STORM CONDITIONS POSSIBLE")
        fcst = fcst.replace("GALE WARNING POSSIBLE", "GALE CONDITIONS POSSIBLE")
        fcst = fcst.replace("TROPICAL STORM WARNING WARNING", "TROPICAL STORM WARNING")
        fcst = fcst.replace("HURRICANE FORCE WIND WARNING POSSIBLE", "HURRICANE FORCE WINDS POSSIBLE")
        fcst = fcst.replace("TROPICAL STORM WARNING POSSIBLE", "TROPICAL STORM CONDITIONS POSSIBLE")
        fcst = fcst.replace("HURRICANE WARNING POSSIBLE", "HURRICANE CONDITIONS POSSIBLE")
        fcst = fcst.replace("SMALL CRAFT ADVISORY", "NONE")
        fcst = fcst.replace("NONE FOR WINDS", "NONE")
        fcst = fcst.replace("GALE WARNING FORCE WINDS", "GALE FORCE WINDS")
        fcst = fcst.replace("NATIONAL HURRICANE WARNING CENTER", "NATIONAL HURRICANE CENTER")
        fcst = fcst.replace("WARNING WARNING", "WARNING")
        fcst = fcst.replace("Gale Watch", "GALE CONDITIONS POSSIBLE") #ADDED GALE AND MIXED CASE ERA 12/01/15
        fcst = self.endline(fcst, linelength=self._lineLength)
        return fcst

    def _postProcessProduct(self, fcst, argDict):
        self.debug_print("Debug: _postProcessProduct in MIM")

        # same as in preProcessArea, see if there were no warnings listed above.
        if fcst.endswith("...\n"):
            fcst += "     None.\n"
        # Add the $$
        fcst += "\n$$\n\n"

        # Get the forecaster name
        self._userInfo = UserInfo.UserInfo()
        forecasterName = self._userInfo._getForecasterName(argDict)

        #add a notice, if needed
        if self._notice:
            self.debug_print("Debug: adding notice")
            notice = self.endline(self._notice, linelength=66, breakStr=" ")
            fcst += notice

        # Add forecaster name at bottom
        fcst = fcst + "*For detailed zone descriptions, please visit:" + \
        "\nhttp://www.nhc.noaa.gov/abouttafbprod.shtml#OWF\n" + \
        "\nNote: gridded marine forecasts are available in the National\n" + \
        "Digital Forecast Database (NDFD) at:\n" + \
        "http://www.nhc.noaa.gov/marine/grids.php\n" + \
        "\nFor additional information, please visit:\n" + \
        "http://www.nhc.noaa.gov/marine\n\n" + "$$\n\n" \
        ".Forecaster " + forecasterName + ". " + self._signature
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



# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #----- WFO ONA MIM Overrides -----

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in MIM_NC_Overrides")

    # Example of Overriding a dictionary from TextRules
    #def phrase_descriptor_dict(self, tree, node):
        #dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        #dict["PoP"] = "chance of"   #Modified from MIM base


    #Modified from TextUtils.py
    #Change start and end of day from 6am/6pm local time to 12z/00z
    def DAY(self):
        return 7 + self.daylight()
    def NIGHT(self):
        return 19 + self.daylight()
