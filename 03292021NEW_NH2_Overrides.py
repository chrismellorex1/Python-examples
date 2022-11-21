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

class NEW_NH2_Overrides:
    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #----- WFO ONA OFF Overrides -----

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in OFF_NC_Overrides")

    # Example of Overriding a dictionary from TextRules
    #def phrase_descriptor_dict(self, tree, node):
        #dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        #dict["PoP"] = "chance of"
        #return dict

    #Modified from OFF base
    def _Text1(self):
        self.debug_print("Debug: _Text1 in NEW_NH2_Overrides")

        #Determine which product
        if self._definition["pil"] == "NEWNT4":
            return "OFFSHORE WATERS FORECAST FOR THE GULF OF MEXICO\n\n" + \
                   "SEAS GIVEN AS SIGNIFICANT WAVE HEIGHT...WHICH IS THE AVERAGE\n" + \
                   "HEIGHT OF THE HIGHEST 1/3 OF THE WAVES. INDIVIDUAL WAVES MAY BE\n" + \
                   "MORE THAN TWICE THE SIGNIFICANT WAVE HEIGHT.\n\n"
        else:
            #OFFNT3
            return "OFFSHORE WATERS FORECAST FOR THE TROPICAL N ATLANTIC FROM 07N TO\n" + \
                   "22N BETWEEN 55W AND 64W...AND THE CARIBBEAN SEA.\n\n" + \
                   "SEAS GIVEN AS SIGNIFICANT WAVE HEIGHT...WHICH IS THE AVERAGE\n" + \
                   "HEIGHT OF THE HIGHEST 1/3 OF THE WAVES. INDIVIDUAL WAVES MAY BE\n" + \
                   "MORE THAN TWICE THE SIGNIFICANT WAVE HEIGHT.\n\n"

    #Modified from OFF base
    def _Text2(self):
        self.debug_print("Debug: _Text2 in NEW_NH2_Overrides")

        #  Try to get Synopsis from previous CWF
        if self._definition["synopsisUGC"] == "GMZ001":

            productID = "MIAOFFNT4"
            synopsis = self.getPreviousProduct(productID, "SYNOPSIS")
            #  Clean up the previous synopsis
            synopsis = re.sub(r'\n', r' ', synopsis)
            synopsis = re.sub(r'  ', r' ', synopsis)
            synopsis = self._synopsisHeading + synopsis
            synopsis = self.endline(synopsis, linelength=65, breakStr=" ")

            #  Convert absolute time pointer to a tuple of values like that
            #  returned by time.gmtime()
            #expTuple = time.strptime('%s' % (self._expireTime),
            #                         '%b %d %y %H:%M:%S GMT')
            expTuple = self._expireTime.utctimetuple()

            #  Format expiration time for inclusion in synopsis header
            expTime = time.strftime('%d%H%M', expTuple)

            return "%s-%s-\n" % ("GMZ001", expTime) + \
                   "%s\n" %  "SYNOPSIS FOR THE GULF OF MEXICO" + \
                   "%s\n" % self._timeLabel + "\n" + \
                   synopsis + "\n$$\n\n"

        else:

            productID = "MIAOFFNT3"
            synopsis = self.getPreviousProduct(productID, "SYNOPSIS")
            #  Clean up the previous synopsis
            synopsis = re.sub(r'\n', r' ', synopsis)
            synopsis = re.sub(r'  ', r' ', synopsis)
            synopsis = self._synopsisHeading + synopsis
            synopsis = self.endline(synopsis, linelength=65, breakStr=" ")

            #  Convert absolute time pointer to a tuple of values like that
            #  returned by time.gmtime()
            #expTuple = time.strptime('%s' % (self._expireTime),
            #                         '%b %d %y %H:%M:%S GMT')
            expTuple = self._expireTime.utctimetuple()

            #  Format expiration time for inclusion in synopsis header
            expTime = time.strftime('%d%H%M', expTuple)

            return"%s-%s-\n" % ("AMZ001", expTime) + \
                  "%s\n" %  "SYNOPSIS FOR CARIBBEAN SEA AND TROPICAL N ATLANTIC FROM 07N TO" + \
                  "%s\n" %  "19N BETWEEN 55W AND 64W" + \
                  "%s\n" % self._timeLabel + "\n" + \
                  synopsis + "\n$$\n\n"

    def _Text3(self):
        synopsis2 = ""
##        if self._definition["synopsis2UGC"] == "AMZ088":
        if self._definition["pil"] == "OFFNT3":
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
            synopsis2 = self._synopsisHeading + synopsis2
            synopsis2 = self.endline(synopsis2, linelength=65, breakStr=" ")

            #  Convert absolute time pointer to a tuple of values like that
            #  returned by time.gmtime()
            expTuple = self._expireTime.utctimetuple()

            #  Format expiration time for inclusion in synopsis header
            expTime = time.strftime('%d%H%M', expTuple)

            return "%s-%s-\n" % ("AMZ101", expTime) + \
                   "%s\n" %  "SYNOPSIS FOR THE SW N ATLANTIC INCLUDING THE BAHAMAS" + \
                   "%s\n" % self._timeLabel + "\n" + \
                   synopsis2 + "\n$$\n\n"
        else:
            pass

    # copy directly from OFF_TextProduct. only modify to add second synopsis
    def generateForecast(self, argDict):
        # Get variables
        error = self._getVariables(argDict)
        if error is not None:
            return error

        # Get the areaList -- derived from defaultEditAreas and
        # may be solicited at run-time from user if desired
        self._areaList = self.getAreaList(argDict)
        if not self._areaList:
            return "WARNING -- No Edit Areas Specified to Generate Product."

        # Determine time ranges
        error = self._determineTimeRanges(argDict)
        if error is not None:
            return error

        # Sample the data
        error = self._sampleData(argDict)
        if error is not None:
            return error

        # Initialize the output string
        fcst = ""
        fcst = self._preProcessProduct(fcst, argDict)

        # Generate the product for each edit area in the list
        fraction = 0
        fractionOne = 1.0/float(len(self._areaList))
        percent = 50.0
        self.setProgressPercentage(percent)
        # Need to know how many areas to process after this.
        # will insert second synopsis before the last fcst area
        areasLeft = len(self._areaList) - 1
        for editArea, areaLabel in self._areaList:
            skipAreas = self._skipAreas(argDict)
            argDict["editArea"] = (editArea, areaLabel)
            if self.currentAreaContains(argDict, skipAreas):
                continue
            self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
            fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
            fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
            fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
            # are we before the Atlantic zones?
            # if so, add synopsis2
            if areasLeft == 44:
                fcst += self._Text3()
            fraction = fractionOne
            areasLeft -= 1
            # next four print lines added for debugging of shapefile problem - 05/05/11
            print("##########################################################")
            print("EDIT AREA IS:")
            print(areaLabel)
            print("##########################################################")
        fcst = self._postProcessProduct(fcst, argDict)
        return fcst

    ########################################################################

    #added by JRL 11/05
    def gust_wind_difference_nlValue(self, tree, node):
        # Difference between gust and maxWind below which gusts are not
        # mentioned. Units are MPH

        if self._includeTropical:
            return 5
        else:
            return 10

    def temporalCoverage_hours(self, parmHisto, timeRange, componentName):
        # COMMENT: At WFO MFL we use 3 hrly wind grids. If you use 1 hrly wind grids
        # and this parameter is 2 or higher, tropical cyclone winds affecting the very
        # early or latter part of a forecast period might be neglected. 1 assures
        # maximum sensitivity.

        # CJ commented out
##        if self._includeTropical:
##            return 1
##        else:
##            return 0

        return 1

    def temporalCoverage_hours_dict(self, parmHisto, timeRange, componentName):
        # This is the temporalCoverage_hours specified per weather element.
        # Used by temporalCoverage_flag
        return {
                "PoP": 2.0,
                "Wx": 2.0,
                "Wind": 3,
                "Swell": 3,
                "pws34": 4,
                "pws64": 4,
                "pwsD34": 4,
                "pwsN34": 4,
                "pwsD64": 4,
                "pwsN64": 4,
                }

    def addTropical(self, analysisList, phraseList, includeHazards=True):
        newAnalysisList = []
        for entry in analysisList:
            #  Sampling defined as a tuple (field, statistic, temporal rate)
            #  If this is NOT a Wind or WindGust statistic
            if entry[0] not in ["Hazards", "Wind", "WindGust", "WaveHeight", "Swell"]:
                #  Add this statistic to the new analysisList
                newAnalysisList.append(entry)
        newAnalysisList += [
                ("Wind", self.vectorModeratedMinMax, [6]),
                ("WindGust", self.moderatedMinMax, [6]),
                ("WaveHeight", self.moderatedMax, [6]),
                ("Swell", self.vectorModeratedMinMax, [6]),
                ("pws34", self.maximum),
                ("pws64", self.maximum),
                ("pwsN34", self.maximum),
                ("pwsN64", self.maximum),
                ("pwsD34", self.maximum),
                ("pwsD64", self.maximum),
                ]
        if includeHazards:
            newAnalysisList.append(("Hazards", self.discreteTimeRangesByKey))

        phraseList.insert(0, self.pws_phrase)
        return newAnalysisList, phraseList

    # SampleAnalysis overrides
    def moderated_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
        if self._includeTropical:
            dict["Wind"] = (0, 0) #JL changed this to 0,0 because the Headlines were not matching
            #the deterministic values (for example, Hurricane Warning with only 35 to 45 KT in the text 10/14/14).
            dict["WindGust"] = (0, 15)
            dict["WaveHeight"] = (15, 10)
            dict["Swell"] = (15, 10)
        else:
            dict["Wind"] = (10, 10)
            dict["WindGust"] = (10, 0)
            dict["WaveHeight"] = (15, 10)
            dict["Swell"] = (10, 10)
#        dict["Wind"] =  (0, 3)
#        dict["WaveHeight"] = (5,5)
        return dict

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] =  3  #changed from 2 to 3 ERA 10/15/14       # Changed to 1 (from 2) by JL/1/31/12 for testing
        #dict["WindWaveHgt"] =  2
        dict["Wind"] = 5 # Changed to 5 (from 10) by JL/1/31/12 for testing
        dict["WindGust"] = 250
        dict["Swell"] =  5
        dict["Visibility"] = 5 # in nautical miles. Report if less than this value.
        return dict

    # ConfigVariables Overrides
    def phrase_descriptor_dict(self, tree, node):
        # Descriptors for phrases
        dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        dict["Wind"] = "winds"
        dict["WaveHeight"] = "seas"
        dict["seas"] = "seas"
        dict["mixed swell"] = "mixed swell"
        dict["waves"] = "seas"
        dict["dominant period"] = "dominant period"
        # Apply only if marine_wind_flag (see above) is set to 1:
        dict["hurricane force winds to"] =  "hurricane force winds to"
        dict["storm force winds to"] = "storm force winds to"
        dict["gales to"] =  "gales to"
        dict["up to"] =  "LESS THAN"
        dict["around"] = ""
        # Used for Tropical
        dict["iminHR"] = "HURRICANE CONDITIONS"
        dict["iminTS"] = "TROPICAL STORM CONDITIONS"
        dict["iminTSposHR"] = "TROPICAL STORM CONDITIONS WITH HURRICANE CONDITIONS POSSIBLE"
        dict["posTS"] = "TROPICAL STORM CONDITIONS POSSIBLE"
        dict["posTSbcmgposHR"] = "TROPICAL STORM CONDITIONS POSSIBLE WITH HURRICANE CONDITIONS ALSO POSSIBLE"
        dict["expTS"] = "TROPICAL STORM CONDITIONS EXPECTED"
        dict["posHR"] = "HURRICANE CONDITIONS POSSIBLE"
        dict["expHR"] = "HURRICANE CONDITIONS EXPECTED"
        dict["expTSposHR"] = "TROPICAL STORM CONDITIONS EXPECTED WITH HURRICANE CONDITIONS POSSIBLE"
        dict["posTSorHR"] = "TROPICAL STORM OR HURRICANE CONDITIONS POSSIBLE"
        return dict

    def first_null_phrase_dict(self, tree, node):
        # Phrase to use if values THROUGHOUT the period or
        # in the first period are Null (i.e. below threshold OR NoWx)
        # E.g.  LIGHT WINDS.    or    LIGHT WINDS BECOMING N 5 MPH.
        dict = TextRules.TextRules.first_null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "seas 2 ft or less"
        #dict["WindWaveHgt"] =  "seas 1 ft or less"
        dict["Wind"] =  "VARIABLE WINDS LESS THAN 5 KT"
        dict["Swell"] =  ""
        return dict

    def null_phrase_dict(self, tree, node):
        # Phrase to use for null values in subPhrases other than the first
        # Can be an empty string
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  ""  #changed from "2 feet or less" to help with repetitive wording 10/01/14 era
        #dict["WindWaveHgt"] =  "1 feet or less"
        dict["Wind"] =  "VARIABLE LESS THAN 5 KT"
        dict["Wx"] =  ""
        dict["Swell"] =  "light"
        dict["hurricane force winds to"] =  "hurricane force winds to"
        dict["storm force winds to"] = "storm force winds to"
        dict["gales to"] =  "gales to"
        dict["up to"] =  "VARIABLE WINDS LESS THAN 5 KT"
        return dict

    def phrase_connector_dict(self, tree, node):
        # Dictionary of connecting phrases for various
        # weather element phrases
        # The value for an element may be a phrase or a method
        # If a method, it will be called with arguments:
        #   tree, node
        dict = TextRules.TextRules.phrase_connector_dict(self, tree, node)
        dict["rising to"] =  {
                                "Wind": "...INCREASING to ",
                                "Swell": "...building to ",
                                "Swell2": "...building to ",
                                "WaveHeight": "...building to ",
                                "WindWaveHgt": "...building to ",
                         }

        dict["easing to"] =  {
                                "Wind": "...diminishing to ",
                                "Swell": "...subsiding to ",
                                "Swell2": "...subsiding to ",
                                "WaveHeight": "...subsiding to ",
                                "WindWaveHgt": "...subsiding to ",
                         }
        dict["backing"] =  {
                                "Wind": "...SHIFTING TO ",
                                "Swell": "...becoming ",
                                "Swell2": "...becoming ",
                                "WaveHeight": "...becoming ",
                                "WindWaveHgt": "...becoming ",
                         }

        dict["veering"] =  {
                                "Wind": "...SHIFTING TO  ",
                                "Swell": "...becoming ",
                                "Swell2": "...becoming ",
                                "WaveHeight": "...becoming ",
                                "WindWaveHgt": "...becoming ",
                         }

        dict["becoming"] =  "...becoming "
        dict["increasing to"] =  {
                                "Wind":  "...INCREASING to ",
                                "Swell": "...building to ",
                                "Swell2": "...building to ",
                                "WaveHeight": "...building to ",
                                "WindWaveHgt": "...building to ",
                             }
        dict["decreasing to"] =  {
                                "Wind":  "...diminishing to ",
                                "Swell": "...subsiding to ",
                                "Swell2": "...subsiding to ",
                                "WaveHeight": "...subsiding to ",
                                "WindWaveHgt": "...subsiding to ",
                             }
        dict["shifting to the"] =  {
                                  "Wind":  "...shifting ",
                                  "Swell": "...becoming ",
                                  "Swell2": "...becoming ",
                                  "WaveHeight": "...becoming ",
                                  "WindWavHgt": "...becoming ",
                             }
#        dict["shifting to the"] =  "...shifting " Corrected wave heights "shifting" with above entries EC - 04/19/12
        dict["becoming onshore"] =  " becoming onshore "
        dict["then"] =  {"Wx": ". ",
                         "Vector": "...becoming ",
                         "Scalar": "...becoming ",
                         #"otherwise": "...becoming ",
                         "otherwise": "...BECOMING ", #Changed BACK to BECOMING for "SEAS 2 FT OR LESS...BECOMING 3 FT" -JL/10/28/14
                                                        #AS THIS IMPACTS BOTH BUILDING AND SUBSIDING
                         }
        return dict

    # added by JRL 11/05
    def maximum_range_nlValue_dict(self, tree, node):
        # Maximum range to be reported within a phrase
        #   e.g. 5 to 10 mph
        # Units depend on the product
        dict = TextRules.TextRules.maximum_range_nlValue_dict(self, tree, node)
        #-----------------------------------------------------------------------
        # COMMENT: Override max ranges for certain fields
        # This dict specifications allows for wind speed ranges of up to 20 mph
        # during tropical cyclone situations allowing for far better wind speed
        # phrases.
        #-----------------------------------------------------------------------
        if self._includeTropical:
            dict["Wind"] = {'default': 5,
                            (0.0, 4.0): 0,
                            (4.0, 33.0): 5,
                            (33.0, 52.0): 10,
                            (52.0, 200.0): 20,
                            }
        else:
            dict["Wind"] = {
            (0, 25): 5,
            (25, 50): 10,
            (50, 200): 25,
            "default": 10,
            }
            dict["Swell"] = {
            (0, 3): 1,
            (3, 7): 2,
            (7, 10): 3,
            (10, 20): 5,
            (20, 200): 10,
            "default": 5,
            }
            dict["Swell2"] = {
            (0, 3): 1,
            (3, 7): 2,
            (7, 10): 3,
            (10, 20): 5,
            (20, 200): 10,
            "default": 5,
            }

            #added by ERA 09/29/14 (old TAFB)
            dict["WaveHeight"] = {
             (1, 3): 0, # changed from 0 to 1 JL/1/31/12
             (3, 7): 2,
             (7, 10): 3,
             (10, 20): 5,
             (20, 200): 10,
             "default": 5,
             }
            #commented by ERA 09/29/14 (OPC)
#             dict["WaveHeight"] = {
#             (0,1):1,
#             (1,4):2,
#             (4,6):3,
#             (6,8):4,
#             (8,10):5,
#             (10,12):6,
#             (12,14):7,
#             (14,16):8,
#             (16,18):9,
#             (18,20):10,
#             (20,200):15,
#             "default":5,
#             }
        dict["WindWaveHgt"] = 2

# commented out TAFB's old def and replaced with OPC's above (except kept TAFB's wind def) JL/8/23/2014
#
#         dict["Swell"] = 5
#         dict["Swell2"] = 5
        #dict["WaveHeight"] = 2
        #dict["WindWaveHgt"] = 2
        return dict

    #commented out era 09/30/14

    # added to force ranges for sea heights with tropical turned on 9/7/11 CNJ/JL
    #commented out below as OPC does not have this - JL/08/23/2014
#     def minimum_range_nlValue_dict(self, tree, node):
#         # This threshold is the "smallest" min/max difference allowed between values reported.
#         # For example, if threshold is set to 5 for "MaxT", and the min value is 45
#         # and the max value is 46, the range will be adjusted to at least a 5 degree
#         # range e.g. 43-48.  These are the values that are then submitted for phrasing
#         # such as:
#         dict = TextRules.TextRules.minimum_range_nlValue_dict(self, tree, node)
#         #   HIGHS IN THE MID 40S
#         if self._includeTropical:
#             dict["WaveHeight"] = {
#             (0,1):1,
#             (1,4):2,
#             (4,6):3,
#             (6,8):4,
#             (8,10):5,
#             (10,12):6,
#             (12,14):7,
#             (14,16):8,
#             (16,18):9,
#             (18,20):10,
#             (20,200):15,
#             "default":5,
#             }
#         return dict


    def vector_mag_difference_nlValue_dict(self, tree, node):
        # Replaces WIND_THRESHOLD
        # Magnitude difference.  If the difference between magnitudes
        # for sub-ranges is greater than or equal to this value,
        # the different magnitudes will be noted in the phrase.
        # Units can vary depending on the element and product
        return  {
#            "Wind": 9,
            "Wind": {
                (0, 12): 10,
                (12, 25): 5,
                (25, 45): 10,
                (45, 70): 15,
                (70, 200): 20,
                "default": 5,
            },
#            "Swell": 5,  # ft
            "Swell": {
                (0, 3): 1,
                (3, 7): 2,
                (7, 10): 3,
                (10, 20): 5,
                (20, 200): 10,
                "default": 5,
                }, # feet
            "Swell2": {
                (0, 3): 1,
                (3, 7): 2,
                (7, 10): 3,
                (10, 20): 5,
                (20, 200): 10,
                "default": 5,
                }, # feet
 #           "Swell2": 5,  # ft
            "otherwise": 5,
            }
#         return  {
#             "Wind": 4,
#             "Swell": 1,  # ft
#             "Swell2": 1,  # ft
#             }
# commented out the above and replaced with OPC's def - JL/08/23/2014

    def vector_dir_difference_dict(self, tree, node):
        # Replaces WIND_DIR_DIFFERENCE
        # Direction difference.  If the difference between directions
        # for sub-ranges is greater than or equal to this value,
        # the different directions will be noted in the phrase.
        # Units are degrees
        return {
            "Wind": 45, # degrees (Was 90 for TAFB)
            "Swell": 60, # degrees
            "Swell2": 60, # degrees
            }

    def element_outUnits_dict(self, tree, node):
        dict = TextRules.TextRules.element_outUnits_dict(self, tree, node)
        dict["Visibility"] = "NM"
        return dict

    def scalar_difference_nlValue_dict(self, tree, node):
        # Scalar difference.  If the difference between scalar values
        # for 2 sub-periods is greater than or equal to this value,
        # the different values will be noted in the phrase.
        return {
           # "WaveHeight": 2.5, #0, # in feet
             "WaveHeight":       {
                 (0, 2): 1, #CHANGED FROM 1 ERA 09/30/14
                 (2, 4): 2,
                 (4, 7): 3,
                 (7, 11): 4,
                 (11, 16): 5,
                 (16, 22): 6,
                 (22, 29): 7,
                 (29, 37): 8,
                 (37, 46): 9,
                 (46, 56): 10,
                 (56, 67): 11,
                 (67, 79): 12,
                 (79, 92): 13,
                 (92, 106): 14,
                 (106, 200): 15,
                 "default": 5,
                 }, #0, # in feet
             }
#         return {
#             "WaveHeight": 3, # feet - changed from 2.5 to 2 - JL/1/31/12
#                              # feet - changed from 2 to 3 - EC/4/20/12 Seems to correct "SEAS 1 FOOT...BUILDING TO 2 TO 3 FT IN AFTERNOON" issues.
#             }
# commented out the above and replaced with OPC's def - JL/08/23/2014

#taken from mfl to test 10/01/14 era
#     def wave_range(self, avg):
#         # Make wave ranges based off the average wave value
#         table = ((0, "less than 1 foot"), (1, "less than 2 feet"),
#                  (2, "around 2 feet"),
#                  (3, "2 to 3 feet"), (4, "2 to 4 feet"),
#                  (5, "3 to 5 feet"), (6, "4 to 6 feet"),
#                  (7, "5 to 7 feet"), (8, "6 to 8 feet"),
#                  (9, "7 to 9 feet"),(10, "8 to 10 feet"),
#                  (11, "9 to 11 feet"),(12, "10 to 12 feet"),
#                  (13, "11 to 13 feet"),(14, "12 to 14 feet"),
#                  (15, "13 to 15 feet"),(16, "14 to 17 feet"),
#                  (17, "15 to 18 feet"),(18, "16 to 20 feet"),
#                  (19, "17 to 21 feet"),(20, "18 to 22 feet"),
#                  (100, "over 20 feet"))
#         range = ""
#         for max, str in table:
#             if avg <= max:
#                 range = str
#                 break
#         return range
#
#     def wave_words(self, tree, node): #5/15/12
#         # Return a phrase for wave and optionally Period for the given subPhrase
#         elementInfo = node.getAncestor("firstElement")
#         elementName = elementInfo.name
#         statDict = node.getStatDict()
#         if statDict is None:
#             return self.setWords(node,"")
#         wave = self.getStats(statDict, elementName)
#         if wave is None:
#             return self.setWords(node, "")
#         min, max = self.getValue(wave, "MinMax")
# #         alpha = self.HiOneTenth(max)  #5/7/12
# #         print "alpha=", alpha  #5/7/12
#
#        # threshold = self.nlValue(self.null_nlValue(
#        #     tree, node, elementName, elementName), max)
#        # if int(min) < threshold and int(max) < threshold:
#        #     return self.setWords(node, "null")
#
#         waveStr = self.getScalarRangeStr(tree, node, elementName, min, max)
#         units = self.units_descriptor(tree, node, "units", "ft")
#         waveUnit = self.units_descriptor(tree, node, "unit", "ft")
#         if int(min) == 1 and int(max) == 1:
#             units = waveUnit
#
# #         avg = (min + max)/2
# #         #words = self.wave_range(avg)  #5/7/12
# #         words = self.wave_range(avg)
# #         alpha = round(alpha)  #5/7/12
# #         alpha = int(alpha)  #5/7/12
# #
# #         if avg in range (0,3) or alpha in range (0,5): #5/16/12
# #             words = words
# #         else:
# #             words = words + " with occasional seas to " + str(alpha) + " feet"  #5/7/12
# #         print "/n/nWORDS", words  #5/7/12
#
#         words = waveStr + " " + units
# #         if "Period" in statDict.keys():
# #             period = self.getStats(statDict, "Period")
# #             if period is not None:
# #                 mode = self.getValue(period, "Mode")
# #                 periodUnits = self.units_descriptor(tree, node, "units", "s")
# #                 periodUnit = self.units_descriptor(tree, node, "unit", "s")
# #                 mode = int(mode)
# #                 if mode == 1:
# #                     periodUnits = periodUnit
# #                 periodDescriptor = self.phrase_descriptor(
# #                     tree, node, "dominant period", elementName)
# #                 words = words + " " + periodDescriptor + " " + `mode` + " " + periodUnits
#         return self.setWords(node, words)



#     def waveht_scalar_value(self,tree,node,elementName,elementName1):
#         # calculating the scalar value for changes based on wave height
#         wave = tree.stats.get("WaveHeight", node.getTimeRange(), node.getAreaLabel(),
#                                              mergeMethod="Max")
# #        print wave, "Wave!"
#         if wave is None:
#             return 10
#         if wave <= 6:
#             rtnval = 6
#         else:
#             val = wave * .25
#             rtnval = int(val+0.5)

    # WxPhrases Overrides
    def pop_wx_lower_threshold(self, tree, node):
        # Always report weather
        return 0

    # MarinePhrases Overrides
    def seasWaveHeight_element(self, tree, node):
        # Weather element to use for reporting seas
        # "COMBINED SEAS 10 TO 15 FEET."
        # IF above wind or swell thresholds
        return "WaveHeight"

    def waveHeight_wind_threshold(self, tree, node):
        # wind value above which waveHeight is reported vs. wind waves
        # Unit is knots
        return 0

    ## This entry below is likely the cause for Period Combining issues at periods 6-8 - JL/NHC 02/12/12
    def splitDay24HourLabel_flag(self, tree, node):
        # Return 0 to have the TimeDescriptor module label 24 hour periods
        # with simply the weekday name (e.g. SATURDAY)
        # instead of including the day and night periods
        # (e.g. SATURDAY AND SATURDAY NIGHT)
        # NOTE: If you set this flag to 1, make sure the "nextDay24HourLabel_flag"
        # is set to zero.
        # NOTE: This applied only to periods that are exactly 24-hours in length.
        # Periods longer than that will always be split into day and night labels
        # (e.g. SUNDAY THROUGH MONDAY NIGHT)
        compName = node.getComponentName()
        if compName == "OFFExtended":
              return 0
        else:
              return 1

    def wxTypeDescriptors(self):
        # This is the list of coverages, wxTypes, intensities, attributes for which special
        # weather type wording is desired.  Wildcards (*) can be used to match any value.
        # If a weather subkey is not found in this list, default wording
        # will be used from the Weather Definition in the server.
        # The format of each tuple is:
        #    (coverage, wxType, intensity, attribute, descriptor)
        # NOTE: descriptor can be a method taking (tree, node, subkey) as arguments
           list = TextRules.TextRules.wxTypeDescriptors(self)
           list.append (("*", "R", "*", "*", "showers"))
           list.append (("*", "S", "*", "*", "showers"))
           list.append (("*", "VA", "*", "*", "volcanic ash"))
           #list.append (("*", "F", "*", "*", "fog"))
           #list.append (("*", "T","*", "*", "tstms"))
           return list

    def wxCoverageDescriptors(self):
        # This is the list of coverages, wxTypes, intensities, attributes for which special
        # weather coverage wording is desired.  Wildcards (*) can be used to match any value.
        # If a weather subkey is not found in this list, default wording
        # will be used from the Weather Definition in the server.
        # The format of each tuple is:
        #    (coverage, wxType, intensity, attribute, descriptor)
        # For example:
        #return [
        #    ("Chc", "*", "*", "*", "a chance of"),
        #    ]
        # NOTE: descriptor can be a method taking (tree, node, subkey) as arguments
           list = TextRules.TextRules.wxCoverageDescriptors(self)
           list.append (("Wide", "*", "*", "*", "scattered"))
           return list


     ########################################################################
    # ADDED CODE BY MUSONDA TO GIVE WIND DIRECTION RANGE LIKE N TO NE

    def dirList(self):
        dirSpan = 22.5
        base = 11.25
        return[
            ('N', 360-base, 361),
            ('N', 0, base),
            ('N TO NE', base, base+1*dirSpan),
            ('NE', base+1*dirSpan, base+2*dirSpan),
            ('NE TO E', base+2*dirSpan, base+3*dirSpan),
            ('E', base+3*dirSpan, base+4*dirSpan),
            ('E TO SE', base+4*dirSpan, base+5*dirSpan),
            ('SE', base+5*dirSpan, base+6*dirSpan),
            ('SE TO S', base+6*dirSpan, base+7*dirSpan),
            ('S', base+7*dirSpan, base+8*dirSpan),
            ('S TO SW', base+8*dirSpan, base+9*dirSpan),
            ('SW', base+9*dirSpan, base+10*dirSpan),
            ('SW TO W', base+10*dirSpan, base+11*dirSpan),
            ('W', base+11*dirSpan, base+12*dirSpan),
            ('W TO NW', base+12*dirSpan, base+13*dirSpan),
            ('NW', base+13*dirSpan, base+14*dirSpan),
            ('NW TO N', base+14*dirSpan, base+15*dirSpan),
            ]

    # J.Lewitsky/NHC 04/15/11 uncommented section below to include Local Effects
    def repeatingEmbedded_localEffect_threshold(self, tree, component):
        # Number of embedded local effect phrases allowed in a component
        # before they are gathered together into a conjunctive local
        # effect clause.  For example, with the threshold set to 2:
        #
        # Instead of:
        #     Cloudy windward and partly cloudy leeward.
        #     Rain likely windward and scattered showers leeward.
        #     Chance of precipitation 50 percent windward and 30
        #     percent leeward.
        #
        # We will produce:
        #     Windward...Cloudy...Rain likely...Chance of precipitation 50 percent.
        #     Leeward...Partly cloudy...Scattered showers...Chance of precipitation
        #     30 percent.
        #
        # NOTE:  If we have even one conjunctive local effect, however, all will be left
        #     conjunctive.  For example, instead of:
        #
        #     Cloudy windward and partly cloudy leeward.
        #     Windward...Rain likely in the morning.
        #     Leeward...Scattered showers in the afternoon.
        #
        #  We will produce:
        #     Windward...Cloudy...Rain likely in the morning.
        #     Leeward...Partly cloudy...Scattered showers in the afternoon.
        #
       return 1

    ########################################################################
    # COMPONENT PRODUCT DEFINITIONS
    ########################################################################

    def _PoP_analysisMethod(self, componentName):
        # Alternative PoP analysis methods for consistency between PoP and Wx
        #return self.maxMode
        #return self.maximum
        return self.stdDevMaxAvg

    def OFFPeriod(self):
#            type = "component",
##            methodList = [
##                          self.consolidateSubPhrases,
##                          self.assemblePhrases,
##                          self.wordWrap,
##                          ],

            analysisList = [
                      # NOTE: Choose from the following analysis options.
                      # Do not remove the "vectorMinMax" analysis for
                      # "Wind". This is necessary to get an absolute max if
                      # the useWindsForGusts flag is on.

                      # Use the following if you want moderated ranges
                      # (e.g. N WIND 10 to 20 KT)
                      # Set the moderating percentage in the "moderated_dict"
                      # dictionary module.
                      # Set the maximum range values in the "maximum_range_nlValue_dict"
                      # dictionary module.
                          ("Wind", self.vectorModeratedMinMax, [3]),
                         # ("Wind", self.vectorMinMax, [6]),
                          ("WindGust", self.moderatedMax, [3]),
                          ("WaveHeight", self.moderatedMinMax, [3]),

                          #added below based on what MFL uses 07/10/14 -JL
                          #("WaveHeight", self.moderatedMax, [6]),

                         # ("WindWaveHgt", self.moderatedMinMax, [6]),
                          ("Swell", self.vectorMax, [3]),
                          ("Swell2", self.vectorMax, [3]),
                         # ("Period", self.moderatedMinMax, [6]),
                         # ("Period2", self.moderatedMinMax, [6]),
                          ("Wx", self.rankedWx, [12]),
                         # ("T", self.minMax),
                         # ("PoP", self._PoP_analysisMethod("OFFPeriod"), [6]),
                         # ("PoP", self.binnedPercent, [6]),


                        ]

            phraseList = [
                           # WINDS
#                           (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
                            # J.Lewitsky/NHC 04/15/11 uncommented line below to include Local Effects
                           (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
                            #CJ try to remove local effects phrase
#                           self.marine_wind_phrase,
                           # Alternative:
#                           (self.marine_wind_phrase, self._windLocalEffects_list()),
#                           self.marine_wind_phrase,
                           #self.gust_phrase,
                           # WAVES
                           ## commented back out for test (commented out below on 08/24/11 - turn back on for swell wording
                           #self.wave_withPeriods_phrase,
                           # Alternative:
                           #self.wave_phrase,
                           # SWELLS AND PERIODS
                           self.wave_withPeriods_phrase,
                           # Alternative:
                           #self.swell_phrase,
                           #self.period_phrase,
                           # WEATHER
#                           self.weather_phrase,

#                           self.weather_phrase,
                           # uncommented below to include Local Effects (JL - 12/12/11)
                           #(self.wave_phrase,self._WaveHeightLocalEffects_list),
                           #self.wave_phrase,

                           self.weather_phrase,
                           self.visibility_phrase,
                           ]
            # CJ Added
            if self._includeTropical:
                analysisList, phraseList = self.addTropical(analysisList, phraseList)

            return {
                "type": "component",
                "methodList": [
                        self.consolidateSubPhrases,
                        self.assemblePhrases,
                        self.wordWrap,
                        ],

            "analysisList": analysisList,
            "phraseList": phraseList,
            "intersectAreas":[
                    #Areas listed by weather element that will be
                    #intersected with the current area then
                    #sampled and analyzed.
                    #E.g. used in local effects methods.
                ("Wind", ["le_NEW013",
                        "le_NEW013_other",
                        "le_NEW015",
                        "le_NEW015_other",
                        "le_NEW017",
                        "le_NEW017_other",
                        "le_NEW019",
                        "le_NEW019_other",
                        "le_NEW021",
                        "le_NEW021_other",
                        "le_NEW023",
                        "le_NEW023_other",
                        "le_NEW025",
                        "le_NEW025_other",
                        "le_NEW027",
                        "le_NEW027_other",
                        "le_NEW029",
                        "le_NEW029_other",
                        "le_NEW031",
                        "le_NEW031_other",
                        "le_NEW033",
                        "le_NEW033_other",
                        "le_NEWc011",
                        "le_NEWc011_other",
                        "le_NEWc013",
                        "le_NEWc013_other",
                        "le_NEWc015",
                        "le_NEWc015_other",
                        "le_NEWc017",
                        "le_NEWc017_other",
                        "le_NEWc021",
                        "le_NEWc021_other",
                        "le_NEWc023",
                        "le_NEWc023_other",
                        "le_NEWc025",
                        "le_NEWc025_other",
                        "le_NEWc027",
                        "le_NEWc027_other",
                        "le_NEWc029",
                        "le_NEWc029_other",
                        "le_NEWc031",
                        "le_NEWc031_other",
                        "le_NEWc033",
                        "le_NEWc033_other",
                        "le_NEWc035",
                        "le_NEWc035_other",
                        "le_NEWc037",
                        "le_NEWc037_other",
                        "le_NEWc039",
                        "le_NEWc039_other",
                        "le_NEWc041",
                        "le_NEWc041_other",
                        "le_NEWc043",
                        "le_NEWc043_other",
                        "le_NEWc045",
                        "le_NEWc045_other",
                        "le_NEWc047",
                        "le_NEWc047_other",
                        "le_NEWc049",
                        "le_NEWc049_other",
                        "le_NEWc051",
                        "le_NEWc051_other",
                        "le_NEWc053",
                        "le_NEWc053_other",
                        "le_NEWc055",
                        "le_NEWc055_other",
                        "le_NEW111",
                        "le_NEW111_other",
                        "le_NEW113",
                        "le_NEW113_other",
                        "le_NEW115",
                        "le_NEW115_other",
                        "le_NEW117",
                        "le_NEW117_other",
                        "le_NEW119",
                        "le_NEW119_other",
                        "le_NEW121",
                        "le_NEW121_other",
                        "le_NEW123",
                        "le_NEW123_other",
                        "le_NEW125",
                        "le_NEW125_other",
                        "le_NEW127",
                        "le_NEW127_other",
                        "le_NEW129",
                        "le_NEW129_other",
                        "le_NEW131",
                        "le_NEW131_other",
                        "le_NEW133",
                        "le_NEW133_other",
                        "le_NEW135",
                        "le_NEW135_other",
                        "le_NEW137",
                        "le_NEW137_other",
                        "le_NEW139",
                        "le_NEW139_other",
                        "le_NEW141",
                        "le_NEW141_other",
                        "le_NEW143",
                        "le_NEW143_other",
                        "le_NEW145",
                        "le_NEW145_other",
                        "le_NEW147",
                        "le_NEW147_other",
                        "le_NEW149",
                        "le_NEW149_other",
                        "le_NEW151",
                        "le_NEW151_other",
                        "le_NEW153",
                        "le_NEW153_other",
                        "le_NEW155",
                        "le_NEW155_other",
                        "le_NEW157",
                        "le_NEW157_other",
                        "le_NEW159",
                        "le_NEW159_other",
                        "le_NEW161",
                        "le_NEW161_other"
                            ]),
                ("WaveHeight", ["le_NEW013",
                        "le_NEW013_other",
                        "le_NEW015",
                        "le_NEW015_other",
                        "le_NEW017",
                        "le_NEW017_other",
                        "le_NEW019",
                        "le_NEW019_other",
                        "le_NEW021",
                        "le_NEW021_other",
                        "le_NEW023",
                        "le_NEW023_other",
                        "le_NEW025",
                        "le_NEW025_other",
                        "le_NEW027",
                        "le_NEW027_other",
                        "le_NEW029",
                        "le_NEW029_other",
                        "le_NEW031",
                        "le_NEW031_other",
                        "le_NEW033",
                        "le_NEW033_other",
                        "le_NEWc011",
                        "le_NEWc011_other",
                        "le_NEWc013",
                        "le_NEWc013_other",
                        "le_NEWc015",
                        "le_NEWc015_other",
                        "le_NEWc017",
                        "le_NEWc017_other",
                        "le_NEWc021",
                        "le_NEWc021_other",
                        "le_NEWc023",
                        "le_NEWc023_other",
                        "le_NEWc025",
                        "le_NEWc025_other",
                        "le_NEWc027",
                        "le_NEWc027_other",
                        "le_NEWc029",
                        "le_NEWc029_other",
                        "le_NEWc031",
                        "le_NEWc031_other",
                        "le_NEWc033",
                        "le_NEWc033_other",
                        "le_NEWc035",
                        "le_NEWc035_other",
                        "le_NEWc037",
                        "le_NEWc037_other",
                        "le_NEWc039",
                        "le_NEWc039_other",
                        "le_NEWc041",
                        "le_NEWc041_other",
                        "le_NEWc043",
                        "le_NEWc043_other",
                        "le_NEWc045",
                        "le_NEWc045_other",
                        "le_NEWc047",
                        "le_NEWc047_other",
                        "le_NEWc049",
                        "le_NEWc049_other",
                        "le_NEWc051",
                        "le_NEWc051_other",
                        "le_NEWc053",
                        "le_NEWc053_other",
                        "le_NEWc055",
                        "le_NEWc055_other",
                        "le_NEW111",
                        "le_NEW111_other",
                        "le_NEW113",
                        "le_NEW113_other",
                        "le_NEW115",
                        "le_NEW115_other",
                        "le_NEW117",
                        "le_NEW117_other",
                        "le_NEW119",
                        "le_NEW119_other",
                        "le_NEW121",
                        "le_NEW121_other",
                        "le_NEW123",
                        "le_NEW123_other",
                        "le_NEW125",
                        "le_NEW125_other",
                        "le_NEW127",
                        "le_NEW127_other",
                        "le_NEW129",
                        "le_NEW129_other",
                        "le_NEW131",
                        "le_NEW131_other",
                        "le_NEW133",
                        "le_NEW133_other",
                        "le_NEW135",
                        "le_NEW135_other",
                        "le_NEW137",
                        "le_NEW137_other",
                        "le_NEW139",
                        "le_NEW139_other",
                        "le_NEW141",
                        "le_NEW141_other",
                        "le_NEW143",
                        "le_NEW143_other",
                        "le_NEW145",
                        "le_NEW145_other",
                        "le_NEW147",
                        "le_NEW147_other",
                        "le_NEW149",
                        "le_NEW149_other",
                        "le_NEW151",
                        "le_NEW151_other",
                        "le_NEW153",
                        "le_NEW153_other",
                        "le_NEW155",
                        "le_NEW155_other",
                        "le_NEW157",
                        "le_NEW157_other",
                        "le_NEW159",
                        "le_NEW159_other",
                        "le_NEW161",
                        "le_NEW161_other"
                                  ]),
                    ]
                }

    #Addition - taken from MFL CWF
    def _WaveHeightLocalEffects_list(self, tree, node):
         leArea1 = self.LocalEffectArea("le_NEW013_other", "ELSEWHERE")
         leArea2 = self.LocalEffectArea("le_NEW013", "S OF 27N")
         leArea3 = self.LocalEffectArea("le_NEW015_other", "ELSEWHERE")
         leArea4 = self.LocalEffectArea("le_NEW015", "S OF 27N")
         leArea5 = self.LocalEffectArea("le_NEW017_other", "ELSEWHERE")
         leArea6 = self.LocalEffectArea("le_NEW017", "S OF 27N")
         leArea7 = self.LocalEffectArea("le_NEW019_other", "ELSEWHERE")
         leArea8 = self.LocalEffectArea("le_NEW019", "W OF 96W")
         leArea9 = self.LocalEffectArea("le_NEW021_other", "ELSEWHERE")
         leArea10 = self.LocalEffectArea("le_NEW021", "S OF 24W")
         leArea11 = self.LocalEffectArea("le_NEW023_other", "ELSEWHERE")
         leArea12 = self.LocalEffectArea("le_NEW023", "S OF 24W")
         leArea13 = self.LocalEffectArea("le_NEW025_other", "ELSEWHERE")
         leArea14 = self.LocalEffectArea("le_NEW025", "W OF 85W")
         leArea15 = self.LocalEffectArea("le_NEW027_other", "ELSEWHERE")
         leArea16 = self.LocalEffectArea("le_NEW027", "W OF 85W")
         leArea17 = self.LocalEffectArea("le_NEW029_other", "ELSEWHERE")
         leArea18 = self.LocalEffectArea("le_NEW029", "S OF 21N W OF 95W")
         leArea19 = self.LocalEffectArea("le_NEW031_other", "ELSEWHERE")
         leArea20 = self.LocalEffectArea("le_NEW031", "S OF 20N")
         leArea21 = self.LocalEffectArea("le_NEW033_other", "ELSEWHERE")
         leArea22 = self.LocalEffectArea("le_NEW033", "W OF 92W")
         leArea23 = self.LocalEffectArea("le_NEWc011_other", "ELSEWHERE")
         leArea24 = self.LocalEffectArea("le_NEWc011", "S OF 20N")
         leArea25 = self.LocalEffectArea("le_NEWc013_other", "ELSEWHERE")
         leArea26 = self.LocalEffectArea("le_NEWc013", "LEE OF CUBA")
         leArea27 = self.LocalEffectArea("le_NEWc015_other", "ELSEWHERE")
         leArea28 = self.LocalEffectArea("le_NEWc015", "E OF 82W")
         leArea29 = self.LocalEffectArea("le_NEWc017_other", "ELSEWHERE")
         leArea30 = self.LocalEffectArea("le_NEWc017", "BETWEEN CUBA AND JAMAICA")
         leArea31 = self.LocalEffectArea("le_NEWc021_other", "ELSEWHERE")
         leArea32 = self.LocalEffectArea("le_NEWc021", "S OF 17N W OF 86W")
         leArea33 = self.LocalEffectArea("le_NEWc023_other", "ELSEWHERE")
         leArea34 = self.LocalEffectArea("le_NEWc023", "S OF 17N")
         leArea35 = self.LocalEffectArea("le_NEWc025_other", "ELSEWHERE")
         leArea36 = self.LocalEffectArea("le_NEWc025", "S OF 17N")
         leArea37 = self.LocalEffectArea("le_NEWc027_other", "ELSEWHERE")
         leArea38 = self.LocalEffectArea("le_NEWc027", "S OF 17N")
         leArea39 = self.LocalEffectArea("le_NEWc029_other", "ELSEWHERE")
         leArea40 = self.LocalEffectArea("le_NEWc029", "LEE OF DOMINICAN REPUBLIC")
         leArea41 = self.LocalEffectArea("le_NEWc031_other", "ELSEWHERE")
         leArea42 = self.LocalEffectArea("le_NEWc031", "W OF 66W")
         leArea43 = self.LocalEffectArea("le_NEWc033_other", "ELSEWHERE")
         leArea44 = self.LocalEffectArea("le_NEWc033", "ATLC EXPOSURES")
         leArea45 = self.LocalEffectArea("le_NEWc035_other", "ELSEWHERE")
         leArea46 = self.LocalEffectArea("le_NEWc035", "W OF 58W")
         leArea47 = self.LocalEffectArea("le_NEWc037_other", "ELSEWHERE")
         leArea48 = self.LocalEffectArea("le_NEWc037", "WITHIN 60 NM OF COAST OF NICARAGUA")
         leArea117 = self.LocalEffectArea("le_NEWc039_other", "ELSEWHERE")
         leArea118 = self.LocalEffectArea("le_NEWc039", "N OF 13N")
         leArea49 = self.LocalEffectArea("le_NEWc041_other", "ELSEWHERE")
         leArea50 = self.LocalEffectArea("le_NEWc041", "N OF 13N")
         leArea51 = self.LocalEffectArea("le_NEWc043_other", "ELSEWHERE")
         leArea52 = self.LocalEffectArea("le_NEWc043", "S OF 13N")
         leArea53 = self.LocalEffectArea("le_NEWc045_other", "ELSEWHERE")
         leArea54 = self.LocalEffectArea("le_NEWc045", "S OF 13N")
         leArea55 = self.LocalEffectArea("le_NEWc047_other", "ELSEWHERE")
         leArea56 = self.LocalEffectArea("le_NEWc047", "ATLC EXPOSURES")
         leArea57 = self.LocalEffectArea("le_NEWc049_other", "ELSEWHERE")
         leArea58 = self.LocalEffectArea("le_NEWc049", "W OF 58W")
         leArea59 = self.LocalEffectArea("le_NEWc051_other", "ELSEWHERE")
         leArea60 = self.LocalEffectArea("le_NEWc051", "N OF 09N")
         leArea61 = self.LocalEffectArea("le_NEWc053_other", "ELSEWHERE")
         leArea62 = self.LocalEffectArea("le_NEWc053", "N OF 10N")
         leArea63 = self.LocalEffectArea("le_NEWc055_other", "ELSEWHERE")
         leArea64 = self.LocalEffectArea("le_NEWc055", "N OF 10N")
         leArea65 = self.LocalEffectArea("le_NEW111_other", "ELSEWHERE")
         leArea66 = self.LocalEffectArea("le_NEW111", "N OF 30N")
         leArea67= self.LocalEffectArea("le_NEW113_other", "ELSEWHERE")
         leArea68 = self.LocalEffectArea("le_NEW113", "N OF 30N")
         leArea69 = self.LocalEffectArea("le_NEW115_other", "ELSEWHERE")
         leArea70 = self.LocalEffectArea("le_NEW115", "N OF 30N")
         leArea71 = self.LocalEffectArea("le_NEW117_other", "ELSEWHERE")
         leArea72 = self.LocalEffectArea("le_NEW117", "W OF 68W")
         leArea73 = self.LocalEffectArea("le_NEW119_other", "ELSEWHERE")
         leArea74 = self.LocalEffectArea("le_NEW119", "W OF 63W")
         leArea75 = self.LocalEffectArea("le_NEW121_other", "ELSEWHERE")
         leArea76 = self.LocalEffectArea("le_NEW121", "W OF 58W")
         leArea77 = self.LocalEffectArea("le_NEW123_other", "ELSEWHERE")
         leArea78 = self.LocalEffectArea("le_NEW123", "N OF 28N")
         leArea79 = self.LocalEffectArea("le_NEW125_other", "ELSEWHERE")
         leArea80 = self.LocalEffectArea("le_NEW125", "N OF 28N")
         leArea81 = self.LocalEffectArea("le_NEW127_other", "ELSEWHERE")
         leArea82 = self.LocalEffectArea("le_NEW127", "N OF 28N")
         leArea83 = self.LocalEffectArea("le_NEW129_other", "ELSEWHERE")
         leArea84 = self.LocalEffectArea("le_NEW129", "W OF 68W")
         leArea85 = self.LocalEffectArea("le_NEW131_other", "ELSEWHERE")
         leArea86 = self.LocalEffectArea("le_NEW131", "W OF 63W")
         leArea87 = self.LocalEffectArea("le_NEW133_other", "ELSEWHERE")
         leArea88 = self.LocalEffectArea("le_NEW133", "W OF 58W")
         leArea89= self.LocalEffectArea("le_NEW135_other", "ELSEWHERE")
         leArea90 = self.LocalEffectArea("le_NEW135", "ATLC EXPOSURES")
         leArea91 = self.LocalEffectArea("le_NEW137_other", "ELSEWHERE")
         leArea92 = self.LocalEffectArea("le_NEW137", "W OF 73W")
         leArea93 = self.LocalEffectArea("le_NEW139_other", "ELSEWHERE")
         leArea94 = self.LocalEffectArea("le_NEW139", "W OF 68W")
         leArea95 = self.LocalEffectArea("le_NEW141_other", "ELSEWHERE")
         leArea96 = self.LocalEffectArea("le_NEW141", "W OF 63W")
         leArea97 = self.LocalEffectArea("le_NEW143_other", "ELSEWHERE")
         leArea98 = self.LocalEffectArea("le_NEW143", "W OF 58W")
         leArea99 = self.LocalEffectArea("le_NEW145_other", "ELSEWHERE")
         leArea100 = self.LocalEffectArea("le_NEW145", "ATLC EXPOSURES")
         leArea101 = self.LocalEffectArea("le_NEW147_other", "ELSEWHERE")
         leArea102 = self.LocalEffectArea("le_NEW147", "W OF 72W")
         leArea103 = self.LocalEffectArea("le_NEW149_other", "ELSEWHERE")
         leArea104 = self.LocalEffectArea("le_NEW149", "W OF 68W")
         leArea105 = self.LocalEffectArea("le_NEW151_other", "ELSEWHERE")
         leArea106 = self.LocalEffectArea("le_NEW151", "W OF 63W")
         leArea107 = self.LocalEffectArea("le_NEW153_other", "ELSEWHERE")
         leArea108 = self.LocalEffectArea("le_NEW153", "W OF 58W")
         leArea109 = self.LocalEffectArea("le_NEW155_other", "ELSEWHERE")
         leArea110 = self.LocalEffectArea("le_NEW155", "APPROACHES TO WINDWARD PASSAGE")
         leArea111 = self.LocalEffectArea("le_NEW157_other", "ELSEWHERE")
         leArea112 = self.LocalEffectArea("le_NEW157", "W OF 68W")
         leArea113 = self.LocalEffectArea("le_NEW159_other", "ELSEWHERE")
         leArea114 = self.LocalEffectArea("le_NEW159", "W OF 63W")
         leArea115 = self.LocalEffectArea("le_NEW161_other", "ELSEWHERE")
         leArea116 = self.LocalEffectArea("le_NEW161", "W OF 58W")

         return [
                 self.LocalEffect([leArea2, leArea1], 2, "...AND "),
                 self.LocalEffect([leArea4, leArea3], 2, "...AND "),
                 self.LocalEffect([leArea6, leArea5], 2, "...AND "),
                 self.LocalEffect([leArea8, leArea7], 2, "...AND "),
                 self.LocalEffect([leArea10, leArea9], 2, "...AND "),
                 self.LocalEffect([leArea12, leArea11], 2, "...AND "),
                 self.LocalEffect([leArea14, leArea13], 2, "...AND "),
                 self.LocalEffect([leArea16, leArea15], 2, "...AND "),
                 self.LocalEffect([leArea18, leArea17], 2, "...AND "),
                 self.LocalEffect([leArea20, leArea19], 2, "...AND "),
                 self.LocalEffect([leArea22, leArea21], 2, "...AND "),
                 self.LocalEffect([leArea24, leArea23], 2, "...AND "),
                 self.LocalEffect([leArea26, leArea25], 2, "...AND "),
                 self.LocalEffect([leArea28, leArea27], 2, "...AND "),
                 self.LocalEffect([leArea30, leArea29], 2, "...AND "),
                 self.LocalEffect([leArea32, leArea31], 2, "...AND "),
                 self.LocalEffect([leArea34, leArea33], 2, "...AND "),
                 self.LocalEffect([leArea36, leArea35], 2, "...AND "),
                 self.LocalEffect([leArea38, leArea37], 2, "...AND "),
                 self.LocalEffect([leArea40, leArea39], 2, "...AND "),
                 self.LocalEffect([leArea42, leArea41], 2, "...AND "),
                 self.LocalEffect([leArea44, leArea43], 2, "...AND "),
                 self.LocalEffect([leArea46, leArea45], 2, "...AND "),
                 self.LocalEffect([leArea48, leArea47], 2, "...AND "),
                 self.LocalEffect([leArea50, leArea49], 2, "...AND "),
                 self.LocalEffect([leArea52, leArea51], 2, "...AND "),
                 self.LocalEffect([leArea54, leArea53], 2, "...AND "),
                 self.LocalEffect([leArea56, leArea55], 2, "...AND "),
                 self.LocalEffect([leArea58, leArea57], 2, "...AND "),
                 self.LocalEffect([leArea60, leArea59], 2, "...AND "),
                 self.LocalEffect([leArea62, leArea61], 2, "...AND "),
                 self.LocalEffect([leArea64, leArea63], 2, "...AND "),
                 self.LocalEffect([leArea66, leArea65], 2, "...AND "),
                 self.LocalEffect([leArea68, leArea67], 2, "...AND "),
                 self.LocalEffect([leArea70, leArea69], 2, "...AND "),
                 self.LocalEffect([leArea72, leArea71], 2, "...AND "),
                 self.LocalEffect([leArea74, leArea73], 2, "...AND "),
                 self.LocalEffect([leArea76, leArea75], 2, "...AND "),
                 self.LocalEffect([leArea78, leArea77], 2, "...AND "),
                 self.LocalEffect([leArea80, leArea79], 2, "...AND "),
                 self.LocalEffect([leArea82, leArea81], 2, "...AND "),
                 self.LocalEffect([leArea84, leArea83], 2, "...AND "),
                 self.LocalEffect([leArea86, leArea85], 2, "...AND "),
                 self.LocalEffect([leArea88, leArea87], 2, "...AND "),
                 self.LocalEffect([leArea90, leArea89], 2, "...AND "),
                 self.LocalEffect([leArea92, leArea91], 2, "...AND "),
                 self.LocalEffect([leArea94, leArea93], 2, "...AND "),
                 self.LocalEffect([leArea96, leArea95], 2, "...AND "),
                 self.LocalEffect([leArea98, leArea97], 2, "...AND "),
                 self.LocalEffect([leArea100, leArea99], 2, "...AND "),
                 self.LocalEffect([leArea102, leArea101], 2, "...AND "),
                 self.LocalEffect([leArea104, leArea103], 2, "...AND "),
                 self.LocalEffect([leArea106, leArea105], 2, "...AND "),
                 self.LocalEffect([leArea108, leArea107], 2, "...AND "),
                 self.LocalEffect([leArea110, leArea109], 2, "...AND "),
                 self.LocalEffect([leArea112, leArea111], 2, "...AND "),
                 self.LocalEffect([leArea114, leArea113], 2, "...AND "),
                 self.LocalEffect([leArea116, leArea115], 2, "...AND "),
                 self.LocalEffect([leArea118, leArea117], 2, "...AND "),
                ]

    def _windLocalEffects_list(self):
         leArea1 = self.LocalEffectArea("le_NEW013_other", "ELSEWHERE")
         leArea2 = self.LocalEffectArea("le_NEW013", "S OF 27N")
         leArea3 = self.LocalEffectArea("le_NEW015_other", "ELSEWHERE")
         leArea4 = self.LocalEffectArea("le_NEW015", "S OF 27N")
         leArea5 = self.LocalEffectArea("le_NEW017_other", "ELSEWHERE")
         leArea6 = self.LocalEffectArea("le_NEW017", "S OF 27N")
         leArea7 = self.LocalEffectArea("le_NEW019_other", "ELSEWHERE")
         leArea8 = self.LocalEffectArea("le_NEW019", "W OF 96W")
         leArea9 = self.LocalEffectArea("le_NEW021_other", "ELSEWHERE")
         leArea10 = self.LocalEffectArea("le_NEW021", "S OF 24W")
         leArea11 = self.LocalEffectArea("le_NEW023_other", "ELSEWHERE")
         leArea12 = self.LocalEffectArea("le_NEW023", "S OF 24W")
         leArea13 = self.LocalEffectArea("le_NEW025_other", "ELSEWHERE")
         leArea14 = self.LocalEffectArea("le_NEW025", "W OF 85W")
         leArea15 = self.LocalEffectArea("le_NEW027_other", "ELSEWHERE")
         leArea16 = self.LocalEffectArea("le_NEW027", "W OF 85W")
         leArea17 = self.LocalEffectArea("le_NEW029_other", "ELSEWHERE")
         leArea18 = self.LocalEffectArea("le_NEW029", "S OF 21N W OF 95W")
         leArea19 = self.LocalEffectArea("le_NEW031_other", "ELSEWHERE")
         leArea20 = self.LocalEffectArea("le_NEW031", "S OF 20N")
         leArea21 = self.LocalEffectArea("le_NEW033_other", "ELSEWHERE")
         leArea22 = self.LocalEffectArea("le_NEW033", "W OF 92W")
         leArea23 = self.LocalEffectArea("le_NEWc011_other", "ELSEWHERE")
         leArea24 = self.LocalEffectArea("le_NEWc011", "S OF 20N")
         leArea25 = self.LocalEffectArea("le_NEWc013_other", "ELSEWHERE")
         leArea26 = self.LocalEffectArea("le_NEWc013", "LEE OF CUBA")
         leArea27 = self.LocalEffectArea("le_NEWc015_other", "ELSEWHERE")
         leArea28 = self.LocalEffectArea("le_NEWc015", "E OF 82W")
         leArea29 = self.LocalEffectArea("le_NEWc017_other", "ELSEWHERE")
         leArea30 = self.LocalEffectArea("le_NEWc017", "BETWEEN CUBA AND JAMAICA")
         leArea31 = self.LocalEffectArea("le_NEWc021_other", "ELSEWHERE")
         leArea32 = self.LocalEffectArea("le_NEWc021", "S OF 17N W OF 86W")
         leArea33 = self.LocalEffectArea("le_NEWc023_other", "ELSEWHERE")
         leArea34 = self.LocalEffectArea("le_NEWc023", "S OF 17N")
         leArea35 = self.LocalEffectArea("le_NEWc025_other", "ELSEWHERE")
         leArea36 = self.LocalEffectArea("le_NEWc025", "S OF 17N")
         leArea37 = self.LocalEffectArea("le_NEWc027_other", "ELSEWHERE")
         leArea38 = self.LocalEffectArea("le_NEWc027", "S OF 17N")
         leArea39 = self.LocalEffectArea("le_NEWc029_other", "ELSEWHERE")
         leArea40 = self.LocalEffectArea("le_NEWc029", "LEE OF DOMINICAN REPUBLIC")
         leArea41 = self.LocalEffectArea("le_NEWc031_other", "ELSEWHERE")
         leArea42 = self.LocalEffectArea("le_NEWc031", "W OF 66W")
         leArea43 = self.LocalEffectArea("le_NEWc033_other", "ELSEWHERE")
         leArea44 = self.LocalEffectArea("le_NEWc033", "ATLC EXPOSURES")
         leArea45 = self.LocalEffectArea("le_NEWc035_other", "ELSEWHERE")
         leArea46 = self.LocalEffectArea("le_NEWc035", "W OF 58W")
         leArea47 = self.LocalEffectArea("le_NEWc037_other", "ELSEWHERE")
         leArea48 = self.LocalEffectArea("le_NEWc037", "WITHIN 60 NM OF COAST OF NICARAGUA")
         leArea117 = self.LocalEffectArea("le_NEWc039_other", "ELSEWHERE")
         leArea118 = self.LocalEffectArea("le_NEWc039", "N OF 13N")
         leArea49 = self.LocalEffectArea("le_NEWc041_other", "ELSEWHERE")
         leArea50 = self.LocalEffectArea("le_NEWc041", "N OF 13N")
         leArea51 = self.LocalEffectArea("le_NEWc043_other", "ELSEWHERE")
         leArea52 = self.LocalEffectArea("le_NEWc043", "S OF 13N")
         leArea53 = self.LocalEffectArea("le_NEWc045_other", "ELSEWHERE")
         leArea54 = self.LocalEffectArea("le_NEWc045", "S OF 13N")
         leArea55 = self.LocalEffectArea("le_NEWc047_other", "ELSEWHERE")
         leArea56 = self.LocalEffectArea("le_NEWc047", "ATLC EXPOSURES")
         leArea57 = self.LocalEffectArea("le_NEWc049_other", "ELSEWHERE")
         leArea58 = self.LocalEffectArea("le_NEWc049", "W OF 58W")
         leArea59 = self.LocalEffectArea("le_NEWc051_other", "ELSEWHERE")
         leArea60 = self.LocalEffectArea("le_NEWc051", "N OF 09N")
         leArea61 = self.LocalEffectArea("le_NEWc053_other", "ELSEWHERE")
         leArea62 = self.LocalEffectArea("le_NEWc053", "N OF 10N")
         leArea63 = self.LocalEffectArea("le_NEWc055_other", "ELSEWHERE")
         leArea64 = self.LocalEffectArea("le_NEWc055", "N OF 10N")
         leArea65 = self.LocalEffectArea("le_NEW111_other", "ELSEWHERE")
         leArea66 = self.LocalEffectArea("le_NEW111", "N OF 30N")
         leArea67= self.LocalEffectArea("le_NEW113_other", "ELSEWHERE")
         leArea68 = self.LocalEffectArea("le_NEW113", "N OF 30N")
         leArea69 = self.LocalEffectArea("le_NEW115_other", "ELSEWHERE")
         leArea70 = self.LocalEffectArea("le_NEW115", "N OF 30N")
         leArea71 = self.LocalEffectArea("le_NEW117_other", "ELSEWHERE")
         leArea72 = self.LocalEffectArea("le_NEW117", "W OF 68W")
         leArea73 = self.LocalEffectArea("le_NEW119_other", "ELSEWHERE")
         leArea74 = self.LocalEffectArea("le_NEW119", "W OF 63W")
         leArea75 = self.LocalEffectArea("le_NEW121_other", "ELSEWHERE")
         leArea76 = self.LocalEffectArea("le_NEW121", "W OF 58W")
         leArea77 = self.LocalEffectArea("le_NEW123_other", "ELSEWHERE")
         leArea78 = self.LocalEffectArea("le_NEW123", "N OF 28N")
         leArea79 = self.LocalEffectArea("le_NEW125_other", "ELSEWHERE")
         leArea80 = self.LocalEffectArea("le_NEW125", "N OF 28N")
         leArea81 = self.LocalEffectArea("le_NEW127_other", "ELSEWHERE")
         leArea82 = self.LocalEffectArea("le_NEW127", "N OF 28N")
         leArea83 = self.LocalEffectArea("le_NEW129_other", "ELSEWHERE")
         leArea84 = self.LocalEffectArea("le_NEW129", "W OF 68W")
         leArea85 = self.LocalEffectArea("le_NEW131_other", "ELSEWHERE")
         leArea86 = self.LocalEffectArea("le_NEW131", "W OF 63W")
         leArea87 = self.LocalEffectArea("le_NEW133_other", "ELSEWHERE")
         leArea88 = self.LocalEffectArea("le_NEW133", "W OF 58W")
         leArea89= self.LocalEffectArea("le_NEW135_other", "ELSEWHERE")
         leArea90 = self.LocalEffectArea("le_NEW135", "ATLC EXPOSURES")
         leArea91 = self.LocalEffectArea("le_NEW137_other", "ELSEWHERE")
         leArea92 = self.LocalEffectArea("le_NEW137", "W OF 73W")
         leArea93 = self.LocalEffectArea("le_NEW139_other", "ELSEWHERE")
         leArea94 = self.LocalEffectArea("le_NEW139", "W OF 68W")
         leArea95 = self.LocalEffectArea("le_NEW141_other", "ELSEWHERE")
         leArea96 = self.LocalEffectArea("le_NEW141", "W OF 63W")
         leArea97 = self.LocalEffectArea("le_NEW143_other", "ELSEWHERE")
         leArea98 = self.LocalEffectArea("le_NEW143", "W OF 58W")
         leArea99 = self.LocalEffectArea("le_NEW145_other", "ELSEWHERE")
         leArea100 = self.LocalEffectArea("le_NEW145", "ATLC EXPOSURES")
         leArea101 = self.LocalEffectArea("le_NEW147_other", "ELSEWHERE")
         leArea102 = self.LocalEffectArea("le_NEW147", "W OF 72W")
         leArea103 = self.LocalEffectArea("le_NEW149_other", "ELSEWHERE")
         leArea104 = self.LocalEffectArea("le_NEW149", "W OF 68W")
         leArea105 = self.LocalEffectArea("le_NEW151_other", "ELSEWHERE")
         leArea106 = self.LocalEffectArea("le_NEW151", "W OF 63W")
         leArea107 = self.LocalEffectArea("le_NEW153_other", "ELSEWHERE")
         leArea108 = self.LocalEffectArea("le_NEW153", "W OF 58W")
         leArea109 = self.LocalEffectArea("le_NEW155_other", "ELSEWHERE")
         leArea110 = self.LocalEffectArea("le_NEW155", "APPROACHES TO WINDWARD PASSAGE")
         leArea111 = self.LocalEffectArea("le_NEW157_other", "ELSEWHERE")
         leArea112 = self.LocalEffectArea("le_NEW157", "W OF 68W")
         leArea113 = self.LocalEffectArea("le_NEW159_other", "ELSEWHERE")
         leArea114 = self.LocalEffectArea("le_NEW159", "W OF 63W")
         leArea115 = self.LocalEffectArea("le_NEW161_other", "ELSEWHERE")
         leArea116 = self.LocalEffectArea("le_NEW161", "W OF 58W")

         return [
                 self.LocalEffect([leArea2, leArea1], 5, "...AND "),
                 self.LocalEffect([leArea4, leArea3], 5, "...AND "),
                 self.LocalEffect([leArea6, leArea5], 5, "...AND "),
                 self.LocalEffect([leArea8, leArea7], 5, "...AND "),
                 self.LocalEffect([leArea10, leArea9], 5, "...AND "),
                 self.LocalEffect([leArea12, leArea11], 5, "...AND "),
                 self.LocalEffect([leArea14, leArea13], 5, "...AND "),
                 self.LocalEffect([leArea16, leArea15], 5, "...AND "),
                 self.LocalEffect([leArea18, leArea17], 5, "...AND "),
                 self.LocalEffect([leArea20, leArea19], 5, "...AND "),
                 self.LocalEffect([leArea22, leArea21], 5, "...AND "),
                 self.LocalEffect([leArea24, leArea23], 5, "...AND "),
                 self.LocalEffect([leArea26, leArea25], 5, "...AND "),
                 self.LocalEffect([leArea28, leArea27], 5, "...AND "),
                 self.LocalEffect([leArea30, leArea29], 5, "...AND "),
                 self.LocalEffect([leArea32, leArea31], 5, "...AND "),
                 self.LocalEffect([leArea34, leArea33], 5, "...AND "),
                 self.LocalEffect([leArea36, leArea35], 5, "...AND "),
                 self.LocalEffect([leArea38, leArea37], 5, "...AND "),
                 self.LocalEffect([leArea40, leArea39], 5, "...AND "),
                 self.LocalEffect([leArea42, leArea41], 5, "...AND "),
                 self.LocalEffect([leArea44, leArea43], 5, "...AND "),
                 self.LocalEffect([leArea46, leArea45], 5, "...AND "),
                 self.LocalEffect([leArea48, leArea47], 5, "...AND "),
                 self.LocalEffect([leArea50, leArea49], 5, "...AND "),
                 self.LocalEffect([leArea52, leArea51], 5, "...AND "),
                 self.LocalEffect([leArea54, leArea53], 5, "...AND "),
                 self.LocalEffect([leArea56, leArea55], 5, "...AND "),
                 self.LocalEffect([leArea58, leArea57], 5, "...AND "),
                 self.LocalEffect([leArea60, leArea59], 5, "...AND "),
                 self.LocalEffect([leArea62, leArea61], 5, "...AND "),
                 self.LocalEffect([leArea64, leArea63], 5, "...AND "),
                 self.LocalEffect([leArea66, leArea65], 5, "...AND "),
                 self.LocalEffect([leArea68, leArea67], 5, "...AND "),
                 self.LocalEffect([leArea70, leArea69], 5, "...AND "),
                 self.LocalEffect([leArea72, leArea71], 5, "...AND "),
                 self.LocalEffect([leArea74, leArea73], 5, "...AND "),
                 self.LocalEffect([leArea76, leArea75], 5, "...AND "),
                 self.LocalEffect([leArea78, leArea77], 5, "...AND "),
                 self.LocalEffect([leArea80, leArea79], 5, "...AND "),
                 self.LocalEffect([leArea82, leArea81], 5, "...AND "),
                 self.LocalEffect([leArea84, leArea83], 5, "...AND "),
                 self.LocalEffect([leArea86, leArea85], 5, "...AND "),
                 self.LocalEffect([leArea88, leArea87], 5, "...AND "),
                 self.LocalEffect([leArea90, leArea89], 5, "...AND "),
                 self.LocalEffect([leArea92, leArea91], 5, "...AND "),
                 self.LocalEffect([leArea94, leArea93], 5, "...AND "),
                 self.LocalEffect([leArea96, leArea95], 5, "...AND "),
                 self.LocalEffect([leArea98, leArea97], 5, "...AND "),
                 self.LocalEffect([leArea100, leArea99], 5, "...AND "),
                 self.LocalEffect([leArea102, leArea101], 5, "...AND "),
                 self.LocalEffect([leArea104, leArea103], 5, "...AND "),
                 self.LocalEffect([leArea106, leArea105], 5, "...AND "),
                 self.LocalEffect([leArea108, leArea107], 5, "...AND "),
                 self.LocalEffect([leArea110, leArea109], 5, "...AND "),
                 self.LocalEffect([leArea112, leArea111], 5, "...AND "),
                 self.LocalEffect([leArea114, leArea113], 5, "...AND "),
                 self.LocalEffect([leArea116, leArea115], 5, "...AND "),
                 self.LocalEffect([leArea118, leArea117], 5, "...AND "),
                ]

#    #Modified from OFF base
#    #Was originally active at OPC
#    #fta 09/09/11 - reactivated - no longer interferes with tropicals
    def OFFExtended(self):
        return { "type": "component",
                 "methodList": [
                          self.consolidateSubPhrases,
                          self.assemblePhrases,
                          self.wordWrap,
                          ],
                 "analysisList": [
                      # NOTE: Choose from the following analysis options.
                      # Do not remove the "vectorMinMax" analysis for
                      # "Wind". This is necessary to get an absolute max if
                      # the useWindsForGusts flag is on.

                      # Use the following if you want moderated ranges
                      # (e.g. N WIND 10 to 20 KT)
                      # Set the moderating percentage in the "moderated_dict"
                      # dictionary module.
                      # Set the maximum range values in the "maximum_range_nlValue_dict"
                      # dictionary module.
                          ("Wind", self.vectorModeratedMinMax, [6]),
                          ("WindGust", self.moderatedMinMax, [6]),
                          ("WaveHeight", self.moderatedMinMax, [6]),
                          ("Swell", self.vectorMax, [6]),
                          ("Swell2", self.vectorMax, [6]),

                          #added below based on what MFL uses 07/10/14 -JL
                          #("WaveHeight", self.moderatedMax, [6]),

                          #need to change the above 24 to 6 or 12 with new 12
                          #hr fcst periods - 07/10/14 - JL

                          # ("WindWaveHgt", self.moderatedMinMax, [24]),
                          #("Wx", self.rankedWx),
                          #("T", self.minMax),  # needed for weather_phrase
                          #("PoP", self._PoP_analysisMethod("OFFExtended")),
                          #("PoP", self.binnedPercent),
                          #("Swell", self.vectorModeratedMinMax, [12]),
                          #("Swell2", self.vectorModeratedMinMax, [12]),

                      ],
                 "phraseList": [
                               # WIND
                               self.marine_wind_phrase,
                               # WAVEHEIGHT
                               # Commented out until fully developed seas wording fixed 9/7/11 CNJ/JL
                               #self.wave_withPeriods_phrase,
                               # Alternative:
                               #self.wave_phrase,
                               # SWELLS AND PERIODS
                               self.wave_withPeriods_phrase,
                               # Alternative:
                               #self.swell_phrase,
                               #self.period_phrase,
                               # WEATHER
                               #self.weather_phrase,
                               #self.visibility_phrase,
                               ],
                }

    def wave_phrase(self):
        return {
            "setUpMethod": self.wave_setUp,
            "wordMethod": self.wave_words,
            "phraseMethods": self.standard_phraseMethods()
            }

    def wave_withPeriods_setUp(self, tree, node):
        return self.wave_setUp(tree, node, periodFlag=1)

# ##  ***commented out entire section below on 08/24/11 for tropical formatter to work***
# ##  ***need to uncomment for swell wording to work along with self.wave_withPeriods_phrase above!
# ##
# ##
    def wave_setUp(self, tree, node, periodFlag=0):
        areaLabel = node.getAreaLabel()
        timeRange = node.getTimeRange()
        print("timeRange:", timeRange)

        inlandWaters = self.inlandWatersAreas(tree, node)
        if self.currentAreaContains(tree, inlandWaters) == 1:
            elementName, elementName2 = self.inlandWatersWave_element(tree, node)
            statsByRange = tree.stats.get(elementName, timeRange, areaLabel, mergeMethod="List")
            if statsByRange is None:
                elementName = elementName2
            # Do not report Period for inland waters
            periodFlag = 0
            descriptor = self.phrase_descriptor(tree, node, "inland waters", elementName)
            node.set("descriptor", descriptor)
        elif self.seasFlag(tree, node):
            # Use wave height elementName (default)
            elementName = self.seasWaveHeight_element(tree, node)
            descriptor = self.phrase_descriptor(tree, node, "seas", elementName)
            node.set("descriptor", descriptor)
        else:
            # Use wind waves (default)
            elementName = self.seasWindWave_element(tree, node)
            periodFlag = 0
            descriptor = self.phrase_descriptor(tree, node, "waves", elementName)
            node.set("descriptor", descriptor)

        wave = self.ElementInfo(elementName, "List")
        elementInfoList = [wave]
        # changed to key on swell instead of period
        # changed to use vector instead of scalar in subPhraseSetUp
        # 05/03/11 CNJ/JL
        if periodFlag:
            print("periodFlag is on")
            node.set("periodFlag", 1)
            period = self.ElementInfo("Swell", "Average", primary=0)
            #period = self.ElementInfo("Period", "Average", primary=0)
            elementInfoList.append(period)
        self.subPhraseSetUp(tree, node, elementInfoList, self.vectorConnector)
        #self.subPhraseSetUp(tree, node, elementInfoList, self.scalarConnector)
        return self.DONE()

    def seasFlag(self, tree, node):
       # Return 1 if we are to report combined seas
       timeRange = node.getTimeRange()
       areaLabel = node.getAreaLabel()
       winds = tree.stats.get("Wind", timeRange, areaLabel, mergeMethod="Max")
       if winds is None:
           return 0
       maxWind, dir = winds

       # Determine if we will report combined seas OR wind waves
       seasFlag = 0
       if maxWind > self.waveHeight_wind_threshold(tree, node):
           seasFlag = 1
       else:
           swell = tree.stats.get("Swell", timeRange, areaLabel, mergeMethod="Max")
           swell2 = tree.stats.get("Swell2", timeRange, areaLabel, mergeMethod="Max")
           maxWave = tree.stats.get("WindWaveHgt", timeRange, areaLabel, mergeMethod="Max")
           if swell is None or maxWave is None:
               pass # Leave seasFlag at zero
           else:
               # We'll decide to report combined seas by looking at
               # the MAX of waves and swells over the entire time period
               swells, dir = swell
               if swell2 is None:
                   swells2 = 0
               else:
                   swells2, dir = swell2
               threshold = self.combinedSeas_threshold(tree, node)
               if maxWave > threshold and \
                  (swells > threshold or swells2 > threshold):
                   seasFlag = 1
       return seasFlag

    def wave_words(self, tree, node):
        # Return a phrase for wave and optionally Period for the given subPhrase
        elementInfo = node.getAncestor("firstElement")
        elementName = elementInfo.name
        print(elementName)
        statDict = node.getStatDict()
        if statDict is None:
            return self.setWords(node, "")
        wave = self.getStats(statDict, elementName)
        if wave is None:
            return self.setWords(node, "")
        min, max = self.getValue(wave, "MinMax")
        threshold = self.nlValue(self.null_nlValue(
            tree, node, elementName, elementName), max)
        if int(min) < threshold and int(max) < threshold:
            return self.setWords(node, "null")
        waveStr = self.getScalarRangeStr(tree, node, elementName, min, max)
        units = self.units_descriptor(tree, node, "units", "ft")
        waveUnit = self.units_descriptor(tree, node, "unit", "ft")
        if int(min) == 1 and int(max) == 1:
            units = waveUnit
        words = waveStr + " " + units
        print("### words before swell code:", words)

        ### added for testing 8/11/15
        #return self.setWords(node, words)

        # add swell direction after wave height phrase - for OFFNT products
        # modified from swell_words in MarinePhrases.TextUtility
        # added 05/03/11 (CNJ/JL)
        if "WaveHeight" in statDict:
        #if "Swell" in statDict.keys():
            print("*** WaveHeight is in statDict.keys ***")
            # Create phrase for swell for a given set of stats in statsByRange
#print("\n in swell words")
            periodFlag = node.getAncestor("periodFlag")
            statDict = node.getStatDict()
            #Check for Swell alone
            swell2 = self.getStats(statDict, "Swell2")
            if swell2 is None:
                oneSwell = 1
            else:
                oneSwell = 0

            # Swell and Swell2 subPhrases
            subPhraseParts = []
            elementInfoList = node.getAncestor("elementInfoList")
            for swell, period in [("Swell", "Period"), ("Swell2", "Period2")]:
                if swell == "Swell":
                    checkRepeating = 1
                else:
                    checkRepeating = 0
                for elementInfo in elementInfoList:
                    if elementInfo.name == swell:
                        swellInfo = elementInfo
                        break
                swellWords = self.simple_vector_phrase_swell(tree, node, swellInfo, checkRepeating)
                print("Swell Words: ", swellWords)
                if swellWords == "null" or not swellWords:
                    subPhraseParts.append("")
                    continue
                # Add Period
                periodPhrase = ""
                if periodFlag == 1:
                    periodStats = self.getStats(statDict, period)
                    periodPhrase = self.embedded_period_phrase(tree, node, periodStats)
                    swellWords += periodPhrase
                subPhraseParts.append(swellWords)

#print("swell", node.getTimeRange(), subPhraseParts)
            if subPhraseParts[0]  and subPhraseParts[1] :
                words += " IN " + subPhraseParts[0] #+ " and " + subPhraseParts[1]
                # Check for mixed swell on first subPhrase
                if node.getIndex() == 0:
                    mixedSwell = self.checkMixedSwell(tree, node, statDict)
                    #if mixedSwell:
                    #    mixedSwellDesc = self.phrase_descriptor(tree, node, "mixed swell", "Swell")
                    #    phrase = node.getParent()
                    #    phrase.set("descriptor", mixedSwellDesc)
                    #    phrase.doneList.append(self.embedDescriptor)
            elif subPhraseParts[0] :
               words += " IN " + subPhraseParts[0]
            elif subPhraseParts[1] :
               words += " IN " + subPhraseParts[1]
            else:
               pass
               #words = "null"
            print("### words after swell code:", words)
            wind2flag = 0

        return self.setWords(node, words)


# Copy of simple_vector_phrase from VectorRelatedPhrases with magnitude values turned off
# Added 05/03/11 (CNJ/JL)
# Changes 08/06/15 to check WaveHeight magnitude instead of Swell magnitude (CNJ/JL/ERA)
    def simple_vector_phrase_swell(self, tree, node, elementInfo, checkRepeating=1):
        # Create a vector subPhrase
        # Do not repeat mag, dir if same as previous phrase
        elementName = elementInfo.name
        statDict = node.getStatDict()
        stats = self.getStats(statDict, elementName)
        if stats is None:
            return ""
        mag, dir = stats
        minMag, maxMag = self.getValue(mag, "MinMax")
        print("### in simple_vector_phrase_swell ###")
        print("minMag of swell = ", minMag)
        print("maxMag of swell = ", maxMag)

        # Save maxMag at component level for other methods to use.
        # THIS IS PARTICULARLY IMPORTANT FOR USE IN THE includeOnlyPhrases_list def
        # below to eliminate certainly wx elements during tropical cyclone
        # situations when certain conditions are met.
        component = node.getComponent()
        maxMagList = component.get("maxMagList")
        if maxMagList is None:
            maxMagList = [maxMag]
        else:
            maxMagList.append(maxMag)
        component.set("maxMagList", maxMagList)

        # added this check to prevent crash with zero swell, lowered to 0.1 from 0.5 to allow swell wording in more cases
        # 08/07/15 CNJ/JL
        if maxMag > 0.1:
            wvhgt = self.getStats(statDict, "WaveHeight")
            min, max = self.getValue(wvhgt, "MinMax")

            print("### calling vector_mag_tafb ###")

            words = self.vector_mag_tafb(tree, node, min, max,
                                         elementInfo.outUnits, "WaveHeight")
        else:
            words = "null"

        print("words after vector_mag_tafb:", words)

        #words = self.vector_mag(tree, node, minMag, maxMag,
        #                        elementInfo.outUnits, elementName)
        if words == "null":
            return words
        magStr = words
        dirStr = self.vector_dir(dir)

        if checkRepeating:
            # Set for future reference
            node.set("dirStr", dirStr)
            node.set("magStr", magStr)
            node.set("minMag", minMag)
            node.set("maxMag", maxMag)
            if minMag == 0.0:
                minMag = maxMag
            # Check for repeating mag or dir
            prevNode = node.getPrev()
            if prevNode is not None:
                prevDirStr = prevNode.get("dirStr")
                prevMagStr = prevNode.get("magStr")
                prevMin = prevNode.get("minMag")
                prevMax = prevNode.get("maxMag")
                if prevMin == 0.0:
                    prevMin = prevMax
                if prevMin is None or prevMax is None or \
                   prevDirStr is None or prevMagStr is None:
                    pass
                elif prevDirStr == dirStr and prevMagStr == magStr:
                    pass
                elif prevDirStr == dirStr:
                    dirStr = ""
                elif prevMagStr == magStr:
                    magStr = ""
                # Prevent "around 10 becoming 5 to 10"
                #         "around 10 becoming 10 to 15"
                elif prevMin == prevMax:
                    if (minMag == prevMax - 5.0) or (maxMag == prevMax + 5.0):
                        magStr = ""
                # Prevent "5 to 10 becoming around 10"
                #         "10 to 15 becoming around 10"
                elif minMag == maxMag:
                    if (prevMin == maxMag - 5.0) or (prevMax == maxMag + 5.0):
                        magStr = ""
        # modified to exclude swell magnitude and include "SWELL" after direction
        print("returning swell words")
        words = dirStr + " SWELL"
        #words = dirStr + self.format(magStr)
        return words.lstrip()

    # override to refer to nlValue_tafb
# changed to check avg WaveHeight against threshold value rather than Swell height - 08/06/15 CNJ/JL/ERA
    def vector_mag_tafb(self, tree, node, minMag, maxMag, units,
                   elementName="WaveHeight"):
        "Create a phrase for a Range of magnitudes"

        # Check for "null" value (below threshold)
        #wvhgt = self.getStats(statDict, "WaveHeight")
        #min, max = self.getValue(wvhgt, "MinMax")
        print("Min wave in vector_mag_tafb: ", minMag)
        print("Max wave in vector_mag_tafb", maxMag)

        avgwave = (minMag + maxMag)/2
        threshold = self.nlValue(self.null_nlValue_tafb(
            tree, node, "WaveHeight", "WaveHeight"), maxMag)
        #threshold = self.nlValue(self.null_nlValue_tafb(
        #    tree, node, elementName, elementName), maxMag)
        #threshold = self.nlValue(self.null_nlValue(
        #    tree, node, elementName, elementName), maxMag)
#print("maxMag: ", maxMag)
        print("avgwave: ", avgwave)
        print("threshold: ", threshold)
        if avgwave < threshold:
        #if maxMag < threshold:
            print("*** avgwave < threshold, returning null ***")
            return "null"

        # Apply max reported threshold
        maxReportedMag = self.maxReported_threshold(tree, node, elementName, elementName)
        if maxMag >= maxReportedMag:
            maxMag = maxReportedMag
            #minMag = 0

        units = self.units_descriptor(tree, node, "units", units)

        if elementName == "Wind":
            if self.marine_wind_flag(tree, node):
                return self.marine_wind_mag(tree, node, minMag, maxMag, units, elementName)

        # Check for SingleValue
        if maxMag == minMag: #or minMag == 0:
            around = self.addSpace(
                self.phrase_descriptor(tree, node, "around", elementName))
            words =  around + repr(int(maxMag)) + " " + units
        else:
            if int(minMag) < threshold:
                upTo = self.addSpace(
                    self.phrase_descriptor(tree, node, "up to", elementName))
                words = upTo + repr(int(maxMag)) + " " + units
            else:
                valueConnector = self.value_connector(tree, node, elementName, elementName)
                words =  repr(int(minMag)) + valueConnector + repr(int(maxMag)) + " " + units

        # This is an additional hook for customizing the magnitude wording
        words = self.vector_mag_hook(tree, node, minMag, maxMag, units, elementName, words)
        return words

    def marine_wind_withGusts_phrase(self):
        return {
            "setUpMethod": self.marine_wind_withGusts_setUp,
            "wordMethod": self.vector_words,
            "phraseMethods": self.standard_vector_phraseMethods(),
            }

    def vector_words(self, tree, node):
        # Create a words for a vector element
        elementInfo = node.getAncestor("firstElement")

        ######################################################
        # added section below to set global avgwnd variable
        # this is used by null_nlValue_tafb_dict below
        # 05/04/11 - CNJ/JL
        statDict = node.getStatDict()
        print("statDict in vector_words is:")
        print(statDict)
        wspd = self.getStats(statDict, "Wind")
        #wspd = self._windDirSpeed(statDict, argDict)
        #wvhgt = self.getStats(statDict, "WaveHeight")
        mag, dir = wspd
        wspd1 = mag[0]
        wspd2 = mag[1]
        print("low wind speed is:")
        print(wspd1)
        print("high wind speed is:")
        print(wspd2)
        global avgwnd
#         global avgwnd1
#         global avgwnd2
#         avgwnd1 = -1
#         avgwnd2 = -1
        avgwnd = (wspd1 + wspd2) / 2
#         avgwnd1 = avgwnd
#         if wind2flag == 1:
#             avgwnd2 = avgwnd
        print("avg wind speed is:", avgwnd)
#         print("avg wind speed 1 is:", avgwnd1)
#         print("avg wind speed 2 is:", avgwnd2)
#         wind2flag = 1
        # end additional code section
        ######################################################

        if elementInfo is None:
            return self.setWords(node, "")
        words = self.simple_vector_phrase(tree, node, elementInfo)
        if words == "null":
            return self.setWords(node, "null")
        gustPhrase = ""
        if words :
            # Add gusts
            gustFlag = node.getAncestor("gustFlag")
            if gustFlag == 1:
                windStats = tree.stats.get("Wind", node.getTimeRange(), node.getAreaLabel(),
                                             mergeMethod="Max")
                if windStats is not None:
                    maxMag, dir = windStats
                    statDict = node.getStatDict()
                    gustStats = self.getStats(statDict, "WindGust")
                    subRange = node.get("timeRange")
                    gustPhrase = self.embedded_gust_phrase(
                        tree, node, gustStats, maxMag, subRange)
        return self.setWords(node, words + gustPhrase)

    def null_nlValue_tafb(self, tree, node, key, value):
        return self.access_dictionary(tree, node, key, value, "null_nlValue_tafb_dict")

    def null_nlValue_tafb_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        #timeRange = node.getTimeRange()
        statDict = node.getStatDict()
        #self.__argDict = argDict
        #sampleInfo = [1]
        #self._sampler = self.getSampler("", sampleInfo)
        #analysisList = ["Wind", "WaveHeight"]
        #statDict = self.getStatDict(self._sampler, analysisList, self._timeRangeList, editArea)
        #statList = self.getStatList(self._sampler, self._getAnalysisList_tafb(),\
        #                            self._timeRangeList, editArea)
#print("statList is:")
#print(statList)
        print("statDict in null_nlValue is:")
        print(statDict)
        wspd = self.getStats(statDict, "Wind")
        swl = self.getStats(statDict, "Swell")
        wvhgt = self.getStats(statDict, "WaveHeight")
        print("statDict after getStats is:")
        print(statDict)
        #mag, dir = wspd
        swlhgt = swl[0]
        print("avg wind speed in dict is:")
        print(avgwnd)
        print("swlhgt is:")
        print(swlhgt)
        print("wvhgt is:")
        print(wvhgt)

        # changed to calculate min/max/avg wave heights for use below 08/06/15 CNJ/JL/ERA
        min, max = self.getValue(wvhgt, "MinMax")
        print("Min wave in null_nlValue_tafb_dict: ", min)
        print("Max wave in null_nlValue_tafb_dict", max)
        avgwave = (min + max)/2
        print("avgwave in null_nlValue_tafb_dict:", avgwave)

        ######################################################################
        # FDS wind/swell table
        # Adjust the following table to set minimum swell height required for
        # mention at various wind speeds
        ## changed to check wvhgt instead of swell 08/06/15 CNJ/JL/ERA
        if avgwnd < 5: # 0-4 kt
            if avgwave < 3:
                dict["WaveHeight"] = 100
                print("avg wind < 5 & WaveHeight < 3, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 3
                print("avg wind < 5 & WaveHeight >= 3, setting dict[WaveHeight] = 3")

        # changed wave threshold for this case from 5.0 to 4.5 as per JL - 08/10/15 CNJ/JL
        elif (avgwnd >=5) and (avgwnd < 9): # 5-10 kt
            if avgwave < 4.5:
                dict["WaveHeight"] = 100
                print("avg wind 5-8 & WaveHeight < 4.5, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 4.5
                print("avg wind 5-8 & WaveHeight >= 4.5, setting dict[WaveHeight] = 5")
        elif (avgwnd >=9) and (avgwnd < 12): # near 10 kt
            if avgwave < 5.5:
                dict["WaveHeight"] = 100
                print("avg wind 9-11 & WaveHeight < 5.5, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 5.5
                print("avg wind 9-11 & WaveHeight >= 5.5, setting dict[WaveHeight] = 5.5")
        elif (avgwnd >=12) and (avgwnd < 14): # 10-15 kt
            if avgwave < 6.5:
                dict["WaveHeight"] = 100
                print("avg wind 12-13 & WaveHeight < 6.5, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 6.5
                print("avg wind 12-13 & WaveHeight >= 6.5, setting dict[WaveHeight] = 6.5")
        elif (avgwnd >=14) and (avgwnd < 17): # near 15 kt
            if avgwave < 7:
                dict["WaveHeight"] = 100
                print("avg wind 14-16 & WaveHeight < 7, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 7
                print("avg wind 14-16 & WaveHeight >= 7, setting dict[WaveHeight] = 7")
        elif (avgwnd >= 17) and (avgwnd < 19): # 15-20 kt
            if avgwave < 8:
                dict["WaveHeight"] = 100
                print("avg wind < 19 & WaveHeight < 8, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 8
                print("avg wind < 19 & WaveHeight >= 8, setting dict[WaveHeight] = 8")
        elif (avgwnd >= 19) and (avgwnd < 22): # near 20 kt
            if avgwave < 8:
                dict["WaveHeight"] = 100
                print("avg wind 19-21 & WaveHeight < 8, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 8
                print("avg wind 19-21 & WaveHeight >= 8, setting dict[WaveHeight] = 8")
        elif (avgwnd >= 22) and (avgwnd < 24): # 20-25 kt
            if avgwave < 8.5:
                dict["WaveHeight"] = 100
                print("avg wind 22-23 & WaveHeight < 8.5, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 8.5
                print("avg wind 22-23 & WaveHeight >= 8.5, setting dict[WaveHeight] = 8.5")
        elif (avgwnd >= 24) and (avgwnd < 27): # near 25 kt
            if avgwave < 8.5:
                dict["WaveHeight"] = 100
                print("avg wind 24-26 & WaveHeight < 8.5, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 8.5
                print("avg wind 24-26 & WaveHeight >= 8.5, setting dict[WaveHeight] = 8.5")
        elif (avgwnd >= 27) and (avgwnd < 29): # 25-30 kt
            if avgwave < 9:
                dict["WaveHeight"] = 100
                print("avg wind 27-28 & WaveHeight < 9, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 9
                print("avg wind 27-28 & WaveHeight >= 9, setting dict[WaveHeight] = 9")
        elif (avgwnd >= 29) and (avgwnd < 32): # near 30 kt
            if avgwave < 9:
                dict["WaveHeight"] = 100
                print("avg wind 29-31 & WaveHeight < 9, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 9
                print("avg wind 29-31 & WaveHeight >= 9, setting dict[WaveHeight] = 9")
        elif (avgwnd >= 32) and (avgwnd < 34): # 30-35 kt
            if avgwave < 10:
                dict["WaveHeight"] = 100
                print("avg wind 32-33 & WaveHeight < 10, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 10
                print("avg wind 32-33 & WaveHeight >= 10, setting dict[WaveHeight] = 10")
        elif (avgwnd >= 34) and (avgwnd < 37): # near 35 kt
            if avgwave < 11:
                dict["WaveHeight"] = 100
                print("avg wind 34-36 & WaveHeight < 11, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 11
                print("avg wind 34-36 & WaveHeight >= 11, setting dict[WaveHeight] = 11")
        elif (avgwnd >= 37) and (avgwnd < 39): # 35-40 kt
            if avgwave < 12:
                dict["WaveHeight"] = 100
                print("avg wind 37-38 & WaveHeight < 12, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 12
                print("avg wind 37-38 & WaveHeight >= 12, setting dict[WaveHeight] = 12")
        elif (avgwnd >= 39) and (avgwnd < 42): # near 40 kt
            if avgwave < 17:
                dict["WaveHeight"] = 100
                print("avg wind 39-41 & WaveHeight < 17, setting dict[WaveHeight] = 100")
            else:
                dict["WaveHeight"] = 17
                print("avg wind 39-41 & WaveHeight >= 17, setting dict[WaveHeight] = 17")
        else:
            dict["WaveHeight"] = 20
        # end of FDS wind/swell table
        #########################################################################

        return dict

    def _getVariables(self, argDict):
        # Make argDict accessible
        self.__argDict = argDict

        # Get Definition variables
        self._definition = argDict["forecastDef"]
        for key in self._definition:
            exec("self._" + key + "= self._definition[key]")

        # Get VariableList and _issuance_list variables
        varDict = argDict["varDict"]
        for key in varDict:
            if isinstance(key, tuple):
                label, variable = key
                exec("self._" + variable + "= varDict[key]")

#         try:
#             self._pdCombo = varDict["Period Combining?"]
#         except:
#             if self._pdCombo == "Yes":
#                 self._periodCombining = 1
#             else:
#                 self._periodCombining = 0

        # Added CJ
        # Tropical exceptions
        try:
            self._includeTropical = self._includeTropical == "Yes"
        except:
            self._includeTropical = False
#         if self._includeTropical:
#             self._periodCombining = 0 # Changed back from 1 to 0 as PeriodCombining
#             # with IncludeTropical was causing Period issues in forecast text (JL - 10/26/11)
#             if self._productIssuance == "Morning with Pre-1st Period":
#                 self._productIssuance = "Morning"
#             if self._productIssuance == "Afternoon with Pre-1st Period":
#                 self._productIssuance = "Afternoon"

        self._language = argDict["language"]
        return None


    #Modified from OFF base
    #added issuance times and change choices with daylight/standard changeOFF
    def _issuance_list(self, argDict):
        #  This method sets up configurable issuance times with associated
        #  narrative definitions.  See the Text Product User Guide for documentation.

        # Added CJ
        try:
            includeTropical = self._includeTropical
        except:
            includeTropical = False

        if includeTropical:

            narrativeDefAM = [
                ("OFFPeriod", "period1"),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ]
            narrativeDefPM = [
                ("OFFPeriod", "period1"),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ]

#         if includeTropical:
#                 narrativeDefAM = [
#                     ("OFFPeriod", "period1"),
#                     ("OFFPeriod", 12),
#                     ("OFFPeriod", 12),
#                     ("OFFPeriod", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ]
#                 narrativeDefPM = [
#                     ("OFFPeriod", "period1"),
#                     ("OFFPeriod", 12),
#                     ("OFFPeriod", 12),
#                     ("OFFPeriod", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ("OFFExtended", 12),
#                     ] # last line was OFFPeriodMidFFPeriod", 12),
        else:

            if self._definition["includeEveningPeriod"] == 1:
                narrativeDefAM = [
                    ("OFFPeriod", "period1"),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ]
                narrativeDefPM = [
                    ("OFFPeriod", "period1"),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ] # last line was OFFPeriodMid
            else:
                narrativeDefAM = [
                    ("OFFPeriod", "period1"),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ]
                narrativeDefPM = [
                    ("OFFPeriod", "period1"),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ("OFFExtended", 12),
                    ] # last line was OFFPeriodMid

        #determine local time
        localTimeZone = time.strftime("%Z")
#print("\n\n\nTime ZOne = " + localTimeZone + "\n\n\n")
        if self._definition["pil"] == "NEWNT4":
            if localTimeZone == "EDT":
                return [
                   ("530 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1130 AM", "issuanceHour", self.NIGHT(), 16,
                     ".THIS AFTERNOON...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late in the night", "early in the morning",
                     1, narrativeDefPM),
                    ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "early", "towards morning",
                     1, narrativeDefPM)
                    ]
            else:
                return [
                    ("430 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1030 AM", "issuanceHour", self.NIGHT(), 16,
                     ".This afternoon...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late in the night", "early in the morning",
                     1, narrativeDefPM),
                    ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "early", "towards morning",
                     1, narrativeDefPM),
                    ]
        if self._definition["pil"] == "NEWNT3":
            if localTimeZone == "EDT":
                return [
                   ("530 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1130 AM", "issuanceHour", self.NIGHT(), 16,
                     ".THIS AFTERNOON...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late in the night", "early in the morning",
                     1, narrativeDefPM),
                    ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "early", "towards morning",
                     1, narrativeDefPM)
                    ]
            else:
                return [
                    ("430 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1030 AM", "issuanceHour", self.NIGHT(), 16,
                     ".This afternoon...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late in the night", "early in the morning",
                     1, narrativeDefPM),
                    ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "early", "towards morning",
                     1, narrativeDefPM),
                    ]

    # Returns a list of the Hazards allowed for this product in VTEC format.
    # These are sorted in priority order - most important first.
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

#     def periodCombining_elementList(self, tree, node):
#         # Weather Elements to determine whether to combine periods
#         #return ["Sky", "Wind", "Wx", "PoP", "MaxT", "MinT"]
#         # Marine
#         #############################################################################
#         # Swell could be added below if necessary to prevent too much period combining
#         # during periods of changing swell - may affect swell wording
#         # CNJ 05/05/11
#         return ["WaveHeight", "Wind"]
#         #############################################################################
#         # Diurnal Sky Wx pattern
#         #return ["DiurnalSkyWx"]
#
#     def periodCombining_startHour(self, tree, node):
#         # Hour after which periods may be combined
#         return 12

#     def generateForecast(self, argDict):
#         # Get variables
#         error = self._getVariables(argDict)
#         if error is not None:
#             return error
#
#         # Get the areaList -- derived from defaultEditAreas and
#         # may be solicited at run-time from user if desired
#         self._areaList = self.getAreaList(argDict)
#         if len(self._areaList) == 0:
#             return "WARNING -- No Edit Areas Specified to Generate Product."
#
#         # Determine time ranges
#         error = self._determineTimeRanges(argDict)
#         if error is not None:
#             return error
#
#         # Sample the data
#         error = self._sampleData(argDict)
#         if error is not None:
#             return error
#
#         # Initialize the output string
#         fcst = ""
#         fcst = self._preProcessProduct(fcst, argDict)
#
#         # Generate the product for each edit area in the list
#         fraction = 0
#         fractionOne = 1.0/float(len(self._areaList))
#         percent = 50.0
#         self.setProgressPercentage(percent)
#
#         if self._definition["pil"] == "OFFNT3":
#             # Need to know how many areas to process after this.
#             # will insert second synopsis before the last fcst area
#             areasLeft = len(self._areaList) - 1
#             for editArea, areaLabel in self._areaList:
#                 skipAreas = self._skipAreas(argDict)
#                 argDict["editArea"] = (editArea, areaLabel)
#                 if self.currentAreaContains(argDict, skipAreas):
#                     continue
#                 self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
#                 fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
#                 fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
#                 fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#                 # are we on the next to last area yet?
#                 # if so, add synopsis2
#                 if areasLeft == 9:
#                     fcst = fcst + self._Text3()
#                 fraction = fractionOne
#                 areasLeft = areasLeft - 1
#             fcst = self._postProcessProduct(fcst, argDict)
#             return fcst
#
#         else:
#             #Second synopsis isn't defined
#             #use BASE OFF.py code
#             for editArea, areaLabel in self._areaList:
#                 skipAreas = self._skipAreas(argDict)
#                 argDict["editArea"] = (editArea, areaLabel)
#                 if self.currentAreaContains(argDict, skipAreas):
#                     continue
#                 self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
#                 fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
#                 fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
#                 fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#                 fraction = fractionOne
#             fcst = self._postProcessProduct(fcst, argDict)
#             return fcst

    def postProcessPhrase(self, tree, node):
        words = node.get("words")
        rval = None
        if words is not None:
            words =  words.replace("rain showers and thunderstorms", "showers and thunderstorms")
            # Below replace/re.subs format warning headlines in TAFB style
            words = words.replace("POSSIBLE ...", "POSSIBLE...")
            words = words.replace("WARNING ...", "WARNING...")
            # Fixed re.sub regular expressions by escaping leading "..." 9/9/11 CNJ
            # storm warning re.sub no longer affects tropical storm warning headlines
            words = re.sub(r'\.\.\.GALE WARNING.*', r'...GALE WARNING...', words)
            words = re.sub(r'\.\.\.STORM WARNING.*', r'...STORM WARNING...', words)
            words = re.sub(r'\.\.\.HURRICANE FORCE WIND WARNING.*', r'...HURRICANE FORCE WIND WARNING...', words)
            words = re.sub(r'\.\.\.GALE WATCH.*', r'...GALE CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.STORM WATCH.*', r'...STORM CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.HURRICANE WATCH.*', r'...HURRICANE FORCE WINDS POSSIBLE...', words)
            # added line below to handle ashfall advisory and associated special TAFB wording
            words = re.sub(r'\.\.\.ASHFALL ADVISORY.*', r'...ASHFALL ADVISORY...\n[VOLCANO NAME] VOLCANO AT POSITION [xx.xN xx.xW] IS CURRENTLY IN A STATE OF UNREST AND COULD ERUPT WITH LITTLE NOTICE. MARINERS TRAVELING IN THE VICINITY OF [VOLCANO NAME] ARE URGED TO EXERCISE CAUTION. IF MARINERS ENCOUNTER VOLCANIC ASH OR FLOATING VOLCANIC DEBRIS...YOU ARE ENCOURAGED TO REPORT THE OBSERVATION TO THE NATIONAL HURRICANE CENTER BY CALLING 305-229-4424.', words)
            words = re.sub(r'\.\.\.DENSE FOG ADVISORY.*', r'...DENSE FOG ADVISORY...', words)
            words = re.sub(r'\.\.\.DENSE SMOKE ADVISORY.*', r'...DENSE SMOKE ADVISORY...', words)
            words = re.sub(r'\.\.\.GALE CONDITIONS EXPECTED IN EFFECT.*', r'...GALE CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.STORM CONDITIONS EXPECTED IN EFFECT.*', r'...STORM CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.HURRICANE FORCE WINDS EXPECTED IN EFFECT.*', r'...HURRICANE FORCE WINDS POSSIBLE...', words)
            #words = re.sub(r'TSTMS THROUGH THE NIGHT', r'TSTMS', words)
            #words = re.sub(r'TSTMS THROUGH THE DAY', r'TSTMS', words)
            # Translate phrase
            # This is necessary so that word-wrap works correctly
            try:
                words = self.translateForecast(words, self._language)
            except:
                words = self.translateForecast(words, "english")
            rval = self.setWords(node, words)
        return rval

    ## added override to include squalls

    def wxHierarchies(self):
    # This is the hierarchy of which coverage and intensity to choose if
    # wxTypes are the same and to be combined into one subkey.
        return {
        "wxType": ["WP", "R", "RW", "T", "SQ", "L", "ZR", "ZL", "S", "SW",
                  "IP", "F", "ZF", "IF", "IC", "H", "BS", "BN", "K", "BD",
                  "FR", "ZY", "BA", "<NoWx>", "<Invalid>"],
        "coverage": ["Def", "Wide", "Brf", "Frq", "Ocnl", "Pds", "Inter",
                    "Lkly", "Num", "Sct", "Chc", "Areas",
                    "SChc", "WSct", "Iso", "Patchy", "<NoCov>", "<Invalid>"],
        "intensity": ["+", "m", "-", "--", "<NoInten>", "<Invalid>"],
        "visibility": ["0SM", "1/4SM", "1/2SM", "3/4SM", "1SM", "11/2SM", "2SM",
                      "21/2SM", "3SM", "4SM", "5SM", "6SM", "P6SM", "<NoVis>", "<Invalid>"],
        }
