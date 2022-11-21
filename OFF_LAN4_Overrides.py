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

class OFF_LAN4_Overrides:
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
        self.debug_print("Debug: _Text1 in OFF_LAN_Overrides")

        #Determine which product
        if self._definition["pil"] == "OFFNT4":
            return "OFFSHORE WATERS FORECAST FOR THE GULF OF MEXICO\n\n" + \
                   "SEAS GIVEN AS SIGNIFICANT WAVE HEIGHT...WHICH IS THE AVERAGE\n" + \
                   "HEIGHT OF THE HIGHEST 1/3 OF THE WAVES. INDIVIDUAL WAVES MAY BE\n" + \
                   "MORE THAN TWICE THE SIGNIFICANT WAVE HEIGHT.\n\n"
        else:
            #OFFNT3
            return "OFFSHORE WATERS FORECAST FOR THE TROPICAL N ATLANTIC FROM 07N TO\n" + \
                   "22N BETWEEN 55W AND 64W...THE SW N ATLANTIC S OF 31N W OF 65W\n" + \
                   "INCLUDING BAHAMAS...AND THE CARIBBEAN SEA.\n\n" + \
                   "SEAS GIVEN AS SIGNIFICANT WAVE HEIGHT...WHICH IS THE AVERAGE\n" + \
                   "HEIGHT OF THE HIGHEST 1/3 OF THE WAVES. INDIVIDUAL WAVES MAY BE\n" + \
                   "MORE THAN TWICE THE SIGNIFICANT WAVE HEIGHT.\n\n"

#    def _Text2(self, argDict):
#        synopsis = ""
#
#        #  Try to get Synopsis from previous OFF
###        if self._definition["synopsisUGC"] == "AMZ089":
#
#        productID = "MIAOFFNT3"
#        synopsis = self.getPreviousProduct(productID, "SYNOPSIS")
#            #  Clean up the previous synopsis
#        synopsis = re.sub(r'\n', r' ', synopsis)
#        synopsis = self._synopsisHeading + synopsis
#        synopsis = self.endline(synopsis, linelength=66, breakStr=" ")
#
#        #  Convert absolute time pointer to a tuple of values like that
#        #  returned by time.gmtime()
#        expTuple = time.strptime('%s' % (self._expireTime),
#                                 '%b %d %y %H:%M:%S GMT')
#
#        #  Format expiration time for inclusion in synopsis header
#        expTime = time.strftime('%d%H%M', expTuple)
#
#        return "%s-%s-\n" % ("AMZ001", expTime) + \
#               "%s\n" %  "SYNOPSIS FOR CARIBBEAN SEA AND TROPICAL N ATLANTIC FROM 07N TO" + \
#               "%s\n" %  "22N BETWEEN 55W AND 65W" + \
#               "%s\n" % self._timeLabel + "\n" + \
#               synopsis + "\n$$\n\n"
#
#    def _Text3(self):
#        synopsis2 = ""
###        if self._definition["synopsis2UGC"] == "AMZ088":
#
#        productID = "MIAOFFNT3"
#        # Can't just search for "SYNOPSIS"
#        # It will only return the first one it finds
#        entire_product = string.strip(self.getPreviousProduct(productID))
#        # get just the second synopsis
#        # split the product on the synopsisHeading (.SYNOPSIS...)
#        # then split on "$$" and grab everything before the $$ at the end of the synopsis
#        synopsis2 = entire_product.split(self._definition["synopsisHeading"])[2].split("$$")[0]
#
#        #  Clean up the previous synopsis
#        synopsis2 = re.sub(r'\n', r' ', synopsis2)
#        synopsis2 = self._synopsisHeading + synopsis2
#        synopsis2 = self.endline(synopsis2, linelength=66, breakStr=" ")
#
#        #  Convert absolute time pointer to a tuple of values like that
#        #  returned by time.gmtime()
#        expTuple = time.strptime('%s' % (self._expireTime),
#                                 '%b %d %y %H:%M:%S GMT')
#
#        #  Format expiration time for inclusion in synopsis header
#        expTime = time.strftime('%d%H%M', expTuple)
#
#        return "%s-%s-\n" % ("AMZ101", expTime) + \
#               "%s\n" %  "SYNOPSIS FOR THE SW N ATLANTIC INCLUDING THE BAHAMAS" + \
#               "%s\n" % self._timeLabel + "\n" + \
#               synopsis2 + "\n$$\n\n"
#
###        expTuple = time.strptime('%s' % (self._expireTime),
###                                 '%b %d %y %H:%M:%S GMT')
###
###        #  Format expiration time for inclusion in synopsis header
###        expTime = time.strftime('%d%H%M', expTuple)
###
###        return "%s-%s-\n" % (self._synopsis2UGC, expTime) + \
###               self._timeLabel + "\n\n" + \
###               self._synopsisHeading + "\n"  + \
###               synopsis + "\n$$\n\n"
#
#    # copy directly from OFF_TextProduct. only modify to add second synopsis
#    def generateForecast(self, argDict):
#        # Get variables
#        error = self._getVariables(argDict)
#        if error is not None:
#            return error
#
#        # Get the areaList -- derived from defaultEditAreas and
#        # may be solicited at run-time from user if desired
#        self._areaList = self.getAreaList(argDict)
#        if len(self._areaList) == 0:
#            return "WARNING -- No Edit Areas Specified to Generate Product."
#
#        # Determine time ranges
#        error = self._determineTimeRanges(argDict)
#        if error is not None:
#            return error
#
#        # Sample the data
#        error = self._sampleData(argDict)
#        if error is not None:
#            return error
#
#        # Initialize the output string
#        fcst = ""
#        fcst = self._preProcessProduct(fcst, argDict)
#
#        # Generate the product for each edit area in the list
#        fraction = 0
#        fractionOne = 1.0/float(len(self._areaList))
#        percent = 50.0
#        self.setProgressPercentage(percent)
#        # Need to know how many areas to process after this.
#        # will insert second synopsis before the last fcst area
#        areasLeft = len(self._areaList) - 1
#        for editArea, areaLabel in self._areaList:
#            skipAreas = self._skipAreas(argDict)
#            argDict["editArea"] = (editArea, areaLabel)
#            if self.currentAreaContains(argDict, skipAreas):
#                continue
#            self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
#            fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
#            fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
#            fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#            # are we before the Atlantic zones?
#            # if so, add synopsis2
#            if areasLeft == 9:
#                fcst = fcst + self._Text3()
#            fraction = fractionOne
#            areasLeft = areasLeft - 1
#            # next four print lines added for debugging of shapefile problem - 05/05/11
#            print("##########################################################")
#            print("EDIT AREA IS:")
#            print(areaLabel)
#            print("##########################################################")
#        fcst = self._postProcessProduct(fcst, argDict)
#        return fcst

    #Modified from OFF base
    def _Text2(self):
        self.debug_print("Debug: _Text2 in OFF_LAN_Overrides")

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

            return ""
                   #"%s-%s-\n" % ("GMZ001", expTime) + \
                   #"%s\n" %  "SYNOPSIS FOR THE GULF OF MEXICO" + \
                   #"%s\n" % self._timeLabel + "\n" + \
                   #synopsis + "\n$$\n\n"

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

            return ""
                  #"%s-%s-\n" % ("AMZ001", expTime) + \
                  #"%s\n" %  "SYNOPSIS FOR CARIBBEAN SEA AND TROPICAL N ATLANTIC FROM 07N TO" + \
                  #"%s\n" %  "19N BETWEEN 55W AND 64W" + \
                  #"%s\n" % self._timeLabel + "\n" + \
                  #synopsis + "\n$$\n\n"

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

            return ""
                   #"%s-%s-\n" % ("AMZ101", expTime) + \
                   #"%s\n" %  "SYNOPSIS FOR THE SW N ATLANTIC INCLUDING THE BAHAMAS" + \
                   #"%s\n" % self._timeLabel + "\n" + \
                   #synopsis2 + "\n$$\n\n"
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
            if areasLeft == 9:
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

    # SampleAnalysis overrides
    def moderated_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
        if self._includeTropical:
            dict["Wind"] = (0, 0)
            dict["WindGust"] = (0, 15)
            dict["WaveHeight"] = (10, 0)
            dict["Swell"] = (0, 15)
        else:
            dict["Wind"] = (0, 15)
            dict["WindGust"] = (0, 15)
            dict["WaveHeight"] = (10, 0)
            dict["Swell"] = (0, 15)
#        dict["Wind"] =  (0, 3)
#        dict["WaveHeight"] = (5,5)
        return dict

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] =  1 # Changed to 1 (from 2) by JL/1/31/12 for testing
        #dict["WindWaveHgt"] =  2
        dict["Wind"] = 5 # Changed to 5 (from 10) by JL/1/31/12 for testing
        dict["WindGust"] = 120
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
        dict["WaveHeight"] =  "seas 1 ft or less"
        #dict["WindWaveHgt"] =  "seas 1 ft or less"
        dict["Wind"] =  "VARIABLE WINDS LESS THAN 5 KT"
        dict["Swell"] =  ""
        return dict

    def null_phrase_dict(self, tree, node):
        # Phrase to use for null values in subPhrases other than the first
        # Can be an empty string
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "1 FT OR LESS"
        #dict["WindWaveHgt"] =  "1 feet or less"
        dict["Wind"] =  "VARIABLE LESS THAN 5 KT"
        dict["Wx"] =  ""
        dict["Swell"] =  "light"
        dict["hurricane force winds to"] =  "hurricane force winds to"
        dict["storm force winds to"] = "storm force winds to"
        dict["gales to"] =  "gales to"
        dict["up to"] =  "VARIABLE WINDS LESS THAN 5 KT"
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

        dict["WaveHeight"] = {
            (1, 3): 1, # changed from 0 to 1 JL/1/31/12
            (3, 7): 2,
            (7, 10): 3,
            (10, 20): 5,
            (20, 200): 10,
            "default": 5,
            }
        dict["Swell"] = 5
        dict["Swell2"] = 5
        #dict["WaveHeight"] = 2
        #dict["WindWaveHgt"] = 2
        return dict

    # added to force ranges for sea heights with tropical turned on 9/7/11 CNJ/JL
    def minimum_range_nlValue_dict(self, tree, node):
        # This threshold is the "smallest" min/max difference allowed between values reported.
        # For example, if threshold is set to 5 for "MaxT", and the min value is 45
        # and the max value is 46, the range will be adjusted to at least a 5 degree
        # range e.g. 43-48.  These are the values that are then submitted for phrasing
        # such as:
        dict = TextRules.TextRules.minimum_range_nlValue_dict(self, tree, node)
        #   HIGHS IN THE MID 40S
        if self._includeTropical:
            dict["WaveHeight"] = {(1, 3): 1, # changed from 0 to 1 JL/1/31/12
                                  (3, 7): 2,
                                  (7, 10): 3,
                                  (10, 20): 5,
                                  (20, 200): 10,
                                  "default": 5,
                                  }
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
                         "otherwise": "...becoming ",
                         }
        return dict

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
            "Wind": 4,
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
            "WaveHeight": 3, # feet - changed from 2.5 to 2 - JL/1/31/12
                             # feet - changed from 2 to 3 - EC/4/20/12 Seems to correct "SEAS 1 FOOT...BUILDING TO 2 TO 3 FT IN AFTERNOON" issues.
            #"WindWaveHgt": 5, # feet
            }

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


                    #added by JRL 10/14/11
#    def gust_wind_difference_nlValue(self, tree, node):
#        # Difference between gust and maxWind below which gusts are not
#        # mentioned. Units are MPH
#
#        if self._includeTropical:
#            return 5
#        else:
#            return 10
#
#    def temporalCoverage_hours(self, parmHisto, timeRange, componentName):
#        # COMMENT: At WFO MFL we use 3 hrly wind grids. If you use 1 hrly wind grids
#        # and this parameter is 2 or higher, tropical cyclone winds affecting the very
#        # early or latter part of a forecast period might be neglected. 1 assures
#        # maximum sensitivity.
#
#        # CJ commented out
###        if self._includeTropical:
###            return 1
###        else:
###            return 0
#
#        return 1
#
#    def temporalCoverage_hours_dict(self, parmHisto, timeRange, componentName):
#        # This is the temporalCoverage_hours specified per weather element.
#        # Used by temporalCoverage_flag
#        return {
#                "PoP": 2.0,
#                "Wx": 2.0,
#                "Wind": 3,
#                "Swell": 3,
#                "pws34": 4,
#                "pws64": 4,
#                "pwsD34": 4,
#                "pwsN34": 4,
#                "pwsD64": 4,
#                "pwsN64": 4,
#                }
#
##    def _Text3(self):
##        synopsis = ""
##        if self._definition["pil"] == "OFFNT3":
##            productID = "MIAOFFNT3"
##            # Can't just search for "SYNOPSIS"
##            # It will only return the first one it finds
##            entire_product = string.strip(self.getPreviousProduct(productID))
##            # get just the second synopsis from it's area "AMZ088"
##            # then split on "$$" and grab everything before the $$ at the end of the synopsis
##            # Then split on a blank line and grab the second paragraph
##            synopsis = entire_product.split("AMZ088")[1].split("$$")[0].split("\n\n")[1]
##            #  Clean up the previous synopsis
##            synopsis = re.sub(r'\n', r' ', synopsis)
##            synopsis = self.endline(synopsis, linelength=66, breakStr=" ")
##            return "%s\n" %  "\n" + \
##                    synopsis + ""
##        else:
##            pass
#
#    # Inserted since NHC has this
#    def addTropical(self, analysisList, phraseList, includeHazards=True):
#        self.debug_print("Debug: addTropical in OFF_ONA_Overrides")
#
#        newAnalysisList = []
#        for entry in analysisList:
#            #  Sampling defined as a tuple (field, statistic, temporal rate)
#            #  If this is NOT a Wind or WindGust statistic
#            if entry[0] not in ["Hazards", "Wind", "WindGust", "WaveHeight", "Swell"]:
#                #  Add this statistic to the new analysisList
#                newAnalysisList.append(entry)
#        newAnalysisList += [
#                ("Wind", self.vectorModeratedMinMax, [6]),
#                ("WindGust", self.moderatedMinMax, [6]),
#                ("WaveHeight", self.moderatedMinMax, [6]),
#                ("Swell", self.vectorModeratedMinMax, [6]),
#                ("pws34", self.maximum),
#                ("pws64", self.maximum),
#                ("pwsN34", self.maximum),
#                ("pwsN64", self.maximum),
#                ("pwsD34", self.maximum),
#                ("pwsD64", self.maximum),
#                ]
#        if includeHazards:
#            newAnalysisList.append(("Hazards", self.discreteTimeRangesByKey))
#
#        phraseList.insert(0, self.pws_phrase)
#        return newAnalysisList, phraseList
#
#########################################
###### added section below for a1 to a2 variances JRL/01/26/12
#########################################
#
#    def moderated_dict(self, parmHisto, timeRange, componentName):
#        # This dictionary defines the low and high limit at which
#        # outliers will be removed when calculating moderated stats.
#        # By convention the first value listed is the percentage
#        # allowed for low values and second the percentage allowed
#        # for high values.
#        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
#        if self._includeTropical:
#            dict["Wind"] = (0, 0)
#            dict["WindGust"] = (0, 15)
#            dict["WaveHeight"] = (10, 10)
#            dict["Swell"] = (0, 15)
#        else:
#            dict["Wind"] = (0, 15)
#            dict["WindGust"] = (0, 15)
#            dict["WaveHeight"] = (10, 10)
#            dict["Swell"] = (0, 15)
#        return dict
#
#    def null_nlValue_dict(self, tree, node):
#        # Threshold below which values are considered "null" and  not reported.
#        # Units depend on the element and product
#        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
#        dict["WaveHeight"] =  1
#        #dict["WindWaveHgt"] =  2
#        dict["Wind"] = 5
#        dict["WindGust"] = 120
#        dict["Swell"] =  5
#        dict["Visibility"] = 5 # in nautical miles. Report if less than this value.
#        return dict
#
#    # ConfigVariables Overrides
#    def phrase_descriptor_dict(self, tree, node):
#        # Descriptors for phrases
#        dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
#        dict["Wind"] = "winds"
#        dict["WaveHeight"] = "seas"
#        dict["seas"] = "seas"
#        dict["mixed swell"] = "mixed swell"
#        dict["waves"] = "seas"
#        dict["dominant period"] = "dominant period"
#        # Apply only if marine_wind_flag (see above) is set to 1:
#        dict["hurricane force winds to"] =  "hurricane force winds to"
#        dict["storm force winds to"] = "storm force winds to"
#        dict["gales to"] =  "gales to"
#        dict["up to"] =  "LESS THAN"
#        dict["around"] = ""
#        # Used for Tropical
#        dict["iminHR"] = "HURRICANE CONDITIONS"
#        dict["iminTS"] = "TROPICAL STORM CONDITIONS"
#        dict["iminTSposHR"] = "TROPICAL STORM CONDITIONS WITH HURRICANE CONDITIONS POSSIBLE"
#        dict["posTS"] = "TROPICAL STORM CONDITIONS POSSIBLE"
#        dict["posTSbcmgposHR"] = "TROPICAL STORM CONDITIONS POSSIBLE WITH HURRICANE CONDITIONS ALSO POSSIBLE"
#        dict["expTS"] = "TROPICAL STORM CONDITIONS EXPECTED"
#        dict["posHR"] = "HURRICANE CONDITIONS POSSIBLE"
#        dict["expHR"] = "HURRICANE CONDITIONS EXPECTED"
#        dict["expTSposHR"] = "TROPICAL STORM CONDITIONS EXPECTED WITH HURRICANE CONDITIONS POSSIBLE"
#        dict["posTSorHR"] = "TROPICAL STORM OR HURRICANE CONDITIONS POSSIBLE"
#        return dict
#
#    def first_null_phrase_dict(self, tree, node):
#        # Phrase to use if values THROUGHOUT the period or
#        # in the first period are Null (i.e. below threshold OR NoWx)
#        # E.g.  LIGHT WINDS.    or    LIGHT WINDS BECOMING N 5 MPH.
#        dict = TextRules.TextRules.first_null_phrase_dict(self, tree, node)
#        dict["WaveHeight"] =  "seas 1 ft or less"
##        dict["WindWaveHgt"] =  "seas 2 ft or less"
#        dict["Wind"] =  "VARIABLE WINDS LESS THAN 5 KT"
#        dict["Swell"] =  ""
#        return dict
#
#    def null_phrase_dict(self, tree, node):
#        # Phrase to use for null values in subPhrases other than the first
#        # Can be an empty string
#        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
#        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
#        dict["WaveHeight"] =  "1 ft or less"
##        dict["WindWaveHgt"] =  "2 feet or less"
#        dict["Wind"] =  "VARIABLE LESS THAN 5 KT"
#        dict["Wx"] =  ""
#        dict["Swell"] =  "light"
#        dict["hurricane force winds to"] =  "hurricane force winds to"
#        dict["storm force winds to"] = "storm force winds to"
#        dict["gales to"] =  "gales to"
#        dict["up to"] =  "VARIABLE WINDS LESS THAN 5 KT"
#        return dict
#
#    # added by JRL 11/05
#    def maximum_range_nlValue_dict(self, tree, node):
#        # Maximum range to be reported within a phrase
#        #   e.g. 5 to 10 mph
#        # Units depend on the product
#        dict = TextRules.TextRules.maximum_range_nlValue_dict(self, tree, node)
#        #-----------------------------------------------------------------------
#        # COMMENT: Override max ranges for certain fields
#        # This dict specifications allows for wind speed ranges of up to 20 mph
#        # during tropical cyclone situations allowing for far better wind speed
#        # phrases.
#        #-----------------------------------------------------------------------
#        if self._includeTropical:
#            dict["Wind"] = {'default': 5,
#                            (0.0, 4.0): 0,
#                            (4.0, 33.0): 5,
#                            (33.0, 52.0): 10,
#                            (52.0, 200.0): 20,
#                            }
#        else:
#            dict["Wind"] = {
#            (0,25):5,
#            (25,50):10,
#            (50,200):25,
#            "default":10,
#            }
#
#        dict["WaveHeight"] = {
#            (0,3):1,
#            (3,7):2,
#            (7,10):3,
#            (10,20):5,
#            (20,200):10,
#            "default":5,
#            }
#        dict["Swell"] = 5
#        dict["Swell2"] = 5
#        #dict["WaveHeight"] = 2
#        dict["WindWaveHgt"] = 2
#        return dict
#
#    # added to force ranges for sea heights with tropical turned on 9/7/11 CNJ/JL
#    def minimum_range_nlValue_dict(self, tree, node):
#        # This threshold is the "smallest" min/max difference allowed between values reported.
#        # For example, if threshold is set to 5 for "MaxT", and the min value is 45
#        # and the max value is 46, the range will be adjusted to at least a 5 degree
#        # range e.g. 43-48.  These are the values that are then submitted for phrasing
#        # such as:
#        dict = TextRules.TextRules.minimum_range_nlValue_dict(self, tree, node)
#        #   HIGHS IN THE MID 40S
#        if self._includeTropical:
#            dict["WaveHeight"] = {(0,3):1,
#                                  (3,7):2,
#                                  (7,10):3,
#                                  (10,20):5,
#                                  (20,200):10,
#                                  "default":5,
#                                  }
#        return dict
#
#    def phrase_connector_dict(self, tree, node):
#        # Dictionary of connecting phrases for various
#        # weather element phrases
#        # The value for an element may be a phrase or a method
#        # If a method, it will be called with arguments:
#        #   tree, node
#        dict = TextRules.TextRules.phrase_connector_dict(self, tree, node)
#        dict["rising to"] =  {
#                                "Wind": "...INCREASING to ",
#                                "Swell": "...building to ",
#                                "Swell2": "...building to ",
#                                "WaveHeight": "...building to ",
#                                "WindWaveHgt": "...building to ",
#                         }
#
#        dict["easing to"] =  {
#                                "Wind": "...diminishing to ",
#                                "Swell": "...subsiding to ",
#                                "Swell2": "...subsiding to ",
#                                "WaveHeight": "...subsiding to ",
#                                "WindWaveHgt": "...subsiding to ",
#                         }
#        dict["backing"] =  {
#                                "Wind": "...becoming ",
#                                "Swell": "...becoming ",
#                                "Swell2": "...becoming ",
#                                "WaveHeight": "...becoming ",
#                                "WindWaveHgt": "...becoming ",
#                         }
#
#        dict["veering"] =  {
#                                "Wind": "...becoming  ",
#                                "Swell": "...becoming ",
#                                "Swell2": "...becoming ",
#                                "WaveHeight": "...becoming ",
#                                "WindWaveHgt": "...becoming ",
#                         }
#
#        dict["becoming"] =  "...becoming "
#        dict["increasing to"] =  {
#                                "Wind":  "...INCREASING to ",
#                                "Swell": "...building to ",
#                                "Swell2": "...building to ",
#                                "WaveHeight": "...building to ",
#                                "WindWaveHgt": "...building to ",
#                             }
#
#        dict["decreasing to"] =  {
#                                "Wind":  "...diminishing to ",
#                                "Swell": "...subsiding to ",
#                                "Swell2": "...subsiding to ",
#                                "WaveHeight": "...subsiding to ",
#                                "WindWaveHgt": "...subsiding to ",
#                             }
#
#        dict["shifting to the"] =  {
#                                  "Wind":  "...shifting ",
#                                  "Swell": "...becoming ",
#                                  "Swell2": "...becoming ",
#                                  "WaveHeight": "...becoming ",
#                                  "WindWavHgt": "...becoming ",
#                             }
##        dict["shifting to the"] =  "...shifting "
#        dict["becoming onshore"] =  " becoming onshore "
#        dict["then"] =  {"Wx": ". ",
#                         "Vector": "...becoming ",
#                         "Scalar": "...becoming ",
#                         "otherwise": "...becoming ",
#                         }
#        return dict
#
#    def vector_mag_difference_nlValue_dict(self, tree, node):
#        # Replaces WIND_THRESHOLD
#        # Magnitude difference.  If the difference between magnitudes
#        # for sub-ranges is greater than or equal to this value,
#        # the different magnitudes will be noted in the phrase.
#        # Units can vary depending on the element and product
#        return  {
#            "Wind": 4,
#            "Swell": 1,  # ft
#            "Swell2": 1,  # ft
#            }
#
#    def vector_dir_difference_dict(self, tree, node):
#        # Replaces WIND_DIR_DIFFERENCE
#        # Direction difference.  If the difference between directions
#        # for sub-ranges is greater than or equal to this value,
#        # the different directions will be noted in the phrase.
#        # Units are degrees
#        return {
#            "Wind": 90, # degrees
#            "Swell":60, # degrees
#            "Swell2":60, # degrees
#            }
#
#    def element_outUnits_dict(self, tree, node):
#        dict = TextRules.TextRules.element_outUnits_dict(self, tree, node)
#        dict["Visibility"] = "NM"
#        return dict
#
###    #Modified from OFF base
###    # THIS IS THE OPC ORIGINAL WHICH IS NOT WORKING FOR TROPICAL WORDING
###    def OFFPeriod(self):
###        self.debug_print("Debug: OFFPeriod in OFF_ONA_Overrides")
###
###
###        return {
###            "type": "component",
###            "methodList": [
###                          self.consolidateSubPhrases,
###                          self.assemblePhrases,
###                          self.wordWrap,
###                          ],
###
###            "analysisList": [
###                      # NOTE: Choose from the following analysis options.
###                      # Do not remove the "vectorMinMax" analysis for
###                      # "Wind". This is necessary to get an absolute max if
###                      # the useWindsForGusts flag is on.
###
###                      # Use the following if you want moderated ranges
###                      # (e.g. N WIND 10 to 20 KT)
###                      # Set the moderating percentage in the "moderated_dict"
###                      # dictionary module.
###                      # Set the maximum range values in the "maximum_range_nlValue_dict"
###                      # dictionary module.
###                         # ("Wind", self.vectorModeratedMinMax, [6]),
###                          ("Wind", self.vectorMinMax, [6]),
###                         # ("WindGust", self.moderatedMax, [3]),
###                          ("WaveHeight", self.minMax, [6]),
###                         # ("WindWaveHgt", self.moderatedMinMax, [6]),
###                         # ("Swell", self.vectorModeratedMinMax, [6]),
###                         # ("Swell2", self.vectorModeratedMinMax, [6]),
###                         # ("Period", self.moderatedMinMax, [6]),
###                         # ("Period2", self.moderatedMinMax, [6]),
###                          ("Wx", self.rankedWx, [6]),
###                         # ("T", self.minMax),
###                         # ("PoP", self._PoP_analysisMethod("OFFPeriod"), [6]),
###                         # ("PoP", self.binnedPercent, [6]),
###
###                      # Use the following if you want moderated
###                      # single values (e.g. N WIND 20 KT).
###                      # Set the moderating percentage in the "moderated_dict"
###                      # dictionary module.
###                      # NOTE:  If you use these methods, include and uncomment
###                      # the "combine_singleValues_flag_dict" in your Local file (see below)
###                         #("Wind", self.vectorModeratedMax, [3]),
###                          #("Wind", self.vectorMinMax, [12]),
###                          #("WindGust", self.moderatedMax, [3]),
###                          #("WaveHeight", self.moderatedMax, [6]),
###                          #("WindWaveHgt", self.moderatedMax, [6]),
###                          #("Swell", self.vectorModeratedMax, [6]),
###                          #("Swell2", self.vectorModeratedMax, [6]),
###                          #("Period", self.moderatedMax, [6]),
###                          #("Period2", self.moderatedMax, [6]),
###                          #("Wx", self.rankedWx, [6]),
###                          #("T", self.minMax),
###                          #("PoP", self._PoP_analysisMethod("OFFPeriod")),
###                          #("PoP", self.binnedPercent, [6]),
###
###                      # Use the following if you want absolute ranges.
###                      # Set the maximum range values in the "maximum_range_nlValue_dict"
###                      # dictionary module.
###                          # Split time range in quarters for Wind and WindGust
###                          #("Wind", self.vectorMinMax, [3]),
###                          #("Wind", self.vectorMinMax, [12]),
###                          #("WindGust", self.maximum, [3]),
###                          #("WaveHeight", self.minMax, [6]),
###                          #("WindWaveHgt", self.minMax, [6]),
###                          # Split time range in half for Wx and Swell
###                          #("Swell", self.vectorMinMax, [6]),
###                          #("Swell2", self.vectorMinMax, [6]),
###                          #("Period", self.avg, [6]),
###                          #("Period2", self.avg, [6]),
###                          #("Wx", self.rankedWx, [6]),
###                          #("T", self.minMax),
###                          #("PoP", self._PoP_analysisMethod("OFFPeriod")),
###                          #("PoP", self.binnedPercent, [6]),
###                        ],
###
###            "phraseList":  [
###                           # WINDS
###                            (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
####                           (self.marine_wind_phrase,self._windLocalEffects_list()),
###                           # Alternative:
####                           (self.marine_wind_phrase,self._windLocalEffects_list()),
####                           self.marine_wind_phrase,
###                           #self.gust_phrase,
###                           # WAVES
###                           #self.wave_withPeriods_phrase,
###                           # Alternative:
###                           #self.wave_phrase,
###                           # SWELLS AND PERIODS
###                           #self.swell_withPeriods_phrase,
###                           # Alternative:
###                           #self.swell_phrase,
###                           #self.period_phrase,
###                           # WEATHER
####                           self.weather_phrase,
###
####                           self.weather_phrase,
###                           (self.wave_phrase,self._WaveHeightLocalEffects_list),
###
###                           self.weather_phrase,
###                           self.visibility_phrase,
###                           ],
###            "intersectAreas":[
###                            #Areas listed by weather element that will be
###                            #intersected with the current area then
###                            #sampled and analyzed.
###                            #E.g. used in local effects methods.
###                            ("Wind", ["GlfofME_NW", "GlfofME_SE", "GeoBnk_NW", "GeoBnk_SE", "SofNE_Wof70W", "SofNE_Eof70W", "HudtoBalt_NW", "HudtoBalt_SE", "BalttoHag_Wof70W", "BalttoHag_Eof70W", "BalttoHat_Eof1000FM", "BalttoHat_Wof1000FM", "HattoCapeFear_Eof75W", "HattoCapeFear_Wof75W", "CapeFearto31N_Eof1000FM", "CapeFearto31N_Wof1000FM"]),
###                            ("WaveHeight", ["GlfofME_NW", "GlfofME_SE", "GeoBnk_NW", "GeoBnk_SE", "SofNE_Wof70W", "SofNE_Eof70W", "HudtoBalt_NW", "HudtoBalt_SE", "BalttoHag_Wof70W", "BalttoHag_Eof70W", "BalttoHat_Eof1000FM", "BalttoHat_Wof1000FM", "HattoCapeFear_Eof75W", "HattoCapeFear_Wof75W", "CapeFearto31N_Eof1000FM", "CapeFearto31N_Wof1000FM"]),
###                            ("Weather", ["GlfofME_NW", "GlfofME_SE", "GeoBnk_NW", "GeoBnk_SE", "SofNE_Wof70W", "SofNE_Eof70W", "HudtoBalt_NW", "HudtoBalt_SE", "BalttoHag_Wof70W", "BalttoHag_Eof70W", "BalttoHat_Eof1000FM", "BalttoHat_Wof1000FM", "HattoCapeFear_Eof75W", "HattoCapeFear_Wof75W", "CapeFearto31N_Eof1000FM", "CapeFearto31N_Wof1000FM"]),
###                                ]
###                }

#    # Adapted from NHC's OFF_NH2_NT4_Overrride
#    def OFFPeriod(self):
#        self.debug_print("Debug: OFFPeriod in OFF_NH2_Overrides")
#
#        analysisList = [
#                      # NOTE: Choose from the following analysis options.
#                      # Do not remove the "vectorMinMax" analysis for
#                      # "Wind". This is necessary to get an absolute max if
#                      # the useWindsForGusts flag is on.
#
#                      # Use the following if you want moderated ranges
#                      # (e.g. N WIND 10 to 20 KT)
#                      # Set the moderating percentage in the "moderated_dict"
#                      # dictionary module.
#                      # Set the maximum range values in the "maximum_range_nlValue_dict"
#                      # dictionary module.
#                          ("Wind", self.vectorModeratedMinMax, [6]),
#                         # ("Wind", self.vectorMinMax, [6]),
#                          ("WindGust", self.moderatedMax, [3]),
#                          ("WaveHeight", self.moderatedMinMax, [6]),
#                          #("WindWaveHgt", self.moderatedMinMax, [6]),
#                          #("Swell", self.vectorModeratedMinMax, [6]),
#                          #("Swell2", self.vectorModeratedMinMax, [6]),
#                          #("Period", self.moderatedMinMax, [6]),
#                          #("Period2", self.moderatedMinMax, [6]),
#                          ("Wx", self.rankedWx, [12]),
#                         # ("T", self.minMax),
#                         # ("PoP", self._PoP_analysisMethod("OFFPeriod"), [6]),
#                         # ("PoP", self.binnedPercent, [6]),
#
#                      # Use the following if you want moderated
#                      # single values (e.g. N WIND 20 KT).
#                      # Set the moderating percentage in the "moderated_dict"
#                      # dictionary module.
#                      # NOTE:  If you use these methods, include and uncomment
#                      # the "combine_singleValues_flag_dict" in your Local file (see below)
#                         #("Wind", self.vectorModeratedMax, [3]),
#                          #("Wind", self.vectorMinMax, [12]),
#                          #("WindGust", self.moderatedMax, [3]),
#                          #("WaveHeight", self.moderatedMax, [6]),
#                          #("WindWaveHgt", self.moderatedMax, [6]),
#                          #("Swell", self.vectorModeratedMax, [6]),
#                          #("Swell2", self.vectorModeratedMax, [6]),
#                          #("Period", self.moderatedMax, [6]),
#                          #("Period2", self.moderatedMax, [6]),
#                          #("Wx", self.rankedWx, [6]),
#                          #("T", self.minMax),
#                          #("PoP", self._PoP_analysisMethod("OFFPeriod")),
#                          #("PoP", self.binnedPercent, [6]),
#
#                      # Use the following if you want absolute ranges.
#                      # Set the maximum range values in the "maximum_range_nlValue_dict"
#                      # dictionary module.
#                          # Split time range in quarters for Wind and WindGust
#                          #("Wind", self.vectorMinMax, [3]),
#                          #("Wind", self.vectorMinMax, [12]),
#                          #("WindGust", self.maximum, [3]),
#                          #("WaveHeight", self.minMax, [6]),
#                          #("WindWaveHgt", self.minMax, [6]),
#                          # Split time range in half for Wx and Swell
#                          #("Swell", self.vectorMinMax, [6]),
#                          #("Swell2", self.vectorMinMax, [6]),
#                          #("Period", self.avg, [6]),
#                          #("Period2", self.avg, [6]),
#                          #("Wx", self.rankedWx, [6]),
#                          #("T", self.minMax),
#                          #("PoP", self._PoP_analysisMethod("OFFPeriod")),
#                          #("PoP", self.binnedPercent, [6]),
#                        ]
#
#        phraseList = [
#                           # WINDS
##                           (self.marine_wind_withGusts_phrase, self._windLocalEffects_list()),
#                            # J.Lewitsky/NHC 04/15/11 uncommented line below to include Local Effects
#                           (self.marine_wind_withGusts_phrase,self._windLocalEffects_list()),
#                            #CJ try to remove local effects phrase
##                           self.marine_wind_phrase,
#                           # Alternative:
##                           (self.marine_wind_phrase, self._windLocalEffects_list()),
##                           self.marine_wind_phrase,
#                           #self.gust_phrase,
#                           # WAVES
#                           #self.wave_withPeriods_phrase,
#                           # Alternative:
#                           #self.wave_phrase,
#                           # SWELLS AND PERIODS
#                           #self.swell_withPeriods_phrase,
#                           # Alternative:
#                           #self.swell_phrase,
#                           #self.period_phrase,
#                           # WEATHER
##                           self.weather_phrase,
#
##                           self.weather_phrase,
#                           #CJ try to remove local effects phrase
#                           (self.wave_phrase,self._WaveHeightLocalEffects_list),
#                           #self.wave_phrase,
#
#                           self.weather_phrase,
#                           self.visibility_phrase,
#                           ]
#
#        # CJ Added 2011-07-26
#        # fta 9/9/11 removed _ in lines 385, 387, 390. self._include Tropical is always true (from a logic pov), even if set to "No"
#        try:
#                self.includeTropical = self._includeTropical == "Yes"
#        except:
#                self.includeTropical = False
#
#        # Tropical occurring all the time now if above not active
#        if self.includeTropical:
#                analysisList, phraseList = self.addTropical(analysisList, phraseList)
#
#
#        return {
#                "type": "component",
#                "methodList": [
#                        self.consolidateSubPhrases,
#                        self.assemblePhrases,
#                        self.wordWrap,
#                        ],
#
#                "analysisList": analysisList,
#                "phraseList": phraseList,
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
                          ("WindGust", self.moderatedMax, [3]),
                          ("WaveHeight", self.moderatedMinMax, [6]),
                         # ("WindWaveHgt", self.moderatedMinMax, [6]),
                         # ("Swell", self.vectorModeratedMinMax, [6]),
                         # ("Swell2", self.vectorModeratedMinMax, [6]),
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
                          "le_amz031_colombian_coast",
                          "le_amz031_main",
                          "le_amz033_s_of_13n_w_of_68w",
                          "le_amz033_main",
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
                                "le_gmz023_s_of_21n_w_of_95w",
                                #"le_gmz023_60nm_of_veracruz",
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
                                "le_amz023_mona_swell",
                                "le_amz023_main_swell",
                                #"le_amz025_anegada",
                                "le_amz025_atlc_exposures_and_passages",
                                "le_amz025_main",
                                "le_amz029_nicaraguan_coast",
                                "le_amz029_main",
                                "le_amz031_colombian_coast",
                                "le_amz031_main",
                                "le_amz033_s_of_13n_w_of_68w",
                                "le_amz033_main",
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
        leArea1 = self.LocalEffectArea("le_gmz013_main", " E OF 90W")
        leArea2 = self.LocalEffectArea("le_gmz013_w_of_90w", "W OF 90W")
        leArea3 = self.LocalEffectArea("le_gmz015_main", " N OF 27N")
        leArea4 = self.LocalEffectArea("le_gmz015_s_of_27n", "S OF 27N")
        leArea5 = self.LocalEffectArea("le_gmz017_main", " E OF 96W")
        leArea6 = self.LocalEffectArea("le_gmz017_w_of_96w", "W OF 96W")
        leArea7 = self.LocalEffectArea("le_gmz019_main", " N OF 24N")
        leArea8 = self.LocalEffectArea("le_gmz019_s_of_24n", "S OF 24N")
        leArea9 = self.LocalEffectArea("le_gmz021_main", "ELSEWHERE")
        leArea10 = self.LocalEffectArea("le_gmz021_straits_of_florida", "STRAITS OF FLORIDA")
        leArea11 = self.LocalEffectArea("le_gmz023_main", "ELSEWHERE")
        leArea12 = self.LocalEffectArea("le_gmz023_s_of_21n_w_of_95w", "S OF 21N W OF 95W")
        #leArea12 = self.LocalEffectArea("le_gmz023_60nm_of_veracruz", "WITHIN 60 NM OF COAST OF VERACRUZ")
        leArea13 = self.LocalEffectArea("le_gmz025_main", "ELSEWHERE")
        leArea14 = self.LocalEffectArea("le_gmz025_60nm_of_campeche", "WITHIN 60 NM OF COAST OF CAMPECHE")
        #leArea15 = self.LocalEffectArea("le_gmz025_s_of_19n", "S OF 19N")
        leArea16 = self.LocalEffectArea("le_amz011_main", "ELSEWHERE")
        leArea17 = self.LocalEffectArea("le_amz011_yucatan_channel", "IN YUCATAN CHANNEL")
        leArea18 = self.LocalEffectArea("le_amz013_main", "ELSEWHERE")
        leArea19 = self.LocalEffectArea("le_amz013_cuba_jamaica", "BETWEEN CUBA AND JAMAICA")
        leArea20 = self.LocalEffectArea("le_amz021_main", " E OF 77W")
        leArea21 = self.LocalEffectArea("le_amz021_w_of_77w", "W OF 77W")
        leArea22 = self.LocalEffectArea("le_amz023_main_swell", "ELSEWHERE")
        leArea23 = self.LocalEffectArea("le_amz023_mona_swell", "IN MONA PASSAGE")
        leArea24 = self.LocalEffectArea("le_amz025_main", "ELSEWHERE")
        leArea25 = self.LocalEffectArea("le_amz025_atlc_exposures_and_passages", "IN ATLANTIC EXPOSURES AND PASSAGES")
       # leArea26 = self.LocalEffectArea("le_amz025_atlantic", "ATLANTIC EXPOSURES")
        leArea27 = self.LocalEffectArea("le_amz029_main", "ELSEWHERE")
        leArea28 = self.LocalEffectArea("le_amz029_nicaraguan_coast", "WITHIN 60 NM OF COAST OF NICARAGUA")
        leArea29 = self.LocalEffectArea("le_amz031_main", "ELSEWHERE")
        leArea30 = self.LocalEffectArea("le_amz031_colombian_coast", "WITHIN 90 NM OF COAST OF COLOMBIA")
        leArea31 = self.LocalEffectArea("le_amz033_main", "ELSEWHERE")
        leArea32 = self.LocalEffectArea("le_amz033_s_of_13n_w_of_68w", "S OF 13N W OF 68W")
        leArea33 = self.LocalEffectArea("le_amz035_main", "ELSEWHERE")
        leArea34 = self.LocalEffectArea("le_amz035_atlantic", "ATLANTIC EXPOSURES")
        leArea35 = self.LocalEffectArea("le_amz037_main", " N OF 10N")
        leArea36 = self.LocalEffectArea("le_amz037_s_of_10n", "S OF 10N")
        leArea37 = self.LocalEffectArea("le_amz039_main", " N OF 10N")
        leArea38 = self.LocalEffectArea("le_amz039_s_of_10n", "S OF 10N")
        #leArea38 = self.LocalEffectArea("le_amz039_w_of_80w", "W OF 80W")
        leArea39 = self.LocalEffectArea("le_amz111_main", "ELSEWHERE")
        leArea40 = self.LocalEffectArea("le_amz111_n_of_29n_w_of_79w", "N OF 29N W OF 79W")
        leArea41 = self.LocalEffectArea("le_amz113_main", " S OF 29N")
        leArea42 = self.LocalEffectArea("le_amz113_n_of_29n", "N OF 29N")
        leArea43 = self.LocalEffectArea("le_amz115_main", " S OF 29N")
        leArea44 = self.LocalEffectArea("le_amz115_n_of_29n", "N OF 29N")
        leArea45 = self.LocalEffectArea("le_amz117_main", "ELSEWHERE")
        leArea46 = self.LocalEffectArea("le_amz117_atlc_exposures", "ATLANTIC EXPOSURES")
        leArea47 = self.LocalEffectArea("le_amz119_main", " S OF 25N")
        leArea48 = self.LocalEffectArea("le_amz119_n_of_25n", "N OF 25N")
        leArea49 = self.LocalEffectArea("le_amz121_main", " S OF 25N")
        leArea50 = self.LocalEffectArea("le_amz121_n_of_25n", "N OF 25N")
        leArea51 = self.LocalEffectArea("le_amz127_main", " W OF 60W")
        leArea52 = self.LocalEffectArea("le_amz127_e_of_60w", "E OF 60W")
        leArea53 = self.LocalEffectArea("le_amz017_main", "ELSEWHERE")
        leArea54 = self.LocalEffectArea("le_amz017_s_of_17n_w_of_87w", "S OF 17N W OF 87W")

        return [self.LocalEffect([leArea1, leArea2], 2, " E OF 90W...AND "),
                #[self.LocalEffect([leArea1, leArea2], 2, "...EXCEPT "),
                # Changed "...EXCEPT " TO "E OF 90W AND ". Renders "SEAS x TO x FT E OF 90W AND x TO x FT W OF 90W" EC - 4/20/12
                #self.LocalEffect([leArea2, leArea1], 2, ". ELSEWHERE..."),
                # Tried the entry above to put leArea first then ELSEWHERE - JL/NHC - 02/12/12
                self.LocalEffect([leArea3, leArea4], 2, " N OF 27N...AND "),
                self.LocalEffect([leArea5, leArea6], 2, " E OF 96W...AND "),
                self.LocalEffect([leArea7, leArea8], 2, " N OF 24N...AND "),
                self.LocalEffect([leArea10, leArea9], 2, "...AND "),
                self.LocalEffect([leArea12, leArea11], 2, "...AND "),
                self.LocalEffect([leArea14, leArea13], 2, "...AND "), # removed leArea15
                self.LocalEffect([leArea17, leArea16], 2, "...AND "),
                self.LocalEffect([leArea19, leArea18], 2, "...AND "),
                self.LocalEffect([leArea20, leArea21], 2, " E OF 77W...AND "),
                self.LocalEffect([leArea23, leArea22], 2, "...AND "),
                self.LocalEffect([leArea25, leArea24], 2, "...AND "),
                self.LocalEffect([leArea28, leArea27], 2, "...AND "),
                self.LocalEffect([leArea30, leArea29], 2, "...AND "),
                self.LocalEffect([leArea32, leArea31], 2, "...AND "),
                self.LocalEffect([leArea34, leArea33], 2, "...AND "),
                self.LocalEffect([leArea35, leArea36], 2, " N OF 10N...AND "),
                self.LocalEffect([leArea37, leArea38], 2, " ...AND "),
                self.LocalEffect([leArea40, leArea39], 2, "...AND "),
                self.LocalEffect([leArea41, leArea42], 2, " S OF 29N...AND "),
                self.LocalEffect([leArea43, leArea44], 2, " S OF 29N...AND "),
                self.LocalEffect([leArea46, leArea45], 2, "...AND "),
                self.LocalEffect([leArea47, leArea48], 2, " S OF 25N...AND "),
                self.LocalEffect([leArea49, leArea50], 2, " S OF 25N...AND "),
                self.LocalEffect([leArea51, leArea52], 2, " W OF 60W...AND "),
                self.LocalEffect([leArea54, leArea53], 2, "...AND "),
                ]

    def _windLocalEffects_list(self):
        leArea1 = self.LocalEffectArea("le_gmz013_main", " E OF 90W")
        leArea2 = self.LocalEffectArea("le_gmz013_w_of_90w", "W OF 90W")
        leArea3 = self.LocalEffectArea("le_gmz015_main", " N OF 27N")
        leArea4 = self.LocalEffectArea("le_gmz015_s_of_27n", "S OF 27N")
        leArea5 = self.LocalEffectArea("le_gmz017_main", " E OF 96W")
        leArea6 = self.LocalEffectArea("le_gmz017_w_of_96w", "W OF 96W")
        leArea7 = self.LocalEffectArea("le_gmz019_main", " N OF 24N")
        leArea8 = self.LocalEffectArea("le_gmz019_s_of_24n", "S OF 24N")
        leArea9 = self.LocalEffectArea("le_gmz021_main", "ELSEWHERE")
        leArea10 = self.LocalEffectArea("le_gmz021_straits_of_florida", "STRAITS OF FLORIDA")
        leArea11 = self.LocalEffectArea("le_gmz023_main", "ELSEWHERE")
        leArea12 = self.LocalEffectArea("le_gmz023_s_of_21n_w_of_95w", "S OF 21N W OF 95W")
        #leArea12 = self.LocalEffectArea("le_gmz023_60nm_of_veracruz", "WITHIN 60 NM OF COAST OF VERACRUZ")
        leArea13 = self.LocalEffectArea("le_gmz025_main", "ELSEWHERE")
        leArea14 = self.LocalEffectArea("le_gmz025_60nm_of_campeche", "WITHIN 60 NM OF COAST OF CAMPECHE")
        #leArea15 = self.LocalEffectArea("le_gmz025_s_of_19n", "S OF 19N")
        leArea16 = self.LocalEffectArea("le_amz011_main", "ELSEWHERE")
        leArea17 = self.LocalEffectArea("le_amz011_yucatan_channel", "IN YUCATAN CHANNEL")
        leArea18 = self.LocalEffectArea("le_amz013_main", "ELSEWHERE")
        leArea19 = self.LocalEffectArea("le_amz013_cuba_jamaica", "BETWEEN CUBA AND JAMAICA")
        leArea20 = self.LocalEffectArea("le_amz021_main", " E OF 77W")
        leArea21 = self.LocalEffectArea("le_amz021_w_of_77w", "W OF 77W")
        leArea22 = self.LocalEffectArea("le_amz023_main_swell", "ELSEWHERE")
        leArea23 = self.LocalEffectArea("le_amz023_mona_swell", "IN MONA PASSAGE")
        leArea24 = self.LocalEffectArea("le_amz025_main", "ELSEWHERE")
        leArea25 = self.LocalEffectArea("le_amz025_atlc_exposures_and_passages", "IN ATLANTIC EXPOSURES AND PASSAGES")
        #leArea26 = self.LocalEffectArea("le_amz025_atlantic", "ATLANTIC EXPOSURES")
        leArea27 = self.LocalEffectArea("le_amz029_main", "ELSEWHERE")
        leArea28 = self.LocalEffectArea("le_amz029_nicaraguan_coast", "WITHIN 60 NM OF COAST OF NICARAGUA")
        leArea29 = self.LocalEffectArea("le_amz031_main", "ELSEWHERE")
        leArea30 = self.LocalEffectArea("le_amz031_colombian_coast", "WITHIN 90 NM OF COAST OF COLOMBIA")
        leArea31 = self.LocalEffectArea("le_amz033_main", "ELSEWHERE")
        leArea32 = self.LocalEffectArea("le_amz033_s_of_13n_w_of_68w", "S OF 13N W OF 68W")
        leArea33 = self.LocalEffectArea("le_amz035_main", "ELSEWHERE")
        leArea34 = self.LocalEffectArea("le_amz035_atlantic", "ATLANTIC EXPOSURES")
        leArea35 = self.LocalEffectArea("le_amz037_main", " N OF 10N")
        leArea36 = self.LocalEffectArea("le_amz037_s_of_10n", "S OF 10N")
        leArea37 = self.LocalEffectArea("le_amz039_main", " N OF 10N")
        leArea38 = self.LocalEffectArea("le_amz039_s_of_10n", "S OF 10N")
        #leArea38 = self.LocalEffectArea("le_amz039_w_of_80w", "W OF 80W")
        leArea39 = self.LocalEffectArea("le_amz111_main", "ELSEWHERE")
        leArea40 = self.LocalEffectArea("le_amz111_n_of_29n_w_of_79w", "N OF 29N W OF 79W")
        leArea41 = self.LocalEffectArea("le_amz113_main", " S OF 29N")
        leArea42 = self.LocalEffectArea("le_amz113_n_of_29n", "N OF 29N")
        leArea43 = self.LocalEffectArea("le_amz115_main", " S OF 29N")
        leArea44 = self.LocalEffectArea("le_amz115_n_of_29n", "N OF 29N")
        leArea45 = self.LocalEffectArea("le_amz117_main", "ELSEWHERE")
        leArea46 = self.LocalEffectArea("le_amz117_atlc_exposures", "ATLANTIC EXPOSURES")
        leArea47 = self.LocalEffectArea("le_amz119_main", " S OF 25N")
        leArea48 = self.LocalEffectArea("le_amz119_n_of_25n", "N OF 25N")
        leArea49 = self.LocalEffectArea("le_amz121_main", " S OF 25N")
        leArea50 = self.LocalEffectArea("le_amz121_n_of_25n", "N OF 25N")
        leArea51 = self.LocalEffectArea("le_amz127_main", " W OF 60W")
        leArea52 = self.LocalEffectArea("le_amz127_e_of_60w", "E OF 60W")
        leArea53 = self.LocalEffectArea("le_amz017_main", "ELSEWHERE")
        leArea54 = self.LocalEffectArea("le_amz017_s_of_17n_w_of_87w", "S OF 17N W OF 87W")

        return [self.LocalEffect([leArea1, leArea2], 5, " E OF 90W...AND "),
                #[self.LocalEffect([leArea1, leArea2], 2, "...EXCEPT "),
                # Changed "...EXCEPT " TO "E OF 90W AND ". Renders "SEAS x TO x FT E OF 90W AND x TO x FT W OF 90W" EC - 4/20/12
                #self.LocalEffect([leArea2, leArea1], 2, ". ELSEWHERE..."),
                # Tried the entry above to put leArea first then ELSEWHERE - JL/NHC - 02/12/12
                self.LocalEffect([leArea3, leArea4], 5, " N OF 27N...AND "),
                self.LocalEffect([leArea5, leArea6], 5, " E OF 96W...AND "),
                self.LocalEffect([leArea7, leArea8], 5, " N OF 24N...AND "),
                self.LocalEffect([leArea10, leArea9], 5, "...AND "),
                self.LocalEffect([leArea12, leArea11], 5, "...AND "),
                self.LocalEffect([leArea14, leArea13], 5, "...AND "), # removed leArea15
                self.LocalEffect([leArea17, leArea16], 5, "...AND "),
                self.LocalEffect([leArea19, leArea18], 5, "...AND "),
                self.LocalEffect([leArea20, leArea21], 5, " E OF 77W...AND "),
                self.LocalEffect([leArea23, leArea22], 5, "...AND "),
                self.LocalEffect([leArea25, leArea24], 5, "...AND "),
                self.LocalEffect([leArea28, leArea27], 5, "...AND "),
                self.LocalEffect([leArea30, leArea29], 5, "...AND "),
                self.LocalEffect([leArea32, leArea31], 5, "...AND "),
                self.LocalEffect([leArea34, leArea33], 5, "...AND "),
                self.LocalEffect([leArea35, leArea36], 5, " N OF 10N...AND "),
                self.LocalEffect([leArea37, leArea38], 5, " ...AND "),
                self.LocalEffect([leArea40, leArea39], 5, "...AND "),
                self.LocalEffect([leArea41, leArea42], 5, " S OF 29N...AND "),
                self.LocalEffect([leArea43, leArea44], 5, " S OF 29N...AND "),
                self.LocalEffect([leArea46, leArea45], 5, "...AND "),
                self.LocalEffect([leArea47, leArea48], 5, " S OF 25N...AND "),
                self.LocalEffect([leArea49, leArea50], 5, " S OF 25N...AND "),
                self.LocalEffect([leArea51, leArea52], 5, " W OF 60W...AND "),
                self.LocalEffect([leArea54, leArea53], 2, "...AND "),
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
                          ("Wind", self.vectorModeratedMinMax, [24]),
                          ("WindGust", self.moderatedMinMax, [24]),
                          ("WaveHeight", self.moderatedMinMax, [24]),
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

##    # Was originaly active at OPC
##    # Commented out by C Juckins 2011-07-26
##    def includeOnlyPhrases_list(self, tree, component):
##        """
##           Used for Tropical phrases.
##           Determines which phrases to keep in each period of the product.
##        """
##        # Return list of phrases to include in the component
##        # Return an empty list if all phrases should be included
##        try:
##            includeTropical = self._includeTropical
##        except:
##            includeTropical = False
##        if not includeTropical:
##            return []
##
##        # See which period we are in
##        compPeriod = int(component.getIndex() + self.firstComponentPeriod(tree, component))
##        self.debug_print("Working in Period %d" % (compPeriod), 1)
##
##        #  See which list of periods we may want to modify
##        if self._pil.find("ZFP") == 0:
##            productType = "ZFP"
##            includeSomeList = [1]
##        else:
##            #productType = "CWF"
##            productType = "OFF"
##            includeSomeList = [6,7,8,9,10]
##
##        #  If this is not one of the periods we might want to remove phrases,
##        #  then return
##        if compPeriod not in includeSomeList:
##            #  Ensure all phrases are used
##            return []
##
##        #  Grab thresholds for this period - handle the first period case
##        windSpdProb_thresholds = self.windSpdProb_thresholds(tree, component)
##        if compPeriod == 1:
##            (thresh34low, thresh34high) = windSpdProb_thresholds[0][0]
##            (thresh64low, thresh64high) = windSpdProb_thresholds[0][1]
##
##            #  Display thresholds so we know what we're using
##            self.debug_print("34 kt thresholds = (%.2f, %.2f)" %
##                             (thresh34low, thresh34high), 1)
##            self.debug_print("64 kt thresholds = (%.2f, %.2f)" %
##                             (thresh64low, thresh64high), 1)
##        #  Otherwise, handle all other periods
##        else:
##            index = int(component.getIndex())
##            (thresh34, thresh64) = windSpdProb_thresholds[index]
##
##            #  Display thresholds so we know what we're using
##            self.debug_print("(34 kt threshold, 64 kt threshold) = (%.2f, %.2f)" %
##                             (thresh34, thresh64), 1)
##
##        #  Get some information about this forecast period
##        dayNight = self.getPeriod(component.getTimeRange(), 1)
##        timeRange = component.getTimeRange()
##        areaLabel = component.getAreaLabel()
##        self.debug_print("dayNight = %s\ttimeRange = %s" % (dayNight,
##                                                            repr(timeRange)), 1)
##
##        # Get pws64
##        if dayNight == 1:
##            pws64 = tree.stats.get("pwsD64", timeRange, areaLabel, mergeMethod="Max")
##            self.debug_print("USING pwsD64", 1)
##        else:
##            pws64 = tree.stats.get("pwsN64", timeRange, areaLabel, mergeMethod="Max")
##            self.debug_print("USING pwsN64", 1)
##
##        self.debug_print("PWS64 = %s" % (pws64), 1)
##
##        if pws64 is None:
##            return []
##
##        # Get pws34
##        if dayNight == 1:
##            pws34 = tree.stats.get("pwsD34", timeRange, areaLabel, mergeMethod="Max")
##            self.debug_print("USING pwsD34", 1)
##        else:
##            pws34 = tree.stats.get("pwsN34", timeRange, areaLabel, mergeMethod="Max")
##            self.debug_print("USING pwsN34", 1)
##
##        self.debug_print("PWS34 = %s" % (pws34), 1)
##
##        if pws34 is None:
##            return []
##
##        # COMMENT: Get the stored wind stats from the component level.
##        # IF WE WERE TO LIMIT ELEMENTS IN THE ZFP BEYOND PERIOD 5,
##        # THE WIND STAT LABEL ABOVE WOULD ALSO BE NEEDED.
##
##        maxMagList = component.get("maxMagList")
##        if maxMagList is None:
##            return self.setWords(component, "")
##        self.debug_print("maxMag from includeOnlyPhrases_list: %s " % (maxMagList), 1)
##        print("maxMagList from includeOnlyPhrases_list: ", maxMagList)
##
##        maxMag = 0.0
##        for mag in maxMagList:
##            if mag > maxMag:
##                maxMag = mag
##
##        ##  maxMag, dir = wind
##        if productType == "ZFP":
##            maxMag = maxMag*0.868976242
##        self.debug_print("maxMag in includeOnlyPhrases_list: %s " % (maxMag), 1)
##        print("maxMag in includeOnlyPhrases_list: ", maxMag)
##
##        if maxMag is None:
##            maxMag = 0.0
##
##       # Retrieve the headlineKeys stored at the component level
##        headlineKeys = component.get("headlineKeys")
##        if headlineKeys is None:
##            headlineKeys = []
##
##        #  If this is the first period, and in the list of periods we might
##        #  want to modify
##        if productType == "ZFP":
##            if compPeriod == 1 and compPeriod in includeSomeList:
##                if "HU.W" in headlineKeys or "HI.W" in headlineKeys:
##                    if pws64 >= thresh64high and maxMag >= 64.0:
##                        #  Limit the phrases we'll report
##                        return ["pws_phrase", "wind_withGusts_phrase", "weather_phrase"]
##                    elif pws64 >= thresh64low and maxMag >= 50.0:
##                        #  Keep all phrases
##                        return []
##                    elif pws34 >= thresh34high and maxMag >= 34.0:
##                        #  Limit the phrases we'll report
##                        return ["pws_phrase", "wind_withGusts_phrase", "weather_phrase"]
##
##                elif "TR.W" in headlineKeys or "TI.W" in headlineKeys:
##                    if pws34 >= thresh34high and maxMag >= 34.0:
##                        #  Limit the phrases we'll report
##                        return ["pws_phrase", "wind_withGusts_phrase", "weather_phrase"]
##
##                else:
##                    return []           #  keep all phrases
##
##        #  If this period is beyond the fifth period, and in the list of
##        #  periods we might want to modify
##        else:
##            if compPeriod >= 6 and compPeriod in includeSomeList:
##                if ((pws34 >= thresh34 or pws34+2.5 >= thresh34) and maxMag >= 20.0) \
##                       or ((pws64 >= thresh64 or pws64+1.0 >= thresh64) and maxMag >= 20.0) \
##                       or maxMag >= 34.0:
##                    #  Limit the phrases we'll report
##                    return ["pws_phrase", "weather_phrase"]
##                else:
##                    #  Return all phrases
##                    return []





##    # Was originally active at OPC
##    # Commented out by C Juckins 2011-07-26
##    def pws_words(self, tree, node):
##        """
##        Words method for the tropical probabilistic wind phrase.
##        """
##        # Get Wind
##        self.debug_print("\nBegin period***********", 1)
##        self.debug_print("\nNode time range -> %s" %
##                         (repr(node.getTimeRange())), 1)
##        self.debug_print("Parent time range -> %s" %
##                         (repr(node.parent.getTimeRange())), 1)
##
##        #  Get name and index of this node's component
##        component = node.getComponent()
##        compIndex = node.getComponent().getIndex()
##        compPeriod = int(compIndex + self.firstComponentPeriod(tree, node))
##        print("COMPONENT IN pws_words", compPeriod)
##        componentName = node.getComponentName()
##
##        if self._pil.find("ZFP") == 0:
##            productType = "ZFP"
##        else:
##            #productType = "CWF"
##            productType = "OFF"
##
##        #  COMMENT: If this is one of the first 5 periods of the ZFP, or this is the CWF
##        if not productType == "ZFP" or compPeriod <= 5:
##            print("I AM IN: ", node.getTimeRange())
##            #!!! Wait for wind phrase to complete
##            #    We're assuming that all the wind phrases have completed (including
##            #    local effect phrases) if one has.
##            if productType == "ZFP":
##                phraseList = ["wind_withGusts_phrase"]
##            else:
##                phraseList = ["marine_wind_withGusts_phrase"]
##            windWords = self.findWords(tree, node, "Wind", phraseList = phraseList)
##            self.debug_print("windWords = '%s'" % (windWords), 1)
##            # Wait for Wind phrase
##            if windWords is None:
##                return
##
##            # Get the stored wind stats from the component level
##            maxMagList = component.get("maxMagList")
##            if maxMagList is None:
##                return self.setWords(node, "")
##
##            self.debug_print("MaxMagList from pws_words %s %s" % (maxMagList,
##                                                repr(node.getTimeRange())), 1)
##            print("MaxMagList from pws_words", maxMagList, node.getTimeRange())
##            maxMag = 0.0
##            for mag in maxMagList:
##                if mag > maxMag:
##                   maxMag = mag
##
##            if productType == "ZFP":
##                # print "PWS MAXMAG in MPH IS: ", maxMag
##                maxMag = maxMag*0.868976242
##            # print "PWS MAXMAG IN KNOTS: ", maxMag
##        #
##        #  COMMENT: Othwerwise Periods 6 and beyond in the ZFP.
##        #  Although wind phrases are not included in extended ZFP you
##        #  still need to do the analysis so tropical cyclone formatter
##        #  logic can be carried out through the extended (day 5) periods.
##        #
##        else:
##            print("I AM IN: ", node.getTimeRange())
##            windStats = tree.stats.get(
##                "Wind", node.getTimeRange(), node.getAreaLabel(),
##                statLabel="vectorModeratedMinMax", mergeMethod="Max")
##            ## print "WINDSTATS", windStats
##            if windStats is None:
##                return self.setWords(node, "")
##            maxMag, dir = windStats
##            maxMag = maxMag*0.868976242
##
##        #  Display maximum wind speed in MPH and KTS
##        self.debug_print("PWS MAXMAG in MPH IS: %s" % (maxMag), 1)
##        self.debug_print("PWS MAXMAG in KTS IS: %s" % (maxMag), 1)
##
##        dayNight = self.getPeriod(node.getTimeRange(), 1)
##        self.debug_print("dayNight IS %s" % (dayNight), 1)
##
##        #  See which grids to use for probability of 34 and 64 kts
##        if dayNight == 1:
##            prob34 = "pwsD34"
##            prob64 = "pwsD64"
##        else:
##            prob34 = "pwsN34"
##            prob64 = "pwsN64"
##        self.debug_print("USING pws34 = "+prob34, 1)
##        self.debug_print("USING pws64 = "+prob64, 1)
##        pws64 = tree.stats.get(prob64, node.getTimeRange(),
##                               node.getAreaLabel(), mergeMethod="Max")
##        if pws64 is None:
##            self.debug_print("pws64 NONE", 1)
##            return self.setWords(node, "")
##        pws34 = tree.stats.get(prob34, node.getTimeRange(),
##                               node.getAreaLabel(), mergeMethod="Max")
##        if pws34 is None:
##            self.debug_print("pws34 NONE", 1)
##            return self.setWords(node, "")
##
##        #print "check   ", "check"
##        ####################################################################
##        #print "WORDS1", words
##        words = ""
##        areaLabel = tree.getAreaLabel()
##        print("\nBegin period***********", node.getTimeRange())
##        self.debug_print("\nNode time range -> %s" %
##                         (repr(node.getTimeRange())), 1)
##        self.debug_print("Parent time range -> %s" %
##                         (repr(node.parent.getTimeRange())), 1)
##        self.debug_print("MAXMAG IS -> %s KTS" % (maxMag), 1)
##        self.debug_print("\nNode time and label -> %s %s" %
##                         (repr(node.getTimeRange()),
##                          repr(node.getAreaLabel())), 1)
##        #tree.stats.printDictionary("Hazards")
##        # Get Hazards
##        headlines = tree.stats.get("Hazards", node.getTimeRange(),
##                                   areaLabel, mergeMethod = "List")
##
##        self.debug_print("maxMag = %s" % (maxMag), 1)
##        self.debug_print("warningpws64 = %s" % (pws64), 1)
##        self.debug_print("warningpws34 = %s" % (pws34), 1)
##        self.debug_print("Headline stats for warning -> %s" %
##                         (repr(headlines)), 1)
##        print("maxMag = ", maxMag)
##        print("warningpws64 = ", pws64)
##        print("warningpws34 = ", pws34)
##        print("Headline stats for warning ", headlines)
##
##        if headlines is not None:
##            # Sort the headlines by startTime
##            temp = []
##            for h, tr in headlines:
##                temp.append((tr.startTime(), (h, tr)))
##            temp.sort()
##            newList = []
##            for t in temp:
##                newList.append(t[1])
##            headlines = newList
##
##            # Fetch the set of local headlines allowed for this product
##            allowedHazards = []
##            for key, allActions, cat in self.allowedHazards():
##                allowedHazards.append(key)
##
##            # Create a list of headline keys as strings e.g. HU.A
##            headlineKeys = []
##            for key, tr in headlines:  # value == list of subkeys
##                if key not in allowedHazards:
##                    continue
##                # Don't call headlinesTimeRange_descriptor function due to
##                # an exception which is caused - DR19483
##                #timeDescriptor = self.headlinesTimeRange_descriptor(
##                #    tree, node, key, tr, areaLabel, issuanceTime)
##                if key == "<None>":
##                    continue
##                if key not in headlineKeys:
##                    headlineKeys.append(key)
##                self.debug_print("key: %s" % (key), 1)
##
##            self.debug_print("headlineKeys: %s" % (repr(headlineKeys)), 1)
##            words = self.getTropicalDescription(
##                    tree, node, headlineKeys, maxMag, pws64, pws34)
##            # Store the headlineKeys at the component node for later examination
##            component = node.getComponent()
##            component.set("headlineKeys", headlineKeys)
##
##        elif headlines is None or headlines is NoData:
##            words = words + self.getTropicalDescription(
##                tree, node, "", maxMag, pws64, pws34)
##
##        #  COMMENT: If we have words from the pws_phrase during tropical cyclones
##        #  the following lines of code will make sure wind_summary is
##        #  not printed out.
##        if words is not None and len(words.strip()) > 0:
##            #  Remove the wind sumamry phrase from this component and any local
##            #  effect areas - no need to replace undesirable phrases later on
##            self.removeComponentPhrases(tree, node, "wind_summary",
##                 areaLabels=[node.getAreaLabel(),
##                             node.getComponent().getAreaLabel()
##                            ])
##        self.debug_print("\nSetting words '%s' for %s" %
##                         (words, node.getAncestor('name')), 1)
##        self.debug_print("%s %s\n" % (node.getComponentName(),
##                                      repr(node.getTimeRange())), 1)
##        return self.setWords(node, words)

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
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 24),
                    ("OFFExtended", 24)
                    ]
                narrativeDefPM = [
                    ("OFFPeriod", "period1"),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 24),
                    ("OFFExtended", 24)
                    ]

            else:

                narrativeDefAM = [
                    ("OFFPeriod", "period1"),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 24),
                    ("OFFExtended", 24),
                    ("OFFExtended", 24)
                    ]
                narrativeDefPM = [
                    ("OFFPeriod", "period1"),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFPeriod", 12),
                    ("OFFExtended", 24),
                    ("OFFExtended", 24),
                    ("OFFExtended", 24)
                    ]

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
        if self._definition["pil"] == "OFFNT3":
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

#    def allowedHeadlines(self):
#
#        allActions = ["NEW", "EXA", "EXB", "EXT", "CAN", "CON", "EXP"]
#        tropicalActions = ["NEW", "EXA", "EXB", "EXT", "UPG", "CAN", "CON",
#          "EXP"]
#        marineActions = ["NEW", "EXA", "EXB", "EXT", "CON"]
#        return [
#            ('HU.W', tropicalActions, 'Tropical'),     # HURRICANE WARNING
##            ('TY.W', tropicalActions, 'Tropical'),     # TYPHOON WARNING
#            ('TR.W', tropicalActions, 'Tropical'),     # TROPICAL STORM WARNING
#            ('HF.W', marineActions, 'Marine'),       # HURRICANE FORCE WIND WARNING
#            ('SR.W', marineActions, 'Marine'),       # STORM WARNING
#            ('GL.W', marineActions, 'Marine'),       # GALE WARNING
##            ('SE.W', marineActions, 'Marine'),       # HAZARDOUS SEAS
##            ('UP.W', allActions, 'IceAccr'),                        # HEAVY FREEZING SPRAY WARNING
#
#            # added by J. Lewitsky/NHC on 02/12/11 for expected wording
#            ('GALE CONDITIONS EXPECTED', marineActions, 'Marine'),
#            ('STORM CONDITIONS EXPECTED', marineActions, 'Marine'),
#            ('HURRICANE FORCE WINDS EXPECTED', marineActions, 'Marine')
#            ('MF.Y', allActions, 'Fog'),                            # DENSE FOG ADVISORY
#            ('MS.Y', allActions, 'Smoke'),                          # DENSE SMOKE ADVISORY
###            ('UP.Y', allActions, 'IceAccr'),                        # HEAVY FREEZING SPRAY ADVISORY
#            ('MH.Y', allActions, 'Ashfall'),                        # VOLCANIC ASHFALL ADVISORY
#            ]

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

#    def _preProcessArea(self, fcst, editArea, areaLabel, argDict):
#        self.debug_print("Debug: _preProcessArea in NAVTEX_SANJUAN_Overrides")
#
#        # This is the header for an edit area combination
#        print("Generating Forecast for", areaLabel)
###        areaHeader = self.makeAreaHeader(
###            argDict, areaLabel, self._issueTime, self._expireTime,
###            self._areaDictionary, self._defaultEditAreas)
###        fcst = fcst + areaHeader
#
#
#        # get the hazards text
#        self._hazards = argDict['hazards']
#        self._combinations = argDict["combinations"]
#        print("here1")
#
#        headlines = self.generateProduct("Hazards", argDict, area = editArea,
#                                         areaLabel=areaLabel,
#                                         timeRange = self._timeRange)
#        # remove any double spaces
#        headlines = re.sub(r'  ', r' ',headlines)
#        print("here2")
#
#        # Navtex only needs the area desription as the header
#        if argDict["combinations"] is not None:
#            print("here3")
#            areaList = self.getCurrentAreaNames(argDict, areaLabel)
#        else:
#            print("here4")
#            for editArea, label in self._defaultEditAreas:
#                print("here5")
#                if label == areaLabel:
#                    print("here6")
#                    areaList = [editArea]
#        print(areaList)
#        # Access the UGC information for the area(s) if available
#        print("here7")
#        accessor = ModuleAccessor.ModuleAccessor()
#
#        print("here8")
#        areaDict = accessor.variable(self._areaDictionary, "AreaDictionary")
#        for areaName in areaList:
#                print(areaName + "\n")
#                entry = areaDict[areaName]
#        areaHeader = entry['ugcName'] + "\n"
#        fcst = fcst + areaHeader
#
#        #add headlines to forecast
#        fcst = fcst + headlines
#
#
#
#        return fcst
#
#
###    #Modified from OFF base
###    #modifed for Navtex
###    def _preProcessArea(self, fcst, editArea, areaLabel, argDict):
###        self.debug_print("Debug: _preProcessArea in OFF_NAV_ONA_Overrides")
###
###        # This is the header for an edit area combination
###        print("Generating Forecast for", areaLabel)
#####        areaHeader = self.makeAreaHeader(
#####            argDict, areaLabel, self._issueTime, self._expireTime,
#####            self._areaDictionary, self._defaultEditAreas)
###
###        # Navtex only needs the area desription as the header
###        if argDict["combinations"] is not None:
###            areaList = self.getCurrentAreaNames(argDict, areaLabel)
###        else:
###            for editArea, label in self._defaultEditAreas:
###                if label == areaLabel:
###                    areaList = [editArea]
###        print(areaList)
###        # Access the UGC information for the area(s) if available
###        accessor = ModuleAccessor.ModuleAccessor()
###        areaDict = accessor.variable(self._areaDictionary, "AreaDictionary")
###        for areaName in areaList:
###                print(areaName + "\n")
###                entry = areaDict[areaName]
###        areaHeader = entry['ugcName'] + "\n\n"
###        fcst = fcst + areaHeader
###
###        # get the hazards text
###        self._hazards = argDict['hazards']
###        self._combinations = argDict["combinations"]
###
###        headlines = self.generateProduct("Hazards", argDict, area = editArea,
###                                         areaLabel=areaLabel,
###                                         timeRange = self._timeRange)
###        # remove any double spaces
###        headlines = re.sub(r'  ', r' ',headlines)
###
###        #add headlines to forecast
###        fcst = fcst + headlines
###
###        return fcst

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

        if self._definition["pil"] == "OFFNT3":
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
                if areasLeft == 9:
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
#
#    def generateForecast(self, argDict):
#        # Get variables
#        error = self._getVariables(argDict)
#        if error is not None:
#            return error
#
#        # Get the areaList -- derived from defaultEditAreas and
#        # may be solicited at run-time from user if desired
#        self._areaList = self.getAreaList(argDict)
#        if len(self._areaList) == 0:
#            return "WARNING -- No Edit Areas Specified to Generate Product."
#
#        # Determine time ranges
#        error = self._determineTimeRanges(argDict)
#        if error is not None:
#            return error
#
#        # Sample the data
#        error = self._sampleData(argDict)
#        if error is not None:
#            return error
#
#        # Initialize the output string
#        fcst = ""
#        fcst = self._preProcessProduct(fcst, argDict)
#
#        # Generate the product for each edit area in the list
#        fraction = 0
#        fractionOne = 1.0/float(len(self._areaList))
#        percent = 50.0
#        self.setProgressPercentage(percent)
#
#        if self._definition["pil"] == "OFFN05":
#            # Need to know how many areas to process after this.
#            # will insert second synopsis before the last fcst area
#            areasLeft = len(self._areaList) - 1
#            for editArea, areaLabel in self._areaList:
#                skipAreas = self._skipAreas(argDict)
#                argDict["editArea"] = (editArea, areaLabel)
#                if self.currentAreaContains(argDict, skipAreas):
#                    continue
#                self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
#                fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
#                fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
#                fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#                # are we on the next to last area yet?
#                # if so, add synopsis2
#                if areasLeft == 1:
#                    fcst = fcst + self._Text3()
#                fraction = fractionOne
#                areasLeft = areasLeft - 1
#            fcst = self._postProcessProduct(fcst, argDict)
#            return fcst
#
#        else:
#            #Second synopsis isn't defined
#            #use BASE OFF.py code
#            for editArea, areaLabel in self._areaList:
#                skipAreas = self._skipAreas(argDict)
#                argDict["editArea"] = (editArea, areaLabel)
#                if self.currentAreaContains(argDict, skipAreas):
#                    continue
#                self.progressMessage(fraction, percent, "Making Product for " + areaLabel)
#                fcst = self._preProcessArea(fcst, editArea, areaLabel, argDict)
#                fcst  = self._makeProduct(fcst, editArea, areaLabel, argDict)
#                fcst = self._postProcessArea(fcst, editArea, areaLabel, argDict)
#                fraction = fractionOne
#            fcst = self._postProcessProduct(fcst, argDict)
#            return fcst
#
#    #Modified from OFF base
#    # Modified for Navtex
#    def _postProcessArea(self, fcst, editArea, areaLabel, argDict):
#        self.debug_print("Debug: _postProcessArea in NAVTEX_SANJUAN_Overrides")
#
###        return fcst + "\n$$\n\n"
#        # Don't include $$ at end of area forecast
#        return fcst + ""
#
#    #For Navtex - return to OFF base
#    def _postProcessProduct(self, fcst, argDict):
#        self.debug_print("Debug: _postProcessProduct in NAVTEX_SANJUAN_Overrides")
#
#        #fcst = fcst + """NNNN   """
#        self.setProgressPercentage(100)
#        self.progressMessage(0, 100, self._displayName + " Complete")
#        return fcst

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
