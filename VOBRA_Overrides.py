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


#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class VOBRA_Overrides:
    def __init__(self):
        pass

    VariableList = []

    def __init__(self):
        TextRules.TextRules.__init__(self)
        SampleAnalysis.SampleAnalysis.__init__(self)

##################################################################################

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

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #Modified from OFF base

    def _Text1(self):
        self.debug_print("Debug: _Text1 in VOBRA_NT4_Overrides")

        #Determine which product
        if self._definition["pil"] == "OFFN21":
            return "Marine Weather HF Voice Broadcast for the Gulf of Mexico\n" + \
               "\n" + \
               "Seas given as significant wave height, which is the average\n" + \
               "height of the highest 1/3 of the waves. Individual waves may be\n" + \
               "more than twice the significant wave height.\n\n" + \
               "Synopsis for the Gulf of Mexico" + "\n\n"
        else:
            #OFFNT3
            return "Marine Weather HF Voice Broadcast for the Tropical N Atlantic\n" + \
               "from 07N to 22N between 55W and 64W, the SW N Atlantic S of\n" + \
               "31N W of 65W including Bahamas, and the Caribbean Sea.\n\n" + \
               "Seas given as significant wave height, which is the average\n" + \
               "height of the highest 1/3 of the waves. Individual waves may be\n" + \
               "more than twice the significant wave height.\n\n" + \
               "" + \
               "Synopsis for Caribbean Sea and Tropical N Atlantic from\n" + \
               "07N to 19N between 55W and 64W" + "\n\n"

    def _Text2(self):
        self.debug_print("Debug: _Text2 in NAVTEX_SANJUAN_Overrides")

        synopsis = ""

        #  Try to get Synopsis from previous CWF
        if self._definition["synopsisUGC"] == "AMZ001":

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

        else:

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

            #  Format expiration time for inclusion in synopsis header
            #expTime = time.strftime('%d%H%M', expTuple)

        return synopsis

    def _Text3(self):
        synopsis = ""
        if self._definition["pil"] == "OFFN20":
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
            synopsis = self.endline(synopsis, linelength=66, breakStr=" ")
            return "%s" %  "\n" + "Synopsis for the the SW N Atlantic including the Bahamas\n\n" + \
                    synopsis
        else:
            pass

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

    ########################################################################

    # SampleAnalysis overrides
    # SampleAnalysis overrides
    def moderated_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
        if self._includeTropical:
             # changed to increase formatter sensitivity for strong winds 9/7/11 CNJ/JL
            dict["Wind"] = (0, 0)
            #dict["Wind"] = (0, 15)
            dict["WindGust"] = (0, 15)
            # changed 9/7/11 CNJ/JL - wanted to remove zero pixels near coasts without WW3 coverage
            dict["WaveHeight"] = (10, 10)
            dict["Swell"] = (0, 15)
#        dict["Wind"] =  (0, 3)
        # added 9/7/11 CNJ/JL - these values are used by WFO Key West
        else:
            dict["WaveHeight"] = (10, 5) #added era 03/05/16 for testing
            #dict["WaveHeight"] = (10, 10)
        return dict

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] =  3 #changed from 2 to 3 ERA 10/15/14       # Changed to 1 (from 2) by JL/1/31/12 for testing
        dict["WindWaveHgt"] =  2
        dict["Wind"] = 10
        dict["WindGust"] = 120
        dict["Swell"] =  1
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
        dict["WaveHeight"] =  "seas 2 ft or less"
        dict["WindWaveHgt"] =  "seas 2 ft or less"
        dict["Wind"] =  "Variable winds less than 10 kt"
        dict["Swell"] =  ""
        return dict

    def null_phrase_dict(self, tree, node):
        # Phrase to use for null values in subPhrases other than the first
        # Can be an empty string
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "2 feet or less"
        dict["WindWaveHgt"] =  "2 feet or less"
        dict["Wind"] =  "variable winds less than 10 kt"
        dict["Wx"] =  ""
        dict["Swell"] =  "light"
        dict["hurricane force winds to"] =  "hurricane force winds to"
        dict["storm force winds to"] = "storm force winds to"
        dict["gales to"] =  "gales to"
        dict["up to"] =  "variable less than 10 kt"
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
        # during  cyclone situations allowing for far better wind speed
        # phrases.
        #-----------------------------------------------------------------------
        if self._includeTropical:
            # changed for VOBRA 9/7/11 CNJ/JL
            dict["Wind"] = {'default': 10,
                            (0.0, 4.0): 10,
                            (4.0, 33.0): 10,
                            (33.0, 52.0): 10,
                            (52.0, 200.0): 20,
                            }
            dict["WaveHeight"] = {(0, 3): 1,
                                  (3, 7): 2,
                                  (7, 10): 3,
                                  (10, 20): 5,
                                  (20, 200): 10,
                                  "default": 5,
                            }
##             dict["Wind"] = {'default': 5,
##                             (0.0, 4.0): 0,
##                             (4.0, 33.0): 5,
##                             (33.0, 52.0): 10,
##                             (52.0, 200.0): 20,
##                             }
        else:
            dict["Wind"] = 10
        dict["Swell"] = 5
        dict["Swell2"] = 5
        #dict["WaveHeight"] = 2
        dict["WaveHeight"] = {
            (1, 3): 0, #CHANGED BY ERA 09/30/14
            (3, 7): 2,
            (7, 10): 3,
            (10, 20): 5,
            (20, 200): 10,
            "default": 5,
            }
        dict["WindWaveHgt"] = 2
        return dict

      #COMMENTED BY ERA 09/30/14
#     def minimum_range_nlValue_dict(self, tree, node):
#         # This threshold is the "smallest" min/max difference allowed between values reported.
#         # For example, if threshold is set to 5 for "MaxT", and the min value is 45
#         # and the max value is 46, the range will be adjusted to at least a 5 degree
#         # range e.g. 43-48.  These are the values that are then submitted for phrasing
#         # such as:
#         dict = TextRules.TextRules.minimum_range_nlValue_dict(self, tree, node)
#         #   HIGHS IN THE MID 40S
#         if self._includeTropical:
#             dict["WaveHeight"] = {(0,3):1,
#                                   (3,7):2,
#                                   (7,10):3,
#                                   (10,20):5,
#                                   (20,200):10,
#                                   "default":5,
#                                   }
#         return dict

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
                                "Wind":  ", incresing to ",
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
        dict["shifting to the"] =  ", shifting "
        dict["becoming onshore"] =  " becoming onshore "
        dict["then"] =  {"Wx": ". ",
                         "Vector": ", becoming ",
                         "Scalar": ", becoming ",
                         "otherwise": ", becoming ",
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

    def rounding_method_dict(self, tree, node):
        # Special rounding methods
        #
        return {
            "Wind": self.marineRounding,
            }

    def vector_mag_difference_nlValue_dict(self, tree, node):
        # Replaces WIND_THRESHOLD
        # Magnitude difference.  If the difference between magnitudes
        # for sub-ranges is greater than or equal to this value,
        # the different magnitudes will be noted in the phrase.
        # Units can vary depending on the element and product
        return  {
            "Wind": 10,  #changed from 4 by ERA 07/20/15 to fix wind wording "10 to 15 becoming 10 to 20"
            "Swell": 1,  # ft
            "Swell2": 1,  # ft
            }

    def vector_dir_difference_dict(self, tree, node):
        # Replaces WIND_DIR_DIFFERENCE
        # Direction difference.  If the difference between directions
        # for sub-ranges is greater than or equal to this value,
        # the different directions will be noted in the phrase.
        # Units are degrees
        return {
            "Wind": 90, # degrees
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
            "WindGust": 18, # knots or mph depending on product
            "Period": 5, # seconds
            "WaveHeight": 2.5, #0, # in feet
            "WindWaveHgt": 5, # feet
            }

    ########################################################################
    # COMPONENT PRODUCT DEFINITIONS
    ########################################################################

    def OFFPeriod(self):
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
    # **May need to uncomment WindGust below for Tropical to work properly - JL/NHC 04/18/12**
                          ("WindGust", self.moderatedMax, [6]),
                          ("WaveHeight", self.moderatedMinMax, [6]), #activated era 3/5/16
                          #("WaveHeight", self.maximum, [6]), #added era 3/2/16

                         # ("WindWaveHgt", self.moderatedMinMax, [6]),
                         # ("Swell", self.vectorModeratedMinMax, [6]),
                         # ("Swell2", self.vectorModeratedMinMax, [6]),
                         # ("Period", self.moderatedMinMax, [6]),
                         # ("Period2", self.moderatedMinMax, [6]),
                         # ("Wx", self.rankedWx, [6]),
                         # ("T", self.minMax),
                         # ("PoP", self._PoP_analysisMethod("OFFPeriod"), [6]),
                         # ("PoP", self.binnedPercent, [6]),
                        ]

            phraseList = [
                           # WINDS
                           (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
#                            (self.marine_wind_phrase,self._windLocalEffects_list()),
                           # Alternative:
#                           (self.marine_wind_phrase, self._windLocalEffects_list()),
#                           self.marine_wind_phrase,
                           #self.gust_phrase,
                           # WAVES
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
                           (self.wave_phrase, self._WaveHeightLocalEffects_list),

                           #self.weather_phrase,
                           self.visibility_phrase,
                           ]

#            # CJ Added
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
                ("Wind", ["le_VOBRA03_60nm_of_veracruz",
                          "le_VOBRA03_main",
                          "le_VOBRA07_colombian_coast",
                          "le_VOBRA07_main",
                          "le_VOBRA09_gulf_of_venezuela",
                          "le_VOBRA09_main",
                          "le_VOBRA13_W_of_70W",
                          "le_VOBRA13_main",
                          "le_VOBRA15_W_of_70W",
                          "le_VOBRA15_main",
                          "le_VOBRA06_S_of_18N",
                          "le_VOBRA06_main",
                            ]),
                ("WaveHeight", ["le_VOBRA03_60nm_of_veracruz",
                                "le_VOBRA03_main",
                                "le_VOBRA07_colombian_coast",
                                "le_VOBRA07_main",
                                "le_VOBRA09_gulf_of_venezuela",
                                "le_VOBRA09_main",
                                "le_VOBRA13_W_of_70W",
                                "le_VOBRA13_main",
                                "le_VOBRA15_W_of_70W",
                                "le_VOBRA15_main",
                                "le_VOBRA06_S_of_18N",
                                "le_VOBRA06_main",
                                ]),
                    ]
                }

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
                      ],
                 "phraseList": [
                               # WIND
                               #self.marine_wind_phrase,
                               (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
                               # WAVEHEIGHT
                               #self.wave_withPeriods_phrase,
                               # Alternative:
                               #self.wave_phrase,
                               (self.wave_phrase, self._WaveHeightLocalEffects_list),
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

    def _WaveHeightLocalEffects_list(self, tree, node):
        leArea1 = self.LocalEffectArea("le_VOBRA07_main", "elsewhere")
        leArea2 = self.LocalEffectArea("le_VOBRA07_colombian_coast", "within 90 nm of coast of Colombia")
        leArea3 = self.LocalEffectArea("le_VOBRA13_main", "elsewhere")
        leArea4 = self.LocalEffectArea("le_VOBRA13_W_of_70W", "W of 70W")
        leArea5 = self.LocalEffectArea("le_VOBRA15_main", "elsewhere")
        leArea6 = self.LocalEffectArea("le_VOBRA15_W_of_70W", "W of 70W")
        leArea7 = self.LocalEffectArea("le_VOBRA06_main", "elsewhere")
        leArea8 = self.LocalEffectArea("le_VOBRA06_S_of_18N", "S of 18N")
        leArea11 = self.LocalEffectArea("le_VOBRA09_main", "elsewhere")
        leArea12 = self.LocalEffectArea("le_VOBRA09_gulf_of_venezuela", "Gulf of Venezuela")

        leArea9 = self.LocalEffectArea("le_VOBRA03_main", "elsewhere")
        leArea10 = self.LocalEffectArea("le_VOBRA03_60nm_of_veracruz", "within 60 nm of coast of Veracruz")

        return [self.LocalEffect([leArea2, leArea1], 2, ", and "),
                self.LocalEffect([leArea4, leArea3], 2, ", and "),
                self.LocalEffect([leArea6, leArea5], 2, ", and "),
                self.LocalEffect([leArea8, leArea7], 2, ", and "),
                self.LocalEffect([leArea10, leArea9], 2, ", and "),
                self.LocalEffect([leArea12, leArea11], 2, ", and "),
                ]

    def _windLocalEffects_list(self):
        leArea1 = self.LocalEffectArea("le_VOBRA07_main", "elsewhere")
        leArea2 = self.LocalEffectArea("le_VOBRA07_colombian_coast", "within 90 nm of coast of Colombia")
        leArea3 = self.LocalEffectArea("le_VOBRA13_main", "elsewhere")
        leArea4 = self.LocalEffectArea("le_VOBRA13_W_of_70W", "W of 70W")
        leArea5 = self.LocalEffectArea("le_VOBRA15_main", "elsewhere")
        leArea6 = self.LocalEffectArea("le_VOBRA15_W_of_70W", "W of 70W")
        leArea7 = self.LocalEffectArea("le_VOBRA06_main", "elsewhere")
        leArea8 = self.LocalEffectArea("le_VOBRA06_S_of_18N", "S of 18N")
        leArea11 = self.LocalEffectArea("le_VOBRA09_main", "elsewhere")
        leArea12 = self.LocalEffectArea("le_VOBRA09_gulf_of_venezuela", "Gulf of Venezuela")

        leArea9 = self.LocalEffectArea("le_VOBRA03_main", "elsewhere")
        leArea10 = self.LocalEffectArea("le_VOBRA03_60nm_of_veracruz", "within 60 nm of coast of Veracruz")

        return [self.LocalEffect([leArea2, leArea1], 2, ", and "),
                self.LocalEffect([leArea4, leArea3], 2, ", and "),
                self.LocalEffect([leArea6, leArea5], 2, ", and "),
                self.LocalEffect([leArea8, leArea7], 2, ", and "),
                self.LocalEffect([leArea10, leArea9], 2, ", and "),
                self.LocalEffect([leArea12, leArea11], 2, ", and "),
                ]

    ########################################################################
    # PRODUCT-SPECIFIC METHODS
    ########################################################################
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
                 ".Today...", "early", "in the afternoon",
                 1, narrativeDefAM),
                ("1130 AM", "issuanceHour", self.NIGHT(), 16,
                 ".THIS AFTERNOON...", "early", "late",
                 1, narrativeDefAM),
                ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                 ".Tonight...", "late", "early",
                 1, narrativeDefPM),
                ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                 ".Overnight...", "late", "early",
                 1, narrativeDefPM)
                ]
        else:
            return [
                ("430 AM", self.DAY(), self.NIGHT(), 16,
                 ".Today...", "early", "in the afternoon",
                 1, narrativeDefAM),
                ("1030 AM", self.DAY(), self.NIGHT(), 16,
                 ".Today...", "early", "late",
                 1, narrativeDefAM),
                ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                 ".Tonight...", "late", "early",
                 1, narrativeDefPM),
                ("1030 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                 ".Tonight...", "late", "early",
                 1, narrativeDefPM),
                ]

#added on 1/24/16 to get rid of morning/afternoon wording...ERA

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





    def lateDay_descriptor(self, statDict, argDict, timeRange):
       # If time range is in the first period, return period1 descriptor for
       #  late day -- default 3pm-6pm
       if self._issuanceInfo.period1TimeRange().contains(timeRange):
           return self._issuanceInfo.period1LateDayPhrase()
       else:
           return "LATE" #changed from ""...ERA 1/24/16

    def lateNight_descriptor(self, statDict, argDict, timeRange):
       # If time range is in the first period, return period1 descriptor for
       #  late night -- default 3am-6am
       if self._issuanceInfo.period1TimeRange().contains(timeRange):
           return self._issuanceInfo.period1LateNightPhrase()
       else:
           return "late"

    def _preProcessProduct(self, fcst, argDict):
        if self._areaName:
             productName = self._productName.strip() + " FOR " + \
                           self._areaName.strip()
        else:
             productName = self._productName.strip()

        issuedByString = self.getIssuedByString()

        fcst =  fcst + self._wmoID + " " + self._fullStationID + " " + \
               self._ddhhmmTime + "\n" + self._pil + "\n\n" +\
               productName + "\n" +\
               "NWS National Hurricane Center " + self._wfoCityState + \
               "\n" + issuedByString + self._timeLabel + "\n\n"
        fcst += self._Text1()
        try:
            text2 = self._Text2(argDict["host"])
        except:
            text2 = self._Text2()
        fcst += text2
        return fcst

    #### CHECK THIS SECTION FOR 'SAN JUAN ATLANTIC WATERS' DOUBLE HEADING. REFERENCED
    #### IN THE AREADICTIONARY TOO
    #modifed for Navtex
    def _preProcessArea(self, fcst, editArea, areaLabel, argDict):
        self.debug_print("Debug: _preProcessArea in OFF_NAV_ONA_Overrides")

        # This is the header for an edit area combination
        print("Generating Forecast for", areaLabel)
##        areaHeader = self.makeAreaHeader(
##            argDict, areaLabel, self._issueTime, self._expireTime,
##            self._areaDictionary, self._defaultEditAreas)

        # get the hazards text
        self._hazards = argDict['hazards']
        self._combinations = argDict["combinations"]

        headlines = self.generateProduct("Hazards", argDict, area = editArea,
                                         areaLabel=areaLabel,
                                         timeRange = self._timeRange)
        # remove any double spaces
        headlines = re.sub(r'  ', r' ', headlines)

        # Navtex only needs the area description as the header
        if argDict["combinations"] is not None:
            areaList = self.getCurrentAreaNames(argDict, areaLabel)
        else:
            for editArea, label in self._defaultEditAreas:
                if label == areaLabel:
                    areaList = [editArea]
        print(areaList)
        # Access the UGC information for the area(s) if available
        accessor = ModuleAccessor.ModuleAccessor()
        areaDict = accessor.variable(self._areaDictionary, "AreaDictionary")
        for areaName in areaList:
                print(areaName + "\n")
                entry = areaDict[areaName]
        areaHeader = entry['ugcName'] + "\n"
        fcst += "\n" + areaHeader + "\n"
        fcst = re.sub(r'OFFSHORE LEEWARD ISLANDS AND ADJACENT ATLC WATERS FROM 15N TO 19N W OF 55W',
                      "OFFSHORE LEEWARD ISLANDS AND ADJACENT ATLC WATERS FROM 15N TO\n + \ 19N W OF 55W", fcst)
        fcst = re.sub(r'OFFSHORE WINDWARD ISLANDS AND ADJACENT ATLC WATERS FROM 07N TO 15N W OF 55W',
                      "OFFSHORE WINDWARD ISLANDS AND ADJACENT ATLC WATERS FROM 07N TO\n + \ 15N W OF 55W", fcst)

        #add headlines to forecast
        fcst += headlines
        fcst = re.sub(r'CONDITIONS POSSIBLE IN EFFECT', "CONDITIONS POSSIBLE", fcst)
        fcst = re.sub(r'WINDS POSSIBLE IN EFFECT', "WINDS POSSIBLE", fcst)
        fcst = re.sub(r'WARNING IN EFFECT', "WARNING", fcst)
        return fcst

    # Returns a list of the Hazards allowed for this product in VTEC format.
    # These are sorted in priority order - most important first.

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

            ('HF.A', marineActions, 'Marine'),
            ('SR.A', marineActions, 'Marine'),
            ('GL.A', marineActions, 'Marine'),

            ('TRE', tropicalActions, 'Tropical'),
            ('HUE', tropicalActions, 'Tropical'),
##            ('GL.O', marineActions, 'Local'),
            ('MF.Y', allActions, 'Fog'),                            # DENSE FOG ADVISORY
            ('MS.Y', allActions, 'Smoke'),                          # DENSE SMOKE ADVISORY
##            ('UP.Y', allActions, 'IceAccr'),                        # HEAVY FREEZING SPRAY ADVISORY
            ('MH.Y', allActions, 'Ashfall')                        # VOLCANIC ASHFALL ADVISORY
            ]

#####################################################################
#####################################################################

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

    def periodCombining_elementList(self, tree, node):
        # Weather Elements to determine whether to combine periods
        #return ["Sky", "Wind", "Wx", "PoP", "MaxT", "MinT"]
        # Marine
        return ["WaveHeight", "Wind"]
        # Diurnal Sky Wx pattern
        #return ["DiurnalSkyWx"]

    def periodCombining_startHour(self, tree, node):
        # Hour after which periods may be combined
        return 12

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
            words = re.sub(r'\.\.\.GALE CONDITIONS POSSIBLE.*', r'...GALE CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.STORM CONDITIONS POSSIBLE THROUGH.*', r'...STORM CONDITIONS POSSIBLE...', words)
            words = re.sub(r'\.\.\.HURRICANE FORCE WINDS POSSIBLE THROUGH.*', r'...HURRICANE FORCE WINDS POSSIBLE...', words)
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

        if self._definition["pil"] == "OFFN20":
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
                # are we on the next to last area yet?
                # if so, add synopsis2
                if areasLeft == 6:
                    fcst += self._Text3()
                fraction = fractionOne
                areasLeft -= 1
            fcst = self._postProcessProduct(fcst, argDict)
            fcst = self.endline(fcst, linelength=self._lineLength)
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
            fcst = self.endline(fcst, linelength=self._lineLength)
            return fcst

    # Modified for Navtex
    def _postProcessArea(self, fcst, editArea, areaLabel, argDict):
##        return fcst + "\n$$\n\n"
        # Don't include $$ at end of area forecast
        return fcst + ""

    def _postProcessProduct(self, fcst, argDict):
        """CWF_ER_Overrides version of CWF._postProcessProduct.

        Modified to add the capability of retaining forecast text from the
        previous CWF.
        """
        self.debug_print("\tCWF_ER_Overrides version of " +
                         "CWF._postProcessProduct")

        fcst = fcst.replace("%expireTime", self._expireTimeStr)
        #fcst = fcst.upper()

        self.setProgressPercentage(100)
        self.progressMessage(0, 100, self._displayName + " Complete")
        fcst = re.sub(r'  ', " ", fcst)
        fcst = fcst.replace(" + \ 19N W of 55W", "19N W of 55W")
        fcst = fcst.replace(" + \ 15N W of 55W", "15N W of 55W")
        fcst = fcst.replace("W of 70W... ", "W of 70W,")
        fcst = fcst.replace("...within ", "...Within ") #added on 7/21/17 to test le wording...era
        #fcst = string.replace(fcst, "AFTER MIDNIGHT","LATE")
        #fcst = string.replace(fcst, " AFTER ","")
        #fcst = string.replace(fcst, "MIDNIGHT","LATE")
        #fcst = string.replace(fcst, "MORNING... ","...")
        #fcst = string.replace(fcst, "MORNING... ","MORNING...")
        fcst = fcst.replace("Elsewhere, ", "Elsewhere, ")
        fcst = fcst.replace("KT, ", "KT,")
        fcst = re.sub(r' AFTER\nLATE. SEAS', r' LATE.\nSEAS', fcst)
        fcst = fcst.replace("LESS, BUILDING", "LESS, BUILDING")
        #fcst = string.replace(fcst, ", ", "...")
        fcst = fcst.replace("Today...", "TODAY...")
        fcst = fcst.replace("Tonight...", "TONIGHT...") #added ERA 6/18/17
        fcst = fcst.replace("Overnight...", "OVERNIGHT...")
        fcst = fcst.replace("This Afternoon...", "THIS AFTERNOON...")
        fcst = fcst.replace("... ", "...")
        #fcst = string.replace(fcst, ", BECOMING", ", BECOMING")
        #fcst = string.replace(fcst, ", ", "...")
        fcst = self.endline(fcst, linelength=self._lineLength)

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
