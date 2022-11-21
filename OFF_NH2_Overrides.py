import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis
import mergeProds

import UserInfo
import TextUtils

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class OFF_NH2_Overrides:
    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************

    #Modified from OFF base
    def _Text1(self):
        self.debug_print("Debug: _Text1 in OFF_NH2_Overrides")

        #Determine which product
        if self._definition["pil"] == "OFFNT4":
            return "Offshore Waters Forecast for the Gulf of Mexico\n\n" + \
                   "Seas given as significant wave height, which is the average\n" + \
                   "height of the highest 1/3 of the waves. Individual waves may be\n" + \
                   "more than twice the significant wave height.\n\n"
        else:
            #OFFNT3
            return "Offshore Waters Forecast for the Tropical N Atlantic from 07N to\n" + \
                   "22N between 55W and 64W, the SW N Atlantic S of 31N W of 65W\n" + \
                   "including Bahamas, and the Caribbean Sea.\n\n" + \
                   "Seas given as significant wave height, which is the average\n" + \
                   "height of the highest 1/3 of the waves. Individual waves may be\n" + \
                   "more than twice the significant wave height.\n\n"

    #Modified from OFF base
    def _Text2(self):
        self.debug_print("Debug: _Text2 in OFF_NH2_Overrides")

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
                   "%s\n" %  "Synopsis for the Gulf of Mexico" + \
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
                  "%s\n" %  "Synopsis for Caribbean Sea and Tropical N Atlantic from 07N to" + \
                  "%s\n" %  "19N between 55W and 64W" + \
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
                   "%s\n" %  "Synopsis for the SW N Atlantic including the Bahamas" + \
                   "%s\n" % self._timeLabel + "\n" + \
                   synopsis2 + "\n$$\n\n"
        else:
            pass

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
            dict["WaveHeight"] = (15, 10)#changed 3/4/16 for testing ERA
            dict["Swell"] = (15, 10)
        else:
            dict["Wind"] = (10, 10)
            dict["WindGust"] = (10, 0)
            #dict["WaveHeight"] = (15, 10)
            dict["WaveHeight"] = (10, 5) #changed 3/4/16 for testing ERA
            dict["Swell"] = (10, 10)
#        dict["Wind"] =  (0, 3)
#        dict["WaveHeight"] = (5,5)
        return dict

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] =  3  #changed from 2 to 3 ERA 10/15/14... # Changed to 1 (from 2) by JL/1/31/12 for testing
        #dict["WindWaveHgt"] =  2
        dict["Wind"] = 10 # Changed to 5 (from 10) by JL/1/31/12 for testing
        dict["WindGust"] = 250
        dict["Swell"] =  5
        dict["Visibility"] = 5 # in nautical miles. Report if less than this value.
        return dict

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
        print("wspd = ", wspd) #added this line 06/26/2016 per CJacobson for testing of failure -JL
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
        if words:
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
        dict["up to"] =  "less than"
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
        dict["Wind"] =  "variable winds less than 5 kt"
        dict["Swell"] =  ""
        return dict

    def null_phrase_dict(self, tree, node):
        # Phrase to use for null values in subPhrases other than the first
        # Can be an empty string
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
        # Was changed to "" to help with repetitive wording 10/01/14 era
        # blank null phrase caused problems with transition phrases for low wave height values
        # changed back to "2 feet or less" 08/06/15 CNJ/JL/ERA
        dict["WaveHeight"] =  "2 feet or less"
        #dict["WindWaveHgt"] =  "1 feet or less"
        dict["Wind"] =  "variable less than 5 kt"
        dict["Wx"] =  ""
        dict["Swell"] =  "light"
        dict["hurricane force winds to"] =  "hurricane force winds to"
        dict["storm force winds to"] = "storm force winds to"
        dict["gales to"] =  "gales to"
        dict["up to"] =  "variable winds less than 5 kt"
        return dict

    def phrase_connector_dict(self, tree, node):
        # Dictionary of connecting phrases for various
        # weather element phrases
        # The value for an element may be a phrase or a method
        # If a method, it will be called with arguments:
        #   tree, node
        dict = TextRules.TextRules.phrase_connector_dict(self, tree, node)
        dict["rising to"] =  {
                                "Wind": ", increasing to ",
                                "Swell": ", building to ",
                                "Swell2": ", building to ",
                                "WaveHeight": ", building to ",
                                "WindWaveHgt": ", building to ",
                         }

        dict["easing to"] =  {
                                "Wind": ", diminishing to ",
                                "Swell": ", subsiding to ",
                                "Swell2": ", subsiding to ",
                                "WaveHeight": ", subsiding to ",
                                "WindWaveHgt": ", subsiding to ",
                         }
        dict["backing"] =  {
                                "Wind": ", shifting to ",
                                "Swell": ", becoming ",
                                "Swell2": ", becoming ",
                                "WaveHeight": ", becoming ",
                                "WindWaveHgt": ", becoming ",
                         }

        dict["veering"] =  {
                                "Wind": ", shifting to ",
                                "Swell": ", becoming ",
                                "Swell2": ", becoming ",
                                "WaveHeight": ", becoming ",
                                "WindWaveHgt": ", becoming ",
                         }

        dict["becoming"] =  ", becoming "
        dict["increasing to"] =  {
                                "Wind":  ", increasing to ",
                                "Swell": ", building to ",
                                "Swell2": ", building to ",
                                "WaveHeight": ", building to ",
                                "WindWaveHgt": ", building to ",
                             }
        dict["decreasing to"] =  {
                                "Wind":  ", diminishing to ",
                                "Swell": ", subsiding to ",
                                "Swell2": ", subsiding to ",
                                "WaveHeight": ", subsiding to ",
                                "WindWaveHgt": ", subsiding to ",
                             }
        dict["shifting to the"] =  {
                                  "Wind":  ", shifting ",
                                  "Swell": ", becoming ",
                                  "Swell2": ", becoming ",
                                  "WaveHeight": ", becoming ",
                                  "WindWavHgt": ", becoming ",
                             }
#        dict["shifting to the"] =  "...shifting " Corrected wave heights "shifting" with above entries EC - 04/19/12
        dict["becoming onshore"] =  " becoming onshore "
        dict["then"] =  {"Wx": ". ",
                         "Vector": ", becoming ",
                         "Scalar": ", becoming ",
                         #"otherwise": "...becoming ",
                         "otherwise": ", becoming ", #Changed BACK to BECOMING for "SEAS 2 FT OR LESS...BECOMING 3 FT" -JL/10/28/14
                                                        #AS THIS IMPACTS BOTH BUILDING AND SUBSIDING
                         }
        return dict

    # Connectors - override to fix null phrase transition problem - 8/7/15 CNJ/JL
    def scalarConnector(self, tree, subPhrase):
        # return connector phrase to connect subPhrase and previous one
        elementName = subPhrase.getAncestor("firstElement").name
        then = self.phrase_connector(tree, subPhrase, "then", elementName)
        #if subPhrase.get("null") or subPhrase.getPrev().get("null"):
        prev = subPhrase.getPrev()
        if self.isNull(subPhrase) or self.isNull(prev):
            if elementName == "WaveHeight":
                subPhrase1 = subPhrase.getPrev()
                val1 = self.getScalarData(tree, subPhrase1, elementName, "Average")
                val2 = self.getScalarData(tree, subPhrase, elementName, "Average")
                if val1 > val2:
                    connector = ", subsiding to "
                elif val1 < val2:
                    connector = ", building to "
                else:
                    connector = then
                return connector
            else:
                return then
        # Check for either subPhrase specifying only special connector
        connector = subPhrase.get("connector")
        if connector is not None:
            return connector
        connector = prev.get("connector")
        if connector is not None:
            return connector

        # Check for increasing/decreasing values
        subPhrase1 = subPhrase.getPrev()
        val1 = self.getScalarData(tree, subPhrase1, elementName, "Average")
        val2 = self.getScalarData(tree, subPhrase, elementName, "Average")
        if val1 > val2:
            connector = self.phrase_connector(tree, subPhrase, "decreasing to", elementName)
        elif val1 < val2:
            connector = self.phrase_connector(tree, subPhrase, "increasing to", elementName)
        else:
            connector = then
        return connector

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
                (12, 25): 10, #CHANGED FROM 5 ERA 12/1/15
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
            "Wind": 60, # degrees (Was 90 for TAFB) #CHANGED FROM 45 TO 60 AFTER 3HRLY GRIDS IMPLEMENTATION-ERA
            "Swell": 60, # degrees
            "Swell2": 60, # degrees
            }

    def element_outUnits_dict(self, tree, node):
        dict = TextRules.TextRules.element_outUnits_dict(self, tree, node)
        dict["Visibility"] = "NM"
        return dict

    def rounding_method_dict(self, tree, node):
        # Special rounding methods
        #
        return {
            "Wind": self.marineRounding,
            }

    def scalar_difference_nlValue_dict(self, tree, node):
        # Scalar difference.  If the difference between scalar values
        # for 2 sub-periods is greater than or equal to this value,
        # the different values will be noted in the phrase.
        return {
           # "WaveHeight": 2.5, #0, # in feet
             "WaveHeight":       {
                 (0, 2): 2, #CHANGED FROM 1 ERA 09/30/14, 12/02/15
                 (2, 4): 2,
                 (4, 7): 3,
                 (7, 11): 3, #changed from 4 era 2/25/18
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

# added 4/18/18 to fix controversy ERA

    def wave_range(self, avg):
        # Make wave ranges based off the average wave value
        table = ((0, "3 ft or less"), (1, "3 ft or less"),
                 (1.5, "3 ft or less"), (2, "3 ft or less"),
                 (3, "3 ft or less"), (4, "2 to 4 ft"),
                 (5, "3 to 5 ft"), (6, "4 to 6 ft"),
                 (7, "5 to 7 ft"), (8, "6 to 8 ft"),
                 (9, "6 to 9 ft"), (10, "7 to 10 ft"),
                 (11, "7 to 11 ft"), (12, "8 to 12 ft"),
                 (13, "9 to 13 ft"), (14, "9 to 14 ft"),
                 (15, "10 to 15 ft"), (16, "10 to 16 ft"),
                 (17, "11 to 17 ft"), (18, "12 to 18 ft"),
                 (19, "12 to 19 ft"), (20, "13 to 20 ft"),
                 (21, "14 to 21 ft"), (22, "14 to 22 ft"),
                 (23, "15 to 23 ft"), (24, "16 to 24 ft"),
                 (25, "16 to 25 ft"), (26, "17 to 26 ft"),
                 (27, "18 to 27 ft"), (28, "19 to 28 ft"),
                 (29, "19 to 29 ft"), (30, "20 to 30 ft"),
                 (31, "21 to 31 ft"), (32, "21 to 32 ft"),
                 (33, "22 to 33 ft"), (34, "22 to 34 ft"),
                 (35, "23 to 35 ft"), (36, "24 to 36 ft"),
                 (37, "25 to 37 ft"), (38, "26 to 38 ft"),
                 (39, "26 to 39 ft"), (40, "27 to 40 ft"),
                 (45, "30 to 45 ft"), (50, "33 to 50 ft"),
                 (55, "over 50 ft"))
        range = ""
        for max, str in table:
            if avg <= max:
                range = str
                break
        return range

#commented out ERA 2/16/18 ############################################################

#     def wave_range(self, avg):
#         # Make wave ranges based off the average wave value
#         table = ((0, "less than 1 ft"), (1, "1 ft or less"),
#                  (1.5, "1 to 2 ft"), (2, "1 to 3 ft"),
#                  (3, "2 to 4 ft"), (4, "3 to 5 ft"),
#                  (5, "3 to 6 ft"), (6, "4 to 7 ft"),
#                  (7, "5 to 8 ft"), (8, "6 to 10 ft"),
#                  (9, "8 to 10 ft"), (10, "9 to 11 ft"),
#                  (11, "10 to 12 ft"), (12, "11 to 13 ft"),
#                  (13, "12 to 14 ft"), (14, "12 to 16 ft"),
#                  (15, "13 to 17 ft"), (16, "14 to 18 ft"),
#                  (17, "15 to 20 ft"), (18, "15 to 20 ft"),
#                  (19, "17 to 23 ft"), (20, "17 to 23 ft"),
#                  (21, "18 to 24 ft"), (22, "19 to 25 ft"),
#                  (23, "20 to 26 ft"), (24, "20 to 28 ft"),
#                  (25, "20 to 30 ft"), (26, "20 to 30 ft"),
#                  (27, "22 to 32 ft"), (28, "23 to 33 ft"),
#                  (29, "24 to 34 ft"), (30, "25 to 35 ft"),
#                  (31, "25 to 35 ft"), (32, "27 to 37 ft"),
#                  (33, "28 to 38 ft"), (34, "30 to 40 ft"),
#                  (35, "30 to 40 ft"), (36, "30 to 40 ft"),
#                  (37, "32 to 42 ft"), (38, "33 to 43 ft"),
#                  (38, "34 to 44 ft"), (39, "35 to 45 ft"),
#                  (40, "35 to 45 ft"), (45, "40 to 50 ft"),
#                  (50, "45 to 55 ft"), (55, "50 to 60 ft"),
#                  (100, "over 60 ft"))
#         range = ""
#         for max, str in table:
#             if avg <= max:
#                 range = str
#                 break
#         return range
#######################################################################################

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
############################################################################
#from BASELINE era 2/26/18


#     def wave_range(self, avg):
#         # Make wave ranges based off the average wave value
#         table = ((0, "2 feet or less"), (1, "2 feet or less"),
#                  (1.5, "1 to 2 feet"), (2, "1 to 3 feet"),
#                  (3, "2 to 4 feet"), (4, "3 to 5 feet"),
#                  (5, "3 to 6 feet"), (6, "4 to 7 feet"),
#                  (7, "5 to 7 feet"), (8, "6 to 9 feet"),
#                  (10, "8 to 10 feet"), (12, "10 to 12 feet"),
#                  (14, "12 to 14 feet"), (18, "14 to 18 feet"),
#                  (20, "15 to 20 feet"), (100, "over 20 feet"))
#         range = ""
#         for max, str in table:
#             if avg <= max:
#                 range = str
#                 break
#         return range
#############################################################################


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
# #        print(wave, "Wave!")
#         if wave is None:
#             return 10
#         if wave <= 6:
#             rtnval = 6
#         else:
#             val = wave * .25
#             rtnval = int(val+0.5)

    def waveht_scalar_value(self, tree, node, elementName, elementName1):
        # calculating the scalar value for changes based on wave height
        wave = tree.stats.get("WaveHeight", node.getTimeRange(), node.getAreaLabel(),
                                             mergeMethod="Max")
#        print(wave, "Wave!")
        if wave is None:
            return 10
        if wave <= 6:
            rtnval = 6
        else:
            val = wave * .25
            rtnval = int(val+0.5)

    def wave_phrase(self):
        return {
            "setUpMethod": self.wave_setUp,
            "wordMethod": self.waveHeight_words,
            "phraseMethods": self.standard_phraseMethods()
            }

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


    def subPhrase_limit(self, tree, node):
        # If the number of sub-phrases is greater than this limit, the weather
        # phrase will use 6-hour instead of the higher resolution to produce:
        #
        #    Occasional snow possibly mixed with sleet and freezing
        #    drizzle in the morning, then a chance of rain possibly mixed wiht snow
        #    and sleet and freezing drizzle in the afternoon.
        #
        # instead of:
        #    Occasional snow in the morning. Chance of light sleet and
        #    slight chance of light freezing drizzle in the late morning and
        #    early afternoon. Chance of snow early in the afternoon. Chance of
        #    rain in the afternoon.


        return 30


     ########################################################################
    # ADDED CODE BY MUSONDA TO GIVE WIND DIRECTION RANGE LIKE N TO NE

    def dirList(self):
        dirSpan = 22.5
        base = 11.25
        return[
            ('N', 360-base, 361),
            ('N', 0, base),
            ('N to NE', base, base+1*dirSpan),
            ('NE', base+1*dirSpan, base+2*dirSpan),
            ('NE to E', base+2*dirSpan, base+3*dirSpan),
            ('E', base+3*dirSpan, base+4*dirSpan),
            ('E to SE', base+4*dirSpan, base+5*dirSpan),
            ('SE', base+5*dirSpan, base+6*dirSpan),
            ('SE to S', base+6*dirSpan, base+7*dirSpan),
            ('S', base+7*dirSpan, base+8*dirSpan),
            ('S to SW', base+8*dirSpan, base+9*dirSpan),
            ('SW', base+9*dirSpan, base+10*dirSpan),
            ('SW to W', base+10*dirSpan, base+11*dirSpan),
            ('W', base+11*dirSpan, base+12*dirSpan),
            ('W to NW', base+12*dirSpan, base+13*dirSpan),
            ('NW', base+13*dirSpan, base+14*dirSpan),
            ('NW to N', base+14*dirSpan, base+15*dirSpan),
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
#
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
                          ("Wind", self.vectorModeratedMinMax, [6]),
                         # ("Wind", self.vectorMinMax, [6]),
                          ("WindGust", self.moderatedMax, [6]),
                          ("WaveHeight", self.moderatedMinMax, [6]), #changed from moderatedMax ERA 7/27/20

                          #added below based on what MFL uses 07/10/14 -JL
                          #("WaveHeight", self.maximum, [3]), #changed era 3/2/16

                         # ("WindWaveHgt", self.moderatedMinMax, [6]),
                         ("Swell", self.vectorModeratedMinMax, [6]),
                         ("Swell2", self.vectorModeratedMinMax, [6]),
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
                           #self.swell_withPeriods_phrase,
                           # Alternative:
                           #self.swell_phrase,
                           #self.period_phrase,
                           # WEATHER
#                           self.weather_phrase,

#                           self.weather_phrase,
                           # uncommented below to include Local Effects (JL - 12/12/11)
                           (self.wave_phrase, self._WaveHeightLocalEffects_list),
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
                ("Wind", ["le_gmz013_w_of_90w",
                          "le_gmz013_main",
                          "le_gmz015_s_of_27n",
                          "le_gmz015_main",
                          "le_gmz017_w_of_96w",
                          "le_gmz017_main",
                          "le_gmz019_s_of_24n",
                          "le_gmz019_main",
                          "le_gmz021_straits_of_florida",
                          "le_gmz021_main",
                          #"le_gmz023_60nm_of_veracruz",
                          "le_gmz023_s_of_21n_w_of_95w",
                          "le_gmz023_main",
                          #"le_gmz025_s_of_19n",
                          "le_gmz025_60nm_of_campeche",
                          "le_gmz025_main",
                          "le_amz011_yucatan_channel",
                          "le_amz011_main",
                          "le_amz013_cuba_jamaica",
                          "le_amz013_main",
                          "le_amz017_s_of_17n_w_of_87w",
                          "le_amz017_main",
                          "le_amz021_w_of_77w",
                          "le_amz021_main",
                          "le_amz023_lee_of_dr",
                          "le_amz023_main_wind",
                          #"le_amz025_anegada",
                          "le_amz025_atlc_exposures_and_passages",
                          "le_amz025_main",
                          "le_amz029_nicaraguan_coast",
                          "le_amz029_main",
                          "le_amz055_colombian_coast",
                          "le_amz055_main",
                          #"le_amz033_s_of_13n_w_of_68w",
                          "le_amz056_gulf_of_venezuela",
                          "le_amz056_main",
                          "le_amz035_atlantic",
                          "le_amz035_main",
                          "le_amz037_s_of_10n",
                          "le_amz037_main",
                          "le_amz039_s_of_10n",
                          #"le_amz039_w_of_80w",
                          "le_amz039_main",
                          "le_amz111_n_of_29n_w_of_79w",
                          "le_amz111_main",
                          "le_amz113_n_of_29n",
                          "le_amz113_main",
                          "le_amz115_n_of_29n",
                          "le_amz115_main",
                          "le_amz117_atlc_exposures",
                          "le_amz117_main",
                          "le_amz119_n_of_25n",
                          "le_amz119_main",
                          "le_amz121_n_of_25n",
                          "le_amz121_main",
                          "le_amz127_e_of_60w",
                          "le_amz127_main"
                            ]),
                ("WaveHeight", ["le_gmz013_w_of_90w",
                                "le_gmz013_main",
                                "le_gmz015_s_of_27n",
                                "le_gmz015_main",
                                "le_gmz017_w_of_96w",
                                "le_gmz017_main",
                                "le_gmz019_s_of_24n",
                                "le_gmz019_main",
                                "le_gmz021_straits_of_florida",
                                "le_gmz021_main",
                                #"le_gmz023_s_of_21n_w_of_95w",
                                #"le_gmz023_60nm_of_veracruz",
                                #"le_gmz023_main",
                                #"le_gmz025_s_of_19n",
                                "le_gmz025_60nm_of_campeche",
                                "le_gmz025_main",
                                "le_amz011_yucatan_channel",
                                "le_amz011_main",
                                "le_amz013_cuba_jamaica",
                                "le_amz013_main",
                                "le_amz017_s_of_17n_w_of_87w",
                                "le_amz017_main",
                                "le_amz021_w_of_77w",
                                "le_amz021_main",
                                #"le_amz023_mona_swell",
                                #"le_amz023_main_swell",
                                #"le_amz025_anegada",
                                "le_amz025_atlc_exposures_and_passages",
                                "le_amz025_main",
                                "le_amz029_nicaraguan_coast",
                                "le_amz029_main",
                                "le_amz055_colombian_coast",
                                "le_amz055_main",
                                #"le_amz033_s_of_13n_w_of_68w",
                                "le_amz056_gulf_of_venezuela",
                                "le_amz056_main",
                                "le_amz035_atlantic",
                                "le_amz035_main",
                                "le_amz037_s_of_10n",
                                "le_amz037_main",
                                "le_amz039_s_of_10n",
                                #"le_amz039_w_of_80w",
                                "le_amz039_main",
                                "le_amz111_n_of_29n_w_of_79w",
                                "le_amz111_main",
                                "le_amz113_n_of_29n",
                                "le_amz113_main",
                                "le_amz115_n_of_29n",
                                "le_amz115_main",
                                "le_amz117_atlc_exposures",
                                "le_amz117_main",
                                "le_amz119_n_of_25n",
                                "le_amz119_main",
                                "le_amz121_n_of_25n",
                                "le_amz121_main",
                                "le_amz127_e_of_60w",
                                "le_amz127_main"
                                  ]),
                    ]
                }

    #Addition - taken from MFL CWF
    def _WaveHeightLocalEffects_list(self, tree, node):
        leArea1 = self.LocalEffectArea("le_gmz013_main", "elsewhere")
        leArea2 = self.LocalEffectArea("le_gmz013_w_of_90w", "W of 90W")
        leArea3 = self.LocalEffectArea("le_gmz015_main", "elsewhere")
        leArea4 = self.LocalEffectArea("le_gmz015_s_of_27n", "S of 27N")
        leArea5 = self.LocalEffectArea("le_gmz017_main", "elsewhere")
        leArea6 = self.LocalEffectArea("le_gmz017_w_of_96w", "W of 96W")
        leArea7 = self.LocalEffectArea("le_gmz019_main", "elsewhere")
        leArea8 = self.LocalEffectArea("le_gmz019_s_of_24n", "S of 24N")
        leArea9 = self.LocalEffectArea("le_gmz021_main", "elsewhere")
        leArea10 = self.LocalEffectArea("le_gmz021_straits_of_florida", "Straits of Florida")
        leArea11 = self.LocalEffectArea("le_gmz023_main", "elsewhere")
        leArea12 = self.LocalEffectArea("le_gmz023_s_of_21n_w_of_95w", "S of 21N W of 95W")
        #leArea12 = self.LocalEffectArea("le_gmz023_60nm_of_veracruz", "WITHIN 60 NM OF COAST OF VERACRUZ")
        leArea13 = self.LocalEffectArea("le_gmz025_main", "elsewhere")
        leArea14 = self.LocalEffectArea("le_gmz025_60nm_of_campeche", "within 60 nm of coast of Campeche")
        #leArea15 = self.LocalEffectArea("le_gmz025_s_of_19n", "S OF 19N")
        leArea16 = self.LocalEffectArea("le_amz011_main", "elsewhere")
        leArea17 = self.LocalEffectArea("le_amz011_yucatan_channel", "in Yucatan Channel")
        leArea18 = self.LocalEffectArea("le_amz013_main", "elsewhere")
        leArea19 = self.LocalEffectArea("le_amz013_cuba_jamaica", "between Cuba and Jamaica")
        leArea20 = self.LocalEffectArea("le_amz021_main", "elsewhere")
        leArea21 = self.LocalEffectArea("le_amz021_n_of_17n", "N of 17N")
        #leArea21 = self.LocalEffectArea("le_amz021_w_of_77w", "W OF 77W")
        leArea22 = self.LocalEffectArea("le_amz023_main_swell", "elsewhere")
        leArea23 = self.LocalEffectArea("le_amz023_mona_swell", "in Mona Passage")
        leArea24 = self.LocalEffectArea("le_amz025_main", "elsewhere")
        leArea25 = self.LocalEffectArea("le_amz025_atlc_exposures_and_passages", "in Atlantic exposures and passages")
       # leArea26 = self.LocalEffectArea("le_amz025_atlantic", "ATLANTIC EXPOSURES")
        leArea27 = self.LocalEffectArea("le_amz029_main", "elsewhere")
        leArea28 = self.LocalEffectArea("le_amz029_nicaraguan_coast", "within 60 nm of coast of Nicaragua")
        leArea29 = self.LocalEffectArea("le_amz055_main", "elsewhere")
        leArea30 = self.LocalEffectArea("le_amz055_colombian_coast", "within 90 nm of coast of Colombia")
        leArea31 = self.LocalEffectArea("le_amz056_main", "elsewhere")
        #leArea32 = self.LocalEffectArea("le_amz033_s_of_13n_w_of_68w", "S OF 13N W OF 68W")
        leArea32 = self.LocalEffectArea("le_amz056_gulf_of_venezueula", "Gulf of Venezuela")
        leArea33 = self.LocalEffectArea("le_amz035_main", "elsewhere")
        leArea34 = self.LocalEffectArea("le_amz035_atlantic", "Atlantic Exposures")
        leArea35 = self.LocalEffectArea("le_amz037_main", "elsewhere")
        leArea36 = self.LocalEffectArea("le_amz037_s_of_10n", "S of 10N")
        leArea37 = self.LocalEffectArea("le_amz039_main", "elsewhere")
        leArea38 = self.LocalEffectArea("le_amz039_s_of_10n", "S of 10N")
        #leArea38 = self.LocalEffectArea("le_amz039_w_of_80w", "W OF 80W")
        leArea39 = self.LocalEffectArea("le_amz111_main", "elsewhere")
        leArea40 = self.LocalEffectArea("le_amz111_n_of_29n_w_of_79w", "N of 29N W of 79W")
        leArea41 = self.LocalEffectArea("le_amz113_main", "elsewhere")
        leArea42 = self.LocalEffectArea("le_amz113_n_of_29n", "N of 29N")
        leArea43 = self.LocalEffectArea("le_amz115_main", "elsewhere")
        leArea44 = self.LocalEffectArea("le_amz115_n_of_29n", "N of 29N")
        leArea45 = self.LocalEffectArea("le_amz117_main", "elsewhere")
        leArea46 = self.LocalEffectArea("le_amz117_atlc_exposures", "Atlantic Exposures")
        leArea47 = self.LocalEffectArea("le_amz119_main", "elsewhere")
        leArea48 = self.LocalEffectArea("le_amz119_n_of_25n", "N of 25N")
        leArea49 = self.LocalEffectArea("le_amz121_main", "elsewhere")
        leArea50 = self.LocalEffectArea("le_amz121_n_of_25n", "N of 25N")
        leArea51 = self.LocalEffectArea("le_amz127_main", "elsewhere")
        leArea52 = self.LocalEffectArea("le_amz127_e_of_60w", "E of 60W")
        leArea53 = self.LocalEffectArea("le_amz017_main", "elsewhere")
        leArea54 = self.LocalEffectArea("le_amz017_s_of_17n_w_of_87w", "S of 17N W of 87W")

        return [self.LocalEffect([leArea2, leArea1], 2, ", and "),
                #[self.LocalEffect([leArea1, leArea2], 2, "...EXCEPT "),
                # Changed "...EXCEPT " TO "E OF 90W AND ". Renders "SEAS x TO x FT E OF 90W AND x TO x FT W OF 90W" EC - 4/20/12
                #self.LocalEffect([leArea2, leArea1], 2, ". elsewhere..."),
                # Tried the entry above to put leArea first then elsewhere - JL/NHC - 02/12/12
                self.LocalEffect([leArea4, leArea3], 2, ", and "),
                self.LocalEffect([leArea6, leArea5], 2, ", and "),
                self.LocalEffect([leArea8, leArea7], 2, ", and "),
                self.LocalEffect([leArea10, leArea9], 2, ", and "),
                self.LocalEffect([leArea12, leArea11], 2, ", and "),
                self.LocalEffect([leArea14, leArea13], 2, ", and "), # removed leArea15
                self.LocalEffect([leArea17, leArea16], 2, ", and "),
                self.LocalEffect([leArea19, leArea18], 2, ", and "),
                self.LocalEffect([leArea21, leArea20], 2, ", and "),
                self.LocalEffect([leArea23, leArea22], 2, ", and "),
                self.LocalEffect([leArea25, leArea24], 2, ", and "),
                self.LocalEffect([leArea28, leArea27], 2, ", and "),
                self.LocalEffect([leArea30, leArea29], 1, ", and "),
                self.LocalEffect([leArea32, leArea31], 2, ", and "),
                self.LocalEffect([leArea34, leArea33], 2, ", and "),
                self.LocalEffect([leArea36, leArea35], 2, ", and "),
                self.LocalEffect([leArea38, leArea37], 2, ", and "),
                self.LocalEffect([leArea40, leArea39], 2, ", and "),
                self.LocalEffect([leArea42, leArea41], 2, ", and "),
                self.LocalEffect([leArea44, leArea43], 2, ", and "),
                self.LocalEffect([leArea46, leArea45], 1, ", and "), #changed from 2 to get "seas less than 2 ft" wording ERA 6/26/16
                self.LocalEffect([leArea48, leArea47], 2, ", and "),
                self.LocalEffect([leArea50, leArea49], 2, ", and "),
                self.LocalEffect([leArea52, leArea51], 2, ", and "),
                self.LocalEffect([leArea54, leArea53], 2, ", and "),
                ]

    def _windLocalEffects_list(self):
        leArea1 = self.LocalEffectArea("le_gmz013_main", "elsewhere")
        leArea2 = self.LocalEffectArea("le_gmz013_w_of_90w", "W of 90W")
        leArea3 = self.LocalEffectArea("le_gmz015_main", "elsewhere")
        leArea4 = self.LocalEffectArea("le_gmz015_s_of_27n", "S of 27N")
        leArea5 = self.LocalEffectArea("le_gmz017_main", "elsewhere")
        leArea6 = self.LocalEffectArea("le_gmz017_w_of_96w", "W of 96W")
        leArea7 = self.LocalEffectArea("le_gmz019_main", "elsewhere")
        leArea8 = self.LocalEffectArea("le_gmz019_s_of_24n", "S of 24N")
        leArea9 = self.LocalEffectArea("le_gmz021_main", "elsewhere")
        leArea10 = self.LocalEffectArea("le_gmz021_straits_of_florida", "Straits of Florida")
        leArea11 = self.LocalEffectArea("le_gmz023_main", "elsewhere")
        leArea12 = self.LocalEffectArea("le_gmz023_s_of_21n_w_of_95w", "S of 21N W of 95W")
        #leArea12 = self.LocalEffectArea("le_gmz023_60nm_of_veracruz", "WITHIN 60 NM OF COAST OF VERACRUZ")
        leArea13 = self.LocalEffectArea("le_gmz025_main", "elsewhere")
        leArea14 = self.LocalEffectArea("le_gmz025_60nm_of_campeche", "within 60 nm of coast of Campeche")
        #leArea15 = self.LocalEffectArea("le_gmz025_s_of_19n", "S OF 19N")
        leArea16 = self.LocalEffectArea("le_amz011_main", "elsewhere")
        leArea17 = self.LocalEffectArea("le_amz011_yucatan_channel", "in Yucatan Channel")
        leArea18 = self.LocalEffectArea("le_amz013_main", "elsewhere")
        leArea19 = self.LocalEffectArea("le_amz013_cuba_jamaica", "between Cuba and Jamaica")
        leArea20 = self.LocalEffectArea("le_amz021_main", "elsewhere")
        leArea21 = self.LocalEffectArea("le_amz021_n_of_17n", "N of 17N")
        #leArea21 = self.LocalEffectArea("le_amz021_w_of_77w", "W OF 77W")

        #leArea22 = self.LocalEffectArea("le_amz023_main_swell","elsewhere")
        #leArea23 = self.LocalEffectArea("le_amz023_mona_swell", "In Mona Passage")

        #changed to test tropical crash incident ERA 8/30/20

        leArea22 = self.LocalEffectArea("le_amz023_main_wind", "elsewhere")
        leArea23 = self.LocalEffectArea("le_amz023_lee_of_dr", "In Mona Passage")

        leArea24 = self.LocalEffectArea("le_amz025_main", "elsewhere")
        leArea25 = self.LocalEffectArea("le_amz025_atlc_exposures_and_passages", "In Atlantic Exposures and Passages")
        #leArea26 = self.LocalEffectArea("le_amz025_atlantic", "ATLANTIC EXPOSURES")
        leArea27 = self.LocalEffectArea("le_amz029_main", "elsewhere")
        leArea28 = self.LocalEffectArea("le_amz029_nicaraguan_coast", "within 60 nm of coast of Nicaragua")
        leArea29 = self.LocalEffectArea("le_amz055_main", "elsewhere")
        leArea30 = self.LocalEffectArea("le_amz055_colombian_coast", "within 90 nm of coast of Colombia")
        leArea31 = self.LocalEffectArea("le_amz056_main", "elsewhere")
        #leArea32 = self.LocalEffectArea("le_amz033_s_of_13n_w_of_68w", "S OF 13N W OF 68W")
        leArea32 = self.LocalEffectArea("le_amz056_gulf_of_venezuela", "Gulf of Venezuela")
        leArea33 = self.LocalEffectArea("le_amz035_main", "elsewhere")
        leArea34 = self.LocalEffectArea("le_amz035_atlantic", "Atlantic Exposures")
        leArea35 = self.LocalEffectArea("le_amz037_main", "elsewhere")
        leArea36 = self.LocalEffectArea("le_amz037_s_of_10n", "S of 10N")
        leArea37 = self.LocalEffectArea("le_amz039_main", "elsewhere")
        leArea38 = self.LocalEffectArea("le_amz039_s_of_10n", "S of 10N")
        #leArea38 = self.LocalEffectArea("le_amz039_w_of_80w", "W OF 80W")
        leArea39 = self.LocalEffectArea("le_amz111_main", "elsewhere")
        leArea40 = self.LocalEffectArea("le_amz111_n_of_29n_w_of_79w", "N of 29N W of 79W")
        leArea41 = self.LocalEffectArea("le_amz113_main", "elsewhere")
        leArea42 = self.LocalEffectArea("le_amz113_n_of_29n", "N of 29N")
        leArea43 = self.LocalEffectArea("le_amz115_main", "elsewhere")
        leArea44 = self.LocalEffectArea("le_amz115_n_of_29n", "N of 29N")
        leArea45 = self.LocalEffectArea("le_amz117_main", "elsewhere")
        leArea46 = self.LocalEffectArea("le_amz117_atlc_exposures", "Atlantic Exposures")
        leArea47 = self.LocalEffectArea("le_amz119_main", "elsewhere")
        leArea48 = self.LocalEffectArea("le_amz119_n_of_25n", "N of 25N")
        leArea49 = self.LocalEffectArea("le_amz121_main", "elsewhere")
        leArea50 = self.LocalEffectArea("le_amz121_n_of_25n", "N of 25N")
        leArea51 = self.LocalEffectArea("le_amz127_main", "elsewhere")
        leArea52 = self.LocalEffectArea("le_amz127_e_of_60w", "E of 60W")
        leArea53 = self.LocalEffectArea("le_amz017_main", "elsewhere")
        leArea54 = self.LocalEffectArea("le_amz017_s_of_17n_w_of_87w", "S of 17N W of 87W")

        return [self.LocalEffect([leArea2, leArea1], 5, ", and "),
                #[self.LocalEffect([leArea1, leArea2], 2, "...EXCEPT "),
                # Changed "...EXCEPT " TO "E OF 90W AND ". Renders "SEAS x TO x FT E OF 90W AND x TO x FT W OF 90W" EC - 4/20/12
                #self.LocalEffect([leArea2, leArea1], 2, ". elsewhere..."),
                # Tried the entry above to put leArea first then elsewhere - JL/NHC - 02/12/12
                self.LocalEffect([leArea4, leArea3], 5, ", and "),
                self.LocalEffect([leArea6, leArea5], 5, ", and "),
                self.LocalEffect([leArea8, leArea7], 5, ", and "),
                self.LocalEffect([leArea10, leArea9], 5, ", and "),
                self.LocalEffect([leArea12, leArea11], 5, ", and "),
                self.LocalEffect([leArea14, leArea13], 5, ", and "), # removed leArea15
                self.LocalEffect([leArea17, leArea16], 5, ", and "),
                self.LocalEffect([leArea19, leArea18], 5, ", and "),
                self.LocalEffect([leArea21, leArea20], 5, ", and "),
                self.LocalEffect([leArea23, leArea22], 5, ", and "),
                self.LocalEffect([leArea25, leArea24], 5, ", and "),
                self.LocalEffect([leArea28, leArea27], 5, ", and "),
                self.LocalEffect([leArea30, leArea29], 4, ", and "),
                self.LocalEffect([leArea32, leArea31], 4, ", and "),
                self.LocalEffect([leArea34, leArea33], 5, ", and "),
                self.LocalEffect([leArea36, leArea35], 5, ", and "),
                self.LocalEffect([leArea38, leArea37], 5, ", and "),
                self.LocalEffect([leArea40, leArea39], 5, ", and "),
                self.LocalEffect([leArea42, leArea41], 5, ", and "),
                self.LocalEffect([leArea44, leArea43], 5, ", and "),
                self.LocalEffect([leArea46, leArea45], 5, ", and "),
                self.LocalEffect([leArea48, leArea47], 5, ", and "),
                self.LocalEffect([leArea50, leArea49], 5, ", and "),
                self.LocalEffect([leArea52, leArea51], 5, ", and "),
                self.LocalEffect([leArea54, leArea53], 2, ", and "),
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
                          ("Wind", self.vectorModeratedMinMax, [12]),
                          ("WindGust", self.moderatedMinMax, [12]),
                          ("WaveHeight", self.moderatedMinMax, [12]), #changed from 3 era 2/26/18...also changed it from moderatedMax

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
                               self.wave_phrase,
                               # SWELLS AND PERIODS
                               #self.swell_withPeriods_phrase,
                               # Alternative:
                               #self.swell_phrase,
                               #self.period_phrase,
                               # WEATHER
                               #self.weather_phrase,
                               #self.visibility_phrase,
                               ],
                }

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

        try:
            self._pdCombo = varDict["Period Combining?"]
        except:
            if self._pdCombo == "Yes":
                self._periodCombining = 1
            else:
                self._periodCombining = 0

        # Added CJ
        # Tropical exceptions
        try:
            self._includeTropical = self._includeTropical == "Yes"
        except:
            self._includeTropical = False
        if self._includeTropical:
            self._periodCombining = 0 # Changed back from 1 to 0 as PeriodCombining
            # with IncludeTropical was causing Period issues in forecast text (JL - 10/26/11)
            if self._productIssuance == "Morning with Pre-1st Period":
                self._productIssuance = "Morning"
            if self._productIssuance == "Afternoon with Pre-1st Period":
                self._productIssuance = "Afternoon"

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
                ("OFFPeriod", 12), #added by Mello 8/29/19

                ]
            narrativeDefPM = [
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12),
                ("OFFPeriod", 12), #added by Mello 8/29/19

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
                    ("OFFPeriod", 12),#changed from "period1" to 12 ERA 02/15/20
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
                    ("OFFPeriod", 12),#changed from "period1" to 12 ERA 02/15/20
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
        if self._definition["pil"] == "OFFNT4":
            if localTimeZone == "EDT":
                return [
                   ("530 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1130 AM", "issuanceHour", self.NIGHT(), 16,
                     ".Today...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "late", #CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "late", "towards morning", #CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM)
                    ]
            else:
                return [
                    ("430 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1030 AM", "issuanceHour", self.NIGHT(), 16,
                     ".Today...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "late",#CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "late", "towards morning",#CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM),
                    ]
        if self._definition["pil"] == "OFFNT3":
            if localTimeZone == "EDT":
                return [
                   ("530 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1130 AM", "issuanceHour", self.NIGHT(), 16,
                     ".Today...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "late",#CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "late", "towards morning",#CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM)
                    ]
            else:
                return [
                    ("430 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1030 AM", "issuanceHour", self.NIGHT(), 16,
                     ".Today...", "early", "towards evening",
                     1, narrativeDefAM),
                    ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "late",#CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "late", "towards morning",#CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM),
                    ]

#         #determine local time
#         localTimeZone = time.strftime("%Z")
# #print("\n\n\nTime ZOne = " + localTimeZone + "\n\n\n")
#         if self._definition["pil"] == "OFFNT4":
#             if localTimeZone == "EDT":
#                 return [
#                    ("530 AM", self.DAY(), self.NIGHT(), 16,
#                      ".Today...", "in the morning", "in the afternoon",
#                      1, narrativeDefAM),
#                     ("1130 AM", "issuanceHour", self.NIGHT(), 16,
#                      ".Today...", "early", "towards evening",
#                      1, narrativeDefAM),
#                     ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
#                      ".Tonight...", "late in the night", "early in the morning",
#                      1, narrativeDefPM),
#                     ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
#                      ".Overnight...", "early", "towards morning",
#                      1, narrativeDefPM)
#                     ]
#             else:
#                 return [
#                     ("430 AM", self.DAY(), self.NIGHT(), 16,
#                      ".Today...", "in the morning", "in the afternoon",
#                      1, narrativeDefAM),
#                     ("1030 AM", "issuanceHour", self.NIGHT(), 16,
#                      ".Today...", "early", "towards evening",
#                      1, narrativeDefAM),
#                     ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
#                      ".Tonight...", "late in the night", "early in the morning",
#                      1, narrativeDefPM),
#                     ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
#                      ".Overnight...", "early", "towards morning",
#                      1, narrativeDefPM),
#                     ]
#         if self._definition["pil"] == "OFFNT3":
#             if localTimeZone == "EDT":
#                 return [
#                    ("530 AM", self.DAY(), self.NIGHT(), 16,
#                      ".Today...", "in the morning", "in the afternoon",
#                      1, narrativeDefAM),
#                     ("1130 AM", "issuanceHour", self.NIGHT(), 16,
#                      ".Today...", "early", "towards evening",
#                      1, narrativeDefAM),
#                     ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
#                      ".Tonight...", "late in the night", "early in the morning",
#                      1, narrativeDefPM),
#                     ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
#                      ".Overnight...", "early", "towards morning",
#                      1, narrativeDefPM)
#                     ]
#             else:
#                 return [
#                     ("430 AM", self.DAY(), self.NIGHT(), 16,
#                      ".Today...", "in the morning", "in the afternoon",
#                      1, narrativeDefAM),
#                     ("1030 AM", "issuanceHour" , self.NIGHT(), 16,
#                      ".Today...", "early", "towards evening",
#                      1, narrativeDefAM),
#                     ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
#                      ".Tonight...", "late in the night", "early in the morning",
#                      1, narrativeDefPM),
#                     ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
#                      ".Overnight...", "early", "towards morning",
#                      1, narrativeDefPM),
#                     ]

#added on 2/29/16 to get rid of morning/afternoon wording...ERA

    def timePeriod_descriptor_list(self, tree, node):
        # Contains definition for localtime start/end times and phrase
        # Tuples, 0=startHrLT, 1=endHrLT, 2=phrase
        day = self.DAY()
        return [
                (day, (day+3)%24, ""),    # 6a-9a
                (day, (day+6)%24, "in the morning"),          # 6a-noon
                (day, (day+9)%24, ""),    # 6a-3p
                (day, (day+12)%24, ""),                       # 6a-6p
                (day, (day+15)%24, ""),    # 6a-9p
                (day, (day+18)%24, "through the evening"),    # 6a-midnite

                ((day+2)%24, (day+3)%24, ""),  # 8a-9a

                ((day+3)%24, (day+6)%24, ""), # 9a-noon
                ((day+3)%24, (day+9)%24, ""), # 9a-3p
                ((day+3)%24, (day+12)%24, ""),      # 9a-6p
                ((day+3)%24, (day+15)%24, ""),      # 9a-9p
                ((day+3)%24, (day+18)%24, "through the evening"),      # 9a-midnite

                ((day+5)%24, (day+6)%24, ""),      # 11a-noon

                ((day+6)%24, (day+9)%24,  ""),      # noon-3p
                ((day+6)%24, (day+12)%24, "in the afternoon"),            # noon-6p
                ((day+6)%24, (day+15)%24, ""),# noon-9p
                ((day+6)%24, (day+18)%24, ""),# noon-midnite

                ((day+8)%24, (day+9)%24, ""),      # 2pm-3pm

                ((day+9)%24, (day+12)%24, self.lateDay_descriptor),   # 3p-6p
                ((day+9)%24, (day+15)%24, ""),    # 3p-9p
                ((day+9)%24, (day+18)%24, ""),          # 3p-midnite
                ((day+9)%24, (day+21)%24, ""),     # 3p-3a
                ((day+9)%24,  day, ""),                               # 3p-6a

                ((day+11)%24, (day+12)%24, self.lateDay_descriptor), # 5p-6p

                ((day+12)%24, (day+15)%24, ""),   # 6p-9p
                ((day+12)%24, (day+18)%24, "in the evening"),         # 6p-midnite
                ((day+12)%24, (day+21)%24, ""),    # 6p-3a
                ((day+12)%24, day, ""),                               # 6p-6a

                ((day+14)%24, (day+15)%24, ""), # 8p-9p

                ((day+15)%24, (day+18)%24, ""),                  # 9p-midnite
                ((day+15)%24, (day+21)%24, ""),# 9p-3a
                ((day+15)%24, day, ""),            # 9p-6a

                ((day+17)%24, (day+18)%24, ""), # 11p-midnight

                ((day+18)%24, (day+21)%24, ""),               # midnite-3a
                ((day+18)%24, day, "after midnight"),                       # midnite-6a
                ((day+18)%24, (day+6)%24, ""),                              # midnite-noon

                ((day+20)%24, (day+21)%24, ""), # 2a-3a

                ((day+21)%24, day, self.lateNight_descriptor),              # 3a-6a
                ((day+21)%24, (day+3)%24, ""),          # 3a-9a
                ((day+21)%24, (day+6)%24, ""),          # 3a-noon
                ((day+21)%24, (day+9)%24, ""),               # 3a-3p
                ((day+21)%24, (day+12)%24, ""),                             # 3a-6p

                ((day+23)%24, (day)%24, self.lateNight_descriptor), # 5a-6a

                ]

#ADDED 12/02/15 TO ELIMINATE THE "EARLY MORNING" IN THE "TONIGHT" PERIOD...ERA (CHECK OFF FORMATTER FOR ORIGINAL VERSION)

    def lateDay_descriptor(self, statDict, argDict, timeRange):
       # If time range is in the first period, return period1 descriptor for
       #  late day -- default 3pm-6pm
       if self._issuanceInfo.period1TimeRange().contains(timeRange):
           return self._issuanceInfo.period1LateDayPhrase()
       else:
           return ""

    def lateNight_descriptor(self, statDict, argDict, timeRange):
       # If time range is in the first period, return period1 descriptor for
       #  late night -- default 3am-6am
       if self._issuanceInfo.period1TimeRange().contains(timeRange):
           return self._issuanceInfo.period1LateNightPhrase()
       else:
           return "late"


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

            ('HF.A', marineActions, 'Marine'),
            ('SR.A', marineActions, 'Marine'),
            ('GL.A', marineActions, 'Marine'),
##            ('GL.O', marineActions, 'Local'),

            ('AF.Y', allActions, 'Ashfall'),
            ('MF.Y', allActions, 'Fog'),                            # DENSE FOG ADVISORY
            ('MS.Y', allActions, 'Smoke'),                          # DENSE SMOKE ADVISORY
##            ('UP.Y', allActions, 'IceAccr'),                        # HEAVY FREEZING SPRAY ADVISORY
            ('MH.Y', allActions, 'Ashfall')                        # VOLCANIC ASHFALL ADVISORY
            ]

    def periodCombining_elementList(self, tree, node):
        # Weather Elements to determine whether to combine periods
        #return ["Sky", "Wind", "Wx", "PoP", "MaxT", "MinT"]
        # Marine
        #############################################################################
        # Swell could be added below if necessary to prevent too much period combining
        # during periods of changing swell - may affect swell wording
        # CNJ 05/05/11
        return ["WaveHeight", "Wind"]
        #############################################################################
        # Diurnal Sky Wx pattern
        #return ["DiurnalSkyWx"]

    def periodCombining_startHour(self, tree, node):
        # Hour after which periods may be combined
        return 12

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
            if areasLeft == 26: # changed from 9 to 26 for new zones 03/16/22 -JRL
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

#Commented out due to issue with NT3 and spaces and $$ after each parragraph. The previous method was found in SWELL_Overrides
# ERA 06/07/16

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
#                 #fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#                 # are we on the next to last area yet?
#                 # if so, add synopsis2
#                 if areasLeft == 9:
#                     fcst = fcst + self._Text3()
#                 fraction = fractionOne
#                 areasLeft = areasLeft - 1
#             fcst = self._postProcessProduct(fcst, argDict)
#             fcst = self.endline(fcst, linelength=self._lineLength)
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
#                 #fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
#                 #fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#                 fraction = fractionOne
#             #fcst = self._postProcessProduct(fcst, argDict)
#             #fcst = self.endline(fcst, linelength=self._lineLength)
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
                  "FR", "ZY", "VA", "<NoWx>", "<Invalid>", "SQ"],
        "coverage": ["Def", "Wide", "Brf", "Frq", "Ocnl", "Pds", "Inter",
                    "Lkly", "Num", "Sct", "Chc", "Areas",
                    "SChc", "WSct", "Iso", "Patchy", "<NoCov>", "<Invalid>"],
        "intensity": ["+", "m", "-", "--", "<NoInten>", "<Invalid>"],
        "visibility": ["0SM", "1/4SM", "1/2SM", "3/4SM", "1SM", "11/2SM", "2SM",
                      "21/2SM", "3SM", "4SM", "5SM", "6SM", "P6SM", "<NoVis>", "<Invalid>"],
        }

    def _postProcessProduct(self, fcst, argDict):
        """CWF_ER_Overrides version of CWF._postProcessProduct.

        Modified to add the capability of retaining forecast text from the
        previous CWF.
        """
        self.debug_print("\tCWF_ER_Overrides version of " +
                         "CWF._postProcessProduct")

        fcst = fcst.replace("%expireTime", self._expireTimeStr)
        #fcst = fcst.upper()

        self._userInfo = UserInfo.UserInfo()
        forecasterName = self._userInfo._getForecasterName(argDict)
        fcst += "Forecaster " + forecasterName
        self.setProgressPercentage(100)
        self.progressMessage(0, 100, self._displayName + " Complete")
        fcst = re.sub(r'  ', " ", fcst)
        fcst = fcst.replace("NATIONAL WEATHER SERVICE", "NWS")
        fcst = fcst.replace("after midnight", "late")
        fcst = re.sub(r' after\nmidnight', r' late', fcst)
        #fcst = string.replace(fcst, "kt, ", "kt,")
        #fcst = string.replace(fcst, "less, ", "less,")
        #fcst = string.replace(fcst, "elsewhere, ", "elsewhere,")
        fcst = fcst.replace(",Seas", ". Seas") #edited to make it work in mixed case ERA 6/18/17

        fcst = fcst.replace(",becoming", ", becoming")
        fcst = fcst.replace(",diminishing", ", diminishing")
        #fcst = string.replace(fcst, "morning, ", "morning,")
     #   fcst = re.sub(r' kt,\nseas', r'kt.\nSeas', fcst)
        fcst = fcst.replace(" IN EFFECT", "")
        fcst = fcst.replace("Today...", "TODAY...")
        fcst = fcst.replace("Tonight...", "TONIGHT...") #added ERA 6/18/17
        fcst = fcst.replace("Overnight...", "OVERNIGHT...")
        fcst = fcst.replace("This Afternoon...", "THIS AFTERNOON...")
        fcst = fcst.replace(",shifting", ", shifting")
        fcst = fcst.replace("Elsewhere...", "Elsewhere, ")
        fcst = fcst.replace("TSTMs", "thunderstorms")
        fcst = fcst.replace("... ", "...") #ADDED 8/25/17 WHEN ISSUE WAS FOUND WHEN TROPICAL WORDING WAS USED ERA

        fcst = fcst.replace("...GALE CONDITIONS POSSIBLE...\n...STORM CONDITIONS POSSIBLE...", "...STORM CONDITIONS POSSIBLE...") #era 1/26/18

        fcst = fcst.replace(" TROPICAL", "TROPICAL")

        fcst = fcst.replace("including including", "including")
        fcst = fcst.replace("from 18N-20N between 80W-85W", "from 18N to 20N between 80W and 85W")
        fcst = fcst.replace("from 18N-20N between 76W-80W", "from 18N to 20N between 76W and 80W")

        #fcst = string.replace(fcst, ", ", "...")
        # commented out - this causes format problems when preserving previous text - 08/11/15 CNJ/JL/ERA
        #fcst = self.endline(fcst, linelength=self._lineLength)
        print("includeTropical is: ", self._includeTropical)
        #  Try to preserve text from previous CWF
        try:
            if self._includeTropical:
                print("includeTropical is yes - previous wording disabled")
                return fcst

            #  Get the module first
            import mergeProds

            #  If this option is desired (i.e. a non zero period was chosen)
            if self._definition["pil"] == "OFFNT3":

                fcst1 = fcst.partition("AMZ101-")[0]

                fcst2 = fcst.partition("AMZ101-")[2]
                fcst2 = fcst2.partition("FORECASTER ")[0]
                fcst2 = "AMZ101-" + fcst2
                fcst2 = "FZNT23 KNHC 101851\nOFFNT3\n\n" + \
                        "OFFSHORE WATERS FORECAST FOR THE SW AND TROPICAL N ATLANTIC AND\n" + \
                        "CARIBBEAN SEA\n" + \
                        "NWS NATIONAL HURRICANE CENTER MIAMI FL\n" + \
                        "251 PM EDT MON AUG 10 2015\n\n" + \
                        "OFFSHORE WATERS FORECAST FOR THE TROPICAL N ATLANTIC FROM 07N TO\n" + \
                        "22N BETWEEN 55W AND 64W...THE SW N ATLANTIC S OF 31N W OF 65W\n" + \
                        "INCLUDING BAHAMAS...AND THE CARIBBEAN SEA.\n\n" + \
                        "SEAS GIVEN AS SIGNIFICANT WAVE HEIGHT...WHICH IS THE AVERAGE\n" + \
                        "HEIGHT OF THE HIGHEST 1/3 OF THE WAVES. INDIVIDUAL WAVES MAY BE\n" + \
                        "MORE THAN TWICE THE SIGNIFICANT WAVE HEIGHT.\n\n" + fcst2

                previousOFF = self.getPreviousProduct(self._prevProdPIL)

                previousOFF1 = previousOFF.partition("AMZ101-")[0]
                print("### previousOFF1 ###", previousOFF1)

                previousOFF2 = previousOFF.partition("AMZ101-")[2]
                previousOFF2 = previousOFF2.partition("FORECASTER ")[0]
                previousOFF2 = "AMZ101-" + previousOFF2
                print("### previousOFF2 ###", previousOFF2)

                if isinstance(self._updatePeriodIndex, type(1)) and self._updatePeriodIndex >= 0:
                    if self._updatePeriodIndex == 0:
                        print('\tRefreshing headlines only...')
                    elif self._updatePeriodIndex == 1:
                        print('\tMerging OFF text for the first period only...')
                    else:
                        print('\tMerging OFF text for the first %d periods...' % \
                                (self._updatePeriodIndex))

                    #  Get OFF1 previous product
                    #  If we actually found the previous text
                    if previousOFF1:
                        #  Merge the forecasts
                        print("*** merging fcst1 ***")
                        fcst1=mergeProds.mergeProds()._mergeCWF(fcst1, previousOFF1,
                                                               self._updatePeriodIndex)
                        print("*** fcst1 after merge:", fcst1)

                    #  Get OFF2 previous product
                    #  If we actually found the previous text
                    if previousOFF2:
                        #  Merge the forecasts
                        print("*** merging fcst2 ***")
                        fcst2=mergeProds.mergeProds()._mergeCWF(fcst2, previousOFF2,
                                                               self._updatePeriodIndex)
                        print("*** fcst2 after merge:", fcst2)
                        fcst2 = fcst2.partition("AMZ101-")[2]
                        fcst2 = fcst2.partition("FORECASTER ")[0]
                        fcst2 = "AMZ101-" + fcst2
                    fcst = fcst1 + "\n" + fcst2
                    fcst += "\nFORECASTER " + forecasterName
            else:
                if isinstance(self._updatePeriodIndex, type(1)) and self._updatePeriodIndex >= 0:
                    if self._updatePeriodIndex == 0:
                        print('\tRefreshing headlines only...')
                    elif self._updatePeriodIndex == 1:
                        print('\tMerging OFF text for the first period only...')
                    else:
                        print('\tMerging OFF text for the first %d periods...' % \
                                (self._updatePeriodIndex))

                    #  Get previous product
                    oldCWF=self.getPreviousProduct(self._prevProdPIL)

                    #  If we actually found the previous text
                    if oldCWF:

                        #  Merge the forecasts
                        fcst=mergeProds.mergeProds()._mergeCWF(fcst, oldCWF,
                                                               self._updatePeriodIndex)

        #  Otherwise, if we cannot get the previous text for whatever reason
        except:
            print('Failed to parse previous OFF!  New text will be created ' + \
                  'for all periods.')

        return fcst

 #added on 1/11/17 after 16.2 and 16.4.1 builds to change "," to "..." in LE phrase starting with "elsewhere". Found on  PhraseBuilder...ERA
    def qualifyWords(self, node, words, qualifierName, lastQualifier,
                     lastPhrase, makeSentence=1):
        # Qualifies words with local effect qualifiers
        # Also, if makeSentence==1, makes the words into a sentence
        #   when appropriate.
        # Returns the modified words and the qualifier (if any)
        #
        # Logic:
        #   If empty words, skip.
        #   If no qualifier:
        #      if makeSentence:
        #         makeSentence and return words and lastQualifier
        #   If there is a qualifier:
        #      Handle a new qualifier.
        #         If qualifier is new and non-empty:
        #           Add the qualifier and ellipses to beginning of words
        #      Handle a continuation: If the next phrase will be qualified
        #           with the same qualifier,
        #           Add ellipses to the end of the words. In this case,
        #             we will not add a period to the end of the words
        #             when making a sentence.
        #      if makeSentence, make the words into a sentence with or without
        #         a period at the end.
        #      return words and qualifier
        #
        qualifier = node.get(qualifierName)
#print("\nQualify words: qualifier, lastQualifier, words", qualifier, lastQualifier, words)
        if not words:
            return words, lastQualifier
        addPeriod = 1
        if qualifier is not None:
            if qualifier != lastQualifier and qualifier:
                words = qualifier + ", " + words
            next = self.getNext_nonEmpty(node, "words")
            if next is not None:
                nextQualifier = next.get(qualifierName)
#print("nextQualifier, qualifier", nextQualifier, "X", qualifier, "X", words)
                if nextQualifier == qualifier:
                    addPeriod = 0
                    words += ","
        if makeSentence:
            words = self.sentence(words, addPeriod)
#print("returning", words)
        return words, qualifier
