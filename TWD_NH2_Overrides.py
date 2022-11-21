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

class TWD_NH2_Overrides:
    def __init__(self):
        pass

#     def _validLabel(self, fcst, argDict):
#
#         curTime = argDict.get("creationTime")
#         timeStr24 = time.strftime(" %a %b %e.", time.gmtime(curTime + 24*3600))
#         timeStr48 = time.strftime(" %a %b %e.", time.gmtime(curTime + 48*3600))
#
#         sfcLabel = time.strftime(" %a %b %e.", time.gmtime(curTime + 24*3600))
#
#         fcst = fcst + "SYNOPSIS VALID " + self._validTime + \
#                self.getCurrentTime(argDict, "  %a %b %e.") + \
#                "\n" + "24 hour forecast valid " + self._validTime + \
#                timeStr24 + "\n" + \
#                "48 hour forecast valid " + self._validTime + \
#                timeStr48 + "\n\n"
#
#         return fcst

    def _Text1(self):
        self.debug_print("Debug: _Text1 in TWD")
        #productDescription = ".FORECAST DISCUSSION: MAJOR FEATURES/WINDS/SEAS/SIGNIFICANT\n" \
        #                   + ".WEATHER FOR THE " + self._longProductDesc + "\n\n"
        productDescription = "Tropical Weather Discussion for North America, Central America\n" \
        "Gulf of Mexico, Caribbean Sea, northern sections of South\n" \
        "America, and Atlantic Ocean to the African coast from the\n" \
        "Equator to 31N. The following information is based on satellite\n" \
        "imagery, weather observations, radar and meteorological analysis.\n\n" \
        "Based on |*XXXX*| UTC surface analysis and satellite imagery through\n" \
        "|*XXXX*| UTC."
        return productDescription


#"|*...PUT DISCUSSION TEXT HERE...*|"

       #### ***THIS SECTION CONTROLS PREVIOUS VERSION***

    def _Text2(self):
        self.debug_print("Debug: _Text2 in TWD")
        # Include the previous TWD is requested
        previousTWD = ""

        if self._includePrevDisc != "No - blank TWD":
            self.debug_print("Debug: including previous discussion")
            #  Try to get previous TWD
            previousTWD = self.getPreviousProduct(self._textdbPil, "")
            # This gets the entire products, so grab just part without header
            #if self._debug: print "looking for :" + self._longProductDesc +"\n"
            #previousTWD = previousTWD.partition(self._longProductDesc)[2]
            previousTWD = previousTWD.partition("UTC.")[2]
            # remove the warning section too if it's headered correctly
            previousTWD = previousTWD.partition("$$")[0]
#            previousTWD = self.endline(previousTWD, linelength=66, breakStr=" ")

            #  add a line and note to separate the two.
            if self._includePrevDisc == "Yes - update - both forecaster names":
                self.debug_print("Debug: Adding PREVIOUS DISCUSSION line")
                previousTWD = "\n\n-----------------------------------------------------------------\n" \
                    + "PREVIOUS DISCUSSION..." + previousTWD
        else:
            self.debug_print("Debug: NOT including previous discussion")
        return  previousTWD #+ "\n"

    def generateForecast(self, argDict):
        self.debug_print("Debug: generateForecast in TWD")
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
        #fcst = string.replace(fcst, "HURRICANE", "HURRICANE WARNING")
        #fcst = string.replace(fcst, "TROPICAL STORM", "TROPICAL STORM WARNING")
        fcst = fcst.replace("HURRICANE WARNING FORCE", "HURRICANE FORCE WIND WARNING")
        #fcst = string.replace(fcst, "STORM", "STORM WARNING")
        #fcst = string.replace(fcst, "GALE", "GALE WARNING")
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

# added 11/06/16 to account for time change...EST added

#     def _determineTimeRanges(self, argDict):
#         # Set up the Narrative Definition and initial Time Range
#         #self._issuanceInfo = self.getIssuanceInfo(
#         #    self._productIssuance, self._issuance_list(argDict))
#         #self._timeRange = self._issuanceInfo.timeRange()
#         #argDict["productTimeRange"] = self._timeRange
#         #self._expireTime = self._issuanceInfo.expireTime()
#         #self._issueTime = self._issuanceInfo.issueTime()
#         #self._definition["narrativeDef"] = self._issuanceInfo.narrativeDef()
#         #if self._periodCombining:
#         #    self._definition["methodList"] = \
#         #       [self.combineComponentStats, self.assembleChildWords]
#         #else:
#         #    self._definition["methodList"] = [self.assembleChildWords]
# 
#         # Calculate current times
#         localTimeZone = time.strftime("%Z")
#         if localTimeZone == "EDT":
#            self._ddhhmmTime = self.getCurrentTime(
#            argDict, "%d%H%M", shiftToLocal=0, stripLeading=0)
#            staticIssueTime=re.sub(r'(\d{3,4} [AP]M).*',r'\1',self._productIssuance)
#            self._timeLabel =  staticIssueTime + " " + self.getCurrentTime(
#                argDict, " %Z %a %b %e %Y", stripLeading=1)
#         # Re-calculate issueTime
#            self._issueTime = self.strToGMT(staticIssueTime)
#            validTimeDict = {
#             "205 AM": 205,
#             "805 AM": 805,
#             "205 PM": 205,
#             "805 PM": 805,
#             }
#            validTime = validTimeDict[self._productIssuance] - 205
#            self._validTime = `validTime`.zfill(4) + " EDT"
# 
#         else:
#            self._ddhhmmTime = self.getCurrentTime(
#            argDict, "%d%H%M", shiftToLocal=0, stripLeading=0)
#            staticIssueTime=re.sub(r'(\d{3,4} [AP]M).*',r'\1',self._productIssuance)
#            self._timeLabel =  staticIssueTime + " " + self.getCurrentTime(
#                argDict, " %Z %a %b %e %Y", stripLeading=1)
#         # Re-calculate issueTime
#            self._issueTime = self.strToGMT(staticIssueTime)
#            validTimeDict = {
#             "105 AM": 105,
#             "705 AM": 705,
#             "105 PM": 105,
#             "705 PM": 705,
#             }
#            validTime = validTimeDict[self._productIssuance] - 205
#            self._validTime = `validTime`.zfill(4) + " EST"
#         #expireTimeRange = self.IFP().TimeRange(self._expireTime, self._expireTime + 3600)
#         #self._expireTimeStr = self.timeDisplay(expireTimeRange, "", "", "%d%H%M", "")
#         return None


    ########################################################################
    # PRODUCT-SPECIFIC METHODS
    ########################################################################
    def _issuance_list(self, argDict):
        #  This method sets up configurable issuance times with associated
        #  narrative definitions.  See the Text Product User Guide for documentation.
        if self._definition["includeEveningPeriod"] == 1:
            narrativeDefAM = [
                ("OFFPeriod", "period1"),
                ("OFFPeriod", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12),
                ("OFFPeriodMid", 12),
                ("OFFExtended", 24), ("OFFExtended", 24)
                ]
            narrativeDefPM = [
                ("OFFPeriod", "period1"),
                ("OFFPeriod", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12),
                ("OFFPeriodMid", 12),
                ("OFFExtended", 24), ("OFFExtended", 24)
                ]
        else:
            narrativeDefAM = [
                ("OFFPeriod", "period1"),
                ("OFFPeriod", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 24),
                ("OFFExtended", 24), ("OFFExtended", 24)
                ]
            narrativeDefPM = [
                ("OFFPeriod", "period1"),
                ("OFFPeriod", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 12), ("OFFPeriodMid", 24),
                ("OFFExtended", 24), ("OFFExtended", 24)
                ]


        return [
                    ("0005 UTC", self.DAY(), self.NIGHT(), 16,
                    ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("0605 UTC", "issuanceHour", self.NIGHT(), 16,
                     ".THIS AFTERNOON...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("1205 UTC", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late in the night", "early in the morning",
                     1, narrativeDefPM),
                    ("1805 UTC", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "early", "towards morning",
                     1, narrativeDefPM)
            ]
        #determine local time
#         localTimeZone = time.strftime("%Z")
#         #print "\n\n\nTime ZOne = " + localTimeZone + "\n\n\n"
#         if self._definition["pil"] == "TWDAT":
#             if localTimeZone == "EDT":
#                 return [
#                    ("205 AM", self.DAY(), self.NIGHT(), 16,
#                      ".Today...", "in the morning", "in the afternoon",
#                      1, narrativeDefAM),
#                     ("805 AM", "issuanceHour", self.NIGHT(), 16,
#                      ".THIS AFTERNOON...", "early", "towards evening",
#                      1, narrativeDefAM),
#                     ("205 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
#                      ".Tonight...", "late in the night", "early in the morning",
#                      1, narrativeDefPM),
#                     ("805 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
#                      ".Overnight...", "early", "towards morning",
#                      1, narrativeDefPM)
#                     ]
#             else:
#                     return [
#                     ("105 AM", self.DAY(), self.NIGHT(), 16,
#                      ".Today...", "in the morning", "in the afternoon",
#                      1, narrativeDefAM),
#                     ("705 AM", "issuanceHour", self.NIGHT(), 16,
#                      ".This afternoon...", "early", "towards evening",
#                      1, narrativeDefAM),
#                     ("105 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
#                      ".Tonight...", "late in the night", "early in the morning",
#                      1, narrativeDefPM),
#                     ("705 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
#                      ".Overnight...", "early", "towards morning",
#                      1, narrativeDefPM),
#                     ]

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #----- WFO ONA TWD Overrides -----

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in TWD_NC_Overrides")

    # Example of Overriding a dictionary from TextRules
    #def phrase_descriptor_dict(self, tree, node):
        #dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        #dict["PoP"] = "chance of"   #Modified from TWD base


    #Modified from TextUtils.py
    #Change start and end of day from 6am/6pm local time to 12z/00z
    def DAY(self):
        return 7 + self.daylight()
    def NIGHT(self):
        return 19 + self.daylight()

