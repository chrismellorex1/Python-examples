##
# This software was developed and / or modified by Raytheon Company,
# pursuant to Contract DG133W-05-CQ-1067 with the US Government.
# 
# U.S. EXPORT CONTROLLED TECHNICAL DATA
# This software product contains export-restricted data whose
# export/transfer/disclosure is restricted by U.S. law. Dissemination
# to non-U.S. persons whether in the United States or abroad requires
# an export license or other authorization.
# 
# Contractor Name:        Raytheon Company
# Contractor Address:     6825 Pine Street, Suite 340
#                         Mail Stop B8
#                         Omaha, NE 68106
#                         402.291.0100
# 
# See the AWIPS II Master Rights File ("Master Rights File.pdf") for
# further licensing information.
##
# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# OFF_ONA_Overrides.TextUtility
#
#  This file is used for WFO specific overrides of the OFF
#  formatter.  
#
#
# Methods:
#   Overrides:
#       _Text1(self)
#       _Text2()
#       OFFPeriod(self)
#       OFFPeriodMid(self)
#       _issuance_list(self, argDict)
#
#   Additions:
#       _WaveHeightLocalEffects_list(self, tree, node)
#       _windLocalEffects_list(self)
#       includeOnlyPhrases_list
#       pws_words
#
# History
# 2011-07-26: CJuckins/OPC  Adapted OFFPeriod from NHC's scripts; made it call
#                           "marine_wind_withGusts_phrase" for tropical wording.
#                           Inserted "addTropical" definition.
#                           Commented out includeOnlyPhrases_list and
#                           pws_words as they were not in use at NHC.
# 2011-09-09 F&K.Achorn/OPC Modified OFFPeriod and issuance_list methods to respond
#                to a "No" self._includeTropical. The value "No" is 
#                considered True by python, so it was always including tropicals
#                Also uncommented out the OFFPeriodMid method, as it no longer
#                interfears with tropicals.
# F.Achorn/K.Achorn/OPC    11/07/2011    Migrated from WNOR
# ---------------------------------------------------------------------

import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis

import UserInfo

import sys
import numpy as np

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class SWELL_Overrides:
    def __init__(self):
        pass

    VariableList = [
        #(copy.deepcopy(CWF.TextProduct.VariableList)),
        (("Include Tropical?", "includeTropical") , "No", "radio", ["Yes", "No"]),
        #(("Forecaster Name", "forecasterName") , "99", "radio",
        # ["NELSON", "STRIPLING", "SCHAUER", "CHRISTENSEN",
        #  "LEWITSKY", "AL", "GR", "AGUIRRE", "DGS",
        #  "MUNDELL", "COBB", "LANDSEA", "CAB", "PAW",
        #  "FORMOSA", "HUFFMAN", "MT", "NAR"]),
        (("Period Combining?", "pdCombo"), "No", "radio", ["Yes", "No"]),
        ((("Keep Previous Text After Period (Selecting zero\nwill keep all old text but will refresh headlines)",
                      "updatePeriodIndex"), "No old text",
                      "radio", ["No old text", 0, 1, 2, 3, 4, 5, 6, 7, 8]))   
                    ]

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #----- WFO ONA OFF Overrides -----

    # It is helpful to put a debug statement at the beginning of each)
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
        self.debug_print("Debug: _Text2 in SWELL_NT3_Overrides")
        
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
            entire_product = str.strip(self.getPreviousProduct(productID))
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
            if areasLeft == 26:
            #if areasLeft == 9:
                fcst += self._Text3()
            fraction = fractionOne
            areasLeft = areasLeft - 1
            # next four print( lines added for debugging of shapefile problem - 05/05/11)
            print("##########################################################")
            print("EDIT AREA IS:")
            print( areaLabel)
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

    # SampleAnalysis overrides
    def moderated_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
        if self._includeTropical:
            dict["Wind"] = (0, 0) #JL changed this to 0, 0 because the Headlines were not matching 
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
#        dict["WaveHeight"] = (5, 5)
        return dict

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] =  3  #changed from 2 to 3 ERA 10/15/14... # Changed to 1 (from 2) by JL/1/31/12 for testing
        #dict["WindWaveHgt"] =  2 
        dict["Wind"] = 10 # Changed to 5 (from 10) by JL/1/31/12 for testing...changed to 6 for variable winds wording ERA 3/16/19 
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
   #                             "WindWaveHgt": ", building to ",
                         }
             
        dict["easing to"] =  {
                                "Wind": ", diminishing to ",
                                "Swell": ", subsiding to ",
                                "Swell2": ", subsiding to ",
                                "WaveHeight": ", subsiding to ",
      #                          "WindWaveHgt": ", subsiding to ",
                         }                 
        dict["backing"] =  {
                                "Wind": ", shifting to ",
                                "Swell": ", becoming ",
                                "Swell2": ", becoming ",
                                "WaveHeight": ", becoming ",
       #                         "WindWaveHgt": ", becoming ",
                         }
                 
        dict["veering"] =  {
                                "Wind": ", shifting to ",
                                "Swell": ", becoming ",
                                "Swell2": ", becoming ",
                                "WaveHeight": ", becoming ", 
          #                      "WindWaveHgt": ", becoming ",
                         }
 
        dict["becoming"] =  ", becoming "
        dict["increasing to"] =  {
                                "Wind":  ", increasing to ",
                                "Swell": ", building to ",
                                "Swell2": ", building to ",
                                "WaveHeight": ", building to ",
           #                     "WindWaveHgt": ", building to ",
                             }
        dict["decreasing to"] =  {
                                "Wind":  ", diminishing to ",
                                "Swell": ", subsiding to ",
                                "Swell2": ", subsiding to ",
                                "WaveHeight": ", subsiding to ",
           #                     "WindWaveHgt": ", subsiding to ",
                             }  
        dict["shifting to the"] =  {
                                  "Wind":  ", shifting ",
                                  "Swell": ", becoming ",
                                  "Swell2": ", becoming ",
                                  "WaveHeight": ", becoming ", 
             #                     "WindWavHgt": ", becoming ",
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
            (0, 25):5,
            (25, 50):10,
            (50, 200):25,
            "default":10,
            }
            dict["Swell"] = {
            (0, 3):1,
            (3, 7):2,
            (7, 10):3,
            (10, 20):5,
            (20, 200):10,
            "default":5,
            }
            dict["Swell2"] = {
            (0, 3):1,
            (3, 7):2,
            (7, 10):3,
            (10, 20):5,
            (20, 200):10,
            "default":5,
            }
            
            #added by ERA 09/29/14 (old TAFB)
            dict["WaveHeight"] = {
             (1, 3):0, # changed from 0 to 1 JL/1/31/12
             (3, 7):2, 
             (7, 10):3,
             (10, 20):5,
             (20, 200):10,
             "default":5,
             }
            #commented by ERA 09/29/14 (OPC)
#             dict["WaveHeight"] = {
#             (0, 1):1,
#             (1, 4):2,
#             (4, 6):3,
#             (6, 8):4,
#             (8, 10):5,
#             (10, 12):6,
#             (12, 14):7,
#             (14, 16):8,
#             (16, 18):9,
#             (18, 20):10,
#             (20, 200):15,
#             "default":5,
#             }
      #  dict["WindWaveHgt"] = 2

# commented out TAFB's old def and replaced with OPC's above (except kept TAFB's wind def) JL/8/23/2014            
#         
#         dict["Swell"] = 5  
#         dict["Swell2"] = 5  
        #dict["WaveHeight"] = 2
        #dict["WindWaveHgt"] = 2
        return dict
                
    def vector_mag_difference_nlValue_dict(self, tree, node):
        # Replaces WIND_THRESHOLD
        # Magnitude difference.  If the difference between magnitudes
        # for sub-ranges is greater than or equal to this value,
        # the different magnitudes will be noted in the phrase.
        # Units can vary depending on the element and product
        return  {
#            "Wind": 9, 
            "Wind": {
                (0, 12):10,
                (12, 25):10, #CHANGED FROM 5 ERA 12/1/15
                (25, 45):10,
                (45, 70):15,
                (70, 200):20,
                "default":5,
            },  
#            "Swell": 5,  # ft
            "Swell" : {
                (0, 3):1,
                (3, 7):2,
                (7, 10):3,
                (10, 20):5,
                (20, 200):10,
                "default":5,
                }, # feet
            "Swell2": {
                (0, 3):1,
                (3, 7):2,
                (7, 10):3,
                (10, 20):5,
                (20, 200):10,
                "default":5,
                }, # feet
 #           "Swell2": 5,  # ft
            "otherwise": 5,
            }

    def vector_dir_difference_dict(self, tree, node):
        # Replaces WIND_DIR_DIFFERENCE
        # Direction difference.  If the difference between directions
        # for sub-ranges is greater than or equal to this value,
        # the different directions will be noted in the phrase.
        # Units are degrees
        return {
            "Wind": 60, # degrees (Was 90 for TAFB) #CHANGED FROM 45 TO 60 AFTER 3HRLY GRIDS IMPLEMENTATION-ERA
            "Swell":60, # degrees
            "Swell2":60, # degrees
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
                 (0, 2):2, #CHANGED FROM 1 ERA 09/30/14, 12/02/15
                 (2, 4):2,
                 (4, 7):3,
                 (7, 11):4,
                 (11, 16):5,
                 (16, 22):6,
                 (22, 29):7,
                 (29, 37):8,
                 (37, 46):9,
                 (46, 56):10,
                 (56, 67):11,
                 (67, 79):12,
                 (79, 92):13,
                 (92, 106):14,
                 (106, 200):15,                
                 "default":5,
                 }, #0, # in feet
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
   
    def waveht_scalar_value(self, tree, node, elementName, elementName1):
        # calculating the scalar value for changes based on wave height
        wave = tree.stats.get("WaveHeight", node.getTimeRange(), node.getAreaLabel(),
                                             mergeMethod="Max")
#        print( wave, "Wave!")
        if wave is None:
            return 10
        if wave <= 6:
            rtnval = 6
        else:
            val = wave * .25
            rtnval = int(val+0.5)
            
            
            
   
    ## This entry below is likely the cause for Period Combining issues at periods 6-8 - JL/NHC 02/12/12
    def splitDay24HourLabel_flag(self,tree,node):
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
           #list.append (("*", "T", "*", "*", "tstms"))
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

######### NEW OFFSHORE LOCAL EFFECT AREAS 7/30/22 ERA

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
                          ("WaveHeight", self.maximum, [6]), #6/25/22 ERA 
                          #("WaveHeight", self.moderatedMax, [6]), #changed 1/24/2018 CJ/JL/ERA
                          #("WaveHeight", self.moderatedMinMax, [6]),
                       #   ("WindWaveHgt", self.moderatedMinMax, [6]),
                         
                         # changed analysis period to 3 hours to handle swell transitions during a forecast period- 1/24/2018 CNJ/JL/ERA
                          ("Swell", self.vectorModeratedMinMax, [6]),
                          ("Swell2", self.vectorModeratedMinMax, [6]),
                          #("Swell", self.vectorMax, [6]), 
                          #("Swell2", self.vectorMax, [6]),
                     #     ("Period", self.mode, [12]),
                         # ("Period2", self.moderatedMinMax, [6]),
                          ("Wx", self.rankedWx, [12]),

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
#                           (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
                            # J.Lewitsky/NHC 04/15/11 uncommented line below to include Local Effects
                           (self.marine_wind_withGusts_phrase,self._windLocalEffects_list()),
                           #self.marine_wind_withGusts_phrase, 
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
                           
                           # WEATHER
#                           self.weather_phrase,

#                           self.weather_phrase,
                           # uncommented below to include Local Effects (JL - 12/12/11)
                           self.wave_withPeriods_phrase,
                           #self.wave_phrase,
                      #     self.period_phrase, 
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
                ("Wind", ["le_gmz040_n_of_27n",
                          "le_gmz040_s_of_27n",
                          "le_gmz041_e_of_92p5w",
                          "le_gmz041_w_of_92p5w",
                          "le_gmz045_n_of_24n",
                          "le_gmz045_s_of_24n",
                          "le_gmz046_n_of_24n",
                          "le_gmz046_s_of_24n",
                          "le_gmz047_n_of_24n",
                          "le_gmz047_s_of_24n",
                          "le_gmz048_elsewhere",
                          "le_gmz048_s_of_21n_w_of_95w",
                          "le_gmz049_n_of_20n",
                          "le_gmz049_s_of_20n",
                          "le_gmz050_e_of_90w",
                          "le_gmz050_w_of_90w",
                          "le_gmz056_e_of_89w",
                          "le_gmz056_w_of_89w",
                          "le_gmz057_e_of_85w",
                          "le_gmz057_w_of_85w",
                          "le_gmz058_e_of_96w",
                          "le_gmz058_w_of_96w",
                          
                          "le_amz040_n_of_20n",
                          "le_amz040_s_of_20n",
                          "le_amz041_e_of_81w",
                          "le_amz041_w_of_81w",
                          "le_amz042_e_of_82w",
                          "le_amz042_w_of_82w",
                          "le_amz043_e_of_78w",
                          "le_amz043_w_of_78w",
                          "le_amz044_elsewhere",
                          "le_amz044_gulf_of_gonave",
                          "le_amz045_elsewhere",
                          "le_amz045_s_of_17n_w_of_86w",
                          "le_amz046_e_of_82w",
                          "le_amz046_w_of_82w",
                          "le_amz047_n_of_17n",
                          "le_amz047_s_of_17n",
                          "le_amz048_n_of_17n",
                          "le_amz048_s_of_17n",
                          "le_amz049_e_of_70w",
                          "le_amz049_w_of_70w",
                          "le_amz050_e_of_66w",
                          "le_amz050_w_of_66w",
                          "le_amz051_atlantic",
                          "le_amz051_caribbean",
                          "le_amz052_n_of_17n",
                          "le_amz052_s_of_17n",
                          "le_amz053_open_waters",
                          "le_amz053_reefs",
                          "le_amz054_e_of_78w",
                          "le_amz054_w_of_78w",
                          "le_amz055_n_of_13n",
                          "le_amz055_s_of_13n",
                          "le_amz056_n_of_13n",
                          "le_amz056_s_of_13n",
                          "le_amz057_n_of_13n",
                          "le_amz057_s_of_13n",
                          "le_amz058_atlantic",
                          "le_amz058_caribbean",
                          "le_amz059_n_of_13n",
                          "le_amz059_s_of_13n",
                          "le_amz060_n_of_10n",
                          "le_amz060_s_of_10n",
                          "le_amz061_n_of_10n",
                          "le_amz061_s_of_10n",
                          "le_amz062_n_of_09n",
                          "le_amz062_s_of_09n",
                          "le_amz063_e_of_79w",
                          "le_amz063_w_of_79w",
                          "le_amz064_e_of_75p5w",
                          "le_amz064_w_of_75p5w",
                          "le_amz065_e_of_72w",
                          "le_amz065_w_of_72w",
                          "le_amz066_e_of_67p5w",
                          "le_amz066_w_of_67p5w",
                          "le_amz067_e_of_62p5w",
                          "le_amz067_w_of_62p5w",
                          "le_amz068_e_of_57p5w",
                          "le_amz068_w_of_57p5w",
                          "le_amz069_e_of_78w",
                          "le_amz069_w_of_78w",
                          "le_amz070_e_of_75p5w",
                          "le_amz070_w_of_75p5w",
                          "le_amz071_e_of_72w",
                          "le_amz071_w_of_72w",
                          "le_amz072_e_of_67p5w",
                          "le_amz072_w_of_67p5w",
                          "le_amz073_e_of_62p5w",
                          "le_amz073_w_of_62p5w",
                          "le_amz074_e_of_57p5w",
                          "le_amz074_w_of_57p5w",
                          "le_amz075_elsewhere",
                          "le_amz075_open_atlc_waters",
                          "le_amz076_e_of_73w",
                          "le_amz076_w_of_73w",
                          "le_amz077_e_of_67p5w",
                          "le_amz077_w_of_67p5w",
                          "le_amz078_e_of_62p5w",
                          "le_amz078_w_of_62p5w",
                          "le_amz079_e_of_57p5w",
                          "le_amz079_w_of_57p5w",
                          "le_amz081_n_of_23n",
                          "le_amz081_s_of_23n",
                          "le_amz082_n_of_23n",
                          "le_amz082_s_of_23n",
                          "le_amz083_n_of_23n",
                          "le_amz083_s_of_23n",
                          "le_amz084_n_of_23n",
                          "le_amz084_s_of_23n",
                          "le_amz085_n_of_21n",
                          "le_amz085_s_of_21n",
                          "le_amz086_n_of_21n",
                          "le_amz086_s_of_21n",
                          "le_amz087_n_of_20p5n",
                          "le_amz087_s_of_20p5n",
                          "le_amz088_n_of_20p5n",
                          "le_amz088_s_of_20p5n"
                          
                            ]),
                              
                ("WaveHeight", ["le_gmz040_n_of_27n",
                          "le_gmz040_s_of_27n",
                          "le_gmz041_e_of_92p5w",
                          "le_gmz041_w_of_92p5w",
                          "le_gmz045_n_of_24n",
                          "le_gmz045_s_of_24n",
                          "le_gmz046_n_of_24n",
                          "le_gmz046_s_of_24n",
                          "le_gmz047_n_of_24n",
                          "le_gmz047_s_of_24n",
                          "le_gmz048_elsewhere",
                          "le_gmz048_s_of_21n_w_of_95w",
                          "le_gmz049_n_of_20n",
                          "le_gmz049_s_of_20n",
                          "le_gmz050_e_of_90w",
                          "le_gmz050_w_of_90w",
                          "le_gmz056_e_of_89w",
                          "le_gmz056_w_of_89w",
                          "le_gmz057_e_of_85w",
                          "le_gmz057_w_of_85w",
                          "le_gmz058_e_of_96w",
                          "le_gmz058_w_of_96w",                    
                    
                    
                          "le_amz040_n_of_20n",
                          "le_amz040_s_of_20n",
                          "le_amz041_e_of_81w",
                          "le_amz041_w_of_81w",
                          "le_amz042_e_of_82w",
                          "le_amz042_w_of_82w",                    
                          "le_amz043_w_of_78w",
                          "le_amz044_elsewhere",
                          "le_amz044_gulf_of_gonave",
                          "le_amz045_elsewhere",
                          "le_amz045_s_of_17n_w_of_86w",
                          "le_amz046_e_of_82w",
                          "le_amz046_w_of_82w",
                          "le_amz047_n_of_17n",
                          "le_amz047_s_of_17n",
                          "le_amz048_n_of_17n",
                          "le_amz048_s_of_17n",
                          "le_amz049_e_of_70w",
                          "le_amz049_w_of_70w",
                          "le_amz050_e_of_66w",
                          "le_amz050_w_of_66w",
                          "le_amz051_atlantic",
                          "le_amz051_caribbean",
                          "le_amz052_n_of_17n",
                          "le_amz052_s_of_17n",
                          "le_amz053_open_waters",
                          "le_amz053_reefs",
                          "le_amz054_e_of_78w",
                          "le_amz054_w_of_78w",
                          "le_amz055_n_of_13n",
                          "le_amz055_s_of_13n",
                          "le_amz056_n_of_13n",
                          "le_amz056_s_of_13n",
                          "le_amz057_n_of_13n",
                          "le_amz057_s_of_13n",
                          "le_amz058_atlantic",
                          "le_amz058_caribbean",
                          "le_amz059_n_of_13n",
                          "le_amz059_s_of_13n",
                          "le_amz060_n_of_10n",
                          "le_amz060_s_of_10n",
                          "le_amz061_n_of_10n",
                          "le_amz061_s_of_10n",
                          "le_amz062_n_of_09n",
                          "le_amz062_s_of_09n",
                          "le_amz063_e_of_79w",
                          "le_amz063_w_of_79w",
                          "le_amz064_e_of_75p5w",
                          "le_amz064_w_of_75p5w",
                          "le_amz065_e_of_72w",
                          "le_amz065_w_of_72w",
                          "le_amz066_e_of_67p5w",
                          "le_amz066_w_of_67p5w",
                          "le_amz067_e_of_62p5w",
                          "le_amz067_w_of_62p5w",
                          "le_amz068_e_of_57p5w",
                          "le_amz068_w_of_57p5w",
                          "le_amz069_e_of_78w",
                          "le_amz069_w_of_78w",
                          "le_amz070_e_of_75p5w",
                          "le_amz070_w_of_75p5w",
                          "le_amz071_e_of_72w",
                          "le_amz071_w_of_72w",
                          "le_amz072_e_of_67p5w",
                          "le_amz072_w_of_67p5w",
                          "le_amz073_e_of_62p5w",
                          "le_amz073_w_of_62p5w",
                          "le_amz074_e_of_57p5w",
                          "le_amz074_w_of_57p5w",
                          "le_amz075_elsewhere",
                          "le_amz075_open_atlc_waters",
                          "le_amz076_e_of_73w",
                          "le_amz076_w_of_73w",
                          "le_amz077_e_of_67p5w",
                          "le_amz077_w_of_67p5w",
                          "le_amz078_e_of_62p5w",
                          "le_amz078_w_of_62p5w",
                          "le_amz079_e_of_57p5w",
                          "le_amz079_w_of_57p5w",
                          "le_amz081_n_of_23n",
                          "le_amz081_s_of_23n",
                          "le_amz082_n_of_23n",
                          "le_amz082_s_of_23n",
                          "le_amz083_n_of_23n",
                          "le_amz083_s_of_23n",
                          "le_amz084_n_of_23n",
                          "le_amz084_s_of_23n",
                          "le_amz085_n_of_21n",
                          "le_amz085_s_of_21n",
                          "le_amz086_n_of_21n",
                          "le_amz086_s_of_21n",
                          "le_amz087_n_of_20p5n",
                          "le_amz087_s_of_20p5n",
                          "le_amz088_n_of_20p5n",
                          "le_amz088_s_of_20p5n"
                        
                            ]),
                    ]
                }                

    #Addition - taken from MFL CWF
    def _WaveHeightLocalEffects_list(self, tree, node):
        leArea1 = self.LocalEffectArea("le_gmz040_n_of_27n", "N of 27N")
        leArea2 = self.LocalEffectArea("le_gmz040_s_of_27n", "S of 27N")
        leArea3 = self.LocalEffectArea("le_gmz041_e_of_92p5w", "E of 92W")
        leArea4 = self.LocalEffectArea("le_gmz041_w_of_92p5w", "W of 92W")
        leArea5 = self.LocalEffectArea("le_gmz045_n_of_24n", "N of 24N")
        leArea6 = self.LocalEffectArea("le_gmz045_s_of_24n", "S of 24N")
        leArea7 = self.LocalEffectArea("le_gmz046_n_of_24n", "N of 24N")
        leArea8 = self.LocalEffectArea("le_gmz046_s_of_24n", "S of 24N")
        leArea9 = self.LocalEffectArea("le_gmz047_n_of_24n", "N of 24N")
        leArea10 = self.LocalEffectArea("le_gmz047_s_of_24n", "S of 24N")
        leArea11 = self.LocalEffectArea("le_gmz048_elsewhere", "elsewhere")
        leArea12 = self.LocalEffectArea("le_gmz048_s_of_21n_w_of_95w", "S of 21N W of 95W")
        leArea13 = self.LocalEffectArea("le_gmz049_n_of_20n", "N of 20N")
        leArea14 = self.LocalEffectArea("le_gmz049_s_of_20n", "S of 20N")
        leArea15 = self.LocalEffectArea("le_gmz050_e_of_90w", "E of 90W")
        leArea16 = self.LocalEffectArea("le_gmz050_w_of_90w", "W of 90W")
        leArea17 = self.LocalEffectArea("le_gmz056_e_of_89w", "E of 89W")
        leArea18 = self.LocalEffectArea("le_gmz056_w_of_89w", "W of 89W")
        leArea19 = self.LocalEffectArea("le_gmz057_e_of_85w", "E of 85W")   
        leArea20 = self.LocalEffectArea("le_gmz057_w_of_85w", "W of 85W")
        leArea21 = self.LocalEffectArea("le_gmz058_e_of_96w", "E of 96W")   
        leArea22 = self.LocalEffectArea("le_gmz058_w_of_96w", "W of 96W")
        
        leArea23 = self.LocalEffectArea("le_amz040_n_of_20n", "N of 20N")
        leArea24 = self.LocalEffectArea("le_amz040_s_of_20n", "S of 20N")
        leArea25 = self.LocalEffectArea("le_amz041_e_of_81w", "E of 81W")
        leArea26 = self.LocalEffectArea("le_amz041_w_of_81w", "W of 81W")
        leArea27 = self.LocalEffectArea("le_amz042_e_of_82w", "E of 82W")
        leArea28 = self.LocalEffectArea("le_amz042_w_of_82w", "W of 82W")
        leArea29 = self.LocalEffectArea("le_amz043_e_of_78w", "E of 78W")
        leArea30 = self.LocalEffectArea("le_amz043_w_of_78w", "W of 78W")
        leArea31 = self.LocalEffectArea("le_amz044_elsewhere", "elsewhere")
        leArea32 = self.LocalEffectArea("le_amz044_gulf_of_gonave", "in the Gulf of Gonave")
        leArea33 = self.LocalEffectArea("le_amz045_elsewhere", "elsewhere")
        leArea34 = self.LocalEffectArea("le_amz045_s_of_17n_w_of_86w", "S of 17N W of 86W")
        leArea35 = self.LocalEffectArea("le_amz046_e_of_82w", "E of 82W")
        leArea36 = self.LocalEffectArea("le_amz046_w_of_82w", "W of 82W")
        leArea37 = self.LocalEffectArea("le_amz047_n_of_17n", "N of 17N")
        leArea38 = self.LocalEffectArea("le_amz047_s_of_17n", "S of 17N")
        leArea39 = self.LocalEffectArea("le_amz048_n_of_17n", "N of 17N")
        leArea40 = self.LocalEffectArea("le_amz048_s_of_17n", "S of 17N")
        leArea41 = self.LocalEffectArea("le_amz049_e_of_70w", "E of 70W")
        leArea42 = self.LocalEffectArea("le_amz049_w_of_70w", "W of 70W")
        leArea43 = self.LocalEffectArea("le_amz050_e_of_66w", "E of 66W")
        leArea44 = self.LocalEffectArea("le_amz050_w_of_66w", "W of 66W")
        leArea45 = self.LocalEffectArea("le_amz051_atlantic", "in the Atlantic")
        leArea46 = self.LocalEffectArea("le_amz051_caribbean", "in the Caribbean")
        leArea47 = self.LocalEffectArea("le_amz052_n_of_17n", "N of 17N")
        leArea48 = self.LocalEffectArea("le_amz052_s_of_17n", "S of 17N")
        leArea49 = self.LocalEffectArea("le_amz053_open_waters", "in the open waters")
        leArea50 = self.LocalEffectArea("le_amz053_reefs", "in the reefs")
        leArea51 = self.LocalEffectArea("le_amz054_e_of_78w", "E of 78W")
        leArea52 = self.LocalEffectArea("le_amz054_w_of_78w", "W of 78W")
        leArea53 = self.LocalEffectArea("le_amz055_n_of_13n", "N of 13N")
        leArea54 = self.LocalEffectArea("le_amz055_s_of_13n", "S of 13N")
        leArea55 = self.LocalEffectArea("le_amz056_n_of_13n", "N of 13N")
        leArea56 = self.LocalEffectArea("le_amz056_s_of_13n", "S of 13N")
        leArea57 = self.LocalEffectArea("le_amz057_n_of_13n", "N of 13N")
        leArea58 = self.LocalEffectArea("le_amz057_s_of_13n", "S of 13N")
        leArea59 = self.LocalEffectArea("le_amz058_atlantic", "in the Atlantic")
        leArea60 = self.LocalEffectArea("le_amz058_caribbean", "in the Caribbean")
        leArea61 = self.LocalEffectArea("le_amz059_n_of_13n", "N of 13N")
        leArea62 = self.LocalEffectArea("le_amz059_s_of_13n", "S of 13N")
        leArea63 = self.LocalEffectArea("le_amz060_n_of_10n", "N of 10N")
        leArea64 = self.LocalEffectArea("le_amz060_s_of_10n", "S of 10N")
        leArea65 = self.LocalEffectArea("le_amz061_n_of_10n", "N of 10N")
        leArea66 = self.LocalEffectArea("le_amz061_s_of_10n", "S of 10N")
        leArea67 = self.LocalEffectArea("le_amz062_n_of_09n", "N of 09N")
        leArea68 = self.LocalEffectArea("le_amz062_s_of_09n", "S of 09N")
        leArea69 = self.LocalEffectArea("le_amz063_e_of_79w", "E of 79W")
        leArea70 = self.LocalEffectArea("le_amz063_w_of_79w", "W of 79W")
        leArea71 = self.LocalEffectArea("le_amz064_e_of_75p5w", "E of 75W")
        leArea72 = self.LocalEffectArea("le_amz064_w_of_75p5w", "W of 75W")
        leArea73 = self.LocalEffectArea("le_amz065_e_of_72w", "E of 72W")
        leArea74 = self.LocalEffectArea("le_amz065_w_of_72w", "W of 72W")
        leArea75 = self.LocalEffectArea("le_amz066_e_of_67p5w", "E of 67W")
        leArea76 = self.LocalEffectArea("le_amz066_w_of_67p5w", "W of 67W")
        leArea77 = self.LocalEffectArea("le_amz067_e_of_62p5w", "E of 62W")
        leArea78 = self.LocalEffectArea("le_amz067_w_of_62p5w", "W of 62W")
        leArea79 = self.LocalEffectArea("le_amz068_e_of_57p5w", "E of 57W")
        leArea80 = self.LocalEffectArea("le_amz068_w_of_57p5w", "W of 57W")
        leArea81 = self.LocalEffectArea("le_amz069_e_of_78w", "E of 78W")
        leArea82 = self.LocalEffectArea("le_amz069_w_of_78w", "W of 78W")
        leArea83 = self.LocalEffectArea("le_amz070_e_of_75p5w", "E of 75W")
        leArea84 = self.LocalEffectArea("le_amz070_w_of_75p5w", "W of 75W")
        leArea85 = self.LocalEffectArea("le_amz071_e_of_72w", "E of 72W")
        leArea86 = self.LocalEffectArea("le_amz071_w_of_72w", "W of 72W")
        leArea87 = self.LocalEffectArea("le_amz072_e_of_67p5w", "E of 67W")
        leArea88 = self.LocalEffectArea("le_amz072_w_of_67p5w", "W of 67W")
        leArea89 = self.LocalEffectArea("le_amz073_e_of_62p5w", "E of 62W")
        leArea90 = self.LocalEffectArea("le_amz073_w_of_62p5w", "W of 62W")
        leArea91 = self.LocalEffectArea("le_amz074_e_of_57p5w", "E of 57W")
        leArea92 = self.LocalEffectArea("le_amz074_w_of_57p5w", "W of 57W")
        leArea93 = self.LocalEffectArea("le_amz075_elsewhere", "elsewhere")
        leArea94 = self.LocalEffectArea("le_amz075_open_atlc_waters", "in the open Atlantic waters")
        leArea95 = self.LocalEffectArea("le_amz076_e_of_73w", "E of 73W")
        leArea96 = self.LocalEffectArea("le_amz076_w_of_73w", "W of 73W")
        leArea97 = self.LocalEffectArea("le_amz077_e_of_67p5w", "E of 67W")
        leArea98 = self.LocalEffectArea("le_amz077_w_of_67p5w", "W of 67W")
        leArea99 = self.LocalEffectArea("le_amz078_e_of_62p5w", "E of 62W")
        leArea100 = self.LocalEffectArea("le_amz078_w_of_62p5w", "W of 62W")
        leArea101 = self.LocalEffectArea("le_amz079_e_of_57p5w", "E of 57W")
        leArea102 = self.LocalEffectArea("le_amz079_w_of_57p5w", "W of 57W")
        leArea103 = self.LocalEffectArea("le_amz081_n_of_23n", "N of 23N")
        leArea104 = self.LocalEffectArea("le_amz081_s_of_23n", "S of 23N")
        leArea105 = self.LocalEffectArea("le_amz082_n_of_23n", "N of 23N")
        leArea106 = self.LocalEffectArea("le_amz082_s_of_23n", "S of 23N")
        leArea107 = self.LocalEffectArea("le_amz083_n_of_23n", "N of 23N")
        leArea108 = self.LocalEffectArea("le_amz083_s_of_23n", "S of 23N")
        leArea109 = self.LocalEffectArea("le_amz084_n_of_23n", "N of 23N")
        leArea110 = self.LocalEffectArea("le_amz084_s_of_23n", "S of 23N")
        leArea111 = self.LocalEffectArea("le_amz085_n_of_21n", "N of 21N")
        leArea112 = self.LocalEffectArea("le_amz085_s_of_21n", "S of 21N")
        leArea113 = self.LocalEffectArea("le_amz086_n_of_21n", "N of 21N")
        leArea114 = self.LocalEffectArea("le_amz086_s_of_21n", "S of 21N")
        leArea115 = self.LocalEffectArea("le_amz087_n_of_20p5n", "N of 20N")
        leArea116 = self.LocalEffectArea("le_amz087_s_of_20p5n", "S of 20N")
        leArea117 = self.LocalEffectArea("le_amz088_n_of_20p5n", "N of 20N")
        leArea118 = self.LocalEffectArea("le_amz088_s_of_20p5n", "S of 20N")
       
          
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
                self.LocalEffect([leArea14, leArea13], 2, ", and "),                
                self.LocalEffect([leArea16, leArea15], 2, ", and "),
                self.LocalEffect([leArea18, leArea17], 2, ", and "),
                self.LocalEffect([leArea20, leArea19], 2, ", and "),
                self.LocalEffect([leArea22, leArea21], 2, ", and "),
                
                self.LocalEffect([leArea24, leArea23], 2, ", and "),
                self.LocalEffect([leArea26, leArea25], 2, ", and "),
                self.LocalEffect([leArea28, leArea27], 1, ", and "),
                self.LocalEffect([leArea30, leArea29], 2, ", and "),
                self.LocalEffect([leArea32, leArea31], 2, ", and "),
                self.LocalEffect([leArea34, leArea33], 2, ", and "),
                self.LocalEffect([leArea36, leArea35], 0, ", and "), #6/25/22
                self.LocalEffect([leArea38, leArea37], 2, ", and "),
                self.LocalEffect([leArea40, leArea39], 2, ", and "),
                self.LocalEffect([leArea42, leArea41], 2, ", and "),
                self.LocalEffect([leArea44, leArea43], 1, ", and "), #changed from 2 to get "seas less than 2 ft" wording ERA 6/26/16 
                self.LocalEffect([leArea46, leArea45], 2, ", and "),
                self.LocalEffect([leArea48, leArea47], 2, ", and "),
                self.LocalEffect([leArea50, leArea49], 2, ", and "),
                self.LocalEffect([leArea52, leArea51], 2, ", and "),
                self.LocalEffect([leArea54, leArea53], 2, ", and "),
                self.LocalEffect([leArea56, leArea55], 2, ", and "),
                self.LocalEffect([leArea58, leArea57], 2, ", and "),
                self.LocalEffect([leArea60, leArea59], 2, ", and "),
                self.LocalEffect([leArea62, leArea61], 2, ", and "),
                self.LocalEffect([leArea64, leArea63], 2, ", and "),
                self.LocalEffect([leArea66, leArea65], 2, ", and "),
                self.LocalEffect([leArea68, leArea67], 2, ", and "),
                self.LocalEffect([leArea70, leArea69], 2, ", and "),
                self.LocalEffect([leArea72, leArea71], 2, ", and "),
                self.LocalEffect([leArea74, leArea73], 2, ", and "),
                self.LocalEffect([leArea76, leArea75], 2, ", and "),
                self.LocalEffect([leArea78, leArea77], 2, ", and "),
                self.LocalEffect([leArea80, leArea79], 2, ", and "),
                self.LocalEffect([leArea82, leArea81], 2, ", and "),
                self.LocalEffect([leArea84, leArea83], 2, ", and "),
                self.LocalEffect([leArea86, leArea85], 2, ", and "),
                self.LocalEffect([leArea88, leArea87], 2, ", and "),
                self.LocalEffect([leArea90, leArea89], 2, ", and "),
                self.LocalEffect([leArea92, leArea91], 2, ", and "),
                self.LocalEffect([leArea94, leArea93], 2, ", and "),
                self.LocalEffect([leArea96, leArea95], 2, ", and "),
                self.LocalEffect([leArea98, leArea97], 2, ", and "),
                self.LocalEffect([leArea100, leArea99], 2, ", and "),
                self.LocalEffect([leArea102, leArea101], 2, ", and "),
                self.LocalEffect([leArea104, leArea103], 2, ", and "),
                self.LocalEffect([leArea106, leArea105], 2, ", and "),
                self.LocalEffect([leArea108, leArea107], 2, ", and "),
                self.LocalEffect([leArea110, leArea109], 2, ", and "),
                self.LocalEffect([leArea112, leArea111], 2, ", and "),
                self.LocalEffect([leArea114, leArea113], 2, ", and "),
                self.LocalEffect([leArea116, leArea115], 2, ", and "),
                self.LocalEffect([leArea118, leArea117], 2, ", and "),
                
                
                ]

    def _windLocalEffects_list(self):
        leArea1 = self.LocalEffectArea("le_gmz040_n_of_27n", "N of 27N")
        leArea2 = self.LocalEffectArea("le_gmz040_s_of_27n", "S of 27N")
        leArea3 = self.LocalEffectArea("le_gmz041_e_of_92p5w", "E of 92W")
        leArea4 = self.LocalEffectArea("le_gmz041_w_of_92p5w", "W of 92W")
        leArea5 = self.LocalEffectArea("le_gmz045_n_of_24n", "N of 24N")
        leArea6 = self.LocalEffectArea("le_gmz045_s_of_24n", "S of 24N")
        leArea7 = self.LocalEffectArea("le_gmz046_n_of_24n", "N of 24N")
        leArea8 = self.LocalEffectArea("le_gmz046_s_of_24n", "S of 24N")
        leArea9 = self.LocalEffectArea("le_gmz047_n_of_24n", "N of 24N")
        leArea10 = self.LocalEffectArea("le_gmz047_s_of_24n", "S of 24N")
        leArea11 = self.LocalEffectArea("le_gmz048_elsewhere", "elsewhere")
        leArea12 = self.LocalEffectArea("le_gmz048_s_of_21n_w_of_95w", "S of 21N W of 95W")
        leArea13 = self.LocalEffectArea("le_gmz049_n_of_20n", "N of 20N")
        leArea14 = self.LocalEffectArea("le_gmz049_s_of_20n", "S of 20N")
        leArea15 = self.LocalEffectArea("le_gmz050_e_of_90w", "E of 90W")
        leArea16 = self.LocalEffectArea("le_gmz050_w_of_90w", "W of 90W")
        leArea17 = self.LocalEffectArea("le_gmz056_e_of_89w", "E of 89W")
        leArea18 = self.LocalEffectArea("le_gmz056_w_of_89w", "W of 89W")
        leArea19 = self.LocalEffectArea("le_gmz057_e_of_85w", "E of 85W")   
        leArea20 = self.LocalEffectArea("le_gmz057_w_of_85w", "W of 85W")
        leArea21 = self.LocalEffectArea("le_gmz058_e_of_96w", "E of 96W")   
        leArea22 = self.LocalEffectArea("le_gmz058_w_of_96w", "W of 96W")
        
        leArea23 = self.LocalEffectArea("le_amz040_n_of_20n", "N of 20N")
        leArea24 = self.LocalEffectArea("le_amz040_s_of_20n", "S of 20N")
        leArea25 = self.LocalEffectArea("le_amz041_e_of_81w", "E of 81W")
        leArea26 = self.LocalEffectArea("le_amz041_w_of_81w", "W of 81W")
        leArea27 = self.LocalEffectArea("le_amz042_e_of_82w", "E of 82W")
        leArea28 = self.LocalEffectArea("le_amz042_w_of_82w", "W of 82W")
        leArea29 = self.LocalEffectArea("le_amz043_e_of_78w", "E of 78W")
        leArea30 = self.LocalEffectArea("le_amz043_w_of_78w", "W of 78W")
        leArea31 = self.LocalEffectArea("le_amz044_elsewhere", "elsewhere")
        leArea32 = self.LocalEffectArea("le_amz044_gulf_of_gonave", "in the Gulf of Gonave")
        leArea33 = self.LocalEffectArea("le_amz045_elsewhere", "elsewhere")
        leArea34 = self.LocalEffectArea("le_amz045_s_of_17n_w_of_86w", "S of 17N W of 86W")
        leArea35 = self.LocalEffectArea("le_amz046_e_of_82w", "E of 82W")
        leArea36 = self.LocalEffectArea("le_amz046_w_of_82w", "W of 82W")
        leArea37 = self.LocalEffectArea("le_amz047_n_of_17n", "N of 17N")
        leArea38 = self.LocalEffectArea("le_amz047_s_of_17n", "S of 17N")
        leArea39 = self.LocalEffectArea("le_amz048_n_of_17n", "N of 17N")
        leArea40 = self.LocalEffectArea("le_amz048_s_of_17n", "S of 17N")
        leArea41 = self.LocalEffectArea("le_amz049_e_of_70w", "E of 70W")
        leArea42 = self.LocalEffectArea("le_amz049_w_of_70w", "W of 70W")
        leArea43 = self.LocalEffectArea("le_amz050_e_of_66w", "E of 66W")
        leArea44 = self.LocalEffectArea("le_amz050_w_of_66w", "W of 66W")
        leArea45 = self.LocalEffectArea("le_amz051_atlantic", "in the Atlantic")
        leArea46 = self.LocalEffectArea("le_amz051_caribbean", "in the Caribbean")
        leArea47 = self.LocalEffectArea("le_amz052_n_of_17n", "N of 17N")
        leArea48 = self.LocalEffectArea("le_amz052_s_of_17n", "S of 17N")
        leArea49 = self.LocalEffectArea("le_amz053_open_waters", "in the open waters")
        leArea50 = self.LocalEffectArea("le_amz053_reefs", "in the reefs")
        leArea51 = self.LocalEffectArea("le_amz054_e_of_78w", "E of 78W")
        leArea52 = self.LocalEffectArea("le_amz054_w_of_78w", "W of 78W")
        leArea53 = self.LocalEffectArea("le_amz055_n_of_13n", "N of 13N")
        leArea54 = self.LocalEffectArea("le_amz055_s_of_13n", "S of 13N")
        leArea55 = self.LocalEffectArea("le_amz056_n_of_13n", "N of 13N")
        leArea56 = self.LocalEffectArea("le_amz056_s_of_13n", "S of 13N")
        leArea57 = self.LocalEffectArea("le_amz057_n_of_13n", "N of 13N")
        leArea58 = self.LocalEffectArea("le_amz057_s_of_13n", "S of 13N")
        leArea59 = self.LocalEffectArea("le_amz058_atlantic", "in the Atlantic")
        leArea60 = self.LocalEffectArea("le_amz058_caribbean", "in the Caribbean")
        leArea61 = self.LocalEffectArea("le_amz059_n_of_13n", "N of 13N")
        leArea62 = self.LocalEffectArea("le_amz059_s_of_13n", "S of 13N")
        leArea63 = self.LocalEffectArea("le_amz060_n_of_10n", "N of 10N")
        leArea64 = self.LocalEffectArea("le_amz060_s_of_10n", "S of 10N")
        leArea65 = self.LocalEffectArea("le_amz061_n_of_10n", "N of 10N")
        leArea66 = self.LocalEffectArea("le_amz061_s_of_10n", "S of 10N")
        leArea67 = self.LocalEffectArea("le_amz062_n_of_09n", "N of 09N")
        leArea68 = self.LocalEffectArea("le_amz062_s_of_09n", "S of 09N")
        leArea69 = self.LocalEffectArea("le_amz063_e_of_79w", "E of 79W")
        leArea70 = self.LocalEffectArea("le_amz063_w_of_79w", "W of 79W")
        leArea71 = self.LocalEffectArea("le_amz064_e_of_75p5w", "E of 75W")
        leArea72 = self.LocalEffectArea("le_amz064_w_of_75p5w", "W of 75W")
        leArea73 = self.LocalEffectArea("le_amz065_e_of_72w", "E of 72W")
        leArea74 = self.LocalEffectArea("le_amz065_w_of_72w", "W of 72W")
        leArea75 = self.LocalEffectArea("le_amz066_e_of_67p5w", "E of 67W")
        leArea76 = self.LocalEffectArea("le_amz066_w_of_67p5w", "W of 67W")
        leArea77 = self.LocalEffectArea("le_amz067_e_of_62p5w", "E of 62W")
        leArea78 = self.LocalEffectArea("le_amz067_w_of_62p5w", "W of 62W")
        leArea79 = self.LocalEffectArea("le_amz068_e_of_57p5w", "E of 57W")
        leArea80 = self.LocalEffectArea("le_amz068_w_of_57p5w", "W of 57W")
        leArea81 = self.LocalEffectArea("le_amz069_e_of_78w", "E of 78W")
        leArea82 = self.LocalEffectArea("le_amz069_w_of_78w", "W of 78W")
        leArea83 = self.LocalEffectArea("le_amz070_e_of_75p5w", "E of 75W")
        leArea84 = self.LocalEffectArea("le_amz070_w_of_75p5w", "W of 75W")
        leArea85 = self.LocalEffectArea("le_amz071_e_of_72w", "E of 72W")
        leArea86 = self.LocalEffectArea("le_amz071_w_of_72w", "W of 72W")
        leArea87 = self.LocalEffectArea("le_amz072_e_of_67p5w", "E of 67W")
        leArea88 = self.LocalEffectArea("le_amz072_w_of_67p5w", "W of 67W")
        leArea89 = self.LocalEffectArea("le_amz073_e_of_62p5w", "E of 62W")
        leArea90 = self.LocalEffectArea("le_amz073_w_of_62p5w", "W of 62W")
        leArea91 = self.LocalEffectArea("le_amz074_e_of_57p5w", "E of 57W")
        leArea92 = self.LocalEffectArea("le_amz074_w_of_57p5w", "W of 57W")
        leArea93 = self.LocalEffectArea("le_amz075_elsewhere", "elsewhere")
        leArea94 = self.LocalEffectArea("le_amz075_open_atlc_waters", "in the open Atlantic waters")
        leArea95 = self.LocalEffectArea("le_amz076_e_of_73w", "E of 73W")
        leArea96 = self.LocalEffectArea("le_amz076_w_of_73w", "W of 73W")
        leArea97 = self.LocalEffectArea("le_amz077_e_of_67p5w", "E of 67W")
        leArea98 = self.LocalEffectArea("le_amz077_w_of_67p5w", "W of 67W")
        leArea99 = self.LocalEffectArea("le_amz078_e_of_62p5w", "E of 62W")
        leArea100 = self.LocalEffectArea("le_amz078_w_of_62p5w", "W of 62W")
        leArea101 = self.LocalEffectArea("le_amz079_e_of_57p5w", "E of 57W")
        leArea102 = self.LocalEffectArea("le_amz079_w_of_57p5w", "W of 57W")
        leArea103 = self.LocalEffectArea("le_amz081_n_of_23n", "N of 23N")
        leArea104 = self.LocalEffectArea("le_amz081_s_of_23n", "S of 23N")
        leArea105 = self.LocalEffectArea("le_amz082_n_of_23n", "N of 23N")
        leArea106 = self.LocalEffectArea("le_amz082_s_of_23n", "S of 23N")
        leArea107 = self.LocalEffectArea("le_amz083_n_of_23n", "N of 23N")
        leArea108 = self.LocalEffectArea("le_amz083_s_of_23n", "S of 23N")
        leArea109 = self.LocalEffectArea("le_amz084_n_of_23n", "N of 23N")
        leArea110 = self.LocalEffectArea("le_amz084_s_of_23n", "S of 23N")
        leArea111 = self.LocalEffectArea("le_amz085_n_of_21n", "N of 21N")
        leArea112 = self.LocalEffectArea("le_amz085_s_of_21n", "S of 21N")
        leArea113 = self.LocalEffectArea("le_amz086_n_of_21n", "N of 21N")
        leArea114 = self.LocalEffectArea("le_amz086_s_of_21n", "S of 21N")
        leArea115 = self.LocalEffectArea("le_amz087_n_of_20p5n", "N of 20N")
        leArea116 = self.LocalEffectArea("le_amz087_s_of_20p5n", "S of 20N")
        leArea117 = self.LocalEffectArea("le_amz088_n_of_20p5n", "N of 20N")
        leArea118 = self.LocalEffectArea("le_amz088_s_of_20p5n", "S of 20N")
     
                 
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
                self.LocalEffect([leArea14, leArea13], 5, ", and "),                
                self.LocalEffect([leArea16, leArea15], 5, ", and "),
                self.LocalEffect([leArea18, leArea17], 5, ", and "),
                self.LocalEffect([leArea20, leArea19], 5, ", and "),
                self.LocalEffect([leArea22, leArea21], 5, ", and "),
                
                self.LocalEffect([leArea24, leArea23], 2, ", and "),
                self.LocalEffect([leArea26, leArea25], 2, ", and "),
                self.LocalEffect([leArea28, leArea27], 1, ", and "),
                self.LocalEffect([leArea30, leArea29], 2, ", and "),
                self.LocalEffect([leArea32, leArea31], 2, ", and "),
                self.LocalEffect([leArea34, leArea33], 2, ", and "),
                self.LocalEffect([leArea36, leArea35], 0, ", and "), #6/25/22
                self.LocalEffect([leArea38, leArea37], 2, ", and "),
                self.LocalEffect([leArea40, leArea39], 2, ", and "),
                self.LocalEffect([leArea42, leArea41], 2, ", and "),
                self.LocalEffect([leArea44, leArea43], 1, ", and "), #changed from 2 to get "seas less than 2 ft" wording ERA 6/26/16 
                self.LocalEffect([leArea46, leArea45], 2, ", and "),
                self.LocalEffect([leArea48, leArea47], 2, ", and "),
                self.LocalEffect([leArea50, leArea49], 2, ", and "),
                self.LocalEffect([leArea52, leArea51], 2, ", and "),
                self.LocalEffect([leArea54, leArea53], 2, ", and "),
                self.LocalEffect([leArea56, leArea55], 2, ", and "),
                self.LocalEffect([leArea58, leArea57], 2, ", and "),
                self.LocalEffect([leArea60, leArea59], 2, ", and "),
                self.LocalEffect([leArea62, leArea61], 2, ", and "),
                self.LocalEffect([leArea64, leArea63], 2, ", and "),
                self.LocalEffect([leArea66, leArea65], 2, ", and "),
                self.LocalEffect([leArea68, leArea67], 2, ", and "),
                self.LocalEffect([leArea70, leArea69], 2, ", and "),
                self.LocalEffect([leArea72, leArea71], 2, ", and "),
                self.LocalEffect([leArea74, leArea73], 2, ", and "),
                self.LocalEffect([leArea76, leArea75], 2, ", and "),
                self.LocalEffect([leArea78, leArea77], 2, ", and "),
                self.LocalEffect([leArea80, leArea79], 2, ", and "),
                self.LocalEffect([leArea82, leArea81], 2, ", and "),
                self.LocalEffect([leArea84, leArea83], 2, ", and "),
                self.LocalEffect([leArea86, leArea85], 2, ", and "),
                self.LocalEffect([leArea88, leArea87], 2, ", and "),
                self.LocalEffect([leArea90, leArea89], 2, ", and "),
                self.LocalEffect([leArea92, leArea91], 2, ", and "),
                self.LocalEffect([leArea94, leArea93], 2, ", and "),
                self.LocalEffect([leArea96, leArea95], 2, ", and "),
                self.LocalEffect([leArea98, leArea97], 2, ", and "),
                self.LocalEffect([leArea100, leArea99], 2, ", and "),
                self.LocalEffect([leArea102, leArea101], 2, ", and "),
                self.LocalEffect([leArea104, leArea103], 2, ", and "),
                self.LocalEffect([leArea106, leArea105], 2, ", and "),
                self.LocalEffect([leArea108, leArea107], 2, ", and "),
                self.LocalEffect([leArea110, leArea109], 2, ", and "),
                self.LocalEffect([leArea112, leArea111], 2, ", and "),
                self.LocalEffect([leArea114, leArea113], 2, ", and "),
                self.LocalEffect([leArea116, leArea115], 2, ", and "),
                self.LocalEffect([leArea118, leArea117], 2, ", and "),
                
                ]

    def OFFExtended(self):
#         return { "type": "component",
#                  "methodList": [
#                           self.consolidateSubPhrases,
#                           self.assemblePhrases,
#                           self.wordWrap,          
#                           ],
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
                          ("WindGust", self.moderatedMinMax, [6]),
                          ("WaveHeight", self.maximum,  [6]),
                           # changed analysis period to 3 hours to match short-term period - 1/24/2018 CNJ/JL/ERA
                          #("WaveHeight", self.moderatedMinMax, [6]), #changed from 3 and moderatedMax era 2/26/18
                          #("WaveHeight", self.moderatedMinMax, [6]),
                          
                          # changed analysis period to 3 hours to handle swell transitions during a forecast period
                          #("Swell", self.vectorMax, [6]), #era 2/26/18 
                          #("Swell2", self.vectorMax, [6]), #era 2/26/18 
                          #("Swell", self.vectorMax, [6]),
                          #("Swell2", self.vectorMax, [6]),
                          # ("WindWaveHgt", self.moderatedMinMax, [24]),
                          #("Wx", self.rankedWx),
                          #("T", self.minMax),  # needed for weather_phrase
                          #("PoP", self._PoP_analysisMethod("OFFExtended")),
                          #("PoP", self.binnedPercent),
                          ("Swell", self.vectorModeratedMinMax, [12]),
                          ("Swell2", self.vectorModeratedMinMax, [12]),
                          
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
                   #       ("Period", self.mode, [12]),
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
                      ]
            phraseList = [ 
                               # WIND
                               (self.marine_wind_phrase, self._windLocalEffects_list()),
                               # WAVEHEIGHT
                               # Commented out until fully developed seas wording fixed 9/7/11 CNJ/JL
                               #self.wave_withPeriods_phrase,
                               # Alternative:
                               (self.wave_withPeriods_phrase, self._WaveHeightLocalEffects_list),
                      #         self.period_phrase,
                               # SWELLS AND PERIODS
                               #self.swell_withPeriods_phrase,
                               # Alternative:
                               #self.swell_phrase,
                               #self.period_phrase,
                               # WEATHER
                               #self.weather_phrase,
                               #self.visibility_phrase,
                               ]
                
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
                ("Wind", ["le_gmz040_n_of_27n",
                          "le_gmz040_s_of_27n",
                          "le_gmz041_e_of_92p5w",
                          "le_gmz041_w_of_92p5w",
                          "le_gmz045_n_of_24n",
                          "le_gmz045_s_of_24n",
                          "le_gmz046_n_of_24n",
                          "le_gmz046_s_of_24n",
                          "le_gmz047_n_of_24n",
                          "le_gmz047_s_of_24n",
                          "le_gmz048_elsewhere",
                          "le_gmz048_s_of_21n_w_of_95w",
                          "le_gmz049_n_of_20n",
                          "le_gmz049_s_of_20n",
                          "le_gmz050_e_of_90w",
                          "le_gmz050_w_of_90w",
                          "le_gmz056_e_of_89w",
                          "le_gmz056_w_of_89w",
                          "le_gmz057_e_of_85w",
                          "le_gmz057_w_of_85w",
                          "le_gmz058_e_of_96w",
                          "le_gmz058_w_of_96w",
                          
                          "le_amz040_n_of_20n",
                          "le_amz040_s_of_20n",
                          "le_amz041_e_of_81w",
                          "le_amz041_w_of_81w",
                          "le_amz042_e_of_82w",
                          "le_amz042_w_of_82w",
                          "le_amz043_e_of_78w",
                          "le_amz043_w_of_78w",
                          "le_amz044_elsewhere",
                          "le_amz044_gulf_of_gonave",
                          "le_amz045_elsewhere",
                          "le_amz045_s_of_17n_w_of_86w",
                          "le_amz046_e_of_82w",
                          "le_amz046_w_of_82w",
                          "le_amz047_n_of_17n",
                          "le_amz047_s_of_17n",
                          "le_amz048_n_of_17n",
                          "le_amz048_s_of_17n",
                          "le_amz049_e_of_70w",
                          "le_amz049_w_of_70w",
                          "le_amz050_e_of_66w",
                          "le_amz050_w_of_66w",
                          "le_amz051_atlantic",
                          "le_amz051_caribbean",
                          "le_amz052_n_of_17n",
                          "le_amz052_s_of_17n",
                          "le_amz053_open_waters",
                          "le_amz053_reefs",
                          "le_amz054_e_of_78w",
                          "le_amz054_w_of_78w",
                          "le_amz055_n_of_13n",
                          "le_amz055_s_of_13n",
                          "le_amz056_n_of_13n",
                          "le_amz056_s_of_13n",
                          "le_amz057_n_of_13n",
                          "le_amz057_s_of_13n",
                          "le_amz058_atlantic",
                          "le_amz058_caribbean",
                          "le_amz059_n_of_13n",
                          "le_amz059_s_of_13n",
                          "le_amz060_n_of_10n",
                          "le_amz060_s_of_10n",
                          "le_amz061_n_of_10n",
                          "le_amz061_s_of_10n",
                          "le_amz062_n_of_09n",
                          "le_amz062_s_of_09n",
                          "le_amz063_e_of_79w",
                          "le_amz063_w_of_79w",
                          "le_amz064_e_of_75p5w",
                          "le_amz064_w_of_75p5w",
                          "le_amz065_e_of_72w",
                          "le_amz065_w_of_72w",
                          "le_amz066_e_of_67p5w",
                          "le_amz066_w_of_67p5w",
                          "le_amz067_e_of_62p5w",
                          "le_amz067_w_of_62p5w",
                          "le_amz068_e_of_57p5w",
                          "le_amz068_w_of_57p5w",
                          "le_amz069_e_of_78w",
                          "le_amz069_w_of_78w",
                          "le_amz070_e_of_75p5w",
                          "le_amz070_w_of_75p5w",
                          "le_amz071_e_of_72w",
                          "le_amz071_w_of_72w",
                          "le_amz072_e_of_67p5w",
                          "le_amz072_w_of_67p5w",
                          "le_amz073_e_of_62p5w",
                          "le_amz073_w_of_62p5w",
                          "le_amz074_e_of_57p5w",
                          "le_amz074_w_of_57p5w",
                          "le_amz075_elsewhere",
                          "le_amz075_open_atlc_waters",
                          "le_amz076_e_of_73w",
                          "le_amz076_w_of_73w",
                          "le_amz077_e_of_67p5w",
                          "le_amz077_w_of_67p5w",
                          "le_amz078_e_of_62p5w",
                          "le_amz078_w_of_62p5w",
                          "le_amz079_e_of_57p5w",
                          "le_amz079_w_of_57p5w",
                          "le_amz081_n_of_23n",
                          "le_amz081_s_of_23n",
                          "le_amz082_n_of_23n",
                          "le_amz082_s_of_23n",
                          "le_amz083_n_of_23n",
                          "le_amz083_s_of_23n",
                          "le_amz084_n_of_23n",
                          "le_amz084_s_of_23n",
                          "le_amz085_n_of_21n",
                          "le_amz085_s_of_21n",
                          "le_amz086_n_of_21n",
                          "le_amz086_s_of_21n",
                          "le_amz087_n_of_20p5n",
                          "le_amz087_s_of_20p5n",
                          "le_amz088_n_of_20p5n",
                          "le_amz088_s_of_20p5n"
                          
                            ]),
                              
                ("WaveHeight", ["le_gmz040_n_of_27n",
                          "le_gmz040_s_of_27n",
                          "le_gmz041_e_of_92p5w",
                          "le_gmz041_w_of_92p5w",
                          "le_gmz045_n_of_24n",
                          "le_gmz045_s_of_24n",
                          "le_gmz046_n_of_24n",
                          "le_gmz046_s_of_24n",
                          "le_gmz047_n_of_24n",
                          "le_gmz047_s_of_24n",
                          "le_gmz048_elsewhere",
                          "le_gmz048_s_of_21n_w_of_95w",
                          "le_gmz049_n_of_20n",
                          "le_gmz049_s_of_20n",
                          "le_gmz050_e_of_90w",
                          "le_gmz050_w_of_90w",
                          "le_gmz056_e_of_89w",
                          "le_gmz056_w_of_89w",
                          "le_gmz057_e_of_85w",
                          "le_gmz057_w_of_85w",
                          "le_gmz058_e_of_96w",
                          "le_gmz058_w_of_96w",                    
                    
                          "le_amz040_n_of_20n",
                          "le_amz040_s_of_20n",
                          "le_amz041_e_of_81w",
                          "le_amz041_w_of_81w",
                          "le_amz042_e_of_82w",
                          "le_amz042_w_of_82w",
                          "le_amz043_e_of_78w",
                          "le_amz043_w_of_78w",
                          "le_amz044_elsewhere",
                          "le_amz044_gulf_of_gonave",
                          "le_amz045_elsewhere",
                          "le_amz045_s_of_17n_w_of_86w",
                          "le_amz046_e_of_82w",
                          "le_amz046_w_of_82w",
                          "le_amz047_n_of_17n",
                          "le_amz047_s_of_17n",
                          "le_amz048_n_of_17n",
                          "le_amz048_s_of_17n",
                          "le_amz049_e_of_70w",
                          "le_amz049_w_of_70w",
                          "le_amz050_e_of_66w",
                          "le_amz050_w_of_66w",
                          "le_amz051_atlantic",
                          "le_amz051_caribbean",
                          "le_amz052_n_of_17n",
                          "le_amz052_s_of_17n",
                          "le_amz053_open_waters",
                          "le_amz053_reefs",
                          "le_amz054_e_of_78w",
                          "le_amz054_w_of_78w",
                          "le_amz055_n_of_13n",
                          "le_amz055_s_of_13n",
                          "le_amz056_n_of_13n",
                          "le_amz056_s_of_13n",
                          "le_amz057_n_of_13n",
                          "le_amz057_s_of_13n",
                          "le_amz058_atlantic",
                          "le_amz058_caribbean",
                          "le_amz059_n_of_13n",
                          "le_amz059_s_of_13n",
                          "le_amz060_n_of_10n",
                          "le_amz060_s_of_10n",
                          "le_amz061_n_of_10n",
                          "le_amz061_s_of_10n",
                          "le_amz062_n_of_09n",
                          "le_amz062_s_of_09n",
                          "le_amz063_e_of_79w",
                          "le_amz063_w_of_79w",
                          "le_amz064_e_of_75p5w",
                          "le_amz064_w_of_75p5w",
                          "le_amz065_e_of_72w",
                          "le_amz065_w_of_72w",
                          "le_amz066_e_of_67p5w",
                          "le_amz066_w_of_67p5w",
                          "le_amz067_e_of_62p5w",
                          "le_amz067_w_of_62p5w",
                          "le_amz068_e_of_57p5w",
                          "le_amz068_w_of_57p5w",
                          "le_amz069_e_of_78w",
                          "le_amz069_w_of_78w",
                          "le_amz070_e_of_75p5w",
                          "le_amz070_w_of_75p5w",
                          "le_amz071_e_of_72w",
                          "le_amz071_w_of_72w",
                          "le_amz072_e_of_67p5w",
                          "le_amz072_w_of_67p5w",
                          "le_amz073_e_of_62p5w",
                          "le_amz073_w_of_62p5w",
                          "le_amz074_e_of_57p5w",
                          "le_amz074_w_of_57p5w",
                          "le_amz075_elsewhere",
                          "le_amz075_open_atlc_waters",
                          "le_amz076_e_of_73w",
                          "le_amz076_w_of_73w",
                          "le_amz077_e_of_67p5w",
                          "le_amz077_w_of_67p5w",
                          "le_amz078_e_of_62p5w",
                          "le_amz078_w_of_62p5w",
                          "le_amz079_e_of_57p5w",
                          "le_amz079_w_of_57p5w",
                          "le_amz081_n_of_23n",
                          "le_amz081_s_of_23n",
                          "le_amz082_n_of_23n",
                          "le_amz082_s_of_23n",
                          "le_amz083_n_of_23n",
                          "le_amz083_s_of_23n",
                          "le_amz084_n_of_23n",
                          "le_amz084_s_of_23n",
                          "le_amz085_n_of_21n",
                          "le_amz085_s_of_21n",
                          "le_amz086_n_of_21n",
                          "le_amz086_s_of_21n",
                          "le_amz087_n_of_20p5n",
                          "le_amz087_s_of_20p5n",
                          "le_amz088_n_of_20p5n",
                          "le_amz088_s_of_20p5n"
                        
                            ]),
                    ]
                }                

    #Addition - taken from MFL CWF
    def _WaveHeightLocalEffects_list(self, tree, node):
        leArea1 = self.LocalEffectArea("le_gmz040_n_of_27n", "N of 27N")
        leArea2 = self.LocalEffectArea("le_gmz040_s_of_27n", "S of 27N")
        leArea3 = self.LocalEffectArea("le_gmz041_e_of_92p5w", "E of 92W")
        leArea4 = self.LocalEffectArea("le_gmz041_w_of_92p5w", "W of 92W")
        leArea5 = self.LocalEffectArea("le_gmz045_n_of_24n", "N of 24N")
        leArea6 = self.LocalEffectArea("le_gmz045_s_of_24n", "S of 24N")
        leArea7 = self.LocalEffectArea("le_gmz046_n_of_24n", "N of 24N")
        leArea8 = self.LocalEffectArea("le_gmz046_s_of_24n", "S of 24N")
        leArea9 = self.LocalEffectArea("le_gmz047_n_of_24n", "N of 24N")
        leArea10 = self.LocalEffectArea("le_gmz047_s_of_24n", "S of 24N")
        leArea11 = self.LocalEffectArea("le_gmz048_elsewhere", "elsewhere")
        leArea12 = self.LocalEffectArea("le_gmz048_s_of_21n_w_of_95w", "S of 21N W of 95W")
        leArea13 = self.LocalEffectArea("le_gmz049_n_of_20n", "N of 20N")
        leArea14 = self.LocalEffectArea("le_gmz049_s_of_20n", "S of 20N")
        leArea15 = self.LocalEffectArea("le_gmz050_e_of_90w", "E of 90W")
        leArea16 = self.LocalEffectArea("le_gmz050_w_of_90w", "W of 90W")
        leArea17 = self.LocalEffectArea("le_gmz056_e_of_89w", "E of 89W")
        leArea18 = self.LocalEffectArea("le_gmz056_w_of_89w", "W of 89W")
        leArea19 = self.LocalEffectArea("le_gmz057_e_of_85w", "E of 85W")   
        leArea20 = self.LocalEffectArea("le_gmz057_w_of_85w", "W of 85W")
        leArea21 = self.LocalEffectArea("le_gmz058_e_of_96w", "E of 96W")   
        leArea22 = self.LocalEffectArea("le_gmz058_w_of_96w", "W of 96W")
        
        leArea23 = self.LocalEffectArea("le_amz040_n_of_20n", "N of 20N")
        leArea24 = self.LocalEffectArea("le_amz040_s_of_20n", "S of 20N")
        leArea25 = self.LocalEffectArea("le_amz041_e_of_81w", "E of 81W")
        leArea26 = self.LocalEffectArea("le_amz041_w_of_81w", "W of 81W")
        leArea27 = self.LocalEffectArea("le_amz042_e_of_82w", "E of 82W")
        leArea28 = self.LocalEffectArea("le_amz042_w_of_82w", "W of 82W")
        leArea29 = self.LocalEffectArea("le_amz043_e_of_78w", "E of 78W")
        leArea30 = self.LocalEffectArea("le_amz043_w_of_78w", "W of 78W")
        leArea31 = self.LocalEffectArea("le_amz044_elsewhere", "elsewhere")
        leArea32 = self.LocalEffectArea("le_amz044_gulf_of_gonave", "in the Gulf of Gonave")
        leArea33 = self.LocalEffectArea("le_amz045_elsewhere", "elsewhere")
        leArea34 = self.LocalEffectArea("le_amz045_s_of_17n_w_of_86w", "S of 17N W of 86W")
        leArea35 = self.LocalEffectArea("le_amz046_e_of_82w", "E of 82W")
        leArea36 = self.LocalEffectArea("le_amz046_w_of_82w", "W of 82W")
        leArea37 = self.LocalEffectArea("le_amz047_n_of_17n", "N of 17N")
        leArea38 = self.LocalEffectArea("le_amz047_s_of_17n", "S of 17N")
        leArea39 = self.LocalEffectArea("le_amz048_n_of_17n", "N of 17N")
        leArea40 = self.LocalEffectArea("le_amz048_s_of_17n", "S of 17N")
        leArea41 = self.LocalEffectArea("le_amz049_e_of_70w", "E of 70W")
        leArea42 = self.LocalEffectArea("le_amz049_w_of_70w", "W of 70W")
        leArea43 = self.LocalEffectArea("le_amz050_e_of_66w", "E of 66W")
        leArea44 = self.LocalEffectArea("le_amz050_w_of_66w", "W of 66W")
        leArea45 = self.LocalEffectArea("le_amz051_atlantic", "in the Atlantic")
        leArea46 = self.LocalEffectArea("le_amz051_caribbean", "in the Caribbean")
        leArea47 = self.LocalEffectArea("le_amz052_n_of_17n", "N of 17N")
        leArea48 = self.LocalEffectArea("le_amz052_s_of_17n", "S of 17N")
        leArea49 = self.LocalEffectArea("le_amz053_open_waters", "in the open waters")
        leArea50 = self.LocalEffectArea("le_amz053_reefs", "in the reefs")
        leArea51 = self.LocalEffectArea("le_amz054_e_of_78w", "E of 78W")
        leArea52 = self.LocalEffectArea("le_amz054_w_of_78w", "W of 78W")
        leArea53 = self.LocalEffectArea("le_amz055_n_of_13n", "N of 13N")
        leArea54 = self.LocalEffectArea("le_amz055_s_of_13n", "S of 13N")
        leArea55 = self.LocalEffectArea("le_amz056_n_of_13n", "N of 13N")
        leArea56 = self.LocalEffectArea("le_amz056_s_of_13n", "S of 13N")
        leArea57 = self.LocalEffectArea("le_amz057_n_of_13n", "N of 13N")
        leArea58 = self.LocalEffectArea("le_amz057_s_of_13n", "S of 13N")
        leArea59 = self.LocalEffectArea("le_amz058_atlantic", "in the Atlantic")
        leArea60 = self.LocalEffectArea("le_amz058_caribbean", "in the Caribbean")
        leArea61 = self.LocalEffectArea("le_amz059_n_of_13n", "N of 13N")
        leArea62 = self.LocalEffectArea("le_amz059_s_of_13n", "S of 13N")
        leArea63 = self.LocalEffectArea("le_amz060_n_of_10n", "N of 10N")
        leArea64 = self.LocalEffectArea("le_amz060_s_of_10n", "S of 10N")
        leArea65 = self.LocalEffectArea("le_amz061_n_of_10n", "N of 10N")
        leArea66 = self.LocalEffectArea("le_amz061_s_of_10n", "S of 10N")
        leArea67 = self.LocalEffectArea("le_amz062_n_of_09n", "N of 09N")
        leArea68 = self.LocalEffectArea("le_amz062_s_of_09n", "S of 09N")
        leArea69 = self.LocalEffectArea("le_amz063_e_of_79w", "E of 79W")
        leArea70 = self.LocalEffectArea("le_amz063_w_of_79w", "W of 79W")
        leArea71 = self.LocalEffectArea("le_amz064_e_of_75p5w", "E of 75W")
        leArea72 = self.LocalEffectArea("le_amz064_w_of_75p5w", "W of 75W")
        leArea73 = self.LocalEffectArea("le_amz065_e_of_72w", "E of 72W")
        leArea74 = self.LocalEffectArea("le_amz065_w_of_72w", "W of 72W")
        leArea75 = self.LocalEffectArea("le_amz066_e_of_67p5w", "E of 67W")
        leArea76 = self.LocalEffectArea("le_amz066_w_of_67p5w", "W of 67W")
        leArea77 = self.LocalEffectArea("le_amz067_e_of_62p5w", "E of 62W")
        leArea78 = self.LocalEffectArea("le_amz067_w_of_62p5w", "W of 62W")
        leArea79 = self.LocalEffectArea("le_amz068_e_of_57p5w", "E of 57W")
        leArea80 = self.LocalEffectArea("le_amz068_w_of_57p5w", "W of 57W")
        leArea81 = self.LocalEffectArea("le_amz069_e_of_78w", "E of 78W")
        leArea82 = self.LocalEffectArea("le_amz069_w_of_78w", "W of 78W")
        leArea83 = self.LocalEffectArea("le_amz070_e_of_75p5w", "E of 75W")
        leArea84 = self.LocalEffectArea("le_amz070_w_of_75p5w", "W of 75W")
        leArea85 = self.LocalEffectArea("le_amz071_e_of_72w", "E of 72W")
        leArea86 = self.LocalEffectArea("le_amz071_w_of_72w", "W of 72W")
        leArea87 = self.LocalEffectArea("le_amz072_e_of_67p5w", "E of 67W")
        leArea88 = self.LocalEffectArea("le_amz072_w_of_67p5w", "W of 67W")
        leArea89 = self.LocalEffectArea("le_amz073_e_of_62p5w", "E of 62W")
        leArea90 = self.LocalEffectArea("le_amz073_w_of_62p5w", "W of 62W")
        leArea91 = self.LocalEffectArea("le_amz074_e_of_57p5w", "E of 57W")
        leArea92 = self.LocalEffectArea("le_amz074_w_of_57p5w", "W of 57W")
        leArea93 = self.LocalEffectArea("le_amz075_elsewhere", "elsewhere")
        leArea94 = self.LocalEffectArea("le_amz075_open_atlc_waters", "in the open Atlantic waters")
        leArea95 = self.LocalEffectArea("le_amz076_e_of_73w", "E of 73W")
        leArea96 = self.LocalEffectArea("le_amz076_w_of_73w", "W of 73W")
        leArea97 = self.LocalEffectArea("le_amz077_e_of_67p5w", "E of 67W")
        leArea98 = self.LocalEffectArea("le_amz077_w_of_67p5w", "W of 67W")
        leArea99 = self.LocalEffectArea("le_amz078_e_of_62p5w", "E of 62W")
        leArea100 = self.LocalEffectArea("le_amz078_w_of_62p5w", "W of 62W")
        leArea101 = self.LocalEffectArea("le_amz079_e_of_57p5w", "E of 57W")
        leArea102 = self.LocalEffectArea("le_amz079_w_of_57p5w", "W of 57W")
        leArea103 = self.LocalEffectArea("le_amz081_n_of_23n", "N of 23N")
        leArea104 = self.LocalEffectArea("le_amz081_s_of_23n", "S of 23N")
        leArea105 = self.LocalEffectArea("le_amz082_n_of_23n", "N of 23N")
        leArea106 = self.LocalEffectArea("le_amz082_s_of_23n", "S of 23N")
        leArea107 = self.LocalEffectArea("le_amz083_n_of_23n", "N of 23N")
        leArea108 = self.LocalEffectArea("le_amz083_s_of_23n", "S of 23N")
        leArea109 = self.LocalEffectArea("le_amz084_n_of_23n", "N of 23N")
        leArea110 = self.LocalEffectArea("le_amz084_s_of_23n", "S of 23N")
        leArea111 = self.LocalEffectArea("le_amz085_n_of_21n", "N of 21N")
        leArea112 = self.LocalEffectArea("le_amz085_s_of_21n", "S of 21N")
        leArea113 = self.LocalEffectArea("le_amz086_n_of_21n", "N of 21N")
        leArea114 = self.LocalEffectArea("le_amz086_s_of_21n", "S of 21N")
        leArea115 = self.LocalEffectArea("le_amz087_n_of_20p5n", "N of 20N")
        leArea116 = self.LocalEffectArea("le_amz087_s_of_20p5n", "S of 20N")
        leArea117 = self.LocalEffectArea("le_amz088_n_of_20p5n", "N of 20N")
        leArea118 = self.LocalEffectArea("le_amz088_s_of_20p5n", "S of 20N")
       
          
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
                self.LocalEffect([leArea14, leArea13], 2, ", and "),                
                self.LocalEffect([leArea16, leArea15], 2, ", and "),
                self.LocalEffect([leArea18, leArea17], 2, ", and "),
                self.LocalEffect([leArea20, leArea19], 2, ", and "),
                self.LocalEffect([leArea22, leArea21], 2, ", and "),
                
                self.LocalEffect([leArea24, leArea23], 2, ", and "),
                self.LocalEffect([leArea26, leArea25], 2, ", and "),
                self.LocalEffect([leArea28, leArea27], 1, ", and "),
                self.LocalEffect([leArea30, leArea29], 2, ", and "),
                self.LocalEffect([leArea32, leArea31], 2, ", and "),
                self.LocalEffect([leArea34, leArea33], 2, ", and "),
                self.LocalEffect([leArea36, leArea35], 0, ", and "), #changed from 2  ERA 6/25/22
                self.LocalEffect([leArea38, leArea37], 2, ", and "),
                self.LocalEffect([leArea40, leArea39], 2, ", and "),
                self.LocalEffect([leArea42, leArea41], 2, ", and "),
                self.LocalEffect([leArea44, leArea43], 1, ", and "), #changed from 2 to get "seas less than 2 ft" wording ERA 6/26/16 
                self.LocalEffect([leArea46, leArea45], 2, ", and "),
                self.LocalEffect([leArea48, leArea47], 2, ", and "),
                self.LocalEffect([leArea50, leArea49], 2, ", and "),
                self.LocalEffect([leArea52, leArea51], 2, ", and "),
                self.LocalEffect([leArea54, leArea53], 2, ", and "),
                self.LocalEffect([leArea56, leArea55], 2, ", and "),
                self.LocalEffect([leArea58, leArea57], 2, ", and "),
                self.LocalEffect([leArea60, leArea59], 2, ", and "),
                self.LocalEffect([leArea62, leArea61], 2, ", and "),
                self.LocalEffect([leArea64, leArea63], 2, ", and "),
                self.LocalEffect([leArea66, leArea65], 2, ", and "),
                self.LocalEffect([leArea68, leArea67], 2, ", and "),
                self.LocalEffect([leArea70, leArea69], 2, ", and "),
                self.LocalEffect([leArea72, leArea71], 2, ", and "),
                self.LocalEffect([leArea74, leArea73], 2, ", and "),
                self.LocalEffect([leArea76, leArea75], 2, ", and "),
                self.LocalEffect([leArea78, leArea77], 2, ", and "),
                self.LocalEffect([leArea80, leArea79], 2, ", and "),
                self.LocalEffect([leArea82, leArea81], 2, ", and "),
                self.LocalEffect([leArea84, leArea83], 2, ", and "),
                self.LocalEffect([leArea86, leArea85], 2, ", and "),
                self.LocalEffect([leArea88, leArea87], 2, ", and "),
                self.LocalEffect([leArea90, leArea89], 2, ", and "),
                self.LocalEffect([leArea92, leArea91], 2, ", and "),
                self.LocalEffect([leArea94, leArea93], 2, ", and "),
                self.LocalEffect([leArea96, leArea95], 2, ", and "),
                self.LocalEffect([leArea98, leArea97], 2, ", and "),
                self.LocalEffect([leArea100, leArea99], 2, ", and "),
                self.LocalEffect([leArea102, leArea101], 2, ", and "),
                self.LocalEffect([leArea104, leArea103], 2, ", and "),
                self.LocalEffect([leArea106, leArea105], 2, ", and "),
                self.LocalEffect([leArea108, leArea107], 2, ", and "),
                self.LocalEffect([leArea110, leArea109], 2, ", and "),
                self.LocalEffect([leArea112, leArea111], 2, ", and "),
                self.LocalEffect([leArea114, leArea113], 2, ", and "),
                self.LocalEffect([leArea116, leArea115], 2, ", and "),
                self.LocalEffect([leArea118, leArea117], 2, ", and "),
                
                
                ]

    def _windLocalEffects_list(self):
        leArea1 = self.LocalEffectArea("le_gmz040_n_of_27n", "N of 27N")
        leArea2 = self.LocalEffectArea("le_gmz040_s_of_27n", "S of 27N")
        leArea3 = self.LocalEffectArea("le_gmz041_e_of_92p5w", "E of 92W")
        leArea4 = self.LocalEffectArea("le_gmz041_w_of_92p5w", "W of 92W")
        leArea5 = self.LocalEffectArea("le_gmz045_n_of_24n", "N of 24N")
        leArea6 = self.LocalEffectArea("le_gmz045_s_of_24n", "S of 24N")
        leArea7 = self.LocalEffectArea("le_gmz046_n_of_24n", "N of 24N")
        leArea8 = self.LocalEffectArea("le_gmz046_s_of_24n", "S of 24N")
        leArea9 = self.LocalEffectArea("le_gmz047_n_of_24n", "N of 24N")
        leArea10 = self.LocalEffectArea("le_gmz047_s_of_24n", "S of 24N")
        leArea11 = self.LocalEffectArea("le_gmz048_elsewhere", "elsewhere")
        leArea12 = self.LocalEffectArea("le_gmz048_s_of_21n_w_of_95w", "S of 21N W of 95W")
        leArea13 = self.LocalEffectArea("le_gmz049_n_of_20n", "N of 20N")
        leArea14 = self.LocalEffectArea("le_gmz049_s_of_20n", "S of 20N")
        leArea15 = self.LocalEffectArea("le_gmz050_e_of_90w", "E of 90W")
        leArea16 = self.LocalEffectArea("le_gmz050_w_of_90w", "W of 90W")
        leArea17 = self.LocalEffectArea("le_gmz056_e_of_89w", "E of 89W")
        leArea18 = self.LocalEffectArea("le_gmz056_w_of_89w", "W of 89W")
        leArea19 = self.LocalEffectArea("le_gmz057_e_of_85w", "E of 85W")   
        leArea20 = self.LocalEffectArea("le_gmz057_w_of_85w", "W of 85W")
        leArea21 = self.LocalEffectArea("le_gmz058_e_of_96w", "E of 96W")   
        leArea22 = self.LocalEffectArea("le_gmz058_w_of_96w", "W of 96W")
        
        leArea23 = self.LocalEffectArea("le_amz040_n_of_20n", "N of 20N")
        leArea24 = self.LocalEffectArea("le_amz040_s_of_20n", "S of 20N")
        leArea25 = self.LocalEffectArea("le_amz041_e_of_81w", "E of 81W")
        leArea26 = self.LocalEffectArea("le_amz041_w_of_81w", "W of 81W")
        leArea27 = self.LocalEffectArea("le_amz042_e_of_82w", "E of 82W")
        leArea28 = self.LocalEffectArea("le_amz042_w_of_82w", "W of 82W")
        leArea29 = self.LocalEffectArea("le_amz043_e_of_78w", "E of 78W")
        leArea30 = self.LocalEffectArea("le_amz043_w_of_78w", "W of 78W")
        leArea31 = self.LocalEffectArea("le_amz044_elsewhere", "elsewhere")
        leArea32 = self.LocalEffectArea("le_amz044_gulf_of_gonave", "in the Gulf of Gonave")
        leArea33 = self.LocalEffectArea("le_amz045_elsewhere", "elsewhere")
        leArea34 = self.LocalEffectArea("le_amz045_s_of_17n_w_of_86w", "S of 17N W of 86W")
        leArea35 = self.LocalEffectArea("le_amz046_e_of_82w", "E of 82W")
        leArea36 = self.LocalEffectArea("le_amz046_w_of_82w", "W of 82W")
        leArea37 = self.LocalEffectArea("le_amz047_n_of_17n", "N of 17N")
        leArea38 = self.LocalEffectArea("le_amz047_s_of_17n", "S of 17N")
        leArea39 = self.LocalEffectArea("le_amz048_n_of_17n", "N of 17N")
        leArea40 = self.LocalEffectArea("le_amz048_s_of_17n", "S of 17N")
        leArea41 = self.LocalEffectArea("le_amz049_e_of_70w", "E of 70W")
        leArea42 = self.LocalEffectArea("le_amz049_w_of_70w", "W of 70W")
        leArea43 = self.LocalEffectArea("le_amz050_e_of_66w", "E of 66W")
        leArea44 = self.LocalEffectArea("le_amz050_w_of_66w", "W of 66W")
        leArea45 = self.LocalEffectArea("le_amz051_atlantic", "in the Atlantic")
        leArea46 = self.LocalEffectArea("le_amz051_caribbean", "in the Caribbean")
        leArea47 = self.LocalEffectArea("le_amz052_n_of_17n", "N of 17N")
        leArea48 = self.LocalEffectArea("le_amz052_s_of_17n", "S of 17N")
        leArea49 = self.LocalEffectArea("le_amz053_open_waters", "in the open waters")
        leArea50 = self.LocalEffectArea("le_amz053_reefs", "in the reefs")
        leArea51 = self.LocalEffectArea("le_amz054_e_of_78w", "E of 78W")
        leArea52 = self.LocalEffectArea("le_amz054_w_of_78w", "W of 78W")
        leArea53 = self.LocalEffectArea("le_amz055_n_of_13n", "N of 13N")
        leArea54 = self.LocalEffectArea("le_amz055_s_of_13n", "S of 13N")
        leArea55 = self.LocalEffectArea("le_amz056_n_of_13n", "N of 13N")
        leArea56 = self.LocalEffectArea("le_amz056_s_of_13n", "S of 13N")
        leArea57 = self.LocalEffectArea("le_amz057_n_of_13n", "N of 13N")
        leArea58 = self.LocalEffectArea("le_amz057_s_of_13n", "S of 13N")
        leArea59 = self.LocalEffectArea("le_amz058_atlantic", "in the Atlantic")
        leArea60 = self.LocalEffectArea("le_amz058_caribbean", "in the Caribbean")
        leArea61 = self.LocalEffectArea("le_amz059_n_of_13n", "N of 13N")
        leArea62 = self.LocalEffectArea("le_amz059_s_of_13n", "S of 13N")
        leArea63 = self.LocalEffectArea("le_amz060_n_of_10n", "N of 10N")
        leArea64 = self.LocalEffectArea("le_amz060_s_of_10n", "S of 10N")
        leArea65 = self.LocalEffectArea("le_amz061_n_of_10n", "N of 10N")
        leArea66 = self.LocalEffectArea("le_amz061_s_of_10n", "S of 10N")
        leArea67 = self.LocalEffectArea("le_amz062_n_of_09n", "N of 09N")
        leArea68 = self.LocalEffectArea("le_amz062_s_of_09n", "S of 09N")
        leArea69 = self.LocalEffectArea("le_amz063_e_of_79w", "E of 79W")
        leArea70 = self.LocalEffectArea("le_amz063_w_of_79w", "W of 79W")
        leArea71 = self.LocalEffectArea("le_amz064_e_of_75p5w", "E of 75W")
        leArea72 = self.LocalEffectArea("le_amz064_w_of_75p5w", "W of 75W")
        leArea73 = self.LocalEffectArea("le_amz065_e_of_72w", "E of 72W")
        leArea74 = self.LocalEffectArea("le_amz065_w_of_72w", "W of 72W")
        leArea75 = self.LocalEffectArea("le_amz066_e_of_67p5w", "E of 67W")
        leArea76 = self.LocalEffectArea("le_amz066_w_of_67p5w", "W of 67W")
        leArea77 = self.LocalEffectArea("le_amz067_e_of_62p5w", "E of 62W")
        leArea78 = self.LocalEffectArea("le_amz067_w_of_62p5w", "W of 62W")
        leArea79 = self.LocalEffectArea("le_amz068_e_of_57p5w", "E of 57W")
        leArea80 = self.LocalEffectArea("le_amz068_w_of_57p5w", "W of 57W")
        leArea81 = self.LocalEffectArea("le_amz069_e_of_78w", "E of 78W")
        leArea82 = self.LocalEffectArea("le_amz069_w_of_78w", "W of 78W")
        leArea83 = self.LocalEffectArea("le_amz070_e_of_75p5w", "E of 75W")
        leArea84 = self.LocalEffectArea("le_amz070_w_of_75p5w", "W of 75W")
        leArea85 = self.LocalEffectArea("le_amz071_e_of_72w", "E of 72W")
        leArea86 = self.LocalEffectArea("le_amz071_w_of_72w", "W of 72W")
        leArea87 = self.LocalEffectArea("le_amz072_e_of_67p5w", "E of 67W")
        leArea88 = self.LocalEffectArea("le_amz072_w_of_67p5w", "W of 67W")
        leArea89 = self.LocalEffectArea("le_amz073_e_of_62p5w", "E of 62W")
        leArea90 = self.LocalEffectArea("le_amz073_w_of_62p5w", "W of 62W")
        leArea91 = self.LocalEffectArea("le_amz074_e_of_57p5w", "E of 57W")
        leArea92 = self.LocalEffectArea("le_amz074_w_of_57p5w", "W of 57W")
        leArea93 = self.LocalEffectArea("le_amz075_elsewhere", "elsewhere")
        leArea94 = self.LocalEffectArea("le_amz075_open_atlc_waters", "in the open Atlantic waters")
        leArea95 = self.LocalEffectArea("le_amz076_e_of_73w", "E of 73W")
        leArea96 = self.LocalEffectArea("le_amz076_w_of_73w", "W of 73W")
        leArea97 = self.LocalEffectArea("le_amz077_e_of_67p5w", "E of 67W")
        leArea98 = self.LocalEffectArea("le_amz077_w_of_67p5w", "W of 67W")
        leArea99 = self.LocalEffectArea("le_amz078_e_of_62p5w", "E of 62W")
        leArea100 = self.LocalEffectArea("le_amz078_w_of_62p5w", "W of 62W")
        leArea101 = self.LocalEffectArea("le_amz079_e_of_57p5w", "E of 57W")
        leArea102 = self.LocalEffectArea("le_amz079_w_of_57p5w", "W of 57W")
        leArea103 = self.LocalEffectArea("le_amz081_n_of_23n", "N of 23N")
        leArea104 = self.LocalEffectArea("le_amz081_s_of_23n", "S of 23N")
        leArea105 = self.LocalEffectArea("le_amz082_n_of_23n", "N of 23N")
        leArea106 = self.LocalEffectArea("le_amz082_s_of_23n", "S of 23N")
        leArea107 = self.LocalEffectArea("le_amz083_n_of_23n", "N of 23N")
        leArea108 = self.LocalEffectArea("le_amz083_s_of_23n", "S of 23N")
        leArea109 = self.LocalEffectArea("le_amz084_n_of_23n", "N of 23N")
        leArea110 = self.LocalEffectArea("le_amz084_s_of_23n", "S of 23N")
        leArea111 = self.LocalEffectArea("le_amz085_n_of_21n", "N of 21N")
        leArea112 = self.LocalEffectArea("le_amz085_s_of_21n", "S of 21N")
        leArea113 = self.LocalEffectArea("le_amz086_n_of_21n", "N of 21N")
        leArea114 = self.LocalEffectArea("le_amz086_s_of_21n", "S of 21N")
        leArea115 = self.LocalEffectArea("le_amz087_n_of_20p5n", "N of 20N")
        leArea116 = self.LocalEffectArea("le_amz087_s_of_20p5n", "S of 20N")
        leArea117 = self.LocalEffectArea("le_amz088_n_of_20p5n", "N of 20N")
        leArea118 = self.LocalEffectArea("le_amz088_s_of_20p5n", "S of 20N")
     
                 
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
                self.LocalEffect([leArea14, leArea13], 5, ", and "),                
                self.LocalEffect([leArea16, leArea15], 5, ", and "),
                self.LocalEffect([leArea18, leArea17], 5, ", and "),
                self.LocalEffect([leArea20, leArea19], 5, ", and "),
                self.LocalEffect([leArea22, leArea21], 5, ", and "),
                
                self.LocalEffect([leArea24, leArea23], 2, ", and "),
                self.LocalEffect([leArea26, leArea25], 2, ", and "),
                self.LocalEffect([leArea28, leArea27], 1, ", and "),
                self.LocalEffect([leArea30, leArea29], 2, ", and "),
                self.LocalEffect([leArea32, leArea31], 2, ", and "),
                self.LocalEffect([leArea34, leArea33], 2, ", and "),
                self.LocalEffect([leArea36, leArea35], 0, ", and "), #changed from 2 6/25/22 ERA
                self.LocalEffect([leArea38, leArea37], 2, ", and "),
                self.LocalEffect([leArea40, leArea39], 2, ", and "),
                self.LocalEffect([leArea42, leArea41], 2, ", and "),
                self.LocalEffect([leArea44, leArea43], 1, ", and "), #changed from 2 to get "seas less than 2 ft" wording ERA 6/26/16 
                self.LocalEffect([leArea46, leArea45], 2, ", and "),
                self.LocalEffect([leArea48, leArea47], 2, ", and "),
                self.LocalEffect([leArea50, leArea49], 2, ", and "),
                self.LocalEffect([leArea52, leArea51], 2, ", and "),
                self.LocalEffect([leArea54, leArea53], 2, ", and "),
                self.LocalEffect([leArea56, leArea55], 2, ", and "),
                self.LocalEffect([leArea58, leArea57], 2, ", and "),
                self.LocalEffect([leArea60, leArea59], 2, ", and "),
                self.LocalEffect([leArea62, leArea61], 2, ", and "),
                self.LocalEffect([leArea64, leArea63], 2, ", and "),
                self.LocalEffect([leArea66, leArea65], 2, ", and "),
                self.LocalEffect([leArea68, leArea67], 2, ", and "),
                self.LocalEffect([leArea70, leArea69], 2, ", and "),
                self.LocalEffect([leArea72, leArea71], 2, ", and "),
                self.LocalEffect([leArea74, leArea73], 2, ", and "),
                self.LocalEffect([leArea76, leArea75], 2, ", and "),
                self.LocalEffect([leArea78, leArea77], 2, ", and "),
                self.LocalEffect([leArea80, leArea79], 2, ", and "),
                self.LocalEffect([leArea82, leArea81], 2, ", and "),
                self.LocalEffect([leArea84, leArea83], 2, ", and "),
                self.LocalEffect([leArea86, leArea85], 2, ", and "),
                self.LocalEffect([leArea88, leArea87], 2, ", and "),
                self.LocalEffect([leArea90, leArea89], 2, ", and "),
                self.LocalEffect([leArea92, leArea91], 2, ", and "),
                self.LocalEffect([leArea94, leArea93], 2, ", and "),
                self.LocalEffect([leArea96, leArea95], 2, ", and "),
                self.LocalEffect([leArea98, leArea97], 2, ", and "),
                self.LocalEffect([leArea100, leArea99], 2, ", and "),
                self.LocalEffect([leArea102, leArea101], 2, ", and "),
                self.LocalEffect([leArea104, leArea103], 2, ", and "),
                self.LocalEffect([leArea106, leArea105], 2, ", and "),
                self.LocalEffect([leArea108, leArea107], 2, ", and "),
                self.LocalEffect([leArea110, leArea109], 2, ", and "),
                self.LocalEffect([leArea112, leArea111], 2, ", and "),
                self.LocalEffect([leArea114, leArea113], 2, ", and "),
                self.LocalEffect([leArea116, leArea115], 2, ", and "),
                self.LocalEffect([leArea118, leArea117], 2, ", and "),
                
                ]               
                







#######################################################################################################################

#     def OFFPeriod(self):
# #            type = "component",
# ##            methodList = [
# ##                          self.consolidateSubPhrases,
# ##                          self.assemblePhrases,   
# ##                          self.wordWrap,          
# ##                          ],
#             
#             analysisList = [            
#                       # NOTE: Choose from the following analysis options.
#                       # Do not remove the "vectorMinMax" analysis for
#                       # "Wind". This is necessary to get an absolute max if
#                       # the useWindsForGusts flag is on.
#             
#                       # Use the following if you want moderated ranges 
#                       # (e.g. N WIND 10 to 20 KT)
#                       # Set the moderating percentage in the "moderated_dict"
#                       # dictionary module.
#                       # Set the maximum range values in the "maximum_range_nlValue_dict"
#                       # dictionary module.
#                           ("Wind", self.vectorModeratedMinMax, [6]),
#                          # ("Wind", self.vectorMinMax, [6]),
#                           ("WindGust", self.moderatedMax, [6]),
#                           
#                           ("WaveHeight", self.moderatedMax, [6]), #changed 1/24/2018 CJ/JL/ERA
#                           #("WaveHeight", self.moderatedMinMax, [6]),
#                        #   ("WindWaveHgt", self.moderatedMinMax, [6]),
#                          
#                          # changed analysis period to 3 hours to handle swell transitions during a forecast period- 1/24/2018 CNJ/JL/ERA
#                           ("Swell", self.vectorModeratedMinMax, [6]),
#                           ("Swell2", self.vectorModeratedMinMax, [6]),
#                           #("Swell", self.vectorMax, [6]), 
#                           #("Swell2", self.vectorMax, [6]),
#                      #     ("Period", self.mode, [12]),
#                          # ("Period2", self.moderatedMinMax, [6]),
#                           ("Wx", self.rankedWx, [12]),
# 
#                       # Use the following if you want moderated
#                       # single values (e.g. N WIND 20 KT).   
#                       # Set the moderating percentage in the "moderated_dict"
#                       # dictionary module.
#                       # NOTE:  If you use these methods, include and uncomment
#                       # the "combine_singleValues_flag_dict" in your Local file (see below)
#                          #("Wind", self.vectorModeratedMax, [3]),
#                           #("Wind", self.vectorMinMax, [12]),
#                           #("WindGust", self.moderatedMax, [3]),
#                           #("WaveHeight", self.moderatedMax, [6]),
#                           #("WindWaveHgt", self.moderatedMax, [6]),
#                           #("Swell", self.vectorModeratedMax, [6]),
#                           #("Swell2", self.vectorModeratedMax, [6]),
#                           #("Period", self.moderatedMax, [6]),
#                           #("Period2", self.moderatedMax, [6]),
#                           #("Wx", self.rankedWx, [6]),                                  
#                           #("T", self.minMax),
#                           #("PoP", self._PoP_analysisMethod("OFFPeriod")),
#                           #("PoP", self.binnedPercent, [6]),
# 
#                       # Use the following if you want absolute ranges.   
#                       # Set the maximum range values in the "maximum_range_nlValue_dict"
#                       # dictionary module.
#                           # Split time range in quarters for Wind and WindGust
#                           #("Wind", self.vectorMinMax, [3]),
#                           #("Wind", self.vectorMinMax, [12]),
#                           #("WindGust", self.maximum, [3]),
#                           #("WaveHeight", self.minMax, [6]),
#                           #("WindWaveHgt", self.minMax, [6]),
#                           # Split time range in half for Wx and Swell
#                           #("Swell", self.vectorMinMax, [6]),
#                           #("Swell2", self.vectorMinMax, [6]),
#                           #("Period", self.avg, [6]),
#                           #("Period2", self.avg, [6]),
#                           #("Wx", self.rankedWx, [6]),                                  
#                           #("T", self.minMax),
#                           #("PoP", self._PoP_analysisMethod("OFFPeriod")),
#                           #("PoP", self.binnedPercent, [6]),
#                         ]
# 
#             phraseList = [
#                            # WINDS
# #                           (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
#                             # J.Lewitsky/NHC 04/15/11 uncommented line below to include Local Effects
#                            (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
#                            #self.marine_wind_withGusts_phrase, 
#                             #CJ try to remove local effects phrase
# #                           self.marine_wind_phrase,
#                            # Alternative:
# #                           (self.marine_wind_phrase, self._windLocalEffects_list()),
# #                           self.marine_wind_phrase,
#                            #self.gust_phrase,
#                            # WAVES
#                            ## commented back out for test (commented out below on 08/24/11 - turn back on for swell wording
#                            #self.wave_withPeriods_phrase,
#                            # Alternative:
#                            #self.wave_phrase,
#                            # SWELLS AND PERIODS
#                            #self.swell_withPeriods_phrase,
#                            # Alternative:
#                            #self.swell_phrase,
#                            
#                            # WEATHER
# #                           self.weather_phrase,
# 
# #                           self.weather_phrase,
#                            # uncommented below to include Local Effects (JL - 12/12/11)
#                            self.wave_withPeriods_phrase,
#                            #self.wave_phrase,
#                       #     self.period_phrase, 
#                            self.weather_phrase,
#                            self.visibility_phrase,
#                            ]
#             # CJ Added
#             if self._includeTropical:
#                 analysisList, phraseList = self.addTropical(analysisList, phraseList)
#             
#             return {
#                 "type": "component",
#                 "methodList": [
#                         self.consolidateSubPhrases,
#                         self.assemblePhrases,   
#                         self.wordWrap,          
#                         ],
#             
#             "analysisList": analysisList,
#             "phraseList": phraseList,
#             "intersectAreas":[
#                     #Areas listed by weather element that will be
#                     #intersected with the current area then
#                     #sampled and analyzed.
#                     #E.g. used in local effects methods.
#                 ("Wind", ["le_gmz013_w_of_90w",
#                           "le_gmz013_main",
#                           "le_gmz015_s_of_27n",
#                           "le_gmz015_main",
#                           "le_gmz017_w_of_96w",
#                           "le_gmz017_main",
#                           "le_gmz019_s_of_24n",
#                           "le_gmz019_main",
#                           "le_gmz021_straits_of_florida",
#                           "le_gmz021_main",
#                           #"le_gmz023_60nm_of_veracruz",
#                           "le_gmz023_s_of_21n_w_of_95w",
#                           "le_gmz023_main",
#                           #"le_gmz025_s_of_19n",
#                           "le_gmz025_60nm_of_campeche",
#                           "le_gmz025_main",
#                           "le_amz011_yucatan_channel",
#                           "le_amz011_main",
#                           "le_amz013_cuba_jamaica",
#                           "le_amz013_main",
#                           "le_amz017_s_of_17n_w_of_87w",
#                           "le_amz017_main",                          
#                           "le_amz021_w_of_77w",
#                           "le_amz021_main",
#                           "le_amz023_lee_of_dr",
#                           "le_amz023_main_wind",
#                           #"le_amz025_anegada",
#                           "le_amz025_atlc_exposures_and_passages",
#                           "le_amz025_main",
#                           "le_amz029_nicaraguan_coast",
#                           "le_amz029_main",
#                           "le_amz031_colombian_coast",
#                           "le_amz031_main",
#                           #"le_amz033_s_of_13n_w_of_68w",
#                           "le_amz033_gulf_of_venezuela",
#                           "le_amz033_main",
#                           "le_amz035_atlantic",
#                           "le_amz035_main",
#                           "le_amz037_s_of_10n",
#                           "le_amz037_main",
#                           "le_amz039_s_of_10n",
#                           #"le_amz039_w_of_80w",
#                           "le_amz039_main",                          
#                           "le_amz111_n_of_29n_w_of_79w",
#                           "le_amz111_main",
#                           "le_amz113_n_of_29n",
#                           "le_amz113_main",
#                           "le_amz115_n_of_29n",
#                           "le_amz115_main",
#                           "le_amz117_atlc_exposures",
#                           "le_amz117_main",
#                           "le_amz119_n_of_25n",
#                           "le_amz119_main",
#                           "le_amz121_n_of_25n",
#                           "le_amz121_main",
#                           "le_amz127_e_of_60w",
#                           "le_amz127_main"
#                             ]),
#                 ("WaveHeight", ["le_gmz013_w_of_90w",
#                                 "le_gmz013_main",
#                                 "le_gmz015_s_of_27n",
#                                 "le_gmz015_main",
#                                 "le_gmz017_w_of_96w",
#                                 "le_gmz017_main",
#                                 "le_gmz019_s_of_24n",
#                                 "le_gmz019_main",
#                                 "le_gmz021_straits_of_florida",
#                                 "le_gmz021_main",
#                                 "le_gmz023_s_of_21n_w_of_95w",
#                                 #"le_gmz023_60nm_of_veracruz",
#                                 "le_gmz023_main",
#                                 #"le_gmz025_s_of_19n",
#                                 "le_gmz025_60nm_of_campeche",
#                                 "le_gmz025_main",
#                                 "le_amz011_yucatan_channel",
#                                 "le_amz011_main",
#                                 "le_amz013_cuba_jamaica",
#                                 "le_amz013_main",
#                                 "le_amz017_s_of_17n_w_of_87w",
#                                 "le_amz017_main", 
#                                 "le_amz021_w_of_77w",
#                                 "le_amz021_main",
#                                 "le_amz023_mona_swell",
#                                 "le_amz023_main_swell",
#                                 #"le_amz025_anegada",
#                                 "le_amz025_atlc_exposures_and_passages",
#                                 "le_amz025_main",
#                                 "le_amz029_nicaraguan_coast",
#                                 "le_amz029_main",
#                                 "le_amz031_colombian_coast",
#                                 "le_amz031_main",
#                                 #"le_amz033_s_of_13n_w_of_68w",
#                                 "le_amz033_gulf_of_venezuela",
#                                 "le_amz033_main",
#                                 "le_amz035_atlantic",
#                                 "le_amz035_main",
#                                 "le_amz037_s_of_10n",
#                                 "le_amz037_main",
#                                 "le_amz039_s_of_10n",
#                                 #"le_amz039_w_of_80w",
#                                 "le_amz039_main",  
#                                 "le_amz111_n_of_29n_w_of_79w",
#                                 "le_amz111_main",
#                                 "le_amz113_n_of_29n",
#                                 "le_amz113_main",
#                                 "le_amz115_n_of_29n",
#                                 "le_amz115_main",
#                                 "le_amz117_atlc_exposures",
#                                 "le_amz117_main",
#                                 "le_amz119_n_of_25n",
#                                 "le_amz119_main",
#                                 "le_amz121_n_of_25n",
#                                 "le_amz121_main",
#                                 "le_amz127_e_of_60w",
#                                 "le_amz127_main"
#                                   ]),
#                     ]
#                 }                
# 
#     #Addition - taken from MFL CWF
#     def _WaveHeightLocalEffects_list(self, tree, node):
#         leArea1 = self.LocalEffectArea("le_gmz013_main", "elsewhere")
#         leArea2 = self.LocalEffectArea("le_gmz013_w_of_90w", "W of 90W")
#         leArea3 = self.LocalEffectArea("le_gmz015_main", "elsewhere")
#         leArea4 = self.LocalEffectArea("le_gmz015_s_of_27n", "S of 27N")
#         leArea5 = self.LocalEffectArea("le_gmz017_main", "elsewhere")
#         leArea6 = self.LocalEffectArea("le_gmz017_w_of_96w", "W of 96W")
#         leArea7 = self.LocalEffectArea("le_gmz019_main", "elsewhere")
#         leArea8 = self.LocalEffectArea("le_gmz019_s_of_24n", "S of 24N")
#         leArea9 = self.LocalEffectArea("le_gmz021_main", "elsewhere")
#         leArea10 = self.LocalEffectArea("le_gmz021_straits_of_florida", "Straits of Florida")
#         leArea11 = self.LocalEffectArea("le_gmz023_main", "elsewhere")
#         leArea12 = self.LocalEffectArea("le_gmz023_s_of_21n_w_of_95w", "S of 21N W of 95W")
#         #leArea12 = self.LocalEffectArea("le_gmz023_60nm_of_veracruz", "WITHIN 60 NM OF COAST OF VERACRUZ")
#         leArea13 = self.LocalEffectArea("le_gmz025_main", "elsewhere")
#         leArea14 = self.LocalEffectArea("le_gmz025_60nm_of_campeche", "within 60 nm of coast of Campeche")
#         #leArea15 = self.LocalEffectArea("le_gmz025_s_of_19n", "S OF 19N")
#         leArea16 = self.LocalEffectArea("le_amz011_main", "elsewhere")
#         leArea17 = self.LocalEffectArea("le_amz011_yucatan_channel", "in Yucatan Channel")
#         leArea18 = self.LocalEffectArea("le_amz013_main", "elsewhere")
#         leArea19 = self.LocalEffectArea("le_amz013_cuba_jamaica", "between Cuba and Jamaica")
#         leArea20 = self.LocalEffectArea("le_amz021_main", "elsewhere")
#         leArea21 = self.LocalEffectArea("le_amz021_n_of_17n", "N of 17N")
#         #leArea21 = self.LocalEffectArea("le_amz021_w_of_77w", "W OF 77W")
#         leArea22 = self.LocalEffectArea("le_amz023_main_swell", "elsewhere")
#         leArea23 = self.LocalEffectArea("le_amz023_mona_swell", "in Mona Passage")
#         leArea24 = self.LocalEffectArea("le_amz025_main", "elsewhere")
#         leArea25 = self.LocalEffectArea("le_amz025_atlc_exposures_and_passages", "in Atlantic exposures and passages")
#        # leArea26 = self.LocalEffectArea("le_amz025_atlantic", "ATLANTIC EXPOSURES")
#         leArea27 = self.LocalEffectArea("le_amz029_main", "elsewhere")
#         leArea28 = self.LocalEffectArea("le_amz029_nicaraguan_coast", "within 60 nm of coast of Nicaragua")
#         leArea29 = self.LocalEffectArea("le_amz031_main", "elsewhere")
#         leArea30 = self.LocalEffectArea("le_amz031_colombian_coast", "within 90 nm of coast of Colombia")
#         leArea31 = self.LocalEffectArea("le_amz033_main", "elsewhere")
#         #leArea32 = self.LocalEffectArea("le_amz033_s_of_13n_w_of_68w", "S OF 13N W OF 68W")
#         leArea32 = self.LocalEffectArea("le_amz033_gulf_of_venezueula", "Gulf of Venezuela")
#         leArea33 = self.LocalEffectArea("le_amz035_main", "elsewhere")
#         leArea34 = self.LocalEffectArea("le_amz035_atlantic", "Atlantic Exposures")
#         leArea35 = self.LocalEffectArea("le_amz037_main", "elsewhere")
#         leArea36 = self.LocalEffectArea("le_amz037_s_of_10n", "S of 10N")
#         leArea37 = self.LocalEffectArea("le_amz039_main", "elsewhere")
#         leArea38 = self.LocalEffectArea("le_amz039_s_of_10n", "S of 10N")
#         #leArea38 = self.LocalEffectArea("le_amz039_w_of_80w", "W OF 80W")
#         leArea39 = self.LocalEffectArea("le_amz111_main", "elsewhere")
#         leArea40 = self.LocalEffectArea("le_amz111_n_of_29n_w_of_79w", "N of 29N W of 79W")
#         leArea41 = self.LocalEffectArea("le_amz113_main", "elsewhere")
#         leArea42 = self.LocalEffectArea("le_amz113_n_of_29n", "N of 29N")
#         leArea43 = self.LocalEffectArea("le_amz115_main", "elsewhere")
#         leArea44 = self.LocalEffectArea("le_amz115_n_of_29n", "N of 29N")
#         leArea45 = self.LocalEffectArea("le_amz117_main", "elsewhere")
#         leArea46 = self.LocalEffectArea("le_amz117_atlc_exposures", "Atlantic Exposures")
#         leArea47 = self.LocalEffectArea("le_amz119_main", "elsewhere")
#         leArea48 = self.LocalEffectArea("le_amz119_n_of_25n", "N of 25N")
#         leArea49 = self.LocalEffectArea("le_amz121_main", "elsewhere")
#         leArea50 = self.LocalEffectArea("le_amz121_n_of_25n", "N of 25N")
#         leArea51 = self.LocalEffectArea("le_amz127_main", "elsewhere")
#         leArea52 = self.LocalEffectArea("le_amz127_e_of_60w", "E of 60W")
#         leArea53 = self.LocalEffectArea("le_amz017_main", "elsewhere")
#         leArea54 = self.LocalEffectArea("le_amz017_s_of_17n_w_of_87w", "S of 17N W of 87W")          
#           
#         return [self.LocalEffect([leArea2, leArea1], 2, ", and "),
#                 #[self.LocalEffect([leArea1, leArea2], 2, "...EXCEPT "),
#                 # Changed "...EXCEPT " TO "E OF 90W AND ". Renders "SEAS x TO x FT E OF 90W AND x TO x FT W OF 90W" EC - 4/20/12
#                 #self.LocalEffect([leArea2, leArea1], 2, ". elsewhere..."),
#                 # Tried the entry above to put leArea first then elsewhere - JL/NHC - 02/12/12
#                 self.LocalEffect([leArea4, leArea3], 2, ", and "),
#                 self.LocalEffect([leArea6, leArea5], 2, ", and "),
#                 self.LocalEffect([leArea8, leArea7], 2, ", and "),
#                 self.LocalEffect([leArea10, leArea9], 2, ", and "),
#                 self.LocalEffect([leArea12, leArea11], 2, ", and "),
#                 self.LocalEffect([leArea14, leArea13], 2, ", and "), # removed leArea15               
#                 self.LocalEffect([leArea17, leArea16], 2, ", and "),
#                 self.LocalEffect([leArea19, leArea18], 2, ", and "),
#                 self.LocalEffect([leArea21, leArea20], 2, ", and "),
#                 self.LocalEffect([leArea23, leArea22], 2, ", and "),
#                 self.LocalEffect([leArea25, leArea24], 2, ", and "),
#                 self.LocalEffect([leArea28, leArea27], 2, ", and "),
#                 self.LocalEffect([leArea30, leArea29], 1, ", and "),
#                 self.LocalEffect([leArea32, leArea31], 2, ", and "),
#                 self.LocalEffect([leArea34, leArea33], 2, ", and "),
#                 self.LocalEffect([leArea36, leArea35], 2, ", and "),
#                 self.LocalEffect([leArea38, leArea37], 2, ", and "),
#                 self.LocalEffect([leArea40, leArea39], 2, ", and "),
#                 self.LocalEffect([leArea42, leArea41], 2, ", and "),
#                 self.LocalEffect([leArea44, leArea43], 2, ", and "),
#                 self.LocalEffect([leArea46, leArea45], 1, ", and "), #changed from 2 to get "seas less than 2 ft" wording ERA 6/26/16 
#                 self.LocalEffect([leArea48, leArea47], 2, ", and "),
#                 self.LocalEffect([leArea50, leArea49], 2, ", and "),
#                 self.LocalEffect([leArea52, leArea51], 2, ", and "),
#                 self.LocalEffect([leArea54, leArea53], 2, ", and "),
#                 ]
# 
#     def _windLocalEffects_list(self):
#         leArea1 = self.LocalEffectArea("le_gmz013_main", "elsewhere")
#         leArea2 = self.LocalEffectArea("le_gmz013_w_of_90w", "W of 90W")
#         leArea3 = self.LocalEffectArea("le_gmz015_main", "elsewhere")
#         leArea4 = self.LocalEffectArea("le_gmz015_s_of_27n", "S of 27N")
#         leArea5 = self.LocalEffectArea("le_gmz017_main", "elsewhere")
#         leArea6 = self.LocalEffectArea("le_gmz017_w_of_96w", "W of 96W")
#         leArea7 = self.LocalEffectArea("le_gmz019_main", "elsewhere")
#         leArea8 = self.LocalEffectArea("le_gmz019_s_of_24n", "S of 24N")
#         leArea9 = self.LocalEffectArea("le_gmz021_main", "elsewhere")
#         leArea10 = self.LocalEffectArea("le_gmz021_straits_of_florida", "Straits of Florida")
#         leArea11 = self.LocalEffectArea("le_gmz023_main", "elsewhere")
#         leArea12 = self.LocalEffectArea("le_gmz023_s_of_21n_w_of_95w", "S of 21N W of 95W")
#         #leArea12 = self.LocalEffectArea("le_gmz023_60nm_of_veracruz", "WITHIN 60 NM OF COAST OF VERACRUZ")
#         leArea13 = self.LocalEffectArea("le_gmz025_main", "elsewhere")
#         leArea14 = self.LocalEffectArea("le_gmz025_60nm_of_campeche", "within 60 nm of coast of Campeche")
#         #leArea15 = self.LocalEffectArea("le_gmz025_s_of_19n", "S OF 19N")
#         leArea16 = self.LocalEffectArea("le_amz011_main", "elsewhere")
#         leArea17 = self.LocalEffectArea("le_amz011_yucatan_channel", "in Yucatan Channel")
#         leArea18 = self.LocalEffectArea("le_amz013_main", "elsewhere")
#         leArea19 = self.LocalEffectArea("le_amz013_cuba_jamaica", "between Cuba and Jamaica")
#         leArea20 = self.LocalEffectArea("le_amz021_main", "elsewhere")
#         leArea21 = self.LocalEffectArea("le_amz021_n_of_17n", "N of 17N")
#         #leArea21 = self.LocalEffectArea("le_amz021_w_of_77w", "W OF 77W")
#         leArea22 = self.LocalEffectArea("le_amz023_main_swell", "elsewhere")
#         leArea23 = self.LocalEffectArea("le_amz023_mona_swell", "in Mona Passage")
#         leArea24 = self.LocalEffectArea("le_amz025_main", "elsewhere")
#         leArea25 = self.LocalEffectArea("le_amz025_atlc_exposures_and_passages", "in Atlantic Exposures and Passages")
#         #leArea26 = self.LocalEffectArea("le_amz025_atlantic", "ATLANTIC EXPOSURES")
#         leArea27 = self.LocalEffectArea("le_amz029_main", "elsewhere")
#         leArea28 = self.LocalEffectArea("le_amz029_nicaraguan_coast", "within 60 nm of coast of Nicaragua")
#         leArea29 = self.LocalEffectArea("le_amz031_main", "elsewhere")
#         leArea30 = self.LocalEffectArea("le_amz031_colombian_coast", "within 90 nm of coast of Colombia")
#         leArea31 = self.LocalEffectArea("le_amz033_main", "elsewhere")
#         #leArea32 = self.LocalEffectArea("le_amz033_s_of_13n_w_of_68w", "S OF 13N W OF 68W")
#         leArea32 = self.LocalEffectArea("le_amz033_gulf_of_venezuela", "Gulf of Venezuela")
#         leArea33 = self.LocalEffectArea("le_amz035_main", "elsewhere")
#         leArea34 = self.LocalEffectArea("le_amz035_atlantic", "Atlantic Exposures")
#         leArea35 = self.LocalEffectArea("le_amz037_main", "elsewhere")
#         leArea36 = self.LocalEffectArea("le_amz037_s_of_10n", "S of 10N")
#         leArea37 = self.LocalEffectArea("le_amz039_main", "elsewhere")
#         leArea38 = self.LocalEffectArea("le_amz039_s_of_10n", "S of 10N")
#         #leArea38 = self.LocalEffectArea("le_amz039_w_of_80w", "W OF 80W")
#         leArea39 = self.LocalEffectArea("le_amz111_main", "elsewhere")
#         leArea40 = self.LocalEffectArea("le_amz111_n_of_29n_w_of_79w", "N of 29N W of 79W")
#         leArea41 = self.LocalEffectArea("le_amz113_main", "elsewhere")
#         leArea42 = self.LocalEffectArea("le_amz113_n_of_29n", "N of 29N")
#         leArea43 = self.LocalEffectArea("le_amz115_main", "elsewhere")
#         leArea44 = self.LocalEffectArea("le_amz115_n_of_29n", "N of 29N")
#         leArea45 = self.LocalEffectArea("le_amz117_main", "elsewhere")
#         leArea46 = self.LocalEffectArea("le_amz117_atlc_exposures", "Atlantic Exposures")
#         leArea47 = self.LocalEffectArea("le_amz119_main", "elsewhere")
#         leArea48 = self.LocalEffectArea("le_amz119_n_of_25n", "N of 25N")
#         leArea49 = self.LocalEffectArea("le_amz121_main", "elsewhere")
#         leArea50 = self.LocalEffectArea("le_amz121_n_of_25n", "N of 25N")
#         leArea51 = self.LocalEffectArea("le_amz127_main", "elsewhere")
#         leArea52 = self.LocalEffectArea("le_amz127_e_of_60w", "E of 60W")
#         leArea53 = self.LocalEffectArea("le_amz017_main", "elsewhere")
#         leArea54 = self.LocalEffectArea("le_amz017_s_of_17n_w_of_87w", "S of 17N W of 87W")      
#                  
#         return [self.LocalEffect([leArea2, leArea1], 5, ", and "),
#                 #[self.LocalEffect([leArea1, leArea2], 2, "...EXCEPT "),
#                 # Changed "...EXCEPT " TO "E OF 90W AND ". Renders "SEAS x TO x FT E OF 90W AND x TO x FT W OF 90W" EC - 4/20/12
#                 #self.LocalEffect([leArea2, leArea1], 2, ". elsewhere..."),
#                 # Tried the entry above to put leArea first then elsewhere - JL/NHC - 02/12/12
#                 self.LocalEffect([leArea4, leArea3], 5, ", and "),
#                 self.LocalEffect([leArea6, leArea5], 5, ", and "),
#                 self.LocalEffect([leArea8, leArea7], 5, ", and "),
#                 self.LocalEffect([leArea10, leArea9], 5, ", and "),
#                 self.LocalEffect([leArea12, leArea11], 5, ", and "),
#                 self.LocalEffect([leArea14, leArea13], 5, ", and "), # removed leArea15               
#                 self.LocalEffect([leArea17, leArea16], 5, ", and "),
#                 self.LocalEffect([leArea19, leArea18], 5, ", and "),
#                 self.LocalEffect([leArea21, leArea20], 5, ", and "),
#                 self.LocalEffect([leArea23, leArea22], 5, ", and "),
#                 self.LocalEffect([leArea25, leArea24], 5, ", and "),
#                 self.LocalEffect([leArea28, leArea27], 5, ", and "),
#                 self.LocalEffect([leArea30, leArea29], 4, ", and "),
#                 self.LocalEffect([leArea32, leArea31], 4, ", and "),
#                 self.LocalEffect([leArea34, leArea33], 5, ", and "),
#                 self.LocalEffect([leArea36, leArea35], 5, ", and "),
#                 self.LocalEffect([leArea38, leArea37], 5, ", and "),
#                 self.LocalEffect([leArea40, leArea39], 5, ", and "),
#                 self.LocalEffect([leArea42, leArea41], 5, ", and "),
#                 self.LocalEffect([leArea44, leArea43], 5, ", and "),
#                 self.LocalEffect([leArea46, leArea45], 5, ", and "),
#                 self.LocalEffect([leArea48, leArea47], 5, ", and "),
#                 self.LocalEffect([leArea50, leArea49], 5, ", and "),
#                 self.LocalEffect([leArea52, leArea51], 5, ", and "),
#                 self.LocalEffect([leArea54, leArea53], 2, ", and "),
#                 ]
######################################################################################################################
#    #Modified from OFF base
#    #Was originally active at OPC
#    #fta 09/09/11 - reactivated - no longer interferes with tropicals
#     def OFFExtended(self):
#         return { "type": "component",
#                  "methodList": [
#                           self.consolidateSubPhrases,
#                           self.assemblePhrases,
#                           self.wordWrap,          
#                           ],
#                  "analysisList": [
#                       # NOTE: Choose from the following analysis options.
#                       # Do not remove the "vectorMinMax" analysis for
#                       # "Wind". This is necessary to get an absolute max if
#                       # the useWindsForGusts flag is on.
#             
#                       # Use the following if you want moderated ranges 
#                       # (e.g. N WIND 10 to 20 KT)
#                       # Set the moderating percentage in the "moderated_dict"
#                       # dictionary module.
#                       # Set the maximum range values in the "maximum_range_nlValue_dict"
#                       # dictionary module.
#                           ("Wind", self.vectorModeratedMinMax, [6]),                         
#                           ("WindGust", self.moderatedMinMax, [6]),
#                           
#                            # changed analysis period to 3 hours to match short-term period - 1/24/2018 CNJ/JL/ERA
#                           ("WaveHeight", self.moderatedMinMax, [6]), #changed from 3 and moderatedMax era 2/26/18
#                           #("WaveHeight", self.moderatedMinMax, [6]),
#                           
#                           # changed analysis period to 3 hours to handle swell transitions during a forecast period
#                           #("Swell", self.vectorMax, [6]), #era 2/26/18 
#                           #("Swell2", self.vectorMax, [6]), #era 2/26/18 
#                           #("Swell", self.vectorMax, [6]),
#                           #("Swell2", self.vectorMax, [6]),
#                           # ("WindWaveHgt", self.moderatedMinMax, [24]),
#                           #("Wx", self.rankedWx),
#                           #("T", self.minMax),  # needed for weather_phrase
#                           #("PoP", self._PoP_analysisMethod("OFFExtended")),
#                           #("PoP", self.binnedPercent),
#                           ("Swell", self.vectorModeratedMinMax, [12]),
#                           ("Swell2", self.vectorModeratedMinMax, [12]),
#                           
#                       # Use the following if you want moderated
#                       # single values (e.g. N WIND 20 KT).   
#                       # Set the moderating percentage in the "moderated_dict"
#                       # dictionary module.
#                       # NOTE:  If you use these methods, include and uncomment
#                       # the "combine_singleValues_flag_dict" in your Local file (see below)
#                           #("Wind", self.vectorModeratedMax, [6]),                         
#                           #("WindGust", self.moderatedMax, [12]),
#                           #("WaveHeight", self.moderatedMax, [12]),
#                           #("WindWaveHgt", self.moderatedMax, [12]),
#                           #("Wx", self.rankedWx),
#                           #("T", self.minMax),
#                           #("PoP", self._PoP_analysisMethod("OFFExtended")),
#                           #("PoP", self.binnedPercent),
#                    #       ("Period", self.mode, [12]),
#                           #("Swell", self.vectorModeratedMax, [12]),
#                           #("Swell2", self.vectorModeratedMax, [12]),
# 
#                       # Use the following if you want absolute ranges.   
#                       # Set the maximum range values in the "maximum_range_nlValue_dict"
#                       # dictionary module.
#                       # dictionary module.
#                           #("Wind", self.vectorMinMax, [6]),                         
#                           #("WindGust", self.minMax, [12]),
#                           #("WaveHeight", self.minMax, [12]),
#                           #("WindWaveHgt", self.minMax, [12]),
#                           #("Wx", self.rankedWx),     
#                           #("T", self.minMax),
#                           #("PoP", self._PoP_analysisMethod("OFFExtended")),
#                           #("PoP", self.binnedPercent),
#                           #("Swell", self.vectorMinMax, [12]),
#                           #("Swell2", self.vectorMinMax, [12]),
#                       ],
#                  "phraseList":[ 
#                                # WIND
#                                self.marine_wind_phrase,
#                                # WAVEHEIGHT
#                                # Commented out until fully developed seas wording fixed 9/7/11 CNJ/JL
#                                #self.wave_withPeriods_phrase,
#                                # Alternative:
#                                self.wave_withPeriods_phrase,
#                       #         self.period_phrase,
#                                # SWELLS AND PERIODS
#                                #self.swell_withPeriods_phrase,
#                                # Alternative:
#                                #self.swell_phrase,
#                                #self.period_phrase,
#                                # WEATHER
#                                #self.weather_phrase,
#                                #self.visibility_phrase,
#                                ],
#                 }   

#########################################################################################################################
        
    def wave_withPeriods_phrase(self):
        return {
            "setUpMethod": self.wave_withPeriods_setUp,
            "wordMethod": self.waveHeight_words,
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
            
        ## 1/24/2018 - changed to call scalarConnector instead of vectorConnector to fix crashing problem (CJ/JL/ERA)
        #self.subPhraseSetUp(tree, node, elementInfoList, self.vectorConnector)
        self.subPhraseSetUp(tree, node, elementInfoList, self.scalarConnector)
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
      #     maxWave = tree.stats.get("WindWaveHgt", timeRange, areaLabel, mergeMethod="Max")
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
 
    def waveHeight_words(self, tree, node):
        "Create phrase for waves"
        statDict = node.getStatDict()
        stats = self.getStats(statDict, "WaveHeight")
        if stats is None:
            nodataPhrase = self.noWaveHeight_phrase(
                tree, node, "WaveHeight", "WaveHeight")
            return self.setWords(node.parent, nodataPhrase)

        min, max = self.getValue(stats, "MinMax")
        print("min/max from waveHeight_words:", min, max)
        avg = (min + max)/2
        words = self.wave_range(avg)      
        print("words from waveHeight_words:", words)
        
        # add swell direction after wave height phrase - for OFFNT products
        # modified from swell_words in MarinePhrases.TextUtility
        # added 05/03/11 (CNJ/JL)
        if "WaveHeight" in statDict:
        #if "Swell" in statDict:
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
                print("Swell Words: ", swellWords )
                if swellWords == "null" or swellWords == "":
                    subPhraseParts.append("")
                    continue
                # Add Period
                periodPhrase = ""
                if periodFlag == 1:
                    periodStats = self.getStats(statDict, period)
                    periodPhrase = self.embedded_period_phrase(tree, node, periodStats)
                    swellWords += periodPhrase
                subPhraseParts.append(swellWords)
   
            #print("swell", node.getTimeRange(), subPhraseParts )
            if subPhraseParts[0]  and subPhraseParts[1] :
                # changed to properly report direction for both swell sub-phrases in a single forecast period - 1/24/2018 CJ/JL/ERA
                if subPhraseParts[0] == "swell":
                    subPhraseParts[0] = subPhraseParts[1]
                words = words + " in " + subPhraseParts[0] #+ " and " + subPhraseParts[1]
                print("words are ", words)
                # Check for mixed swell on first subPhrase
                if node.getIndex() == 0:
                    mixedSwell = self.checkMixedSwell(tree, node, statDict)
                    #if mixedSwell:
                    #    mixedSwellDesc = self.phrase_descriptor(tree, node, "mixed swell", "Swell")
                    #    phrase = node.getParent()
                    #    phrase.set("descriptor", mixedSwellDesc)
                    #    phrase.doneList.append(self.embedDescriptor)
            elif subPhraseParts[0] :
                words = words + " in " + subPhraseParts[0]
            elif subPhraseParts[1] :
                words = words + " in " + subPhraseParts[1]
            else:
                pass
                #words = "null"        
             
        return self.setWords(node, words)
 
 #added ERA 4/18/18 (previous one was commented out)   
    
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
        words = dirStr + " swell"
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
###        print("statDict in vector_words is:")
###        print( statDict)
        wspd = self.getStats(statDict, "Wind")
###        print("wspd = ", wspd #added this line 06/26/2016 per CJacobson for testing of failure -JL)
        #wspd = self._windDirSpeed(statDict, argDict)
        #wvhgt = self.getStats(statDict, "WaveHeight")
        mag, dir = wspd
        wspd1 = mag[0]
        wspd2 = mag[1]
        print("low wind speed is:")
        print( wspd1)
        print("high wind speed is:")
        print( wspd2)
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
        #print( statList)
###        print("statDict in null_nlValue is:")
###        print( statDict)
        wspd = self.getStats(statDict, "Wind")
        swl = self.getStats(statDict, "Swell")
        wvhgt = self.getStats(statDict, "WaveHeight")
        print("statDict after getStats is:")
        print( statDict)
###        mag, dir = wspd
        swlhgt = swl[0]
        print("avg wind speed in dict is:")
        print( avgwnd)
        print("swlhgt is:")
        print( swlhgt)
        print("wvhgt is:")
        print( wvhgt)
        
        # changed to calculate min/max/avg wave heights for use below 08/06/15 CNJ/JL/ERA
        min, max = self.getValue(wvhgt, "MinMax")
        print("Min wave in null_nlValue_tafb_dict: ", min)
        print("Max wave in null_nlValue_tafb_dict", max)
        avgwave = (min + max)/2
        print("avgwave in null_nlValue_tafb_dict:", avgwave)
        
#         wspd = self.getStats(statDict, "Wind")
#         mag, dir = wspd
#         wspd1 = mag[0]
#         wspd2 = mag[1]
#         avgwnd = (wspd1 + wspd2) / 2
        
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
                print("avg wind 14-16 & WaveHeight >= 7, setting dict[WaveHeight] = 7"            )
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
            exec( "self._" + key + "= self._definition[key]")

        # Get VariableList and _issuance_list variables
        varDict = argDict["varDict"]
        for key in varDict:
            if isinstance(key, tuple):
                label, variable = key
                exec( "self._" + variable + "= varDict[key]")

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
                    ("OFFPeriod", 12), #changed from "period1" to 12 ERA 02/15/20
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
                    ("OFFPeriod", 12), #changed from "period1" to 12 ERA 02/15/20
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
                    ("1130 AM", self.DAY() + 5, self.NIGHT(), 16, #changed from "issuanceHour" in self DAY to get rid of afternoon wording in first period ERA 8/25/22
                     ".Today...", "early", "late",
                     1, narrativeDefAM),
                    ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "", #CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "", "", #CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM)
                    ]
            else:
                return [
                    ("430 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1030 AM", "issuanceHour", self.NIGHT(), 16,
                     ".Today...", "early", "late",
                     1, narrativeDefAM),
                    ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "",#CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "", "",#CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM),
                    ]
        if self._definition["pil"] == "OFFNT3":
            if localTimeZone == "EDT":
                return [
                   ("530 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1130 AM", self.DAY() + 5, self.NIGHT(), 16, #changed from "issuanceHour" in self DAY to get rid of afternoon wording in first period ERA 8/25/22
                     ".Today...", "early", "late",
                     1, narrativeDefAM),
                    ("530 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "",#CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1130 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "", "",#CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM)
                    ]
            else:
                return [
                    ("430 AM", self.DAY(), self.NIGHT(), 16,
                     ".Today...", "in the morning", "in the afternoon",
                     1, narrativeDefAM),
                    ("1030 AM", "issuanceHour" , self.NIGHT(), 16,
                     ".Today...", "early", "late",
                     1, narrativeDefAM),
                    ("430 PM", self.NIGHT(), 24 + self.DAY(), 24 + 4,
                     ".Tonight...", "late", "",#CHANGED FROM "LATE IN THE NIGHT" "EARLY INTHE MORNING" ERA 12/02/15
                     1, narrativeDefPM),
                    ("1030 PM", "issuanceHour", 24 + self.DAY(), 24 + 4,
                     ".Overnight...", "", "",#CHANGED FROM "EARLY" ERA 12/02/15
                     1, narrativeDefPM),
                    ]
#################################################################################################   8/2/22 ERA             

    def lateDay_descriptor(self, statDict, argDict, timeRange):
        # If time range is in the first period, return period1 descriptor for
        #  late day -- default 3pm-6pm
        if self._issuanceInfo.period1TimeRange().contains(timeRange):
            return self._issuanceInfo.period1LateDayPhrase()
        else:
            return "late"

    def lateNight_descriptor(self, statDict, argDict, timeRange):
        # If time range is in the first period, return period1 descriptor for
        #  late night -- default 3am-6am
        if self._issuanceInfo.period1TimeRange().contains(timeRange):
            return self._issuanceInfo.period1LateNightPhrase()
        else:
            return "early"
    
 #####################################################################################################   
    
    
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
            
            ('AF.Y', allActions, 'Ashfall'), #2/2/18 era
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

#commented out 7/9/18...repeated at the beginning ERA
#     def generateForecast(self, argDict):
#         # Get variables
#         error = self._getVariables(argDict)
#         if error is not None:
#             return error
# 
#         # Get the areaList -- derived from defaultEditAreas and
#         # may be solicited at run-time from user if desired
#         self._areaList = self.getAreaList(argDict)
#         if not self._areaList:
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
#         # Need to know how many areas to process after this.
#         # will insert second synopsis before the last fcst area
#         areasLeft = len(self._areaList) - 1
#         for editArea, areaLabel in self._areaList:
#             skipAreas = self._skipAreas(argDict)
#             argDict["editArea"] = (editArea, areaLabel)
#             if self.currentAreaContains(argDict, skipAreas):
#                 continue
#             self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
#             fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
#             fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
#             fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#             # are we before the Atlantic zones? 
#             # if so, add synopsis2
#             if areasLeft == 9:
#                 fcst += self._Text3()
#             fraction = fractionOne
#             areasLeft = areasLeft - 1
#             # next four print( lines added for debugging of shapefile problem - 05/05/11)
#             print("##########################################################")
#             print("EDIT AREA IS:")
#             print( areaLabel)
#             print("##########################################################")
#         fcst = self._postProcessProduct(fcst, argDict)
#         return fcst
    
    
    


    def postProcessPhrase(self, tree, node):
        words = node.get("words")
        rval = None
        if words is not None:
            words =  words.replace("rain showers and thunderstorms", "showers and thunderstorms")
            # Below replace/re.subs format warning headlines in TAFB style
            words = words.replace("POSSIBLE ...", "POSSIBLE...")
            words = words.replace("WARNING ...", "WARNING...")
            words = words.replace(" TROPICAL", "TROPICAL")
            words = words.replace(" HURRICANE", "HURRICANE")
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
        "wxType":["WP", "R", "RW", "T", "SQ", "L", "ZR", "ZL", "S", "SW",
                  "IP", "F", "ZF", "IF", "IC", "H", "BS", "BN", "K", "BD",
                  "FR", "ZY", "VA", "<NoWx>", "<Invalid>", "SQ"], # changed BA for VA era 2/2/18
        "coverage":["Def", "Wide", "Brf", "Frq", "Ocnl", "Pds", "Inter",
                    "Lkly", "Num", "Sct", "Chc", "Areas",
                    "SChc", "WSct", "Iso", "Patchy", "<NoCov>", "<Invalid>"],
        "intensity":["+", "m", "-", "--", "<NoInten>", "<Invalid>"],
        "visibility":["0SM", "1/4SM", "1/2SM", "3/4SM", "1SM", "11/2SM", "2SM",
                      "21/2SM", "3SM", "4SM", "5SM", "6SM", "P6SM", "<NoVis>", "<Invalid>"],
        }

    def _postProcessProduct(self, fcst, argDict):
        """CWF_ER_Overrides version of CWF._postProcessProduct.

        Modified to add the capability of retaining forecast text from the 
        previous CWF.
        """
###        self.debug_print("\tCWF_ER_Overrides version of " +)
###                         "CWF._postProcessProduct")
        
        fcst = fcst.replace("%expireTime", self._expireTimeStr)
        #fcst = fcst.upper()
        
        self._userInfo = UserInfo.UserInfo()
        forecasterName = self._userInfo._getForecasterName(argDict)
        fcst += "Forecaster " + forecasterName
        self.setProgressPercentage(100)
        self.progressMessage(0, 100, self._displayName + " Complete")
        fcst = re.sub(r'  ', " ", fcst)
        fcst = fcst.replace( "NATIONAL WEATHER SERVICE", "NWS")
        fcst = fcst.replace( "after midnight", "late")
        fcst = re.sub(r' after\nmidnight', r' late', fcst)
        #fcst = fcst.replace( "kt, ", "kt, ")
        #fcst = fcst.replace( "less, ", "less, ")
        #fcst = fcst.replace( "elsewhere, ", "elsewhere, ")
        fcst = fcst.replace( "kt...Seas", "kt. Seas")
        fcst = fcst.replace( "kt, Seas", "kt. Seas")
        #fcst = fcst.replace( "morning, ", "morning, ")
        fcst = fcst.replace( "ft swell late", "ft late")
        fcst = re.sub(r' KT...\nseas', r'kt.\nseas', fcst)
        fcst = fcst.replace( " IN EFFECT", "")
        #fcst = fcst.replace( ", ", "...")
        fcst = fcst.replace( "Today...", "TODAY...")
        fcst = fcst.replace( "Tonight...", "TONIGHT...") #added ERA 6/18/17
        fcst = fcst.replace( "Overnight...", "OVERNIGHT...")
        fcst = fcst.replace( "This Afternoon...", "THIS AFTERNOON...")
        fcst = fcst.replace( "Elsewhere...", "Elsewhere, ")
        fcst = fcst.replace( ", shifting", ", shifting")
        fcst = fcst.replace( "TSTMs", "thunderstorms")
     
        fcst = fcst.replace( "...GALE CONDITIONS POSSIBLE...\n...STORM CONDITIONS POSSIBLE...", "...STORM CONDITIONS POSSIBLE...") #era 1/26/18
        
        fcst = fcst.replace( " TROPICAL", "TROPICAL")
        fcst = fcst.replace( " HURRICANE", "HURRICANE")
        
        #fcst = fcst.replace( "TSTMs", "tstms")
        # commented out - this causes format problems when preserving previous text - 08/11/15 CNJ/JL/ERA
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
            if self._definition["pil"] == "OFFNT3": 
                
                fcst1 = fcst.partition("AMZ101-")[0]
                
                fcst2 = fcst.partition("AMZ101-")[2]
                fcst2 = fcst2.partition("Forecaster ")[0]
                fcst2 = "AMZ101-" + fcst2
                fcst2 = "FZNT23 KNHC 082049\nOFFNT3\n\n" + \
                        "Offshore Waters Forecast for the SW and Tropical N Atlantic and\n" + \
                        "Caribbean Sea\n" + \
                        "NWS National Hurricane Center Miami, FL\n" + \
                        "449 PM EDT Sat Jul 8 2017\n\n" + \
                        "Offshore Waters Forecast for the Tropical N Atlantic from 07N to\n" + \
                        "22N between 55W and 64W, the SW N Atlantic S of 31N W of 65W\n" + \
                        "including Bahamas, and the Caribbean Sea.\n\n" + \
                        "Seas given as significant wave height, which is the average\n" + \
                        "height of the highest 1/3 of the waves. Individual waves may be\n" + \
                        "more than twice the significant wave height.\n\n" + fcst2
                
                previousOFF = self.getPreviousProduct(self._prevProdPIL)
                
                previousOFF1 = previousOFF.partition("AMZ101-")[0]
                print("### previousOFF1 ###", previousOFF1)
                
                previousOFF2 = previousOFF.partition("AMZ101-")[2]
                previousOFF2 = previousOFF2.partition("Forecaster ")[0]
                previousOFF2 = "AMZ101-" + previousOFF2
                print("### previousOFF2 ###", previousOFF2)
             
                if type(self._updatePeriodIndex) is type(1) and self._updatePeriodIndex >= 0:
                    if self._updatePeriodIndex == 0:
                        print( '\tRefreshing headlines only...')
                    elif self._updatePeriodIndex == 1:
                        print( '\tMerging OFF text for the first period only...')
                    else:
                        print( '\tMerging OFF text for the first %d periods...')
                     
                    #  Get OFF1 previous product 
                    #  If we actually found the previous text
                    if previousOFF1 : 
                        #  Merge the forecasts
                        print("*** merging fcst1 ***")
                        fcst1=mergeProds.mergeProds()._mergeCWF(fcst1, previousOFF1,
                                                               self._updatePeriodIndex)
                        
                    #  Get OFF2 previous product 
                    #  If we actually found the previous text
                    if previousOFF2 : 
                        #  Merge the forecasts
                        print("*** merging fcst2 ***")
                        fcst2=mergeProds.mergeProds()._mergeCWF(fcst2, previousOFF2,
                                                               self._updatePeriodIndex)
                        print("*** fcst2 after merge:", fcst2)
                        fcst2 = fcst2.partition("AMZ101-")[2]
                        fcst2 = fcst2.partition("Forecaster ")[0]
                        fcst2 = "AMZ101-" + fcst2
                    fcst = fcst1 + "\n" + fcst2
                    fcst += "\Forecaster " + forecasterName
            else:
                if type(self._updatePeriodIndex) is type(1) and self._updatePeriodIndex >= 0:
                    if self._updatePeriodIndex == 0:
                        print( '\tRefreshing headlines only...')
                    elif self._updatePeriodIndex == 1:
                        print( '\tMerging OFF text for the first period only...')
                    else:
                        print( '\tMerging OFF text for the first %d periods...' )
                     
                    #  Get previous product
                    oldCWF=self.getPreviousProduct(self._prevProdPIL)
 
                    #  If we actually found the previous text
                    if oldCWF :
 
                        #  Merge the forecasts
                        fcst=mergeProds.mergeProds()._mergeCWF(fcst, oldCWF,
                                                               self._updatePeriodIndex)
 
        #  Otherwise, if we cannot get the previous text for whatever reason
        except:
            print( 'Failed to parse previous OFF!  New text will be created ' )
        
        return fcst
 
 #added on 1/11/17 after 16.2 and 16.4.1 builds to change ", " to "..." in LE phrase starting with "elsewhere". Found on  PhraseBuilder...ERA  
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
        if words == "":
            return words, lastQualifier
        addPeriod = 1
        if qualifier is not None:
            if qualifier != lastQualifier and qualifier :
                words = qualifier + ", " + words
            next = self.getNext_nonEmpty(node, "words")
            if next is not None:
                nextQualifier = next.get(qualifierName)
                #print("nextQualifier, qualifier", nextQualifier, "X", qualifier, "X", words)
                if nextQualifier == qualifier:
                    addPeriod = 0
                    words = words + ", "
        if makeSentence:
            words = self.sentence(words, addPeriod)
        #print("returning", words)
        return words, qualifier
