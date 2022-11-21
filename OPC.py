import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis
import TimeRange

#from pprint import pprint
import UserInfo

# Define Regional overrides of Product Definition settings and
# default values of additional Regional Definition settings
#  ( This Definition section must be before the Class definition)

#***** THIS NEXT LINE IS REQUIRED *****
Definition = {}

#####################################################
# Override VariableList if desired
#
#VariableList = []
VariableList = [
    (("Include Tropical?", "includeTropical"), "No", "radio", ["Yes", "No"]),
        ]
#
# NC Definitions:
# Definition statements must start in column 1

### Regional settings of baseline options: ###

#Definition["displayName"] = "OFF_NC"
Definition["productName"] = "OFFSHORE WATERS FORECAST"  # name of product
Definition["areaName"] = ""  # Name of state, such as "GEORGIA"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
### all debug on adds about 10 seconds to the run time.
# Definition["debug"] = 1
### only turn on debug printing for specific methods
#Definition["debug"] = {
#                       "getMinMax": 1,
#                       "getMinMaxDirection": 1,
#                       "getMostFrequentDirection": 1,
#                       }
# Uncomment leDebug to debug local effects
Definition["leDebug"] = 0
# Definition["leDebug"] = 1
Definition["editAreaSuffix"] = None

Definition["lineLength"] = 65   #Product line length
Definition["hazardSamplingThreshold"] = (0, 1)  #(%cov, #points)

Definition["periodCombining"] = 0     # If 1, do period combining
Definition["includeEveningPeriod"] = 1  # If 1, include Evening Period
Definition["useAbbreviations"] = 1      # If 1, use marine abbreviations

Definition["hoursSChcEnds"] = 24

Definition["areaDictionary"] = "AreaDictionary"     # For product headers
Definition["language"] = "english"
Definition["useHolidays"] = 0

### New Regional Definitions not in the baseline ###
#Definition["type"] = "smart"

Definition["fixedExpire"] = 1       #ensure VTEC actions don't affect segment expiration time

# Define which forecasts have the 5th period and should list "night" in warnings for
# that period.
Definition["issueTimesWith5thPeriod"] = ("300 PM", "330 PM", "400 PM", "500 PM", "930 PM", "1000 PM", "1030 PM", "1100 PM")

# When using combined zones, "reorganizeCombinations" = 1 will cause
# it to look at the hazard table and regroup by headlines.
Definition["reorganizeCombinations"] = 0

# what percent of the area needs to be covered by winds at or below the nullValue for the
# direction to be variable?
Definition["nullWindMag"] = 5
Definition["nullWindPercent"] = 20
# what percent of the most frequent dir should the next most frequent dir be in order to be mentioned?
Definition["combineDirsThresholdPercent"] = 50
# END NC definitions
############################################################

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the above Definition = {} line
# plus following class definition and the __init__ method with only
# the "pass" line in it.

class OFF_NC_Overrides:
    """Class NNN_FILETYPE - Version: IFPS"""

    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Add methods here making sure to indent inside the class statement
    # NC OFF Overrides ------------------------

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in OFF_NC_Overrides")

    # Inserted since NHC has this
    # taken from CWF.py - modified for wind and wave sampling methods
    def addTropical(self, analysisList, phraseList, includeHazards=True):
        self.debug_print("Debug: addTropical in OFF_ONA_Overrides")

        newAnalysisList = []
        for entry in analysisList:
            #  Sampling defined as a tuple (field, statistic, temporal rate)
            #  If this is NOT a Wind or WindGust statistic
            if entry[0] not in ["Hazards", "Wind", "WindGust", "WaveHeight", "Swell"]:
                #  Add this statistic to the new analysisList
                newAnalysisList.append(entry)
        # No idea why these would be different from regular in OFFPeriod or OFFPeriodMid!! fta
        # changed wind and wave height to remove moderated. fta 05/22/12
        # also - should be in OFF_NC_Overrides...
        newAnalysisList += [
                ("Wind", self.vectorMinMax, [6]),
                ("WindGust", self.moderatedMinMax, [6]),
                ("WaveHeight", self.minMax, [6]),
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


    #Modified from OFF base
    def moderated_dict(self, parmHisto, timeRange, componentName):
        self.debug_print("Debug: moderated_dict in OFF_NC_Overrides")

        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
        dict["Wind"] =  (0, 3)
        dict["WaveHeight"] = (5, 5)
        return dict

    #Modified from OFF base
    # K.Achorn/OPC    10/4/2013  Changed null value from 2 to 3 to stop getting 2 ft becoming 2 ft or less.
    # F.Achorn/OPC    10/15/13    Changed the null value to 1 ft for waves
    # F.Achorn/OPC    05/15/14    Lower wind gust nl value to 30 kt.
    def null_nlValue_dict(self, tree, node):
        self.debug_print("Debug: null_nlValue_dict in OFF_NC_Overrides")

        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] =  1
        dict["WindWaveHgt"] =  1
        dict["Wind"] = self._definition["nullWindMag"]
        dict["WindGust"] = 30
        dict["Swell"] =  5
        dict["Visibility"] = 5 # in nautical miles. Report if less than this value.
        return dict

    #Modified from OFF base
    # ConfigVariables Overrides
    def phrase_descriptor_dict(self, tree, node):
        self.debug_print("Debug: phrase_descriptor_dict in OFF_NC_Overrides")

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
        dict["through the day"] = ""
        dict["through the night"] = ""
        return dict

    #Modified from OFF base
    # F.Achorn/OPC`10/15/13    Changed the null value to 1 ft for waves
    def first_null_phrase_dict(self, tree, node):
        self.debug_print("Debug: first_null_phrase_dict in OFF_NC_Overrides")

        # Phrase to use if values THROUGHOUT the period or
        # in the first period are Null (i.e. below threshold OR NoWx)
        # E.g.  LIGHT WINDS.    or    LIGHT WINDS BECOMING N 5 MPH.
        dict = TextRules.TextRules.first_null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "seas 1 ft"
        dict["WindWaveHgt"] =  "seas 2 ft or less"
        dict["Wind"] =  "VARIABLE WINDS 5 KT OR LESS"
        dict["Swell"] =  ""
        return dict

    #Modified from OFF base
    # F.Achorn/OPC`10/15/13    Changed the null value to 1 ft for waves
    def null_phrase_dict(self, tree, node):
        self.debug_print("Debug: null_phrase_dict in OFF_NC_Overrides")

        # Phrase to use for null values in subPhrases other than the first
        # Can be an empty string
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "1 ft"
        dict["WindWaveHgt"] =  "2 ft or less"
        dict["Wind"] =  "VARIABLE WINDS 5 KT OR LESS"
        dict["Wx"] =  ""
        dict["Swell"] =  "light"
        return dict

    #Modified from OFF base
    def phrase_connector_dict(self, tree, node):
        self.debug_print("Debug: phrase_connector_dict in OFF_NC_Overrides")

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
                                "Wind": "...becoming ",
                                "Swell": "...becoming ",
                                "Swell2": "...becoming ",
                                "WaveHeight": "...becoming ",
                                "WindWaveHgt": "...becoming ",
                         }

        dict["veering"] =  {
                                "Wind": "...becoming  ",
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
        dict["shifting to the"] =  "...shifting "
        dict["becoming onshore"] =  " becoming onshore "
        dict["then"] =  {"Wx": ". ",
                         "Vector": "...becoming ",
                         "Scalar": "...becoming ",
                         "otherwise": "...becoming ",
                         }
        return dict

    #Modified from OFF base
    # F.Achorn/OPC    02/19/13 - modified to make swell ranges, not single values
    # F.Achorn/Kells/OPC  04/04/13    CHanged maximum_range_nlValue_dict to have more ranges for seas
    # F.Achorn/OPC    10/15/13    change wave range on the low end to allow 1-3 ft.
    def maximum_range_nlValue_dict(self, tree, node):
        self.debug_print("Debug: maximum_range_nlValue_dict in OFF_NC_Overrides")

        # Maximum range to be reported within a phrase
        #   e.g. 5 to 10 mph
        # Units depend on the product
        dict = TextRules.TextRules.maximum_range_nlValue_dict(self, tree, node)
        dict["Wind"] = {
            (0, 15): 10,
            (15, 40): 10,
            (40, 60): 15,
            (60, 200): 20,
            "default": 10,
            }
#        dict["Swell"] = 5
#        dict["Swell2"] = 5
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
        dict["WaveHeight"] = {
            (0, 1): 1,
            (1, 4): 2,
            (4, 6): 3,
            (6, 8): 4,
            (8, 10): 5,
            (10, 12): 6,
            (12, 14): 7,
            (14, 16): 8,
            (16, 18): 9,
            (18, 20): 10,
            (20, 200): 15,
            "default": 5,
            }
        dict["WindWaveHgt"] = 2
        return dict

    # Modified from OFF base (which got it from ConfigVariables.py)
    def vector_dir_difference_dict(self, tree, node):
        self.debug_print("Debug: vector_dir_difference_dict in OFF_NC_Overrides")
        # Replaces WIND_DIR_DIFFERENCE
        # Direction difference.  If the difference between directions
        # for sub-ranges is greater than or equal to this value,
        # the different directions will be noted in the phrase.
        # Units are degrees
        return {
            "Wind": 45,  # degrees
            "Swell": 60,  # degrees
            "Swell2": 60, # degrees
            }

    # Modified from ConfigVariables.py
    # F.Achorn/K.Achorn/OPC    02/14/2013
    # F.Achorn/OPC    02/19/13 - modified to make these ranges, not single values
    # F.Achorn/OPC    08/20/2013 - was getting less than 5kt, becoming less than 10 kt. Changed 0-5kt to 10 kt range.
    # K.Achorn/OPC    10/4/2013 - was getting less than 10 kt becoming less than 5 kt. Changed the first wind range to 0 to 12.
    # F.Achorn/OPC    03/13/14 added more ranges - per PRT
    def vector_mag_difference_nlValue_dict(self, tree, node):
        self.debug_print("Debug: vector_mag_difference_nlValue_dict in OFF_NC_Overrides")
        # Replaces WIND_THRESHOLD
        # Magnitude difference.  If the difference between magnitudes
        # for sub-ranges is greater than or equal to this value,
        # the different magnitudes will be noted in the phrase.
        # Units can vary depending on the element and product
        # NOTE - This doesn't have to be one value. It can change
        #        according to the magnitude!
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

    #Modified from OFF base
    # F.Achorn/OPC    02/19/13 - modified to make these ranges, not single values
    # F.Achorn/OPC    03/13/14 added more ranges - per PRT
    def scalar_difference_nlValue_dict(self, tree, node):
        self.debug_print("Debug: scalar_difference_nlValue_dict in OFF_NC_Overrides")

        # Scalar difference.  If the difference between scalar values
        # for 2 sub-periods is greater than or equal to this value,
        # the different values will be noted in the phrase.
        # NOTE - This doesn't have to be one value. It can change
        #        according to the magnitude!
        return {
#            "WindGust": 18, # knots or mph depending on product
            "WindGust": {
                (0, 25): 5,
                (25, 50): 10,
                (50, 200): 15,
                "default": 5,
            }, # knots or mph depending on product
            "Period": 5, # seconds
#            "WaveHeight": 2.5, #0, # in feet
            "WaveHeight": {
                (0, 2): 1,
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
#            "WindWaveHgt": 5, # feet
            "WindWaveHgt": {
                (0, 2): 1,
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
                }, # feet
            }

    # Modified from ConfigVariables
    # 2/5/11:   added maximum_range_bias_nlValue_dict to get wave heights from max
    #           range instead of average. Also changed wind and waveheight from
    #           moderatedMinMax to minMax.  KRA
    def maximum_range_bias_nlValue_dict(self, tree, node):
        self.debug_print("Debug: maximum_range_nlValue_dict in OFF_NC_Overrides")

        # "Min", "Average", "Max"
        #  Should the maximum_range be taken from the "min" "average" or "max"
        #  value of the current range?
        return {
            "Wind": "Max",
            "WaveHeight": "Max",
            "otherwise": "Average",
            }

    # Modified from ConfigVariables
    # F.Achorn/OPC - change to make sure Hurricane force is also rounded correctly
    def marineRounding(self, value, mode, increment, maxFlag):
        # Rounding for marine winds
        mode = "Nearest"
        if maxFlag:
            if value > 30 and value < 34:
                mode = "RoundDown"
            elif value > 45 and value < 48:
                mode = "RoundDown"
            elif value > 60 and value < 64:
                mode = "RoundDown"
            else:
                mode = "Nearest"
        return self.round(value, mode, increment)


    # Modified from PhraseBuilder to ignore differences in the min
    # F.Achorn/OPC    02/25/13
    def checkScalarDifference(self, tree, node, elementName, min1, max1, min2, max2):
        # Return 1 if the min/max pairs show a difference
        # First see if both are below null threshold
        threshold = self.null_nlValue(tree, node, elementName, elementName)
        threshold1 = self.nlValue(threshold, max1)
        threshold2 = self.nlValue(threshold, max2)
        if max1 < threshold1 and max2 < threshold2:
            return 0
        # See if only one is below null threshold
        if self.null_alwaysDistinct_flag(tree, node, elementName, elementName):
            if max1 < threshold1 or max2 < threshold2:
                return 1
        # If one set of min/max has only one value,
        # and that value matches the min or
        # max of the other set, show no difference.
        if min1 == max1 and (min1==min2 or max1==max2):
            return 0
        if min2 == max2 and (min1==min2 or max1==max2):
            return 0
        # Compare mins and compare maxs
        diff_nlValue = self.scalar_difference_nlValue(tree, node, elementName, elementName)
        diff_min = self.nlValue(diff_nlValue, min(min1, min2))
        diff_max = self.nlValue(diff_nlValue, max(max1, max2))
#        if abs(min1-min2) < diff_min and abs(max1-max2) < diff_max:
        if abs(max1-max2) < diff_max:
            return 0
        return 1

    # Modified from PhraseBuilder to ignore differences in the min
    # F.Achorn/OPC    02/25/13
    def checkVectorDifference(self, tree, node, elementName,
                              min1, max1, dir1, min2, max2, dir2, magOnly=0, dirOnly=0):
        # Return 1 if the min/max/dir pairs show a difference
#print("Checking", elementName, min1, max2, dir1, min2, max2, dir2, magOnly)
        if magOnly == 0 or dirOnly == 1:
            # DR_18632
#            if self.direction_difference(dir1, dir2) >= self.vector_dir_difference(
#                tree, node, elementName, elementName):
#                return 1
            diff = self.direction_difference(dir1, dir2)
            nlValue_dict = self.vector_dir_difference_nlValue(
                tree, node, elementName, elementName)
            threshold_min = self.nlValue(nlValue_dict, min(min1, min2))
            threshold_max = self.nlValue(nlValue_dict, max(max1, max2))
            if diff >= min(threshold_min, threshold_max):
                return 1
            if dirOnly == 1:
                return 0

        # Check magnitude
        # Compare mins and maxs

        # Add special check for marine wording:
        # This will prevent:
        #    NORTHWEST GALES TO 35 KNOTS RISING TO GALES TO 35 KNOTS AFTER MIDNIGHT.
        # And will facilitate:
        #    "N WINDS 30 KT IN THE MORNING INCREASING TO
        #     GALES TO 35 KT EARLY IN THE AFTERNOON...THEN
        #     EASING TO 30 KT LATE IN THE AFTERNOON."
        if elementName == "Wind":
            if self.marine_wind_combining_flag(tree, node):
                if max1 > 30 or max2 > 30:
                    # Check for both within the same warning thresholds
                    warnThreshold1 = self.getWarnThreshold(max1)
                    warnThreshold2 = self.getWarnThreshold(max2)
                    if warnThreshold1 == warnThreshold2:
                        return 0
                    else:
                        return 1

        # First see if both are below null threshold
        threshold = self.null_nlValue(tree, node, elementName, elementName)
        threshold1 = self.nlValue(threshold, max1)
        threshold2 = self.nlValue(threshold, max2)
        if max1 < threshold1 and max2 < threshold2:
            return 0
        # See if only one is below null threshold
        if self.null_alwaysDistinct_flag(tree, node, elementName, elementName):
            if max1 < threshold1 or max2 < threshold2:
                return 1
        # If one set of min/max has only one value,
        # and that value matches the min or
        # max of the other set, show no difference.
        if min1 == max1 and (min1==min2 or max1==max2):
            return 0
        if min2 == max2 and (min1==min2 or max1==max2):
            return 0
        # Check for magnitude differences
        mag_nlValue = self.vector_mag_difference_nlValue(
            tree, node, elementName, elementName)
        mag_diff_min = self.nlValue(mag_nlValue, min(min1, min2))
        mag_diff_max = self.nlValue(mag_nlValue, max(max1, max2))
#        if abs(min1-min2) >= mag_diff_min or abs(max1-max2) >= mag_diff_max:
        if abs(max1-max2) >= mag_diff_max:
            return 1
        return 0

    ###From Marine Phrases
    # K.Achorn/OPC    03/13/14    Turn on to show wind changes between warning categories.
    def marine_wind_combining_flag(self, tree, node):
        # If 1, Wind combining will reflect the
        # crossing of significant thresholds such as gales.
        # E.g. "HURRICANE FORCE WINDS TO 100 KNOTS." instead of
        # "NORTH HURRICANE FORCE WINDS TO 100 KNOTS EASING TO
        #  HURRICANE FORCE WINDS TO 80 KNOTS IN THE AFTERNOON."
        return 1

    #Modified from SampleAnalysis
    # ADDED CODE BY MUSONDA TO GIVE WIND DIRECTION RANGE LIKE N TO NE
    # F.Achorn/OPC 01/28/13 - added "VAR" as a null direction
    # F.Achorn/OPC 03/01/13 - changed back to 8 point compass,
    #                         but added directions for combined dirs
    #                         had to make sure they didn't overlap.
    def dirList(self):
        self.debug_print("Debug: dirList in OFF_NC_Overrides")

#        dirSpan = 45 # 45 degrees per direction
#        base = 22.5 # start with N
        # dir - centered on - start dir - end dir
        #N        0           -22.5        22.5
        #NE      45            22.5        67.5
        #E       90            67.5       112.5
        #SE     135           112.5       157.5
        #S      180           157.5       202.5
        #SW     225           202.5       247.5
        #W      270           247.5       292.5
        #NW     315           292.5       337.5
        #N      360           337.5       382.5
        return [
            ('N',  337.6,   361),
            ('N',      0,  22.4),
            ('NE',  22.6,  67.4),
            ('E',   67.6, 112.4),
            ('SE', 112.6, 157.4),
            ('S',  157.6, 202.4),
            ('SW', 202.6, 247.4),
            ('W',  247.6, 292.4),
            ('NW', 292.6, 337.4),
            #N-NE    22.5
            ('N to NE', 22.4, 22.6),
            #E-NE    67.5
            ('E to NE', 67.4, 67.6),
            #E-SE    112.5
            ('E to SE', 112.4, 112.6),
            #S-SE    157.5
            ('S to SE', 157.4, 157.6),
            #S-SW    202.5
            ('S to SW', 202.4, 202.6),
            #W-SW    247.5
            ('W to SW', 247.4, 247.6),
            #W-NW    292.5
            ('W to NW', 292.4, 292.6),
            #N-NW    337.5
            ('N to NW', 337.4, 337.6),
            ('VAR', 9989, 9991)
            ]

    # modified from TextUtils to add variable. Just sending "variable" in
    # resulted in the "e" changing to "east"
    def vector_dir(self, dir):
        self.debug_print("Debug: vector_dir in OFF_NC_Overrides")
        self.debug_print("dir = ", dir)
        if not isinstance(dir, bytes):
            dir = self.dirToText(dir)
        self.debug_print("dir text = ", dir)
        dir = dir.replace("N", "north")
        dir = dir.replace("S", "south")
        dir = dir.replace("E", "east")
        dir = dir.replace("W", "west")
        dir = dir.replace("VAR", "variable")
        self.debug_print("dir text replaced = ", dir)
        return dir

    #from Phrasebuilder. Need to not try averaging directions if the dir is 9990.0 (variable)
    # 9990.0 averaged with 9990.0 ends up as 270.
    # F.Achorn/OPC    03/18/14    Modify to not average W and W to NW. Just use the "to" version.
    def combineVectors(self, tree, phrase, subPhrase1, subPhrase2, elementName):
        self.debug_print("Debug: combineVectors in OFF_NC_Overrides")
        mag1, dir1, dirStr1 = self.getVectorData(tree, subPhrase1, elementName, "MinMax")
        mag2, dir2, dirStr2 = self.getVectorData(tree, subPhrase2, elementName, "MinMax")

        if self._debug:
            timeRange = phrase.getTimeRange()
            print(timeRange)
            print("Vectors before starting:")
            print("    Vector 1:")
            print(mag1, dir1, dirStr1)
            print("    Vector 2:")
            print(mag2, dir2, dirStr2)

        if mag1 is None and mag2 is None:
            return 1, (None, dir1)
        if mag1 is None or mag2 is None:
            return 0, (None, dir1)

        min1, max1 = mag1
        min2, max2 = mag2

        differenceFlag = self.checkVectorDifference(
            tree, subPhrase1, elementName, min1, max1, dir1, min2, max2, dir2)
        if differenceFlag == 0:
            combine_singleValues = self.combine_singleValues_flag(
                tree, subPhrase1, elementName, elementName)
            if combine_singleValues == 1:
                if (dir1 == dir2 == 9990.0):
                    if self._debug: print("Both dirs variable. keep 9990.0")
                    newMag = self.average(min(min1, min2), max(max1, max2))
                    newDir = 9990.0
                else:
                    newMag, newDir = self.vectorAverage((min(min1, min2), dir1), (max(max1, max2), dir2))
                    # is one of these dirs combined in the other?
                    if (dirStr1 + ' to ' in dirStr2) or (' to ' + dirStr1 in dirStr2) or (dirStr2 + ' to ' in dirStr1) or (' to ' + dirStr2 in dirStr1):
                        if ('to' in dirStr1): newDir = dir1
                        if ('to' in dirStr2): newDir = dir2
                        if self._debug: print("Don't average " + dirStr1 + " and " + dirStr2 + ". Just use "+ str(newDir))
                newMag = self.roundStatistic(tree, subPhrase1, newMag, elementName)
                newValue = (newMag, newDir)
            else:
                # Combine using mins and maxs to catch slow trends
                newMin = min(min1, min2)
                newMax = max(max1, max2)
                newMin, newMax = self.applyRanges(tree, phrase, newMin, newMax, elementName)
                if (dir1 == dir2 == 9990.0):
                    if self._debug: print("Both dirs variable. keep 9990.0")
                    magAvg = self.average(newMin, newMax)
                    newDir = 9990.0
                else:
                    magAvg, newDir = self.vectorAverage((newMin, dir1), (newMax, dir2))
                    # is one of these dirs combined in the other?
                    if (dirStr1 + ' to ' in dirStr2) or (' to ' + dirStr1 in dirStr2) or (dirStr2 + ' to ' in dirStr1) or (' to ' + dirStr2 in dirStr1):
                        if ('to' in dirStr1): newDir = dir1
                        if ('to' in dirStr2): newDir = dir2
                        if self._debug: print("Don't average " + dirStr1 + " and " + dirStr2 + ". Just use "+ str(newDir))
                newValue = ((newMin, newMax), newDir)
            if self._debug:
                print("Vectors after combining:")
                print(newValue[0][0], newValue[0][1], newValue[1])
            return 1, newValue
        return 0,  None

    ##From Sample Analysis##
    #default was average
    def vectorDirection_algorithm(self, parmHisto, timeRange, componentName):
        self.debug_print("Debug: vectorDirection_algorithm in OFF_NC_Overrides")
        # Algorithm to use for computing vector direction for vector analysis methods.
        # Can be "Average" or "MostFrequent"
        return "MostFrequent"

    #Taken from SampleAnalysis
    def getMinMax(self, dataType, parmHisto, timeRange, componentName,
                  firstOnly = 0):
        "Return the minimum and maximum values over the given time period"
        firstTime = 1
        minValue = 0.0
        maxValue = 0.0
        minResult = 0.0
        maxResult = 0.0
        noData = 1
        for histSample in parmHisto.histoSamples():
            if self.temporalCoverage_flag(parmHisto, timeRange, componentName,
                                          histSample) == 0:
                continue
            # return None if no histSample pairs
            if histSample.numOfPoints() == 0:
                return None
            noData = 0

            min = histSample.absoluteMin()
            max = histSample.absoluteMax()
            if dataType == self.SCALAR():
                minValue = min.scalar()
                maxValue = max.scalar()
            elif dataType == self.VECTOR() or dataType == self.MAGNITUDE():
                minValue = min.magnitude()
                maxValue = max.magnitude()
            if firstTime == 1:
                firstTime = 0
                minResult = minValue
                maxResult = maxValue
            else:
                if minValue < minResult:
                    minResult = minValue
                if maxValue > maxResult:
                    maxResult = maxValue
            if firstOnly == 1:
                break

        if noData == 1:
            return None
        if dataType == self.VECTOR():
            dir = self.getMinMaxDirection(dataType, parmHisto,
                                            timeRange, componentName, minResult, maxResult)
            return (minResult, maxResult), dir

        return minResult, maxResult

    #Taken from SampleAnalysis
    # modified from getDominantDirection
    # instead, find the direction that matches the wind range we're using.
    def getMinMaxDirection(self, dataType, parmHisto, timeRange, componentName, minMag, maxMag):
        # returns the dominant direction according to "vectorDirection_algorithm"
        # which can be "Average" or "MostFrequent"

        if not dataType == self.VECTOR():
            return None
        if self.vectorDirection_algorithm(parmHisto, timeRange, componentName) == "Average":
            return self.getAverageDirection(parmHisto, timeRange, componentName)
        else: #Most Frequent
            return self.getMostFrequentDirection(parmHisto, timeRange, componentName, minMag, maxMag)

    #Taken from SampleAnalysis
    #Modified to add variable winds.
    # F.Achorn/OPC    03/01/2013 Modified to check for N to NE winds (eg)
    # F.Achorn/OPC    02/03/14 modify to only list both dirs if both are sizable parts of the sample
    # F.Achorn/OPC    03/06/14 always sample from the maxMag. Sampling from the rounded max left some points out and
    #                          sometimes caused no winds to be found
    # F.Achorn/OPC    03/27/14 big changes to this. Get the most frequent direction of the highest binned winds.
    #                          then if there is an adjacent predominant wind, report that too.
    def getMostFrequentDirection(self, parmHisto, timeRange, componentName, minMag, maxMag):
        self.debug_print("Debug: getMostFrequentDirection in OFF_NC_Overrides")
        # returns the most frequent direction binned to 8-point numerical direction
        binDict = {}
        totWeight = 0.0
        percentNullMag = 0.0
        if self._debug:
            print("Getting most frequent", timeRange)
            print("  Area =", parmHisto.area().getId())
            print("  minMag =", minMag)
            print("  maxMag =", maxMag)

        # Round maxMag: needs to rounded to get the correct range.
        roundedMaxMag = self.marineRounding(maxMag, "Nearest", 5, maxFlag=1)
        if self._debug:
            print("  roundedMax =", roundedMaxMag)

        # get the max range dictionary
        maxRangeDict = self.maximum_range_nlValue_dict(None, None)["Wind"]
        if self._debug:
            print("  maxRangeDict =", maxRangeDict)
        #should look like this:
#         {'default': 10,
#          (60, 200): 20,
#          (15, 40): 10,
#          (0, 15): 10,
#          (40, 60): 15}

        # Figure out which range the max falls into
        maxRange = self.nlValue(maxRangeDict, roundedMaxMag)

        if self._debug:
            print("  maxRange =", maxRange)

        allowedMin = roundedMaxMag - maxRange - 2
        if allowedMin > minMag:
            if self._debug:
                print("  Changing min " + str(minMag) + " to lowest allowed min from " + str(minMag) + " to " + str(allowedMin) + ". Max = "+str(maxMag) + " and maxRange = " + str(maxRange))
            minMag=allowedMin

        if self._debug: print("Sampling directions for magnitudes from " + str(minMag) + " to " + str(maxMag))
        for histSample in parmHisto.histoSamples():
            if self.temporalCoverage_flag(parmHisto, timeRange, componentName, histSample) == 0:
                continue
            numOfPoints = histSample.numOfPoints()
            if numOfPoints == 0:
                return None
            histPairs = histSample.histogram()
#             for histPair in histPairs:
#                 validTime = TimeRange.TimeRange(histSample.validTime())
#                 weight = validTime.intersection(timeRange).duration()
#                 weight = weight/float(timeRange.duration()) * 100.0
#                 totWeight += weight
#                 count = float(histPair.count())
#                 binnedDir = self.binDir(histPair.value().direction())
#                 #print "dir, binnedDir", histPair.value().direction(), binnedDir
#                 percent = count/numOfPoints * weight
            for histPair in histPairs:
                validTime = TimeRange.TimeRange(histSample.validTime())
#                 weight = 1

                weight = validTime.intersection(timeRange).duration()
                weight /= float(timeRange.duration()) * 100.0
                totWeight += weight
                count = float(histPair.count())
                percent = count/numOfPoints * weight
                #make sure the Mag is in the range we're reporting before
                #adding it as a point.
                binnedDir = self.binDir(histPair.value().direction())
                mag = histPair.value().magnitude()
                binnedMag = self.marineRounding(mag, "Nearest", 5, maxFlag=1)

                if self._debug:
                    print("Value = " + str(mag) + " at " + str(histPair.value().direction()) + " deg.")
                    print("    Count = " + str(count))
                    print("    Binned Dir = " + str(binnedDir))

                if (maxMag <= 15) and (mag <= self._definition["nullWindMag"]) :
                    if self._debug: print("    Counting null wind " + str(mag))
#                     totWeight += weight
#                     count = float(histPair.count())
#                     percent = count/numOfPoints * weight
                    percentNullMag += percent
                #ok to count low winds twice.... max may be 5.0!
                if (mag >= minMag and mag <= maxMag):
                    if self._debug: print("    Counting " + str(mag) + " at " + str(binnedDir) + " deg. count = " + str(count))
#                     totWeight += weight
#                     count = float(histPair.count())
#
#                     percent = count/numOfPoints * weight
                    if binnedMag in binDict:
                        if binnedDir in binDict[binnedMag]:
                            binDict[binnedMag][binnedDir] += percent
                        else:
                            binDict[binnedMag][binnedDir] = percent
                    else:
                        binDict[binnedMag] = {}
                        binDict[binnedMag][binnedDir] = percent
                else:
                    if self._debug:
                        print("    Not counting " + str(mag) + ". Not in range: " + str(minMag) + " - " + str(maxMag))
        if self._debug:
            print("Number of Mag Bins Used: " + str(len(binDict)))
            print("Total number of points: " + str(numOfPoints))
            print("Total weight: " + str(totWeight))

        if totWeight == 0.0:
            if self._debug: print("no weighted points. exiting")
            return None

        # we have a dictonary of a dictionary. binned magnitudes (only for winds in our wind range)
        # may not be in order. e.g.
        # 10.0, {0: 0.11820895522388059, 315.0: 1.0286567164179106}
        # 15.0, {315.0: 0.49850746268656715}
        # 20.0, {315.0: 0.02507462686567164}
        if self._debug:
            print("Full dictionary")
            print(binDict)
        if self._debug: print("Direction info for highest winds " + str(roundedMaxMag)+ " is " + str(binDict[roundedMaxMag]))
        # get the most frequent direction of the highest wind.
        highestMagMaxFreq = 0
        highestMagMostFreqDir = None
        nextMagMaxFreq = 0
        nextMagMostFreqDir = None
        if self._debug: print("Dir and freq info for highest winds only:")
        for dir in binDict[roundedMaxMag]:
            freq = binDict[roundedMaxMag][dir]
            if self._debug: print("    dir, freq = "+ str(dir) + ", " + str(freq))
            if freq > highestMagMaxFreq:
                nextMagMaxFreq = highestMagMaxFreq
                highestMagMaxFreq = freq
                nextMagMostFreqDir = highestMagMostFreqDir
                highestMagMostFreqDir = dir
        if self._debug:
            print("highest binnedMag most Frequent Dir = "+ str(highestMagMostFreqDir) + " with freq: " + str(highestMagMaxFreq))
            print("next highest binnedMag most Frequent Dir = "+ str(nextMagMostFreqDir) + " with freq: " + str(nextMagMaxFreq))

        # get the direction info on the entire bin (all magnitudes)
        dirBinDict = {}
        for magBin in binDict:
            for dir in binDict[magBin]:
#                 if self._debug: print "Working on bin: " + str(magBin) + " dir: " + str(dir) + " freq: " + str(binDict[magBin][dir])
                if dir in dirBinDict:
                    dirBinDict[dir] += binDict[magBin][dir]
                else:
                    dirBinDict[dir] = binDict[magBin][dir]
#                 if self._debug: print "    New freq: " + str(dirBinDict[dir])

        if self._debug:
            print("Dir and freq info for whole range:")
            for dir in dirBinDict:
                print("    dir, freq = "+ str(dir) + ", " + str(dirBinDict[dir]))


        # Before we set off combining, let's check for the case where the next most frequent dir from the max mag is almost
        # the same frequency and it's much more prevelant in the overall dirs.
        if (nextMagMostFreqDir is not None):
            if (nextMagMaxFreq >=  self._definition["combineDirsThresholdPercent"] * 0.01 * highestMagMaxFreq):
                # the nextMagMaxFreq is significant.
                if self._debug: print("  next highest binnedMag most Frequent Dir is significant")
                if (self._definition["combineDirsThresholdPercent"] * 0.01 * dirBinDict[nextMagMostFreqDir] > dirBinDict[highestMagMostFreqDir]):
                    if self._debug: print("next higest binnedMag is significantly more frequent overall. Use this as our main dir.")
                    highestMagMostFreqDir = nextMagMostFreqDir
                    highestMagMaxFreq = nextMagMaxFreq

        # Set up a dictionary with the central wind dir (e.g. N to NE = 22.5)
        # as the key and the wind dirs associated with those dirs as a list.
        combinedDirs = {
            # N to NE centered on 22.5
            22.5: [0.0, 45.0, 360.0],
            # E to NE centered on 67.5
            67.5: [45.0, 90.0],
            # E to SE centered on 112.5
            112.5: [90.0, 135.0],
            # S to SE centered on 157.5
            157.5: [135.0, 180.0],
            # S to SW centered on 202.5
            202.5: [180.0, 225.0],
            # W to SW centered on 247.5
            247.5: [225.0, 270.0],
            # W to NW centered on 292.5
            292.5: [270.0, 315.0],
            # NW to N centered on 337.5
            337.5: [0.0, 315.0, 360.0]
            }

        # given the highestMagMostFreqDir, is one of the two dirs next to it present
        # in the list of dirs?
        adjacentDirs={}
        for key in combinedDirs:
            if (highestMagMostFreqDir in combinedDirs[key]):
                # what are the other dirs in that key? get their freqencies.
                for dir in combinedDirs[key]:
                    if (dir != highestMagMostFreqDir):
                        #ignoring our main dir.
                        if dir in dirBinDict:
                            if (dir in adjacentDirs):
                                if self._debug: print("already have "+ str(dir) + " in adjacentDirs list")
                            else:
                                if self._debug: print("adding "+ str(dir) + " to adjacentDirs list")
                                adjacentDirs[dir] = dirBinDict[dir]

        # given our list of adjacent dirs, which has the larger frequency?
        # Then see if that frequency is significant, compared to the highestMagMostFreqDir

        mostFreqDir = highestMagMostFreqDir
        maxFreq = dirBinDict[highestMagMostFreqDir]

        if len(adjacentDirs) == 1:
            # use this.
            for adjDir in adjacentDirs:
                # is the weight significant?
                if dirBinDict[adjDir] >= self._definition["combineDirsThresholdPercent"] * 0.01 * dirBinDict[highestMagMostFreqDir]:
                    for key in combinedDirs:
                        if (highestMagMostFreqDir in combinedDirs[key]) and (adjDir in combinedDirs[key]):
                            #this is the right combined key.
                            if self._debug: print("Using a combined direction for " + str(highestMagMostFreqDir) + " and " + str(adjDir) + ": " + str(key))
                            mostFreqDir = key
                            maxFreq = dirBinDict[highestMagMostFreqDir] + dirBinDict[adjDir]
                else:
                    if self._debug: print("Not using a combined direction for " + str(highestMagMostFreqDir) + " and " + str(adjDir) + ". Not frequent enough.")
        elif len(adjacentDirs) > 1:
            # which is most freq?
            maxAdjFreq = 0
            mostFreqAdjDir = ""
            for adjDir in adjacentDirs:
                if adjacentDirs[adjDir] > maxAdjFreq:
                    maxAdjFreq = adjacentDirs[adjDir]
                    mostFreqAdjDir = adjDir
            if self._debug: print("Most frequent adjacent dir: " + str(mostFreqAdjDir))
            # ok, is the weight significant?
            if dirBinDict[mostFreqAdjDir] >= self._definition["combineDirsThresholdPercent"] * 0.01 * dirBinDict[highestMagMostFreqDir]:
                for key in combinedDirs:
                    if (highestMagMostFreqDir in combinedDirs[key]) and (mostFreqAdjDir in combinedDirs[key]):
                        #this is the right combined key.
                        if self._debug: print("Using a combined direction for " + str(highestMagMostFreqDir) + " and " + str(mostFreqAdjDir) + ": " + str(key))
                        mostFreqDir = key
                        maxFreq = dirBinDict[highestMagMostFreqDir] + dirBinDict[mostFreqAdjDir]
            else:
                if self._debug: print("Not using a combined direction for " + str(highestMagMostFreqDir) + " and " + str(mostFreqAdjDir) + ". Not frequent enough.")
        else:
            if self._debug: print("Didn't find an adjacent wind direction. Just use the maxMag's dir.")

        # Return the most frequent direction or variable
        if percentNullMag >= maxFreq:
            if self._debug: print("percentNullMag = "+str(percentNullMag))
            return 9990.0
        else:
            if self._debug:
                print("Choosing NOT to use variable.")
                print("percentNullMag = "+str(percentNullMag))
                print("maxFreq = "+str(maxFreq))
            return mostFreqDir



    #Modified from ConfigVariables
    # default = 2. set to 0
    def repeatingEmbedded_localEffect_threshold(self, tree, component):
        self.debug_print("Debug: repeatingEmbedded_localEffect_threshold in OFF_NC_Overrides")

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
        return 0

    # from PhraseBuilder.py
    # was getting NW PORTION...5 TO 10 KT LATE. WINDS N to NW 5 TO 15 KT. SE PORTION 10 to 20 KT LATE. SEAS 6 to 7 FT.
    # Just exit, results in:
    # NW PORTION...N TO NW WINDS 5 TO 15 KT...BECOMING 5 TO 10 KT LATE.
    # SE PORTION...N TO NW WINDS 5 TO 15 KT...INCREASING TO 10 TO 20 KT LATE.
    # May want to turn this on for other parms.
    # F.Achorn/K.Achorn/OPC    03/05/2013
    def consolidateSubPhrases(self, tree, component):
        self.debug_print("Debug: consolidateSubPhrases in OFF_NC_Overrides")

        ##  Timing: This method runs at the component level
        ##  AFTER all sub-phrase words have been set and
        ##  BEFORE they have been assembled into phrases at the phrase level.
        ##
        ##  Purpose: Check for duplicate subPhrases and consolidate
        #            them into one.
        ##
        ##  For example:  (see Case 2 below)
        ##    Chance of thunderstorms in the morning (windward)
        ##    Chance of thunderstorms in the morning (leeward)
        ##    Chance of rain in the afternoon (windward)
        ##    Chance of snow in the afternoon (leeward)
        ##
        ##  becomes:
        ##    Chance of thunderstorms in the morning (unqualified)
        ##    Chance of rain in the afternoon (windward)
        ##    Chance of snow in the afternoon (leeward)

        # Set a flag to make sure we pass by this method the first time
        # so that the phrase set-up methods have a chance to run and
        # create sub-phrases before we try to consolidate them

        # Easiest way to fix this is to let it be long.
        return self.DONE()

        if component.get('first') is None:
            component.set('first', 1)
            return


        # Make sure all subPhrases have completed i.e. have words set
        subPhraseList = []
        leaves = self.getLeaves(tree, component)
        leFlag = 0
        for child in leaves:
            words = child.get("words")
#print("Consolidate SubPhrases", child.getAncestor("name"), words)
            if words is None:
#print("Returning")
                return
            le = child.getAncestor('localEffect')
            if le is not None:
                leFlag = 1
            subPhraseList.append(child)

        # If no localEffects, skip this method
        if not leFlag:
#print("In Consolidate SubPhrases: No local effects")
            return self.DONE()

        if self.__dict__.get("_leDebug", 0):
            print("\nConsolidateSubPhrases", tree.get('passes'))

        # Create subPhraseDict =
        #    {(words, tr, lePhraseNameGroup):
        #       list of subPhrases with those words, tr, and lePhraseNameGroup}
        lePhraseNameGroups = self.lePhraseNameGroups(tree, component)
        subPhraseDict = {}
        for subPhrase in subPhraseList:
            tr = subPhrase.getTimeRange()
            words = subPhrase.get("words")
            lePhraseNameGroup, firstName = self.getLePhraseNameGroup(
                tree, component, lePhraseNameGroups, subPhrase.parent)
            if not words:
                continue
            if self.__dict__.get("_leDebug", 0):
                print(subPhrase.getAncestor("name"))#, subPhrase.parent
                print("   ", subPhrase.getAreaLabel(), tr, words)
                print("       local effect", subPhrase.getAncestor('localEffect'))
            self.addToDictionary(subPhraseDict, (words, tr, lePhraseNameGroup), subPhrase)
        if self.__dict__.get('_leDebug', 0): print("subPhraseDict", subPhraseDict)

        # Check for duplicate subPhrases and consolidate them into one.
        #  Case 1: If the duplicates are all for the same areaLabel,
        #     set the areaLabel for the consolidated subPhrase to that.
        #  Case 2: If the duplicates are for a local effect and
        #      cover all possible local effect areas for their phrase,
        #      create a new phrase for component.getAreaLabel()
        #      with this subPhrase wording. Remove the local effect subPhrases.
        #  Case 3: If the duplicates are for a local effect
        #      and they cover a subset of the local effect areas,
        #      leave them alone except for removing any component.getAreaLabel()
        #      duplicate subPhrases.
        compArea = component.getAreaLabel()
        if self.__dict__.get('_leDebug', 0):
            print("\nDetermine Case for each set of duplicate phrases. compArea", compArea)
        for key in subPhraseDict:
            words, tr, lePhraseNameGroup = key
            subPhrases = subPhraseDict[key]
            if len(subPhrases) <= 1:
                continue
            # We have duplicate subPhrases to consolidate.
            # Gather the areaLabels for these duplicate subphrases
            # and the possible localEffect Area labels
            areaLabels, leAreas = self.gatherDupAreaLabels(
                tree, component, compArea, subPhrases)
            if self.__dict__.get('_leDebug', 0):
                print("\n", words)
                print("    ", tr, len(subPhrases))
                print("areaLabels, leAreas", areaLabels, leAreas)
            # Determine the consolidated areaLabel
            if len(areaLabels) == 1:
                # Case 1
                if self.__dict__.get('_leDebug', 0): print("CASE 1")
                # Remove all but the first subPhrase
                for subPhrase in subPhrases[1:]:
                    subPhrase.set('words', "")
            else:
                parent = subPhrases[0].parent
                localEffect = subPhrases[0].getAncestor('localEffect')
                if localEffect is None:
                    continue
                # See if all local effect areas are covered
                allAreasCovered = self.allLeAreasCovered(
                    tree, component, compArea, leAreas, areaLabels)
                if allAreasCovered:
                    # Case 2: Consolidate
                    if self.__dict__.get('_leDebug', 0): print("CASE 2")
                    parent = subPhrases[0].parent
                    newNode = tree.copyPhrase(
                        parent, areaLabel=compArea,
                        copyAttrs=["doneList", "disabledSubkeys", "disabledElements",
                                   "firstElement", "elementName", "elementInfoList",
                                   "descriptor", "indentLabel"])
                    # with newFirst not set, it defaulted to putting the
                    # new phrase after any sibligs. In this case, it should always be
                    # first.
#                    component.insertChild(parent, newNode)
                    component.insertChild(parent, newNode, newFirst=1)
                    newSubPhrase = subPhrases[0].copy()
                    newNode.set('childList', [newSubPhrase])
                    for subPhrase in subPhrases:
                        subPhrase.set('words', "")
                else:
                    # Case 3: Throw out any compArea subPhrase and
                    # leave local effect ones alone for now
                    if self.__dict__.get('_leDebug', 0): print("CASE 3")
                    for subPhrase in subPhrases:
                        if subPhrase.getAreaLabel() == compArea:
                            subPhrase.set("words", "")


        leaves = self.getLeaves(tree, component)
        for subPhrase in leaves:
#        for subPhrase in localEffectsList:
            tr = subPhrase.getTimeRange()
            words = subPhrase.get("words")
            if self.__dict__.get("_leDebug", 0):
                print("after checkLocalEffects subPhrases")
                print(subPhrase.getAncestor("name"))#, subPhrase.parent
                print("   ", subPhrase.getAreaLabel(), tr, words)
                print("       local effect", subPhrase.getAncestor('localEffect'))

        if self.__dict__.get('_leDebug', 0): print("subPhraseDict", subPhraseDict)
        return self.DONE()

    #modified from OFF.py to allow product issuances to be any strings instead of just "400 PM" strings.
    def _determineTimeRanges(self, argDict):
        # Set up the Narrative Definition and initial Time Range
        self._issuanceInfo = self.getIssuanceInfo(
            self._productIssuance, self._issuance_list(argDict))
        self._timeRange = self._issuanceInfo.timeRange()
        argDict["productTimeRange"] = self._timeRange
        self._expireTime = self._issuanceInfo.expireTime()
        self._issueTime = self._issuanceInfo.issueTime()
        self._definition["narrativeDef"] = self._issuanceInfo.narrativeDef()
        if self._periodCombining:
            self._definition["methodList"] = \
               [self.combineComponentStats, self.assembleChildWords]
        else:
            self._definition["methodList"] = [self.assembleChildWords]

        # Calculate current times
        self._ddhhmmTime = self.getCurrentTime(
            argDict, "%d%H%M", shiftToLocal=0, stripLeading=0)
        if re.match(r"(\d{3,4} [AP]M).*", self._productIssuance):
            print("using static issuance time")
            staticIssueTime=re.sub(r'(\d{3,4} [AP]M).*', r'\1', self._productIssuance)
            print("staticIssueTime = " + staticIssueTime)
            self._timeLabel =  staticIssueTime + " " + self.getCurrentTime(
                argDict, " %Z %a %b %e %Y", stripLeading=1)
            print("timeLabel = "+self._timeLabel)
            # Re-calculate issueTime
            self._issueTime = self.strToGMT(staticIssueTime)
        else:
            # using time listed in self._issuance_list
            self._timeLabel =  self.getCurrentTime(argDict, "%l%M %p %Z %a %b %e %Y", stripLeading=1)
            # Don't Re-calculate issueTime

        expireTimeRange = TimeRange.TimeRange(self._expireTime, self._expireTime + 3600)
        self._expireTimeStr = self.timeDisplay(expireTimeRange, "", "", "%d%H%M", "")
        return None

    #Modifed from OFF base
    def _preProcessProduct(self, fcst, argDict):
        self.debug_print("Debug: _preProcessProduct in OFF_NC_Overrides")

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
        fcst += text2
        return fcst

    #Modified from OFF base
    #remove any double spaces
    #**********************************************************************************
    #**********************************************************************************
    #*********************** Also in OFF_NAV_[ONA/ONP]_Overrides.py *******************
    #**********************************************************************************
    #**********************************************************************************
    def _preProcessArea(self, fcst, editArea, areaLabel, argDict):
        self.debug_print("Debug: _preProcessArea in OFF_NC_Overrides")

        # This is the header for an edit area combination
        # always print the following.
        print("Generating Forecast for", areaLabel)
        areaHeader = self.makeAreaHeader(
            argDict, areaLabel, self._issueTime, self._expireTime,
            self._areaDictionary, self._defaultEditAreas)
        fcst += areaHeader

        # get the hazards text
        self._hazards = argDict['hazards']
        self._combinations = argDict["combinations"]

        headlines = self.generateProduct("Hazards", argDict, area = editArea,
                                         areaLabel=areaLabel,
                                         timeRange = self._timeRange)

#        # Tropicals are "Until Further Notice" so the day always says "TODAY"
#        # set includeTropical is true/false
#        try:
#                self.includeTropical = self._includeTropical == "Yes"
#        except:
#                self.includeTropical = False

        # generate a new list of tropicals
        # set up sample requests and get the ParmHistos
        parmHistos = argDict['hazards']._HazardsTable__doSamplingOfHazards([editArea])
        # make proposed table
        pTable = argDict['hazards']._HazardsTable__makeProposedTable(parmHistos)
        # Combine time entries
        analyizedHazTable = argDict['hazards']._HazardsTable__timeCombine(pTable)

        ufnKeys = [('HU', 'A'), ('HU', 'S'), ('HU', 'W'), ('TR', 'A'), ('TR', 'W'), ('TY', 'A'), ('TY', 'W')]
        # Look for the "UFN" keys for this zone and generate headlines.
        hazardsToFix=[]
        for h in analyizedHazTable:
            # Only work with Watches.
            if (h['phen'], h['sig']) in ufnKeys and h['sig'] == 'A':
                hazardsToFix.append(h)
                timing = self.getTimingPhrase(h, self._issueTime.unixTime(), "DAY_NIGHT_ONLY", "NONE").upper().strip()
                print(h['hdln'] + " is a UFN headline. Need to adjust timing to "+timing)
        # loop through the hazards and get the first one (in time) of each.
        # should match against the headline we're trying to remove.
        newest_hazard = {}
        for haz in hazardsToFix:
            if haz['phensig'] not in newest_hazard:
                newest_hazard[haz['phensig']] = haz
            else:
                if haz['startTime'] < newest_hazard[haz['phensig']]['startTime']:
                    newest_hazard[haz['phensig']] = haz
        for phensig in newest_hazard:
            timing = self.getTimingPhrase(newest_hazard[phensig], self._issueTime.unixTime(), "DAY_NIGHT_ONLY", "NONE").upper().strip()
            if self._debug: print('old headlines = ' + headlines)
            #replace the old headline (with some timing word like "TODAY" or "EARLY TODAY" for the new time.
            headlines = re.sub('...'+newest_hazard[phensig]['hdln']+r'\s+\w+\s*\w*'+'...', '...'+newest_hazard[phensig]['hdln'] + " " + timing + "...", headlines)
            if self._debug: print('new headlines = ' + headlines)
        # change "WATCH" to "FORCE WINDS POSSIBLE" or "POSSIBLE for tropicals
        headlines = re.sub(r'FORCE WIND WATCH', r'FORCE WINDS POSSIBLE', headlines)
        headlines = re.sub(r'HURRICANE WATCH', r'HURRICANE FORCE WINDS POSSIBLE', headlines)
        headlines = re.sub(r'TROPICAL STORM WATCH', r'TROPICAL STORM FORCE WINDS POSSIBLE', headlines)
        headlines = re.sub(r'WATCH', r'FORCE WINDS POSSIBLE', headlines)
        # remove any double spaces
        headlines = re.sub(r'  ', r' ', headlines)

        # remove extra headlines
        headlines = self.removeExtraOFFHeadlines(headlines)

        #add headlines to forecast
        fcst += headlines

        return fcst

    # new method to collapse headlines
    #should only work for extratrop right now.
    def removeExtraOFFHeadlines(self, headlines):
        self.debug_print("Debug: removeExtraOFFHeadlines in OFF_NC_Overrides")

        # This method will simplify the warning headlines according to OPC's
        # warning decision headline extra-trop and trop tables.
        # use the order as outlined in allowed hazards.
#            ('HU.W', tropicalActions, 'Tropical'),   # HURRICANE WARNING
#            ('TY.W', tropicalActions, 'Tropical'),   # TYPHOON WARNING
#            ('TR.W', tropicalActions, 'Tropical'),   # TROPICAL STORM WARNING
#            ('HF.W', marineActions, 'Marine'),       # HURRICANE FORCE WIND WARNING
#            ('SR.W', marineActions, 'Marine'),       # STORM WARNING
#            ('GL.W', marineActions, 'Marine'),       # GALE WARNING
#            ('SE.W', marineActions, 'Marine'),       # HAZARDOUS SEAS
#            ('UP.W', allActions, 'IceAccr'),         # HEAVY FREEZING SPRAY WARNING
#            ('HF.A', marineActions, 'Marine'),        # HURRICANE FORCE WINDS POSSIBLE
#            ('')
#            ('SR.A', marineActions, 'Marine'),        # STORM FORCE WINDS POSSIBLE
#            ('GL.A', marineActions, 'Marine'),        # GALE FORCE WINDS POSSIBLE
#            ('FG.Y', allActions, 'Fog'),             # DENSE FOG ADVISORY
#            ('SM.Y', allActions, 'Smoke'),           # DENSE SMOKE ADVISORY
#            ('UP.Y', allActions, 'IceAccr'),         # HEAVY FREEZING SPRAY ADVISORY
#            ('AF.Y', allActions, 'Ashfall'),         # VOLCANIC ASHFALL ADVISORY


        #headlines = "....HURRICANE FORCE WIND WARNING...\n...GALE WARNING...\n...STORM WARNING...\n...GALE FORCE WINDS POSSIBLE TUE...\n...VOLCANIC ASHFALL ADVISORY...\n"
        #headlines = "...GALE WARNING...\n...STORM WARNING...\n...GALE FORCE WINDS POSSIBLE TUE...\n...VOLCANIC ASHFALL ADVISORY...\n...HURRICANE FORCE WINDS POSSIBLE WED...\n"
        if len(headlines) <= 1:
            #only one thing in the list: '\n'
            if self._debug:
                print("-----No headlines-----")
                print(len(headlines))
                print(headlines)
                print("----------------------")
            return headlines
        else:
            #headlines exist. Continue.
            if self._debug:
                print("-----headlines before removing extras:-----")
                print(headlines)
                print("-------------------------------------------")

            headline_list = headlines.split("\n")
            if headline_list[-1] not:
                while headline_list[-1] not:
                    headline_list.pop()

            tropcial_warning_list = []
            warning_list = []
            possible_list = []
            other_warning_list = []
            advisory_list = []
            new_headlines_list = []

            for headline in headline_list:
                if self._debug: print(headline)
                if "GALE WARNING" in headline or "STORM WARNING" in headline or "HURRICANE FORCE WIND WARNING" in headline:
                    if self._debug: print("    is a warning")
                    warning_list.append(headline)
                elif "HURRICANE WARNING" in headline or "TYPHOON WARNING" in headline or "TROPCIAL STORM WARNING" in headline:
                    if self._debug: print("    is a tropical warning")
    #                tropcial_warning_list.append(headline)
                    warning_list.append(headline)
                elif "POSSIBLE" in headline:
                    if self._debug: print("    is an possible warning")
                    possible_list.append(headline)
                elif "WARNING" in headline:
                    if self._debug: print("    is another kind of warning")
                    if headline in other_warning_list:
                        #skip
                        if self._debug: print("    is already in the other warning list")
                    else:
                        other_warning_list.append(headline)
                else:
                    if self._debug: print("    is an advisory or an unknown headline")
                    if headline in advisory_list:
                        #skip
                        if self._debug: print("    is already in the advisory list")
                    else:
                        advisory_list.append(headline)

            new_warn_list = []
            if warning_list:
                #collapse into one
                if self._debug: print("looking for HU.W or TY.W")
    #            if tropical_warning_list:
    #            for warn in tropical_warning_list:
                for warn in warning_list:
                    if "HURRICANE WARNING" in warn or "TYPHOON" in warn:
                        new_warn_list.append(warn)
                        warning_found = 1
                        if self._debug: print("****found HU.W or TY.W")
                if self._debug: print("looking for HU.W")
                if not new_warn_list:
                    if self._debug: print("looking for TR.W")
                    for warn in warning_list:
                        if "TROPICAL STORM" in warn:
                            new_warn_list.append(warn)
                            warning_found = 1
                            if self._debug: print("****found TR.W:" + warn)
                            break
                for warn in warning_list:
                    if "HURRICANE FORCE" in warn:
                        if new_warn_list:
                            # deal with tropicals.
                            if "HURRICANE" in new_warn_list[0]:
                                #skip
                                if self._debug: print("hurricane warning already. Not adding non-trop warning.")
                                break
                            else:
                                # must be a TR.W add anyway.
                                new_warn_list.append(warn)
                                if self._debug: print("****found HF.W:" + warn)
                                break
                        else:
                            # no tropicals. Add.
                            new_warn_list.append(warn)
                            if self._debug: print("****found HF.W:" + warn)
                            break
                if not new_warn_list:
                    if self._debug: print("looking for SR.W")
                    for warn in warning_list:
                        if "STORM" in warn:
                            new_warn_list.append(warn)
                            if self._debug: print("****found SR.W:" + warn)
                            break
                if not new_warn_list:
                    if self._debug: print("looking for GL.W")
                    for warn in warning_list:
                        if "GALE" in warn:
                            new_warn_list.append(warn)
                            if self._debug: print("****found GL.W:" + warn)
                            break
                if self._debug: print("collapsed wind warnings:")
                if self._debug: print(new_warn_list)
                for warn in new_warn_list:
                    new_headlines_list.append(warn)
            # add other types of warnings
            # do need to sort the list and remove duplicates





            for warn in other_warning_list:
                new_headlines_list.append(warn)
            if self._debug: print("All warnings to be used:")
            if self._debug: print(new_headlines_list)

            if possible_list:
                #collapse into one
                new_possible_list=[]
                if self._debug: print("looking for HF.A")
                for warn in possible_list:
                    if "HURRICANE FORCE" in warn:
                        new_possible_list.append(warn)
                        if self._debug: print("****found HF.A:" + warn)
                        break
                if not new_possible_list:
                    if self._debug: print("looking for HU.A")
                    for warn in possible_list:
                        if "HURRICANE FORCE" in warn:
                            new_possible_list.append(warn)
                            if self._debug: print("****found HU.A:" + warn)
                            break
                if not new_possible_list:
                    if self._debug: print("looking for TR.A")
                    for warn in possible_list:
                        if "TROPCIAL STORM FORCE" in warn:
                            new_possible_list.append(warn)
                            if self._debug: print("****found TR.A:" + warn)
                            break
                if not new_possible_list:
                    if self._debug: print("looking for SR.A")
                    for warn in possible_list:
                        if "STORM FORCE" in warn:
                            new_possible_list.append(warn)
                            if self._debug: print("****found SR.A:" + warn)
                            break
                if not new_possible_list:
                    if self._debug: print("looking for GL.A")
                    for warn in possible_list:
                        if "GALE FORCE" in warn:
                            new_possible_list.append(warn)
                            if self._debug: print("****found GL.A:" + warn)
                            break
                if self._debug: print(new_possible_list)

                if not new_warn_list:
                    # No warnings. Just use this.
                    new_headlines_list.append(new_possible_list[0])
                else:
                    #compare to the warning and add if greater category.
    #                for new_warn in new_warn_list:
                    if  "HURRICANE FORCE" in new_warn_list[0]:
                        #nevermind
                        if self._debug: print("hurricane force warning...not using possible warning")
                    elif len(new_warn_list) > 1:
                        if "HURRICANE FORCE" in new_warn_list[1]:
                            #nevermind
                            if self._debug: print("hurricane force warning...not using possible warning")
                    elif "STORM" in new_warn_list[0]:
                        if "HURRICANE FORCE" in new_possible_list[0]:
                            if self._debug: print("storm becoming HF. Keeping possible HF.")
                            new_headlines_list.append(new_possible_list[0])
                        elif "TROPICAL STORM FORCE" in new_possible_list[0]:
                            if self._debug: print("storm becoming tropical storm. Keeping possible Tropical.")
                            new_headlines_list.append(new_possible_list[0])
                        else:
                            if self._debug: print("Nothing possible stronger than storm...not using possible warning")
                    elif "GALE" in new_warn_list[0]:
                        if "GALE" in new_possible_list[0]:
                            if self._debug: print("Nothing possible stronger than gale...not using possible warning")
                        else:
                            if self._debug: print("gale becoming stronger. Keeping possible warning.")
                            new_headlines_list.append(new_possible_list[0])

            #add advisories back in at the end
            for warn in advisory_list:
                new_headlines_list.append(warn)
            if self._debug: print(new_headlines_list)
            # turn the list back into a string
            new_headlines = "\n".join(new_headlines_list)
            new_headlines += "\n\n"

            return new_headlines


    #Modified from OFF base
    #Fix up spacing after abbreviations are used
    def _makeProduct(self, fcst, editArea, areaLabel, argDict):
        self.debug_print("Debug: _makeProduct in OFF_NC_Overrides")

        argDict["language"] = self._language
        # Generate Narrative Forecast for Edit Area
        fcstSegment = self._narrativeProcessor.generateForecast(
            argDict, editArea, areaLabel)

        # Handle abbreviations
        if self._useAbbreviations == 1:
            fcstSegment = self.marine_abbreviateText(fcstSegment)
            fcstSegment = re.sub(r'\n', r' ', fcstSegment)
            fcstSegment = re.sub(r' (\.[A-Za-z])', r'\n\1', fcstSegment)

        ## undo indent of next part so it is always done.
        # remove any double spaces
        fcstSegment = re.sub(r'  ', r' ', fcstSegment)

        # reformat to correct line length
        fcstSegment = self.endline(fcstSegment, linelength=self._lineLength)

        # now look for ... WORD and replace the space.
        # do this after first line length change so WORD...WORD doesn't go to
        # next line if only second word should.
        fcstSegment = re.sub(r'(\.\.\.) ([A-Za-z])', r'\1\2', fcstSegment)

        # reformat a second time for correct line length.
        fcstSegment = self.endline(fcstSegment, linelength=self._lineLength)

        fcst += fcstSegment
        return fcst

    #Modified from OFF base
    #**********************************************************************************
    #**********************************************************************************
    #*********************** Also in OFF_NAV_[ONA/ONP]_Overrides.py *******************
    #**********************************************************************************
    #**********************************************************************************
    def _postProcessArea(self, fcst, editArea, areaLabel, argDict):
        self.debug_print("Debug: _postProcessArea in OFF_NC_Overrides")

        # removed \n before $$. was getting 2 blank lines. due to changes in makeProduct
        return fcst + "$$\n\n"

    #Modified from OFF base
    #**********************************************************************************
    #**********************************************************************************
    #*********************** Also in OFF_NAV_[ONA/ONP]_Overrides.py *******************
    #**********************************************************************************
    #**********************************************************************************
    # F.Achorn/OPC    04/04/14    modify to use pil if dislapyName = None
    def _postProcessProduct(self, fcst, argDict):
        self.debug_print("Debug: _postProcessProduct in OFF_NC_Overrides")

        # Get the forecaster name
        self._userInfo = UserInfo.UserInfo()
        self._forecasterName = self._userInfo._getForecasterName(argDict)

        fcst += ".FORECASTER " + self._forecasterName + ". OCEAN PREDICTION CENTER.\n\n"
        self.setProgressPercentage(100)
        if (self._displayName is None):
            self.progressMessage(0, 100, self._pil + " Complete")
        else:
            self.progressMessage(0, 100, self._displayName + " Complete")
        return fcst



    #Modified from OFF base
    def lateDay_descriptor(self, statDict, argDict, timeRange):
        self.debug_print("Debug: lateDay_descriptor in OFF_NC_Overrides")

        # If time range is in the first period, return period1 descriptor for
        #  late day -- default 3pm-6pm
        if self._issuanceInfo.period1TimeRange().contains(timeRange):
            return self._issuanceInfo.period1LateDayPhrase()
        else:
            return "LATE"

    #Modified from OFF base
    def lateNight_descriptor(self, statDict, argDict, timeRange):
        self.debug_print("Debug: lateNight_descriptor in OFF_NC_Overrides")

        # If time range is in the first period, return period1 descriptor for
        #  late night -- default 3am-6am
        if self._issuanceInfo.period1TimeRange().contains(timeRange):
            return self._issuanceInfo.period1LateNightPhrase()
        else:
            return "LATE"

    #Modified from DiscretePhrases
####
# Taken from DiscretePhrases.TextUtility
# modify to remove "action" words like "in effect"
# F.Achorn/K.Achorn/OPC 05/04/2011
####
    # Returns the headline phrase based on the specified hazard.
    # The hazard record contains all geoIDs in the hazard['id'] field,
    # not just a single one.  Doesn't add the dots.
    def makeStandardPhrase(self, hazard, issuanceTime):
        self.debug_print("Debug: makeStandardPhrase in OFF_NC_Overrides")

        # hdln field present?
        if 'hdln' not in hazard:
            return ""

        # make sure the hazard is still in effect or within EXP critiera
        if (hazard['act'] != 'EXP' and issuanceTime >= hazard['endTime']) or \
          (hazard['act'] == 'EXP' and issuanceTime > 30*60 + hazard['endTime']):
            return ""   # no headline for expired hazards

        #assemble the hazard type
        hazStr = hazard['hdln']
        hazStr = self.convertToLower(hazStr)

        # if the hazard is a convective watch, tack on the etn
        phenSig = hazard['phen'] + "." + hazard['sig']
        if phenSig in ["TO.A", "SV.A"]:
            hazStr += " " + str(hazard["etn"])

# never want "action words" like "in effect"
##        # add on the action
##        actionWords = self.actionControlWord(hazard, issuanceTime)
##        hazStr = hazStr + ' ' + actionWords

        #get the timing words
        timeWords = self.getTimingPhrase(hazard, issuanceTime)
        if len(timeWords):
            hazStr += ' ' + timeWords

        return hazStr


#     #Modified from DiscretePhrases
#     #modify to check for instances like: WED NIGHT (mid period - uses night) into WED (extended - no night)
#     #F.Achorn/OPC    01/08/2013
#     def ctp_DAYNIGHT_DAYNIGHT(self,stext,etext,startPrefix,endPrefix):
#         self.debug_print("Debug: ctp_DAYNIGHT_DAYNIGHT in OFF_NC_Overrides")
#         #return phrases like FROM TONIGHT THROUGH WEDNESDAY
#
#         hourStr, hourTZstr, s_description = stext[0]  #starting text
#         hourStr, hourTZstr, e_description = etext[0]  #ending text
#
#         #special case of description the same
#         # instead of checking if s_description == e_description, look to see if the ending string
#         # is in the starting one. We were having issues where the end period was in the extended
#         # period (by calculation of days from issuance time) and wasn't adding "night" to the day.
#         # We resulted in a TUE NIGHT INTO TUE time period.
#         # This would just return TUE NIGHT, which is correct.
#         if e_description in s_description:
#             return s_description
#
#         #normal case of different descriptions
#         s = startPrefix + ' ' + s_description + ' ' + endPrefix + ' ' +\
#           e_description
#
#         return s

    #Modified from DiscretePhrases
    # changed to use abbreviated days of the week
    def asciiDayOfWeek(self, number):
        self.debug_print("Debug: asciiDayOfWeek in OFF_NC_Overrides")

        #converts number (0-Monday) to day of week
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        if number >= 0 and number < 7:
            return days[number]
        else:
            return "?" + repr(number) + "?"

    #Modified from DiscretePhrases
####
# Taken from DiscretePhrases.TextUtility
# modify to change timing wording for NCEP OFF products
# F.Achorn/K.Achorn/OPC 05/04/2011
# F.Achorn/OPC    04/10/2013    Modify DAY_NIGHT_ONLY, None to "", None, not "from", None
####
    def getTimingConnectorType(self, timingType, action):
        self.debug_print("Debug: getTimingConnectorType in OFF_NC_Overrides")

    # Returns the start and end prefix for the given start and end phrase
    # type and action code.
        d = {("NONE", "NONE"):           (None, None),
             ("NONE", "EXPLICIT"):       (None, "until"),
             ("NONE", "FUZZY4"):         (None, "through"),
             ("NONE", "FUZZY8"):         (None, "through"),
             ("EXPLICIT", "EXPLICIT"):   ("from", "to"),
             ("EXPLICIT", "FUZZY4"):     ("from", "through"),
             ("EXPLICIT", "FUZZY8"):     ("from", "through"),
             ("FUZZY4", "FUZZY4"):       ("from", "through"),
             ("FUZZY4", "FUZZY8"):       ("from", "through"),
             ("FUZZY8", "FUZZY4"):       ("from", "through"),
             ("FUZZY8", "FUZZY8"):       ("from", "through"),
             ("NONE", "DAY_NIGHT_ONLY"):          (None, "through"),
             ("EXPLICIT", "DAY_NIGHT_ONLY"):      ("from", "through"),
             ("FUZZY4", "DAY_NIGHT_ONLY"):        ("from", "through"),
             ("FUZZY8", "DAY_NIGHT_ONLY"):        ("from", "through"),
             ("DAY_NIGHT_ONLY", "DAY_NIGHT_ONLY"): ("", "into"),
             ("DAY_NIGHT_ONLY", "NONE"):          ("", None),
             ("DAY_NIGHT_ONLY", "EXPLICIT"):      ("from", "to"),
             ("DAY_NIGHT_ONLY", "FUZZY4"):        ("from", "through"),
             ("DAY_NIGHT_ONLY", "FUZZY8"):        ("from", "through"),
            }

        # special case for expirations.
        if action == 'EXP':
            return (None, "AT")

        return d.get(timingType, ("<startPrefix?>", "<endPrefix?>"))

    #Modified from DiscretePhrases
####
# Taken from DiscretePhrases.TextUtility
# modify to change timing for NCEP OFF products
# F.Achorn/K.Achorn/OPC 05/04/2011
# F.Achorn/Achorn/Juckins/Kosier/Listemaa(LWX) 06/20/2011  Modify to get timing off haz type, not hour
# F.Achorn/OPC    04/10/13    Modify to only list starting time, not ending for expected warnings.
####
    def getTimingType(self, hazRec, issueTime):
        self.debug_print("Debug: getTimingType in OFF_NC_Overrides")

        #Returns the timing type based on the issuanceTime and hazard record
        #Returns (startType, endType), which is NONE, EXPLICIT, FUZZY4, FUZZY8

        # Get the local headlines customizable timing
        tr = self.makeTimeRange(hazRec['startTime'], hazRec['endTime'])
        locStart, locEnd = self.getLocalHeadlinesTiming(
            None, None, hazRec['phen'], tr, hazRec['id'], issueTime)

        #time from issuanceTime
        deltaTstart = hazRec['startTime'] - issueTime  #seconds past now
        deltaTend = hazRec['endTime'] - issueTime  #seconds past now

        HR=3600  #convenience constants
        MIN=60   #convenience constants

        # record in the past, ignore
        if deltaTend <= 0:
            return ("NONE", "NONE")

        # upgrades and cancels
        if hazRec['act'] in ['UPG', 'CAN']:
            return ("NONE", "NONE")   #upgrades/cancels never get timing phrases

        # expirations EXP codes are always expressed explictly, only end time
        if hazRec['act'] == 'EXP':
            return ('NONE', 'EXPLICIT')

        phensig = hazRec['phen'] + '.' + hazRec['sig']

        # SPC Watches always get explicit times, 3 hour start mention
        spcWatches = ['TO.A', 'SV.A']
        if phensig in spcWatches:
            if deltaTstart < 3*HR:
                return ('NONE', 'EXPLICIT')
            else:
                return ('EXPLICIT', 'EXPLICIT')
#
#        # Tropical events never get times at all...except at OPC
#        tpcEvents = ['TY.A','TY.W','HU.A','HU.S','HU.W','TR.A','TR.W']
#        if phensig in tpcEvents:
#            return ('NONE', 'NONE')

        # special marine case?
        marineHazList = ["SC.Y", "SW.Y", "GL.W", "SR.W", 'HF.W', 'BW.Y',
          'UP.W', 'UP.Y', 'RB.Y', 'SE.W', 'SI.Y']  #treat like watches
        marinePils = ['CWF', 'OFF', 'NSH', 'GLF']  #specific marine pils
        oconusSites = ['PGUM', 'PHFO', 'PAFC', 'PAJK', 'PAFG']
        #OPC uses KWBC for normal OFF and KWNM for NAVTEX
        ncepSites = ['KWBC', 'KWNM', 'KNHC']
        marinePossibleWarnings = ['GL.A', 'SR.A', "TR.A", 'HF.A', 'HU.A']

##        # troubleshoot
##        print("oid = " + hazRec['oid'])

        # regular products - not marine
        if hazRec['pil'] not in marinePils:

            if self._debug: print("in marinePils")

            #advisories/warnings
            if hazRec['sig'] in ['Y', 'W']:   #advisories/warnings - explicit
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                else:
                    start = 'EXPLICIT'    #explicit start time after 3 hours
                end = 'EXPLICIT'          #end time always explicit

            #watches
            elif hazRec['sig'] in ['A']:  #watches - mix of explicit/fuzzy
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                elif deltaTstart < 12*HR:
                    start = 'EXPLICIT'    #explicit start time 3-12 hours
                else:
                    start = 'FUZZY4'      #fuzzy times after 12 (4/day)
                if deltaTend < 12*HR:     #explicit end time 0-12 hours
                    end = 'EXPLICIT'
                else:
                    end = 'FUZZY4'        #fuzzy times after 12 (4/day)

            #local hazards
            elif locStart is not None and locEnd is not None:
                start = locStart
                end = locEnd
            else:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                elif deltaTstart < 12*HR:
                    start = 'EXPLICIT'    #explicit start time 3-12 hours
                else:
                    start = 'FUZZY4'      #fuzzy times after 12 (4/day)
                if deltaTend < 12*HR:     #explicit end time 0-12 hours
                    end = 'EXPLICIT'
                else:
                    end = 'FUZZY4'        #fuzzy times after 12 (4/day)


        # marine - CONUS
        elif hazRec['officeid'] not in oconusSites and hazRec['officeid'] not in ncepSites:

            if self._debug: print("in CONUS sites")

            #advisories/warnings - explicit, but not some phensigs
            if hazRec['sig'] in ['Y', 'W'] and phensig not in marineHazList:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                else:
                    start = 'EXPLICIT'    #explicit start time after 3 hours
                end = 'EXPLICIT'          #end time always explicit

            #watches - mix of explicit/fuzzy, some phensig treated as watches
            elif hazRec['sig'] in ['A'] or phensig in marineHazList:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                elif deltaTstart < 12*HR:
                    start = 'EXPLICIT'    #explicit start time 3-12 hours
                else:
                    start = 'FUZZY4'      #fuzzy times after 12 (4/day)
                if deltaTend < 12*HR:     #explicit end time 0-12 hours
                    end = 'EXPLICIT'
                else:
                    end = 'FUZZY4'        #fuzzy times after 12 (4/day)

            #local hazards - treat as watches
            elif locStart is not None and locEnd is not None:
                start = locStart
                end = locEnd
            else:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                elif deltaTstart < 12*HR:
                    start = 'EXPLICIT'    #explicit start time 3-12 hours
                else:
                    start = 'FUZZY4'      #fuzzy times after 12 (4/day)
                if deltaTend < 12*HR:     #explicit end time 0-12 hours
                    end = 'EXPLICIT'
                else:
                    end = 'FUZZY4'        #fuzzy times after 12 (4/day)

        # marine - OCONUS
        elif hazRec['officeid'] in oconusSites:

            if self._debug: print("in oconus sites")

            #advisories/warnings - explicit, but not some phensigs
            if hazRec['sig'] in ['Y', 'W'] and phensig not in marineHazList:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                else:
                    start = 'EXPLICIT'    #explicit start time after 3 hours
                end = 'EXPLICIT'          #end time always explicit

            #special marine phensigs - treat as watches, with fuzzy8
            elif phensig in marineHazList:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                else:
                    start = 'FUZZY8'      #fuzzy start times
                end = 'FUZZY8'            #always fuzzy end times


            #regular watches - fuzzy4
            elif hazRec['sig'] in ['A']:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                elif deltaTstart < 12*HR:
                    start = 'EXPLICIT'    #explicit start time 3-12 hours
                else:
                    start = 'FUZZY4'      #fuzzy times after 12 (4/day)
                if deltaTend < 12*HR:     #explicit end time 0-12 hours
                    end = 'EXPLICIT'
                else:
                    end = 'FUZZY4'        #fuzzy times after 12 (4/day)

            #local hazards - treat as watches
            elif locStart is not None and locEnd is not None:
                start = locStart
                end = locEnd
            else:
                if deltaTstart < 3*HR:    #no start time in first 3 hours
                    start = 'NONE'
                elif deltaTstart < 12*HR:
                    start = 'EXPLICIT'    #explicit start time 3-12 hours
                else:
                    start = 'FUZZY4'      #fuzzy times after 12 (4/day)
                if deltaTend < 12*HR:     #explicit end time 0-12 hours
                    end = 'EXPLICIT'
                else:
                    end = 'FUZZY4'        #fuzzy times after 12 (4/day)
        # MARINE - NCEP
        else:
            # We are relying on the forecaster to have the correct warning
            # in the hazard grids....
            # Is this one of the "Possible" Warnings?
            if self._debug: print(phensig)
            if phensig in marinePossibleWarnings:
                #day/night only start/end time after 24 hours
                start = 'DAY_NIGHT_ONLY'
                end = 'NONE'
                if self._debug: print("Possible Warning")
            else:
                #no start/end time in first 24 hours
                start = 'NONE'
                end = 'NONE'
                if self._debug: print("Other Warning")
##                # All warnings have same timing
##                if deltaTstart < 24*HR:
##                    #no start/end time in first 24 hours
##                    start = 'NONE'
##                    end = 'NONE'
##                else:
##                    #day/night only start/end time after 24 hours
##                    start = 'DAY_NIGHT_ONLY'
##                    end = 'DAY_NIGHT_ONLY'
        return (start, end)


    #Modified from OFF base
    # Returns a list of the Hazards allowed for this product in VTEC format.
    # These are sorted in priority order - most important first.
    # Note: any additions here need to be added to removeExtraOFFHeadlines
    def allowedHazards(self):
        self.debug_print("Debug: allowedHazards in OFF_NC_Overrides")

        allActions = ["NEW", "EXA", "EXB", "EXT", "CAN", "CON", "EXP"]
        tropicalActions = ["NEW", "EXA", "EXB", "EXT", "UPG", "CAN", "CON",
          "EXP"]
        marineActions = ["NEW", "EXA", "EXB", "EXT", "CON"]
        return [
            ('HU.W', tropicalActions, 'Tropical'),   # HURRICANE WARNING
            ('TY.W', tropicalActions, 'Tropical'),   # TYPHOON WARNING
            ('TR.W', tropicalActions, 'Tropical'),   # TROPICAL STORM WARNING
            ('HF.W', marineActions, 'Marine'),       # HURRICANE FORCE WIND WARNING
            ('SR.W', marineActions, 'Marine'),       # STORM WARNING
            ('GL.W', marineActions, 'Marine'),       # GALE WARNING
            ('SE.W', marineActions, 'Marine'),       # HAZARDOUS SEAS
            ('UP.W', allActions, 'IceAccr'),         # HEAVY FREEZING SPRAY WARNING
            ('HF.A', marineActions, 'Marine'),        # HURRICANE FORCE WINDS POSSIBLE (trop and non-trop)
            ('HU.A', tropicalActions, 'Tropical'),   # HURRICANE POSSIBLE
            ('TY.A', tropicalActions, 'Tropical'),   # TYPHOON POSSIBLE
            ('TR.A', tropicalActions, 'Tropical'),    # TROPICAL STORM FORCE WINDS POSSIBLE
            ('SR.A', marineActions, 'Marine'),        # STORM FORCE WINDS POSSIBLE
            ('GL.A', marineActions, 'Marine'),        # GALE FORCE WINDS POSSIBLE
            ('FG.Y', allActions, 'Fog'),             # DENSE FOG ADVISORY
            ('SM.Y', allActions, 'Smoke'),           # DENSE SMOKE ADVISORY
            ('UP.Y', allActions, 'IceAccr'),         # HEAVY FREEZING SPRAY ADVISORY
            ('AF.Y', allActions, 'Ashfall'),         # VOLCANIC ASHFALL ADVISORY
            ]

    #Modified from DiscretePhrases
    # This method uses the allowedHazards() list to determine which
    # hazardTable entry has the most important priority and removes
    # the entry or piece thereof in place.  Returns 1 if something was
    # modified and 0 otherwise
    #
    # Don't need anymore. keep in case we ever have hazards w/o sig.
#    def fixHazardConflict(self, index1, index2, hazardTable):
#        self.debug_print("Debug: fixHazardConflict in OFF_NC_Overrides")
#
#        allowedHazardList = self.getAllowedHazardList()
#        phen1 = hazardTable[index1]['phen']
#        phen2 = hazardTable[index2]['phen']
#        sig1 = hazardTable[index1]['sig']
#        sig2 = hazardTable[index2]['sig']
#        act1 =  hazardTable[index1]['act']
#        act2 =  hazardTable[index2]['act']
#        haz1 = phen1 + "." + sig1
#        haz2 = phen2 + "." + sig2
#        ignoreList = ['CAN', 'EXP', 'UPG']
#
###        print("haz1 = " + haz1 + " act1 = " + act1)
###        print("haz2 = " + haz2 + " act2 = " + act2)
#        # if sig1 or sig2 is blank, it's a local hazard.
#         ##############only real change##############
#        if not sig1 or sig2 not:
#            #build without the . at end. Was coming up as haz? = phen.""
#            haz1 = phen1
#            haz2 = phen2
#        if haz1 in allowedHazardList and haz2 in allowedHazardList and \
#               act1 not in ignoreList and act2 not in ignoreList:
###            print("both allowed and not ignored action")
#
#            if (self.getHazardCategory(haz1) != self.getHazardCategory(haz2)) or \
#                self.getHazardCategory(haz1) is None or \
#                self.getHazardCategory(haz2) is None:
#                return 0
#
#        else:
#            return 0  # no changes were made
#
#        print("haz1 importance = " + str(self.getHazardImportance(haz1)))
#        print("haz2 importance = " + str(self.getHazardImportance(haz2)))
#        if self.getHazardImportance(haz1) < self.getHazardImportance(haz2):
#            lowIndex = index2
#            highIndex = index1
#        else:
#            lowIndex = index1
#            highIndex = index2
#
#        #
#        # Added to prevent a current lower TO.A from overiding a higher SV.A
#        #
#
#        if hazardTable[lowIndex]['phen'] == 'SV' and \
#           hazardTable[lowIndex]['sig'] == 'A' and \
#           hazardTable[highIndex]['phen'] == 'TO' and \
#           hazardTable[highIndex]['sig'] == 'A':
#               if (int(hazardTable[lowIndex]['etn']) > int(hazardTable[highIndex]['etn']) and
#                  (int(hazardTable[highIndex]['etn']) - int(hazardTable[lowIndex]['etn'])) > 50):
#                   lowIndexTemp = lowIndex
#                   lowIndex = highIndex
#                   highIndex = lowIndexTemp
#
#        lowStart = hazardTable[lowIndex]['startTime']
#        lowEnd = hazardTable[lowIndex]['endTime']
#        highStart = hazardTable[highIndex]['startTime']
#        highEnd = hazardTable[highIndex]['endTime']
#
#        # first check to see if high pri completely covers low pri
#        if highStart <= lowStart and highEnd >= lowEnd:  # remove low priority
#            del hazardTable[lowIndex]
#
#        # next check to see if high pri lies within low pri
#        elif lowStart <= highStart and lowEnd >= highEnd:  # high pri in middle
#            if lowStart < highStart:
#                h = copy.deepcopy(hazardTable[lowIndex])
#                # trim the early piece
#                hazardTable[lowIndex]['endTime'] = highStart
#                if lowEnd > highEnd:
#                    # make a new end piece
#                    h['startTime'] = highEnd
#                    hazardTable.append(h)
#            elif lowStart == highStart:
#                hazardTable[lowIndex]['startTime'] = highEnd
#
#        elif highEnd >= lowStart:
#            hazardTable[lowIndex]['startTime'] = highEnd  # change low start
#
#        elif highStart <= lowEnd:
#            hazardTable[lowIndex]['endTime'] = highStart  # change low end
#
#        return 1


#     from WxPhrases.py
#########################################################
#       embedded_visibility_flag
#########################################################
    # Handling visibility within the weather phrase
    def embedded_visibility_flag(self, tree, node):
        self.debug_print("Debug: embedded_visibility_flag in OFF_NC_Overrides")
        # If 1, report visibility embedded with the
        # weather phrase. Set this to 0 if you are using the
        # visibility_phrase.
        return 1
        # changing the return to 1 would mix vis and wx.

#     from WxPhrases.py
#########################################################
#       separateNonPrecip_threshold
#########################################################
    def separateNonPrecip_threshold(self, tree, node):
        self.debug_print("Debug: separateNonPrecip_threshold in OFF_NC_Overrides")
        # Number of sub-phrases required to separate precip from
        # non-precip
        return 10

#     # from TimeDespriptor.py
#     # F.Achorn/OPC 10/04/13    Use different words if it's the first period.
#     # Time period Table Access
#     def timePeriod_descriptor(self, tree, node, timeRange):
#         self.debug_print("Debug: timePeriod_descriptor in OFF_NC_Overrides")
#         # Returns a descriptor phrase for the time range.
#         # Assumes the timeRange is in GMT and converts it to Local time.
#
#         # more than 12 hours, return empty string
#         if timeRange.duration() > 12*3600:
#             return ""
#         if timeRange == node.getTimeRange():
#             return ""
#
#         # determine the local time
#         localTime, shift = self.determineTimeShift()
#         periodStart = timeRange.startTime() + shift
#         periodEnd = timeRange.endTime() + shift
#         startHour = periodStart.hour
#         endHour = periodEnd.hour
#
# #         # Don't want to mention "afternoon" if we're in the "THIS AFTERNOON" time period.
# #         #figure out if we're in a "THIS AFTERNOON" first period. If so, use a different list.
# #         issuanceInfo = tree.get("issuanceInfo")
# #         if self._debug:
# #             print issuanceInfo.period1Label()
# #         if (timeRange.startTime() >=  self._issuanceInfo.period1TimeRange().startTime()) and (timeRange.endTime() <=  self._issuanceInfo.period1TimeRange().endTime()):
# #             inPeriod1TimeRange=1
# #         else:
# #             inPeriod1TimeRange=0
# #
# #         # if the first period is .This Afternoon... and we're in period 1, use a different list.
# #         if (issuanceInfo.period1Label() == ".This afternoon...") and (inPeriod1TimeRange == 1):
# #             if self._debug:
# #                 print " Working in first period of a This Afternoon forecast...use a different list"
# #                 print "   Current time range: ", timeRange
# #                 print "   Period 1 time range: ", self._issuanceInfo.period1TimeRange()
# #             # get the table
# #             table = self.timePeriod_descriptor_list_this_afternoon(tree, node)
# #         else:
# #             # get the table
# #             table = self.timePeriod_descriptor_list(tree, node)
#         table = self.timePeriod_descriptor_list(tree, node)
#
#         # look for the best match entry, start with the startTime match
#         bestIndexes = []
#         bestTime = 9999
#         for i in xrange(len(table)):
#             diff = self.hourDiff(startHour, table[i][0])
#             if diff < bestTime:
#                 bestTime = diff
#         for i in xrange(len(table)):
#             diff = self.hourDiff(startHour, table[i][0])
#             if diff == bestTime:
#                bestIndexes.append(table[i])
#
#         # if nothing found, return "" string
#         if len(bestIndexes) == 0:
#             return ""
#
#         # now find the best match for the ending time, from the ones earlier
#         bestTime = 9999
#         returnValue = ''
#         for i in xrange(len(bestIndexes)):
#             diff = self.hourDiff(endHour, bestIndexes[i][1])
#             if diff < bestTime:
#                 returnValue = bestIndexes[i][2]
#                 bestTime = diff
#
#         if self._debug:
#             print("returnValue = " + str(returnValue))
#
#         if type(returnValue) is types.MethodType:
#             return returnValue(tree, node, timeRange)
#         else:
#             return returnValue
#
#     # from TimeDespriptor.py
#     # F.Achorn/OPC  03/25/13    Replace "late in the evening" with "before midnight"
#     # special list of descriptors. Don't want to mention "afternoon" if we're in the "THIS AFTERNOON" time period.
#     def timePeriod_descriptor_list_this_afternoon(self, tree, node):
#         self.debug_print("Debug: timePeriod_descriptor_list_this_afternoon in OFF_NC_Overrides")
#         # Contains definition for localtime start/end times and phrase
#         # Tuples, 0=startHrLT, 1=endHrLT, 2=phrase
#         # note: due to 3hrly blocks and aligning self.DAY with 12z,
#         # self.DAY = 8am in the summer for ONA.
#         #day = self.DAY()
#         #day = self.DAY() - self.daylight()
#         # just set to 6am...
#         day = 6
#         return [
#                 (day, (day+3)%24, "early in the morning"),    # 6a-9a
#                 (day, (day+6)%24, "in the morning"),          # 6a-noon
#                 (day, (day+9)%24, "until late afternoon"),    # 6a-3p
#                 (day, (day+12)%24, ""),                       # 6a-6p
#                 (day, (day+15)%24, "until early evening"),    # 6a-9p
#                 (day, (day+18)%24, "through the evening"),    # 6a-midnite
#
#                 ((day+2)%24, (day+3)%24, "early in the morning"),  # 8a-9a
#
#                 ((day+3)%24, (day+6)%24, "late in the morning"), # 9a-noon
#                 ((day+3)%24, (day+9)%24, "in the late morning and early afternoon"), # 9a-3p
#                 ((day+3)%24, (day+12)%24, "in the late morning and afternoon"),      # 9a-6p
#                 ((day+3)%24, (day+15)%24, "until early evening"),      # 9a-9p
#                 ((day+3)%24, (day+18)%24, "through the evening"),      # 9a-midnite
#
#                 ((day+5)%24, (day+6)%24, "late in the morning"),      # 11a-noon
#
#                 ((day+6)%24, (day+9)%24,  ""),      # noon-3p
#                 ((day+6)%24, (day+12)%24, ""),            # noon-6p
#                 ((day+6)%24, (day+15)%24, ""),# noon-9p
#                 ((day+6)%24, (day+18)%24, ""),# noon-midnite
#
#                 ((day+8)%24, (day+9)%24, ""),      # 2pm-3pm
#
#                 ((day+9)%24, (day+12)%24, self.lateDay_descriptor),   # 3p-6p
#                 ((day+9)%24, (day+15)%24, "early in the evening"),    # 3p-9p
#                 ((day+9)%24, (day+18)%24, "in the evening"),          # 3p-midnite
#                 ((day+9)%24, (day+21)%24, "until early morning"),     # 3p-3a
#                 ((day+9)%24,  day, ""),                               # 3p-6a
#
#                 ((day+11)%24, (day+12)%24, self.lateDay_descriptor), # 5p-6p
#
#                 ((day+12)%24, (day+15)%24, "early in the evening"),   # 6p-9p
#                 ((day+12)%24, (day+18)%24, "in the evening"),         # 6p-midnite
#                 ((day+12)%24, (day+21)%24, "until early morning"),    # 6p-3a
#                 ((day+12)%24, day, ""),                               # 6p-6a
#
#                 ((day+14)%24, (day+15)%24, "early in the evening"), # 8p-9p
#
#                 ((day+15)%24, (day+18)%24, "before midnight"),                  # 9p-midnite
#                 ((day+15)%24, (day+21)%24, "overnight into early morning"),# 9p-3a
#                 ((day+15)%24, day, "overnight"),            # 9p-6a
#
#                 ((day+17)%24, (day+18)%24, "before midnight"), # 11p-midnight
#
#                 ((day+18)%24, (day+21)%24, "after midnight"),               # midnite-3a
#                 ((day+18)%24, day, "after midnight"),                       # midnite-6a
#                 ((day+18)%24, (day+6)%24, ""),                              # midnite-noon
#
#                 ((day+20)%24, (day+21)%24, "after midnight"), # 2a-3a
#
#                 ((day+21)%24, day, self.lateNight_descriptor),              # 3a-6a
#                 ((day+21)%24, (day+3)%24, "early in the morning"),          # 3a-9a
#                 ((day+21)%24, (day+6)%24, "early in the morning"),          # 3a-noon
#                 ((day+21)%24, (day+9)%24, ""),               # 3a-3p
#                 ((day+21)%24, (day+12)%24, ""),                             # 3a-6p
#
#                 ((day+23)%24, (day)%24, self.lateNight_descriptor), # 5a-6a
#
#                 ]

    # from TimeDespriptor.py
    # F.Achorn/OPC  03/25/13    Replace "late in the evening" with "before midnight"
    # F.Achorn/OPC  03/11/14    Changed "early in the afternoon" to "in the afternoon"
    def timePeriod_descriptor_list(self, tree, node):
        self.debug_print("Debug: timePeriod_descriptor_list in OFF_NC_Overrides")
        # Contains definition for localtime start/end times and phrase
        # Tuples, 0=startHrLT, 1=endHrLT, 2=phrase
        # note: due to 3hrly blocks and aligning self.DAY with 12z,
        # self.DAY = 8am in the summer for ONA.
        #day = self.DAY()
        #day = self.DAY() - self.daylight()
        # just set to 6am...
        day = 6
        return [
                (day, (day+3)%24, "early"),    # 6a-9a
                (day, (day+6)%24, "early"),          # 6a-noon
                (day, (day+9)%24, ""),    # 6a-3p
                (day, (day+12)%24, ""),                       # 6a-6p
                (day, (day+15)%24, ""),    # 6a-9p
                (day, (day+18)%24, ""),    # 6a-midnite

                ((day+2)%24, (day+3)%24, "early"),  # 8a-9a

                ((day+3)%24, (day+6)%24, ""), # 9a-noon
                ((day+3)%24, (day+9)%24, ""), # 9a-3p
                ((day+3)%24, (day+12)%24, ""),      # 9a-6p
                ((day+3)%24, (day+15)%24, "late"),      # 9a-9p
                ((day+3)%24, (day+18)%24, ""),      # 9a-midnite

                ((day+5)%24, (day+6)%24, ""),      # 11a-noon

                ((day+6)%24, (day+9)%24,  "late"),      # noon-3p
                ((day+6)%24, (day+12)%24, "late"),            # noon-6p
                ((day+6)%24, (day+15)%24, "late"),# noon-9p
                ((day+6)%24, (day+18)%24, "late"),# noon-midnite

                ((day+8)%24, (day+9)%24, "late"),      # 2pm-3pm

                ((day+9)%24, (day+12)%24, self.lateDay_descriptor),   # 3p-6p
                ((day+9)%24, (day+15)%24, "late"),    # 3p-9p
                ((day+9)%24, (day+18)%24, "late"),          # 3p-midnite
                ((day+9)%24, (day+21)%24, ""),     # 3p-3a
                ((day+9)%24,  day, ""),                               # 3p-6a

                ((day+11)%24, (day+12)%24, self.lateDay_descriptor), # 5p-6p

                ((day+12)%24, (day+15)%24, "early"),   # 6p-9p
                ((day+12)%24, (day+18)%24, "early"),         # 6p-midnite
                ((day+12)%24, (day+21)%24, "early"),    # 6p-3a
                ((day+12)%24, day, ""),                               # 6p-6a

                ((day+14)%24, (day+15)%24, "early"), # 8p-9p

                ((day+15)%24, (day+18)%24, "early"),                  # 9p-midnite
                ((day+15)%24, (day+21)%24, ""),# 9p-3a
                ((day+15)%24, day, ""),            # 9p-6a

                ((day+17)%24, (day+18)%24, "early"), # 11p-midnight

                ((day+18)%24, (day+21)%24, "late"),               # midnite-3a
                ((day+18)%24, day, "late"),                       # midnite-6a
                ((day+18)%24, (day+6)%24, ""),                              # midnite-noon

                ((day+20)%24, (day+21)%24, "late"), # 2a-3a

                ((day+21)%24, day, self.lateNight_descriptor),              # 3a-6a
                ((day+21)%24, (day+3)%24, "late"),          # 3a-9a
                ((day+21)%24, (day+6)%24, "early"),          # 3a-noon
                ((day+21)%24, (day+9)%24, ""),               # 3a-3p
                ((day+21)%24, (day+12)%24, ""),                             # 3a-6p

                ((day+23)%24, (day)%24, self.lateNight_descriptor), # 5a-6a

                ]

    # modified from WxPhrases.py
    # F.Achorn/OPC 12/17/2013
    # make sure that the formatter specified "moderate" freezing spray.
    def wxIntensityDescriptors(self):
        # This is the list of coverages, wxTypes, intensities, attribute for which special
        # weather intensity wording is desired.  Wildcards (*) can be used to match any value.
        # If a weather subkey is not found in this list, default wording
        # will be used from the Weather Definition in the server.
        # The format of each tuple is:
        #    (coverage, wxType, intensity, attribute, descriptor)
        # NOTE: descriptor can be a method taking (tree, node, subkey) as arguments
        return [
                ("*", "RW", "--", "*", ""),
                ("*", "RW", "-", "*", ""),
                ("*", "R", "--", "*", "light"),
                ("*", "R", "-", "*", ""),
                ("*", "R", "+", "*", ""),
                ("*", "RW", "+", "*", ""),
                ("*", "SW", "--", "*", ""),
                ("*", "SW", "-", "*", ""),
                ("*", "SW", "+", "*", ""),
                ("*", "S", "--", "*", "very light"),
                ("*", "S", "-", "*", ""),
                ("*", "S", "+", "*", ""),
                ("*", "T", "+", "*", ""),
                ("*", "ZR", "--", "*", "light"),
                ("*", "ZR", "+", "*", ""),
                ("*", "L", "*", "*", ""),
                ("*", "F", "+", "*", "dense"),
                ("*", "IP", "+", "*", ""),
                ("*", "ZY", "m", "*", "moderate"),
            ]

    # modified from WxPhrases.py
    # F.Achorn/OPC 06/28/2013
    # We would get sentences like " AND SHOWERS" or "SHOWERS AND AND THUNDERSTORMS"
    # The mix of the two ways to add a conjunction below were sometimes adding one before
    # the current phrase (not useSimple, and sometimes after (useSimple).
    # Modified the loop and code that removed an unwanted conjuntion to get the right ones
    # and leave those we still need.
    def getWeatherWords(self, tree, node, rankList):
        self.debug_print("Debug: getWeatherWords in OFF_NC_Overrides")
        # For each WeatherSubKey, add it to the phrase
        # Use ranking of subkeys to form wording:
        #   If useSimple produce simple wording e.g.
        #       Chance of rain and snow and slight chance of sleet and freezing rain.
        #   Otherwise:
        #    Create a phrase of the form:
        #    <list1 of subkeys> <conjunction> <list2 of subkeys>
        #    where:
        #      list1 and list2 are lists of subkeys separated by
        #        '...' or 'and' e.g.  Snow...rain and sleet
        #      list1 subkeys have similar coverages and ranks
        #      list2 subkeys have coverages or ranks significantly
        #         different from those in list1
        #      conjunction connects the 2 lists appropriately, e.g.
        #         Snow and rain with possible sleet and freezing rain.
        #         Rain and drizzle with pockets of snow.

        rankList.sort(self.rankedSortOrder)
        length = len(rankList)
        words = ""
        index = 0
        # For non-simple phrasing, have we switched to the second list
        # using the conjunction yet?
        switchConjunction = 0
        # Begin by including coverage with weather value
        includeCovInten = 1
        # Handle "Likely" specially
        addLkly = 0
        subkeys = self.getSubkeys(rankList)
        useSimple = self.useSimple(tree, node, rankList, subkeys)
        prevCoverage = prevSubkey = prevRank = None
        prevConj = ""

        for index in range(len(rankList)):
            subkey, rank = rankList[index]
            if self._debug: print("words >"+ words +"<")
            if self._debug: print("NEW LOOP: subkey "+subkey.wxType())
            # If not last one, determine nextCoverage
            if index < length-1:
                nextSubkey, nextRank = rankList[index+1]
            else:
                nextSubkey = None

            # Set so that value is included UNLESS re-set by one of the
            # sub-methods e.g. mixedWith, possiblyMixedWith, etc..
            self.includeValue = 1

            # Add conjunction for non-simple words
            if not useSimple:
                if self._debug: print("not using Simple")
                words, conj, switchConjunction, includeCovInten, addLkly = \
                       self.addWxConjunction(
                    tree, node, words, prevSubkey, prevRank, subkey, rank,
                    index, switchConjunction, includeCovInten, addLkly)
                if self._debug: print("words become >"+ words +"<")

            # Get string for subkey checking previous and next coverage
            value, prevCoverage = self.weather_value(
                tree, node, subkey, prevCoverage, nextSubkey,
                includeCovInten=includeCovInten)
            if self._debug: print("value >"+ value +"<")
            if self.includeValue == 1:
                if value not:
                    if not useSimple:
                        #remove the concunction we just created.
                        if self._debug: print("  removing conjunction >"+conj+"<")
                        words = self.removeLast(words, conj)
                        if self._debug: print("words become >"+ words +"<")
                    else:
                        if index == length - 1:
                            # If empty value string, remove the previous conjunction
                            # so we don't end up with something like "rain and"
                            # Only do this this is the last phrase and we'd be leaving
                            # something like "rain and" behind. Otherwise, leave that
                            # last one in place so you don't end up with "rainscattered showers"
                            # with no conjuntion at all.
                            if self._debug: print("  removing conjunction >"+prevConj+"<")
                            words = self.removeLast(words, prevConj)
                            if self._debug: print("words become >"+ words +"<")
                else:
                    words += value

            # if last one, do not add conjunction
            if index == length - 1: break
            if useSimple:
                if self._debug: print("using simple")
                if value:
                    conj = self.wxConjunction(tree, node, subkey, rank, nextSubkey, nextRank)
                    words += conj
                else:
                    conj = ""
                    if self._debug: print("blank words. don't get a conjuntion.")

            if self._debug: print("words >"+ words +"<")

            # if we have an empty string, let's not check againt it next time.
            # wasnt to be sure we get the right word next loop.

            if (value):
                prevSubkey = subkey
                prevConj = conj
                prevRank = rank

        if addLkly:
            words += " likely"
        if self._debug: print("FINAL words >"+ words +"<")
        return words


    # From PhraseBuilder
    # Modified to ignore differences in mins
    # F.Achorn/OPC     11/19/2013
    def checkLocalEffectDifference(self, tree, node, dataType, threshold,
                                   area1Stats, area2Stats, al1, al2):
        self.debug_print("Debug: checkLocalEffectDifference in OFF_NC_Overrides")
        if dataType == self.DISCRETE():
            if area1Stats != area2Stats:
                return 1
            else:
                return 0
        if dataType == self.WEATHER():
            flag = self.checkWeatherSimilarity(
                tree, node, area1Stats, area2Stats, al1=al1, al2=al2)
            # checkWeatherSimilarity returns 0 if there IS a difference and, thus,
            # should be a local effect
            if flag == 0:
                return 1
            else:
                return 0
        if dataType == self.VECTOR():
            area1Stats, dir = area1Stats
            area2Stats, dir = area2Stats

        if isinstance(area1Stats, tuple):
            min1, max1 = area1Stats
            min2, max2 = area2Stats
#             diff1 = self.absDiff(min1, min2)
            diff2 = self.absDiff(max1, max2)
            # Check to see if one range is included within the other
            if self.rangeIncluded(min1, max1, min2, max2) == 1:
                return 0
            if self.rangeIncluded(min2, max2, min1, max1) == 1:
                return 0
            # Check to see if either min or max is greater than threshold
            # changed to only check min
#             if diff1 > threshold or diff2 > threshold:
            if diff2 > threshold:
                return 1
            else:
                return 0
        else:
            absDiff = self.absDiff(area1Stats, area2Stats)
            if absDiff > threshold:
                return 1
            else:
                return 0

    #from ConfigVariables.py
    # Automatic Collapsing of Sub-phrases for Combined periods
    # F.Achorn/OPC    03/18/14    was set to 23, forcing 24 hour time periods to only have one phrase.
    def collapseSubPhrase_hours_dict(self, tree, node):
        # If the period is longer than these hours, subphrases will automatically
        # be collapsed.
        self.debug_print("Debug: collapseSubPhrase_hours_dict in OFF_NC_Overrides")
        return {
            "otherwise": 24,
            #"Wx": 12,
            }


    ### WindGust
    #Taken from VectorRelatedPhrases
    #modified to add in code to always report
    # if the gusts were in a different warning category.
    # F.Achorn/OPC    05/01/14
    def gust_wind_difference_nlValue(self, tree, node):
        self.debug_print("Debug: gust_wind_difference_nlValue in OFF_NC_Overrides")
        # Difference between gust and maxWind below which gusts are not mentioned
        # Units are mph

        # we would like to see if the max gust and max wind are different warning categories. If so, set the threshold
        # to something low like 1. Otherwise, 15 kt.
        maxWinds = tree.stats.get("Wind", node.getTimeRange(), node.getAreaLabel(), mergeMethod="Max")
        maxGusts = tree.stats.get("WindGust", node.getTimeRange(), node.getAreaLabel(), mergeMethod="Max")

        if self._debug:
            print("maxWinds = " + str(maxWinds[0]))
            print("maxGusts = " + str(maxGusts))

        # Check for both within the same warning thresholds
        warnThresholdWinds = self.getWarnThreshold(maxWinds[0])
        warnThresholdGusts = self.getWarnThreshold(maxGusts)
        if warnThresholdWinds == warnThresholdGusts:
            # no change in warning
            if self._debug: print("Using 10 kt")
            return 10
        else:
            if self._debug: print("Using 1 kt")
            # report, even for a very small change
            return 1

    #Taken from VectorRelatedPhrases
    #modified to remove "around" from the baseline the gust phrase from "with gusts to around 40 kt"
    # F.Achorn/OPC    05/01/14
    def embedded_gust_phrase(self, tree, node, gustStats, maxWind, subRange):
        self.debug_print("Debug: embedded_gust_phrase in OFF_NC_Overrides")
        # Determine what type of gust phrase to add. Day and night are treated
        # differently with gusts phrases toned down a bit for night.
        try:
            includeTropical = self._includeTropical
        except:
            includeTropical = False
        if includeTropical:
            statLabel = "" # Use the moderatedMinMax from the Tropical components
        else:
            statLabel = "vectorMinMax"
        gusts = None
        if gustStats is None:
           # If useWindForGusts_flag is set, use max Wind for reporting gusts
           if self.useWindsForGusts_flag(tree,  node) == 1:
               windStats = tree.stats.get(
                       "Wind", subRange, node.getAreaLabel(), statLabel=statLabel,
                       mergeMethod="Max")
               if windStats is None:
                   return ""
               else:
                   gusts, dir = windStats
        else:
            gusts = self.getValue(gustStats, "Max")
        if gusts is None:
            return ""

        if includeTropical:
            #  Round gusts and maxWind to the nearest 5 kt regardless of users' overrides
            gusts = self.round(gusts, 'Nearest', 5.0)
            maxWind = self.round(maxWind, 'Nearest', 5.0)

        threshold = self.nlValue(self.null_nlValue(tree, node, "WindGust", "WindGust"), gusts)
        if gusts < threshold:
            return ""
        gustPhrase = ""
        outUnits = self.element_outUnits(tree, node, "WindGust", "WindGust")
        units = self.units_descriptor(tree, node, "units", outUnits)
        windDifference = self.nlValue(self.gust_wind_difference_nlValue(tree, node), maxWind)
        if gusts - maxWind > windDifference:
            gustPhrase = " with gusts to " + repr(int(gusts)) + " " + units
        return gustPhrase

###################
# The following two methods timingWordTableDAYNIGHT and ctp_DAYNIGHT_DAYNIGHT are needed if we ever go back to 24 hour long extended periods.
###################
#     #Modified from DiscretePhrases
# ####
# # Taken from DiscretePhrases.TextUtility
# # modify to change timing for NCEP OFF products
# # F.Achorn/K.Achorn/OPC 05/04/2011
# # F.Achorn/OPC    01/08/2013 - modify to use 12 hour periods to determine what wording to use.
# #                              cleaned up if statement and loop.
# ####
#     def timingWordTableDAYNIGHT(self, issueTime, eventTime, timeZone,
#       timeType='start'):
#         self.debug_print("Debug: timingWordTableDAYNIGHT in OFF_NC_Overrides")
#
#         #returns (timeValue, timeZone, descriptiveWord).
#         #eventTime is either the starting or ending time, based on
#         #the timeType flag. timezone is the time zone for the hazard area
#         #table is local time, start, end, descriptive phrase
#         HR=3600
#         sameDay = [
# #          (0*HR,         self.DAY()*HR,   "early today"), #midnght-559am
#           (0*HR,         self.DAY()*HR,   "tonight"), #midnght-559am
#           (self.DAY()*HR,   self.NIGHT()*HR, "today"),       #600am-6pm
#           (self.NIGHT()*HR, 24*HR,        "tonight")]     #6pm-midnight
#
#         nextDay = [
#           (0*HR,         self.DAY()*HR,   "tonight"),           #midnght-559am
#           (self.DAY()*HR,   self.NIGHT()*HR, "<dayOfWeek>"),       #600am-6pm
#           (self.NIGHT()*HR, 24*HR, "<dayOfWeek> night"),] #6pm-midnight
#
#         midPeriod = [
#           (0*HR,         self.DAY()*HR,   "<dayOfWeek-1> night"), #midnght-559am
#           (self.DAY()*HR,   self.NIGHT()*HR, "<dayOfWeek>"),         #600am-6pm
#           (self.NIGHT()*HR, 24*HR,        "<dayOfWeek> night")]   #6pm-midnight
#
# #        fifthPeriod = [
# #          (0*HR,         self.DAY()*HR,   "<dayOfWeek-1> night"), #midnght-559am
# #          (self.DAY()*HR,   self.NIGHT()*HR, "<dayOfWeek>"),         #600am-6pm
# #          (self.NIGHT()*HR, 24*HR,        "<dayOfWeek> night")]   #6pm-midnight
#
#         # In the extendeds, we don't want "NIGHT" added.
#         subsequentDay = [
#           (0*HR,         self.DAY()*HR,   "<dayOfWeek-1>"), #midnght-559am
#           (self.DAY()*HR,   self.NIGHT()*HR, "<dayOfWeek>"),         #600am-6pm
#           (self.NIGHT()*HR, 24*HR,        "<dayOfWeek>")]   #6pm-midnight
# ##        subsequentDay = [
# ##          (0*HR,         self.DAY()*HR,   "<dayOfWeek-1> night"), #midnght-559am
# ##          (self.DAY()*HR,   self.NIGHT()*HR, "<dayOfWeek>"),         #600am-6pm
# ##          (self.NIGHT()*HR, 24*HR,        "<dayOfWeek> night")]   #6pm-midnight
# #        print "0*HR = " + str(0*HR)
# #        print "self.DAY()*HR = 6*HR = " + str(self.DAY()*HR)
# #        print "24*HR = " + str(24*HR)
#
#         #determine local time
#         myTimeZone = os.environ["TZ"]  # save the defined time zone
#         os.environ["TZ"] = timeZone    # set the new time zone
#         ltissue = time.localtime(issueTime) # issuance local time
#         ltevent = time.localtime(eventTime) # event local time
#         utcevent = time.gmtime(eventTime)
#
#         #determine Epoch time - return as an integer
#         epochIssue = int(time.mktime(ltissue))
#         epochEvent = int(time.mktime(ltevent))
#         diffSeconds = epochEvent - epochIssue
#         diffHours = diffSeconds/float(HR)
#         # how many 12 hour periods? use round to round up or down
#         diff12HourPeriods = int(round (diffHours/12.0))
# #        diff12HourPeriods = diffHours/12.0
# #        print str(epochEvent) + " - " + str(epochIssue) + " = " + str(diffSeconds)
#         if self._debug: print "diffHours = " + str(diffHours)
#         if self._debug: print "diff12HourPeriods = " + str(diff12HourPeriods)
#         #determine the delta days from issuance to event
#         diffDays = ltevent[7] - ltissue[7]  #julian day
#         if diffDays < 0:   #year wrap around, assume Dec/Jan
#             diffDays = ltevent[2] + 31 - ltissue[2]  #day of month
# #        print "timeType ="+timeType
# #        print "timeZone ="+timeZone
# #        print "ltissue ="+ str(ltissue[7])
# #        print "ltissue ="+ str(ltissue[2])+ " " + str(ltissue[3])+ ":" +str(ltissue[4])
# #        print "ltevent ="+ str(ltevent[7])
# #        print "ltevent ="+ str(ltevent[2])+ " " + str(ltevent[3])+ ":" +str(ltevent[4])
# #        print "eventTime (UTC) ="+ str(utcevent[2])+ " " + str(utcevent[3])+ ":" +str(utcevent[4])
# #        print "diffDays ="+str(diffDays)
# #        print "self._productIssuance =" +self._productIssuance
#
#         #get description time phrase
#         description = "<day>"
#         hourmin = ltevent[3]*HR + ltevent[4]*60   #hour, minute
# #        print "hourmin = "+str(hourmin)+" = "+str(hourmin/HR)
#
#         #choose proper table
#         #if diffDays == 0:
#         if diff12HourPeriods <2:
#             #periods 1 and 2
#             if self._debug: print "using sameDay"
#             table = sameDay
# #            for (startT, endT, desc) in sameDay:
# #                print "startT = "+str(startT)+" = "+str(startT/3600)
# #                print "endT = "+str(endT)+" = "+str(endT/3600)
# #                print "desc = "+ desc
# #                if hourmin >= startT and hourmin < endT and timeType=='start':
# #                    description = desc
# #                    break
# #                elif hourmin <= endT and timeType=='end':
# #                    description = desc
# #                    break
#         elif diff12HourPeriods < 3:
#             #nextDay
#             if self._debug: print "using nextDay"
#             table = nextDay
#
#         elif diff12HourPeriods <= 4 or ((diff12HourPeriods <= 5) and self._productIssuance in self._issueTimesWith5thPeriod):
#             # midPeriod
#             if self._debug: print "using midPeriod"
#             table = midPeriod
# #            # if it's the next day (periods 3/4)
# #            print "using nextDay"
# #            table = nextDay
# #        elif (diff12HourPeriods == 5) and self._productIssuance in self._issueTimesWith5thPeriod:
# #            print "using fifthPeriod"
# #            table = fifthPeriod
#         else:
#             if self._debug: print "using subsequentDay"
#             table = subsequentDay
#
#         if self._debug: print "Trying time periods"
#         for (startT, endT, desc) in table:
# #            print "  startT = "+str(startT)+" = "+str(startT/HR)
# #            print "  endT = "+str(endT)+" = "+str(endT/HR)
# #            print "  desc = "+ desc
# #            hourmin = ltevent[3]*HR + ltevent[4]*60   #hour, minute
# #            print "  hourmin in loop = "+str(hourmin)+" = "+str(hourmin/HR)
#             if hourmin >= startT and hourmin < endT and timeType=='start':
#                 if self._debug: print "  choosing " + desc
#                 description = desc
#                 break
#             elif hourmin <= endT and timeType=='end':
#                 if self._debug: print "  choosing " + desc
#                 description = desc
#                 break
#         dow = ltevent[6]  #day of week
#         dowMinusOne = ltevent[6] - 1
#         if dowMinusOne < 0:
#             dowMinusOne = 6   #week wraparound
#         description = string.replace(description, "<dayOfWeek>",
#           self.asciiDayOfWeek(dow))   #day of week
#         description = string.replace(description, "<dayOfWeek-1>",
#           self.asciiDayOfWeek(dowMinusOne))   #day of week
#
# #        print "dow =" + str(dow) + " = " + self.asciiDayOfWeek(dow)
# #        print "dowMinusOne ="+ str(dowMinusOne) + " = " + self.asciiDayOfWeek(dowMinusOne)
# #        print "description ="+description
#
#         os.environ["TZ"] = myTimeZone  # reset the defined time zone
#
#         hourStr = None
#         hourTZstr = None
#         return (hourStr, hourTZstr, description)
#
#     #Modified from DiscretePhrases
#     #modify to check for instances like: WED NIGHT (mid period - uses night) into WED (extended - no night)
#     #F.Achorn/OPC    01/08/2013
#     def ctp_DAYNIGHT_DAYNIGHT(self,stext,etext,startPrefix,endPrefix):
#         self.debug_print("Debug: ctp_DAYNIGHT_DAYNIGHT in OFF_NC_Overrides")
#         #return phrases like FROM TONIGHT THROUGH WEDNESDAY
#
#         hourStr, hourTZstr, s_description = stext[0]  #starting text
#         hourStr, hourTZstr, e_description = etext[0]  #ending text
#
#         #special case of description the same
#         # instead of checking if s_description == e_description, look to see if the ending string
#         # is in the starting one. We were having issues where the end period was in the extended
#         # period (by calculation of days from issuance time) and wasn't adding "night" to the day.
#         # We resulted in a TUE NIGHT INTO TUE time period.
#         # This would just return TUE NIGHT, which is correct.
#         if e_description in s_description:
#             return s_description
#
#         #normal case of different descriptions
#         s = startPrefix + ' ' + s_description + ' ' + endPrefix + ' ' +\
#           e_description
#
#         return s

###################
# The previous two methods timingWordTableDAYNIGHT and ctp_DAYNIGHT_DAYNIGHT are needed if we ever go back to 24 hour long extended periods.
###################


    def wxCombinations(self):
        # This is the list of which wxTypes should be combined into one
        # WITHIN a sub-phrase.
        # For example, if ("RW", "R") appears, then wxTypes of "RW" and "R" will
        # be combined into one key and the key with the dominant coverage will
        # be used as the combined key.
        # You may also specify a method which will be
        #  -- given arguments subkey1 and subkey2 and
        #  -- should return
        #     -- a flag = 1 if they are to be combined, 0 otherwise
        #     -- the combined key to be used
        #  Note: The method will be called twice, once with (subkey1, subkey2)
        #  and once with (subkey2, subkey1) so you can assume one ordering.
        #  See the example below, "combine_T_RW"
        #
        return [
                ("RW", "R"),
                ("SW", "S"),
                ("T", "R"),
     #           self.combine_T_RW,
                ]

#     # Taken from Wx Phrases. Limit weather phrases to one. No Showers and tstms, becoming showers late.
#     # F.Achorn/OPC    03/30/14    Changed from default of 3 to 1
#
#    def subPhrase_limit(self, tree, node):
#         # If the number of sub-phrases is greater than this limit, the weather
#         # phrase will use 6-hour instead of the higher resolution to produce:
#         #
#         #    OCCASIONAL SNOW POSSIBLY MIXED WITH SLEET AND FREEZING
#         #    DRIZZLE IN THE MORNING...THEN A CHANCE OF RAIN POSSIBLY MIXED WITH SNOW
#         #    AND SLEET AND FREEZING DRIZZLE IN THE AFTERNOON.
#         #
#         # instead of:
#         #    OCCASIONAL SNOW IN THE MORNING. CHANCE OF LIGHT SLEET AND
#         #    SLIGHT CHANCE OF LIGHT FREEZING DRIZZLE IN THE LATE MORNING AND
#         #    EARLY AFTERNOON. CHANCE OF SNOW EARLY IN THE AFTERNOON. CHANCE OF
#         #    RAIN IN THE AFTERNOON.
#         return 1
#
