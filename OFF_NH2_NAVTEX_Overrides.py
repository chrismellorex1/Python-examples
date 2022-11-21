import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis
import ModuleAccessor
import mergeProds
import sys
import numpy as np

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class OFF_NH2_NAVTEX_Overrides:
    def __init__(self):
        pass

#     VariableList = [
#         (("Include Tropical?", "includeTropical") , "No", "radio", ["Yes","No"]),
#         #(("Period Combining?","pdCombo"), "No", "radio", ["Yes","No"]),
#         ]

    VariableList = [
        #(copy.deepcopy(CWF.TextProduct.VariableList)),
        (("Include Tropical?", "includeTropical"), "No", "radio", ["Yes", "No"]),
        #(("Forecaster Name", "forecasterName") , "99", "radio",
        # ["NELSON","STRIPLING","SCHAUER","CHRISTENSEN",
        #  "LEWITSKY", "AL", "GR", "AGUIRRE", "DGS",
        #  "MUNDELL", "COBB", "LANDSEA", "CAB", "PAW",
        #  "FORMOSA", "HUFFMAN", "MT", "NAR"]),
        (("Period Combining?", "pdCombo"), "No", "radio", ["Yes", "No"]),
#         ((("Keep Previous Text After Period (Selecting zero\nwill keep all old text but will refresh headlines)",
#                       "updatePeriodIndex"), "No old text",
#                       "radio", ["No old text",0,1,2,3,4,5,6,7,8]))
        ]

    def __init__(self):
        TextRules.TextRules.__init__(self)
        SampleAnalysis.SampleAnalysis.__init__(self)

# End MAKE NO CHANGES HERE

    def _Text1(self):
        self.debug_print("Debug: _Text1 in NAVTEX_MIAMI_Overrides")

        return  "%s\n" % "...Please refer to Coastal Waters Forecasts (CWF) available" + \
                "%s\n" % "through NOAA Weather Radio and other means for detailed" + \
                "%s\n" % "Coastal Waters Forecasts..." + "\n"

    #Modified from OFF base
    def _Text2(self):
        self.debug_print("Debug: _Text2 in NAVTEX_MIAMI_Overrides")

        synopsis = ""

        #  Try to get Synopsis from previous CWF
        if self._definition["synopsisUGC"] == "AMZ101":

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

            #  Format expiration time for inclusion in synopsis header
            #expTime = time.strftime('%d%H%M', expTuple)

        elif self._definition["synopsisUGC"] == "GMZ001":

            productID = "MIAOFFNT4"
            synopsis = self.getPreviousProduct(productID, "SYNOPSIS")
            #  Clean up the previous synopsis
            synopsis = re.sub(r'\n', r' ', synopsis)
            synopsis = re.sub(r'  ', r' ', synopsis)
            synopsis = self._synopsisHeading + synopsis
            synopsis = self.endline(synopsis, linelength=65, breakStr=" ") + "\n"

            #  Convert absolute time pointer to a tuple of values like that
            #  returned by time.gmtime()
            #expTuple = time.strptime('%s' % (self._expireTime),
            #                         '%b %d %y %H:%M:%S GMT')

            #  Format expiration time for inclusion in synopsis header
            #expTime = time.strftime('%d%H%M', expTuple)
 #ADDED TO FIX ISSUE WITH SYNOPSIS ISSUE ERA 3/25/17
 #CHANGED FROM SJU CWF SYNOPSIS TO PREVIOUS VERSION 5/19/17 ERA

        else:

            #productID = "SJUCWFSJU"
            productID = "MIAOFFN05"
            #synopsis = self.getPreviousProduct(productID, "SYNOPSIS FOR PUERTO RICO AND THE U.S. VIRGIN ISLANDS WATERS")
            #synopsis = self.getPreviousProduct(productID, "SYNOPSIS")
            #  Clean up the previous synopsis
            #synopsis = re.sub(r'\n', r' ', synopsis)
            #synopsis = re.sub(r'  ', r' ', synopsis)
            entire_product = self.getPreviousProduct(productID).strip()
            #synopsis = entire_product.split("AMZ700")[1].split("$$")[0].split("\n\n")[1]
            synopsis = entire_product.split("Forecasts...")[1].split("San Juan")[0].split("\n\n")[1]
            #commented out line above and replaced with line below to add the NOTICE 10/09/2019 JRL
            #synopsis = entire_product.split("2019.")[1].split("San Juan")[0].split("\n\n")[1]
            #synopsis = self._synopsisHeading + synopsis
            synopsis = self.endline(synopsis, linelength=65, breakStr=" ") + '\n'

            #  Convert absolute time pointer to a tuple of values like that
            #  returned by time.gmtime()
            #expTuple = time.strptime('%s' % (self._expireTime),
            #                         '%b %d %y %H:%M:%S GMT')

            #  Format expiration time for inclusion in synopsis header
            #expTime = time.strftime('%d%H%M', expTuple)

        #    return synopsis

        return synopsis + ""

#             #productID = "SJUCWFSJU"
#             productID = "MIAOFFN05"
#             #synopsis = self.getPreviousProduct(productID, "SYNOPSIS FOR PUERTO RICO AND THE U.S. VIRGIN ISLANDS WATERS")
#             synopsis = self.getPreviousProduct(productID, ".SYNOPSIS...")
#             #  Clean up the previous synopsis
#             synopsis = re.sub(r'\n', r' ', synopsis)
#             synopsis = re.sub(r'  ', r' ', synopsis)
#             synopsis = self._synopsisHeading + synopsis
#             synopsis = self.endline(synopsis, linelength=65, breakStr=" ") + '\n'
#
#             #  Convert absolute time pointer to a tuple of values like that
#             #  returned by time.gmtime()
#             #expTuple = time.strptime('%s' % (self._expireTime),
#             #                         '%b %d %y %H:%M:%S GMT')
#
#             #  Format expiration time for inclusion in synopsis header
#             #expTime = time.strftime('%d%H%M', expTuple)
#
#         #    return synopsis

        #return synopsis + ""

    #Need second synopsis for NFDOFFN03
    def _Text3(self):
        synopsis = ""
        if self._definition["pil"] == "OFFN04":
            productID = "MIAOFFNT3"
            # Can't just search for "SYNOPSIS"
            # It will only return the first one it finds
            entire_product = self.getPreviousProduct(productID).strip()
            # get just the second synopsis from it's area "AMZ088"
            # then split on "$$" and grab everything before the $$ at the end of the synopsis
            # Then split on a blank line and grab the second paragraph
            synopsis = entire_product.split("AMZ101")[1].split("$$")[0].split("\n\n")[1]
            #  Clean up the previous synopsis
            synopsis = re.sub(r'\n', r' ', synopsis)
            synopsis = self.endline(synopsis, linelength=65, breakStr=" ")
            return "%s\n" %  "Within 200 nm east of the coast of Florida\n" + \
                    synopsis + "" + "\n"
        else:
            pass

            #added by JRL 10/14/11
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

    # Inserted since NHC has this
    def addTropical(self, analysisList, phraseList, includeHazards=True):
        self.debug_print("Debug: addTropical in OFF_ONA_Overrides")

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
                ("WaveHeight", self.moderatedMinMax, [6]),
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

########################################
##### added section below for a1 to a2 variances JRL/01/26/12
########################################

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
            #dict["WaveHeight"] = (15, 10)
            dict["WaveHeight"] = (10, 5)
            dict["Swell"] = (10, 10)
#        dict["Wind"] =  (0, 3)
#        dict["WaveHeight"] = (5,5)
        return dict

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] =  3 #changed from 2 to 3 ERA 10/15/14       # Changed to 1 (from 2) by JL/1/31/12 for testing
        #dict["WindWaveHgt"] =  2
        dict["Wind"] = 5
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
        dict["WaveHeight"] =  "seas 2 ft or less" #ERA 09/30/14
#        dict["WindWaveHgt"] =  "seas 2 ft or less"
        dict["Wind"] =  "variable winds less than 5 kt"
        dict["Swell"] =  ""
        return dict

    def null_phrase_dict(self, tree, node):
        # Phrase to use for null values in subPhrases other than the first
        # Can be an empty string
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "2 ft or less" #ERA 09/30/14
#        dict["WindWaveHgt"] =  "2 feet or less"
        dict["Wind"] =  "variable less than 5 kt"
        dict["Wx"] =  ""
        dict["Swell"] =  "light"
        dict["hurricane force winds to"] =  "hurricane force winds to"
        dict["storm force winds to"] = "storm force winds to"
        dict["gales to"] =  "gales to"
        dict["up to"] =  "variable winds less than 5 kt"
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

    def significant_wx_visibility_subkeys(self, tree, node):
        # Weather values that constitute significant weather to
        # be reported regardless of visibility.
        # If your visibility_wx_threshold is None, you do not need
        # to set up these subkeys since weather will always be
        # reported.
        # Set of tuples of weather key search tuples in the form:
        #  (cov type inten)
        # Wildcards are permitted.
        return [("* *")]

    def wxHierarchies(self):
    # This is the hierarchy of which coverage and intensity to choose if
    # wxTypes are the same and to be combined into one subkey.
    # override to correct baseline error in wxType for "VA" (baseline has "BA") 9/8/11 CNJ/JL
        return {
        "wxType": ["WP", "R", "RW", "T", "L", "ZR", "ZL", "S", "SW",
                  "IP", "F", "ZF", "IF", "IC", "H", "BS", "BN", "K", "BD",
                  "FR", "ZY", "VA", "<NoWx>", "SQ"], #added SQ on 06/06/16 ERA
        #"wxType":["WP", "R", "RW", "T", "L", "ZR", "ZL", "S", "SW",
        #          "IP", "F", "ZF", "IF", "IC", "H", "BS", "BN", "K", "BD",
        #          "FR", "ZY", "BA", "<NoWx>"],
        "coverage": ["Def", "Wide", "Brf", "Frq", "Ocnl", "Pds", "Inter",
                    "Lkly", "Num", "Sct", "Chc", "Areas",
                    "SChc", "WSct", "Iso", "Patchy", "<NoCov>"],
        "intensity": ["+", "m", "-", "--", "<NoInten>"],
        "visibility": ["0SM", "1/4SM", "1/2SM", "3/4SM", "1SM", "11/2SM", "2SM",
                      "21/2SM", "3SM", "4SM", "5SM", "6SM", "P6SM", "<NoVis>"],
        }

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
                                "Wind": ",  shifting to ",
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
                (12, 25): 10, #changed from 5 2/19/16 ERA
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
#     def vector_mag_difference_nlValue_dict(self, tree, node):
#         # Replaces WIND_THRESHOLD
#         # Magnitude difference.  If the difference between magnitudes
#         # for sub-ranges is greater than or equal to this value,
#         # the different magnitudes will be noted in the phrase.
#         # Units can vary depending on the element and product
#         return  {
#
#             "Wind": 4,
#             "Swell": 1,  # ft
#             "Swell2": 1,  # ft
#             }

    def vector_dir_difference_dict(self, tree, node):
        # Replaces WIND_DIR_DIFFERENCE
        # Direction difference.  If the difference between directions
        # for sub-ranges is greater than or equal to this value,
        # the different directions will be noted in the phrase.
        # Units are degrees
        return {
            "Wind": 60, # degrees...changed from 40 ERA 2/19/16
            "Swell": 60, # degrees
            "Swell2": 60, # degrees
            }

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
             "WaveHeight":
                 {

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

    #Modified from OFF base
    def OFFPeriod(self):
        self.debug_print("Debug: OFFPeriod in NAVTEX_MIAMI_Overrides")

#            type = "component",
        methodList = [
                          self.consolidateSubPhrases,
                          self.assemblePhrases,
                          self.wordWrap,
                          ],

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
                          ("WaveHeight", self.moderatedMinMax, [6]),
                          ("WindWaveHgt", self.moderatedMinMax, [6]),
                          ("Swell", self.vectorModeratedMinMax, [6]),
                          ("Swell2", self.vectorModeratedMinMax, [6]),
                         # ("Period", self.moderatedMinMax, [6]),
                         # ("Period2", self.moderatedMinMax, [6]),
                          ("Wx", self.rankedWx, [12]),
                         # ("T", self.minMax),
                         # ("PoP", self._PoP_analysisMethod("OFFPeriod"), [6]),
                         # ("PoP", self.binnedPercent, [6]),

                      # Use the following if you want moderated
                      # single values (e.g. N WIND 20 KT).
                      # Set the moderating percentage in the "moderated_dict"
                      # dictionary module.
                      # NOTE:  If you use these methods, include and uncomment
                      # the "combine_singleValues_flag_dict" in your Local file (see below)
                         #("Wind", self.vectorModeratedMax, [3]),
                          #("Wind", self.vectorMinMax, [12]),
                          #("WindGust", self.moderatedMax, [3]),
                          #("WaveHeight", self.moderatedMax, [6]),
                          #("WindWaveHgt", self.moderatedMax, [6]),
                          #("Swell", self.vectorModeratedMax, [6]),
                          #("Swell2", self.vectorModeratedMax, [6]),
                          #("Period", self.moderatedMax, [6]),
                          #("Period2", self.moderatedMax, [6]),
                          #("Wx", self.rankedWx, [6]),
                          #("T", self.minMax),
                          #("PoP", self._PoP_analysisMethod("OFFPeriod")),
                          #("PoP", self.binnedPercent, [6]),

                      # Use the following if you want absolute ranges.
                      # Set the maximum range values in the "maximum_range_nlValue_dict"
                      # dictionary module.
                          # Split time range in quarters for Wind and WindGust
                          #("Wind", self.vectorMinMax, [3]),
                          #("Wind", self.vectorMinMax, [12]),
                          #("WindGust", self.maximum, [3]),
                          #("WaveHeight", self.minMax, [6]),
                          #("WindWaveHgt", self.minMax, [6]),
                          # Split time range in half for Wx and Swell
                          #("Swell", self.vectorMinMax, [6]),
                          #("Swell2", self.vectorMinMax, [6]),
                          #("Period", self.avg, [6]),
                          #("Period2", self.avg, [6]),
                          #("Wx", self.rankedWx, [6]),
                          #("T", self.minMax),
                          #("PoP", self._PoP_analysisMethod("OFFPeriod")),
                          #("PoP", self.binnedPercent, [6]),
                        ]

        phraseList = [
                           # WINDS
                           (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
                           #(self.marine_wind_phrase,self._windLocalEffects_list()),
                           # Alternative:
#                           (self.marine_wind_phrase, self._windLocalEffects_list()),
                           #self.marine_wind_phrase,
                           #self.gust_phrase,
                           # WAVES
                           #self.wave_withPeriods_phrase,
                           # Alternative:
                           (self.wave_phrase, self._WaveHeightLocalEffects_list),
                           # SWELLS AND PERIODS
                           self.swell_withPeriods_phrase,
                           # Alternative:
                           #self.swell_phrase,
                           #self.period_phrase,
                           # WEATHER
#                           self.weather_phrase,

#                           self.weather_phrase,
#                          (self.wave_phrase,self._WaveHeightLocalEffects_list),

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
                ("Wind", ["NAV04B_N_of_27N",
                          "NAV04B_S_of_27N",
                            ]),
                ("WaveHeight", ["NAV04B_N_of_27N",
                                "NAV04B_S_of_27N"
                                  ]),
                #Areas listed by weather element that will be
                #intersected with the current area then
                #sampled and analyzed.
                #E.g. used in local effects methods.
                #("Wind", ["GlfofME_NW", "GlfofME_SE", "GeoBnk_NW", "GeoBnk_SE", "SofNE_Wof70W", "SofNE_Eof70W", "HudtoBalt_NW", "HudtoBalt_SE", "BalttoHag_Wof70W", "BalttoHag_Eof70W", "BalttoHat_Eof1000FM", "BalttoHat_Wof1000FM", "HattoCapeFear_Eof75W", "HattoCapeFear_Wof75W", "CapeFearto31N_Eof1000FM", "CapeFearto31N_Wof1000FM"]),
                #("WaveHeight", ["GlfofME_NW", "GlfofME_SE", "GeoBnk_NW", "GeoBnk_SE", "SofNE_Wof70W", "SofNE_Eof70W", "HudtoBalt_NW", "HudtoBalt_SE", "BalttoHag_Wof70W", "BalttoHag_Eof70W", "BalttoHat_Eof1000FM", "BalttoHat_Wof1000FM", "HattoCapeFear_Eof75W", "HattoCapeFear_Wof75W", "CapeFearto31N_Eof1000FM", "CapeFearto31N_Wof1000FM"]),
                #("Weather", ["A1", "A1_NE", "A2", "A2_SE", "A3", "A3_E", "A94_W", "A94_E", "A6_W", "A6_E", "A7_W", "A7_E", "A8_W", "A8_E"]),
                    ]
        }

    def _WaveHeightLocalEffects_list(self, tree, node):
        leArea1 = self.LocalEffectArea("NAV04B_S_of_27N", "S of 27N")
        leArea2 = self.LocalEffectArea("NAV04B_N_of_27N", "N of 27N")

        return [self.LocalEffect([leArea1, leArea2], 1, ", and "),
                ]

    def _windLocalEffects_list(self):
        leArea1 = self.LocalEffectArea("NAV04B_S_of_27N", "S of 27N")
        leArea2 = self.LocalEffectArea("NAV04B_N_of_27N", "N of 27N")

        return [self.LocalEffect([leArea1, leArea2], 2, ", and "),
                ]

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
                         # ("WindGust", self.moderatedMinMax, [24]),
                          ("WaveHeight", self.moderatedMinMax, [6]),
                          # ("WindWaveHgt", self.moderatedMinMax, [24]),
                          #("Wx", self.rankedWx),
                          #("T", self.minMax),  # needed for weather_phrase
                          #("PoP", self._PoP_analysisMethod("OFFExtended")),
                          #("PoP", self.binnedPercent),
                          #("Swell", self.vectorModeratedMinMax, [12]),
                          #("Swell2", self.vectorModeratedMinMax, [12]),

                      # Use the following if you want moderated
                      # single values (e.g. N WIND 20 KT).
                      # Set the moderating percentage in the "moderated_dict"
                      # dictionary module.
                      # NOTE:  If you use these methods, include and uncomment
                      # the "combine_singleValues_flag_dict" in your Local file (see below)
                          #("Wind", self.vectorModeratedMax, [6]),
                          #("WindGust", self.moderatedMax, [12]),
                          #("WaveHeight", self.moderatedMax, [12]),
                          #("WindWaveHgt", self.moderatedMax, [12]),
                          #("Wx", self.rankedWx),
                          #("T", self.minMax),
                          #("PoP", self._PoP_analysisMethod("OFFExtended")),
                          #("PoP", self.binnedPercent),
                          #("Swell", self.vectorModeratedMax, [12]),
                          #("Swell2", self.vectorModeratedMax, [12]),

                      # Use the following if you want absolute ranges.
                      # Set the maximum range values in the "maximum_range_nlValue_dict"
                      # dictionary module.
                      # dictionary module.
                          #("Wind", self.vectorMinMax, [6]),
                          #("WindGust", self.minMax, [12]),
                          #("WaveHeight", self.minMax, [12]),
                          #("WindWaveHgt", self.minMax, [12]),
                          #("Wx", self.rankedWx),
                          #("T", self.minMax),
                          #("PoP", self._PoP_analysisMethod("OFFExtended")),
                          #("PoP", self.binnedPercent),
                          #("Swell", self.vectorMinMax, [12]),
                          #("Swell2", self.vectorMinMax, [12]),
                      ],
                 "phraseList": [
                               # WIND
                               self.marine_wind_phrase,
                               # WAVEHEIGHT
                               # Commented out until fully developed seas wording fixed 9/7/11 CNJ/JL
                               #self.wave_withPeriods_phrase,
                               # Alternative:
                               (self.wave_phrase, self._WaveHeightLocalEffects_list),
                               #self.wave_phrase,
                               # SWELLS AND PERIODS
                               #self.swell_withPeriods_phrase,
                               # Alternative:
                               #self.swell_phrase,
                               #self.period_phrase,
                               # WEATHER
                               #self.weather_phrase,
                               #self.visibility_phrase,
                               ],
                "intersectAreas": [
                         ("Wind", ["NAV04B_N_of_27N",
                                   "NAV04B_S_of_27N",
                            ]),
                         ("WaveHeight", ["NAV04B_N_of_27N",
                                         "NAV04B_S_of_27N"
                                  ])],
                }

    def _WaveHeightLocalEffects_list(self, tree, node):
        leArea1 = self.LocalEffectArea("NAV04B_S_of_27N", "S of 27N")
        leArea2 = self.LocalEffectArea("NAV04B_N_of_27N", "N of 27N")

        return [self.LocalEffect([leArea1, leArea2], 1, ", and "),
                ]

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
        if localTimeZone == "EDT":
            return [
               ("530 AM", self.DAY(), self.NIGHT(), 16,
                 ".Today...", "early in the morning", "late",
                 1, narrativeDefAM),
                ("1130 AM", "issuanceHour", self.NIGHT(), 16,
                 ".THIS AFTERNOON...", "early in the morning", "late",
                 1, narrativeDefAM),
                ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                 ".Tonight...", "late", "late", #CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 02/19/16
                 1, narrativeDefPM),
                ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                 ".Overnight...", "late", "early in the evening", #CHANGED FROM "LATE IN THE NIGHT" ERA 02/19/16
                 1, narrativeDefPM)
                ]
        else:
            return [
                ("430 AM", self.DAY(), self.NIGHT(), 16,
                 ".Today...", "early in the morning", "late",
                 1, narrativeDefAM),
                ("1030 AM", self.DAY(), self.NIGHT(), 16,
                 ".Today...", "early in the morning", "late",
                 1, narrativeDefAM),
                ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                 ".Tonight...", "late", "late", #CHANGED FROM "LATE IN THE NIGHT" "EARLY IN THE MORNING" ERA 02/19/16
                 1, narrativeDefPM),
                ("1030 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                 ".Tonight...", "late", "early in the evening", #CHANGED FROM "LATE IN THE NIGHT" ERA 02/19/16
                 1, narrativeDefPM),
                ]

#added 2/19/16 ERA

    def timePeriod_descriptor_list(self, tree, node):
        # Contains definition for localtime start/end times and phrase
        # Tuples, 0=startHrLT, 1=endHrLT, 2=phrase
        day = self.DAY()
        return [
               # (day, (day+3)%24, "early in the morning"),    # 6a-9a
                (day, (day+6)%24, "in the morning"),          # 6a-noon
                #(day, (day+9)%24, ""),    # 6a-3p
                (day, (day+12)%24, ""),                       # 6a-6p
               # (day, (day+15)%24, "until early evening"),    # 6a-9p
               # (day, (day+18)%24, "through the evening"),    # 6a-midnite

                #((day+2)%24, (day+3)%24, "early in the morning"),  # 8a-9a

              #  ((day+3)%24, (day+6)%24, "late"), # 9a-noon
               # ((day+3)%24, (day+9)%24, "in the late morning and early afternoon"), # 9a-3p
               # ((day+3)%24, (day+12)%24, "in the late morning and afternoon"),      # 9a-6p
               # ((day+3)%24, (day+15)%24, "until early evening"),      # 9a-9p
               # ((day+3)%24, (day+18)%24, "through the evening"),      # 9a-midnite

              #  ((day+5)%24, (day+6)%24, "late in the morning"),      # 11a-noon

              #  ((day+6)%24, (day+9)%24,  "early in the afternoon"),      # noon-3p
                ((day+6)%24, (day+12)%24, "in the afternoon"),            # noon-6p
               # ((day+6)%24, (day+15)%24, "in the afternoon and evening"),# noon-9p
              #  ((day+6)%24, (day+18)%24, "in the afternoon and evening"),# noon-midnite

               # ((day+8)%24, (day+9)%24, "early in the afternoon"),      # 2pm-3pm

                ((day+9)%24, (day+12)%24, self.lateDay_descriptor),   # 3p-6p
               # ((day+9)%24, (day+15)%24, "early in the evening"),    # 3p-9p
                ((day+9)%24, (day+18)%24, "in the evening"),          # 3p-midnite
              #  ((day+9)%24, (day+21)%24, "until early morning"),     # 3p-3a
                ((day+9)%24,  day, ""),                               # 3p-6a

                ((day+11)%24, (day+12)%24, self.lateDay_descriptor), # 5p-6p

              #  ((day+12)%24, (day+15)%24, "early in the evening"),   # 6p-9p
               # ((day+12)%24, (day+18)%24, "in the evening"),         # 6p-midnite
               # ((day+12)%24, (day+21)%24, "until early morning"),    # 6p-3a
                ((day+12)%24, day, ""),                               # 6p-6a

              #  ((day+14)%24, (day+15)%24, "early in the evening"), # 8p-9p

                ((day+15)%24, (day+18)%24, "late"),                  # 9p-midnite
               # ((day+15)%24, (day+21)%24, "in the late evening and early morning"),# 9p-3a
                ((day+15)%24, day, "late"),            # 9p-6a

               # ((day+17)%24, (day+18)%24, "late"), # 11p-midnight

              #  ((day+18)%24, (day+21)%24, "after midnight"),               # midnite-3a
                ((day+18)%24, day, "late"),                       # midnite-6a
                ((day+18)%24, (day+6)%24, ""),                              # midnite-noon

              #  ((day+20)%24, (day+21)%24, "after midnight"), # 2a-3a

                ((day+21)%24, day, self.lateNight_descriptor),              # 3a-6a
             #   ((day+21)%24, (day+3)%24, "early in the morning"),          # 3a-9a
              #  ((day+21)%24, (day+6)%24, "early in the morning"),          # 3a-noon
             #   ((day+21)%24, (day+9)%24, "until afternoon"),               # 3a-3p
                ((day+21)%24, (day+12)%24, ""),                             # 3a-6p

                ((day+23)%24, (day)%24, self.lateNight_descriptor), # 5a-6a

                ]


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

    def _preProcessArea(self, fcst, editArea, areaLabel, argDict):
        self.debug_print("Debug: _preProcessArea in NAVTEX_MIAMI_Overrides")

        # This is the header for an edit area combination
        print("Generating Forecast for", areaLabel)
##        areaHeader = self.makeAreaHeader(
##            argDict, areaLabel, self._issueTime, self._expireTime,
##            self._areaDictionary, self._defaultEditAreas)
##        fcst = fcst + areaHeader


        # get the hazards text
        self._hazards = argDict['hazards']
        self._combinations = argDict["combinations"]
        print("here1")

        headlines = self.generateProduct("Hazards", argDict, area = editArea,
                                         areaLabel=areaLabel,
                                         timeRange = self._timeRange)
        # remove any double spaces
        headlines = re.sub(r'  ', r' ', headlines)
        print("here2")

        # Navtex only needs the area desription as the header
        if argDict["combinations"] is not None:
            print("here3")
            areaList = self.getCurrentAreaNames(argDict, areaLabel)
        else:
            print("here4")
            for editArea, label in self._defaultEditAreas:
                print("here5")
                if label == areaLabel:
                    print("here6")
                    areaList = [editArea]
        print(areaList)
        # Access the UGC information for the area(s) if available
        print("here7")
        accessor = ModuleAccessor.ModuleAccessor()

        print("here8")
        areaDict = accessor.variable(self._areaDictionary, "AreaDictionary")
        for areaName in areaList:
                print(areaName + "\n")
                entry = areaDict[areaName]
                if entry['ugcName'] == '':
                #if entry['ugcName'] not:
                    areaHeader = entry['ugcName']
                else:
                    areaHeader = entry['ugcName'] + "\n\n"
        fcst += areaHeader

        #add headlines to forecast
        fcst += headlines
        fcst = re.sub(r'CONDITIONS POSSIBLE IN EFFECT', "CONDITIONS POSSIBLE", fcst)
        fcst = re.sub(r'WINDS POSSIBLE IN EFFECT', "WINDS POSSIBLE", fcst)
        fcst = re.sub(r'SEAS 0 TO 1 FT', "SEAS 1 FT OR LESS", fcst)
        fcst = re.sub(r'WARNING IN EFFECT', "WARNING", fcst)
        #fcst = string.replace(fcst, "!--NOT SENT--!", "")
        return fcst

    def allowedHazards(self):
        allActions = ["NEW", "EXA", "EXB", "EXT", "CAN", "CON", "EXP"]
        tropicalActions = ["NEW", "EXA", "EXB", "EXT", "UPG", "CAN", "CON",
          "EXP"]
        marineActions = ["NEW", "EXA", "EXB", "EXT", "CON"]
        return [
            ('HU.W', tropicalActions, 'Tropical'),     # HURRICANE WARNING
#            ('TY.W', tropicalActions, 'Tropical'),     # TYPHOON WARNING
            ('TR.W', tropicalActions, 'Tropical'),     # TROPICAL STORM WARNING
            ('HF.W', marineActions, 'Marine'),       # HURRICANE FORCE WIND WARNING
            ('SR.W', marineActions, 'Marine'),       # STORM WARNING
            ('GL.W', marineActions, 'Marine'),       # GALE WARNING
#            ('SE.W', marineActions, 'Marine'),       # HAZARDOUS SEAS
#            ('UP.W', allActions, 'IceAccr'),                        # HEAVY FREEZING SPRAY WARNING

             # added 05/03/11 CNJ/JL to enable expected wording
            ('GCE', marineActions, 'Marine'),
            ('SCE', marineActions, 'Marine'),
            ('HFE', marineActions, 'Marine'),

            ('GL.A', marineActions, 'Marine'),
            ('SR.A', marineActions, 'Marine'),
            ('HF.A', marineActions, 'Marine'),

            ('TRE', tropicalActions, 'Tropical'),
            ('HUE', tropicalActions, 'Tropical'),
##            ('GL.O', marineActions, 'Local'),
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

    # added by J. Lewitsky/NHC 04/17/11 to attempt to combine periods
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

        try:
            self._includeTropical = self._includeTropical == "Yes"
        except:
            self._includeTropical = False
        if self._includeTropical:
            #self._periodCombining = 0 # Changed back from 1 to 0 as PeriodCombining
            # with IncludeTropical was causing Period issues in forecast text (JL - 10/26/11)
            if self._productIssuance == "Morning with Pre-1st Period":
                self._productIssuance = "Morning"
            if self._productIssuance == "Afternoon with Pre-1st Period":
                self._productIssuance = "Afternoon"

        self._language = argDict["language"]
        return None

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

        if self._definition["pil"] == "OFFN04":
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
                print("editArea = ", editArea, type(editArea))
                print("areaLabel = ", areaLabel, type(areaLabel))
                print("argDict = ", argDict, type(argDict))
                fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
                fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
                # are we on the next to last area yet?
                # if so, add synopsis2
                if areasLeft == 1:
                    fcst += self._Text3()
                fraction = fractionOne
                areasLeft -= 1
            fcst = self._postProcessProduct(fcst, argDict)
            return fcst

        else:
            #Second synopsis isn't defined
            #use BASE OFF.py code
            for editArea, areaLabel in self._areaList:
                skipAreas = self._skipAreas(argDict)
                argDict["editArea"] = (editArea, areaLabel)
                if self.currentAreaContains(argDict, skipAreas):
                    continue
                self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
                fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
                fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
                fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
                fraction = fractionOne
            fcst = self._postProcessProduct(fcst, argDict)
            return fcst

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
            # added line below to handle ashfall advisory and associated special TAFB wording
            words = re.sub(r'\.\.\.ASHFALL ADVISORY.*', r'...ASHFALL ADVISORY...\n[VOLCANO NAME] VOLCANO AT POSITION [xx.xN xx.xW] IS CURRENTLY IN A STATE OF UNREST AND COULD ERUPT WITH LITTLE NOTICE. MARINERS TRAVELING IN THE VICINITY OF [VOLCANO NAME] ARE URGED TO EXERCISE CAUTION. IF MARINERS ENCOUNTER VOLCANIC ASH OR FLOATING VOLCANIC DEBRIS...YOU ARE ENCOURAGED TO REPORT THE OBSERVATION TO THE NATIONAL HURRICANE CENTER BY CALLING 305-229-4424.', words)
            words = re.sub(r'\.\.\.DENSE FOG ADVISORY.*', r'...DENSE FOG ADVISORY...', words)
            words = re.sub(r'\.\.\.DENSE SMOKE ADVISORY.*', r'...DENSE SMOKE ADVISORY...', words)
            words = re.sub(r'\.\.\.GALE CONDITIONS POSSIBLE IN EFFECT.*', r'...GALE CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.STORM CONDITIONS POSSIBLE IN EFFECT.*', r'...STORM CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.HURRICANE FORCE WINDS POSSIBLE IN EFFECT.*', r'...HURRICANE FORCE WINDS POSSIBLE...', words)
            words = re.sub(r'\.\.\.GALE WATCH.*', r'...GALE CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.STORM WATCH.*', r'...STORM CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.HURRICANE WATCH.*', r'...HURRICANE FORCE WINDS POSSIBLE...', words)
            #words = re.sub(r'TSTMS THROUGH THE NIGHT', r'TSTMS', words)
            #words = re.sub(r'TSTMS THROUGH THE DAY', r'TSTMS', words)
            #words = words.replace("SEAS 0 TO 1 FT.", "SEAS 1 FT OR LESS.")
            # Translate phrase
            # This is necessary so that word-wrap works correctly
            try:
                words = self.translateForecast(words, self._language)
            except:
                words = self.translateForecast(words, "english")
            rval = self.setWords(node, words)
        return rval

    #Modified from OFF base
    # Modified for Navtex
    def _postProcessArea(self, fcst, editArea, areaLabel, argDict):
        self.debug_print("Debug: _postProcessArea in NAVTEX_MIAMI_Overrides")

##        return fcst + "\n$$\n\n"
        # Don't include $$ at end of area forecast
        return fcst + "\n" + ""

    #For Navtex - return to OFF base
    def _postProcessProduct(self, fcst, argDict):
        """CWF_ER_Overrides version of CWF._postProcessProduct.

        Modified to add the capability of retaining forecast text from the
        previous CWF.
        """
        self.debug_print("\tCWF_ER_Overrides version of " +
                         "CWF._postProcessProduct")

        fcst = fcst.replace("%expireTime", self._expireTimeStr)
        #fcst = fcst.upper()

        self.debug_print("Debug: _postProcessProduct in NAVTEX_MIAMI_Overrides")
        self.setProgressPercentage(100)
        self.progressMessage(0, 100, self._displayName + " Complete")
        fcst = fcst.replace(".SYNOPSIS FOR PUERTO RICO AND THE U.S. VIRGIN ISLANDS WATERS...", ".SYNOPSIS...") #added 3/25/17 era
        fcst = fcst.replace("NATIONAL WEATHER SERVICE", "NWS")
        #fcst = string.replace(fcst, ", ", "...")
        fcst = fcst.replace("Today...", "TODAY...")
        fcst = fcst.replace("Tonight...", "TONIGHT...") #added ERA 6/18/17
        fcst = fcst.replace("Overnight...", "OVERNIGHT...")
        fcst = fcst.replace("This Afternoon...", "THIS AFTERNOON...")
        fcst = fcst.replace("TSTMs", "thunderstorms")
        fcst = fcst.replace("... ", "...")
        #fcst = string.replace(fcst, "FT... ", "FT...")
        fcst = fcst.replace("LESS THAN", "less than")
        #fcst = string.replace(fcst, "KT...SEAS", "KT. SEAS")
        #fcst = string.replace(fcst, "AFTERNOON...SEAS", "AFTERNOON. SEAS")
        #fcst = string.replace(fcst, "MIDNIGHT...SEAS", "MIDNIGHT. SEAS")
        #fcst = string.replace(fcst, "KT... ", "KT...")
        #fcst = string.replace(fcst, "LESS... BUILDING", "LESS...BUILDING")
        #fcst = string.replace(fcst, "morning, subsiding", "MORNING...SUBSIDING")
        #fcst = string.replace(fcst, ", ", "...")
        #fcst = string.replace(fcst, "...BECOMING  ", "...BECOMING ")
       # fcst = string.replace(fcst, "SHIFTING TO  ", "SHIFTING TO ")

        print("includeTropical is: ", self._includeTropical)
        #  Try to preserve text from previous CWF
        try:
            if self._includeTropical:
                print("includeTropical is yes - previous wording disabled")
                return fcst

            #  Get the module first
            import mergeProds

            #  If this option is desired (i.e. a non zero period was chosen)
            if isinstance(self._updatePeriodIndex, type(1)) and \
                    self._updatePeriodIndex >= 0:

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
#                     fcst=mergeProds.mergeProds()._mergeOFF2(fcst, oldCWF,
#                                                         self._updatePeriodIndex)

        #  Otherwise, if we cannot get the previous text for whatever reason
        except:
            print('Failed to parse previous OFF!  New text will be created ' + \
                  'for all periods.')

        return fcst
