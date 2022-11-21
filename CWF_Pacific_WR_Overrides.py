# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# CWF_Pacific_WR_Overrides
#
#    VERSION 16.k.1  (2005-02-16)
#    William R. Schneider
#    Science and Operations Officer
#    Portland, Oregon
#
#  This file provides any product specific regional overrides for the
#  CWF_Pacific product.  This file is under configuration control by
#  the region and should not be edited by the site.
#
# Definition Section:
#   Overrides:
#   Additions:
#
# Methods:
#   Overrides:
#   Additions:
#
# ---------------------------------------------------------------------

import string, time, re, os, types, copy, AFPS
import TextRules
#<16.f> - WRS >>>>>> Added the import of the SampleAnalysis class so it can
#       be overridden
import SampleAnalysis


# Define Regional overrides of Product Definition settings and
# default values of additional Regional Definition settings
#  ( This Definition section must be before the Class definition)

#***** THIS NEXT LINE IS REQUIRED *****
Definition = {}

#####################################################
# Override VariableList if desired
#
#VariableList = []
#
# WR Definitions:
# Definition statements must start in column 1

############################################################################
#
#<16.f> - WRS >>>>>> WR CWF_Pacific definition ovrrides to baseline settings
# If desired, change these settings in you CWF_Pacific_XXX_Definition.TextUtility file
#
################ Regional settings of baseline options: ####################

Definition["displayName"] = None#"CWF_Pacific_WR"

# Note the default combinations file is "Combinations_CWF_PQR"  I changed
# the name to be more consistant with the file naming convention
# The combinations files are saved in the directory:
# AWIPS - "/awips/GFESuite/primary/data/databases/SITE/TEXT/TextUtility"
# RPP - "~/release/data/databases/SITE/TEXT/TextUtility"
#
Definition["defaultEditAreas"] = "Combinations_CWF_Pacific"
Definition["mapNameForCombinations"] = "" # Map background for creating Combinations

# Header configuration items
Definition["productName"] = "COASTAL WATERS FORECAST"  # name of product
Definition["fullStationID"] = "KXXX"  # full station identifier (4letter)
Definition["wmoID"] = "FZUS56"        # WMO ID
Definition["pil"] = "CWFXXX"          # product pil
Definition["areaName"] = ""  # Name of state, such as "GEORGIA"

Definition["wfoCityState"] = ""  # Location of WFO - city st
Definition["textdbPil"] = "PDXWRKCWF"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = ""   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/CWF_Pacific.txt"


# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
#Definition["debug"] = 1

#Automatic Functions
Definition["autoSend"] = 0   #set to 1 to automatically transmit product
Definition["autoSendAddress"] = "000"   #transmission address
# Set to automatically store the product in the AWIPS database (but not transmit)
Definition["autoStore"] = 1   #set to 1 to store product in textDB
Definition["autoWrite"] = 0   #set to 1 to write product to file

Definition["periodCombining"] = 0     # If 1, do period combining
Definition["includeEveningPeriod"] = 1 # If 1, include Evening Period
Definition["useAbbreviations"] = 1     # If 1, use marine abbreviations

# Weather-related flags
Definition["periodSChcEnds"] = 1

Definition["areaDictionary"] = ""     # For product headers
Definition["language"] = "english"
Definition["lineLength"] = 64
Definition["useHolidays"] = 0

# Trouble-shooting items
#Definition["passLimit"] = 20       # Limit on passes allowed through Narrative Tree
#Definition["trace"] = 1            # Set to 1 to turn on trace through
                                   # Narrative Tree for trouble-shooting

###################################################################################
#
#<16.f> - WRS >>>>>> WR CWF_Pacific definition additions
# You should override all of these settings in you CWF_Pacific_XXX_Definition.TextUtility file
#
#################### New Regional Definitions not in the baseline #################

# Definition of the area covered by you CWF which will appear at the
# top of the CWF
# You should override this in you CWF_Pacific_XXX_Definition.TextUtility file
Definition["CWFAreaLabel"] = "COASTAL WATERS"

# AWIPS key of product used for previous synopsis and/or bar forecast
# You should override this in you CWF_Pacific_XXX_Definition.TextUtility file
Definition["previousProductID"]  = ""

# "synopsisHeading defines the heading for your CWF synopsis (or "None" if you don't want a previous synopsis"
# You should override this in you CWF_Pacific_XXX_Definition.TextUtility file
Definition["synopsisHeading"]  = "SYNOPSIS..."

# "synopsisUGC" is the UGC FIPS code for your synopsis
# You should override this in you CWF_Pacific_XXX_Definition.TextUtility file
Definition["synopsisUGC"]  = "PZZ???"

# If you do a river bar forecast supply the barzone and barname deffinitions
# otherwise return None
# You should override this in you CWF_Pacific_XXX_Definition.TextUtility file
Definition["riverBarForecast_dict"] = None

# host and user for login to awips if running on non AWIPS (e.g. RPP) box
# You should override this in you CWF_Pacific_XXX_Definition.TextUtility file
Definition["awipsTEXTDBhost"] = "pv1"
Definition["awipsTEXTDBuser"] = "fxa"



###########  END WR Regional CWF_Pacific Definitions Section   ######################


#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the above Definition = {} line
# plus following class definition and the __init__ method with only
# the "pass" line in it.

class CWF_Pacific_WR_Overrides:
    """Class NNN_FILETYPE - Version: IFPS"""

    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Add methods here making sure to indent inside the class statement
    # WR CWF_Pacific Overrides ------------------------

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in CWF_Pacific_WR_Overrides")
################################################################################
#
#    CWF_Pacific_WR_Overrides
#    AWIPS - "/awips/GFESuite/primary/data/databases/BASE/TEXT/TextUtility/CWF_FPPacific_FPWR_FPOverrides.TextUtility
#    RPP - "~/release/data/databases/BASE/TEXT/TextUtility/CWF_FPPacific_FPWR_FPOverrides.TextUtility
#    William R. Schneider
#    WFO Portland, OR
#    (503) 326-2340 Ex. 224
#
#    Version 1 for IFPS16.f
#    2/9/2005
#
################################################################################

###########################################################################
#
#    CWF_FPPacific.TextProduct OVERRIDES
#
#     AWIPS - "/awips/GFESuite/primary/data/databases/BASE/TEXT/TextProduct/CWF_FPPacific.TextProduct
#    RPP -   "~/release/data/databases/BASE/TEXT/TextProduct/CWF_FPPacific.TextProduct
#
###########################################################################

#<16.f> - WRS >>>>>> Changed this to read the definition from the CWFAreaLabel
#      variable which should be set in the local definition file.

    def _Text1(self):
        return self._CWFAreaLabel

#<16.f> - WRS >>>>>> Changed to read the previous synopsis provided the
#     "previousProductID" and "synopsisHeading" variables are set correctly
#     in the definition file.

    def _Text2(self):
        synopsis = ""

        #  Try to get Synopsis from previous CWF
#        synopsis = self.getPreviousProduct(self._previousProductID, [(self._synopsisHeading,"\$\$",1,0,0,self._lineLength)],self._awipsTEXTDBhost,self._awipsTEXTDBuser)
        synopsis = self.getPreviousProduct(self._previousProductID, [(self._synopsisHeading,"\$\$",1,0,0,self._lineLength)])

        #  Convert absolute time pointer to a tuple of values like that
        #  returned by time.gmtime()
        expTuple = time.strptime('%s' % (self._expireTime),
                                 '%b %d %y %H:%M:%S GMT')

        #  Format expiration time for inclusion in synopsis header
        expTime = time.strftime('%d%H%M', expTuple)

        return "%s-%s-\n" % (self._synopsisUGC, expTime) + self._timeLabel\
         + "\n\n" + self._synopsisHeading + "\n" + synopsis + "\n$$\n\n"

#<16.f> - WRS >>>>>> override _postProcessProduct method to add River Bar forecast

    def _postProcessProduct(self, fcst, argDict):
        #<16.f> - WRS >>>>>> Modified the following line from original version to add call to
        # my "modifyText" method
        fcst = self.modifyText(fcst)
        #<16.f> - WRS >>>>>> removed the host from the list of argments as it is not needed
    #       in my new riverBarForecast method
        fcst = self.riverBarForecast(fcst)
        fcst = string.upper(fcst)

#<16.f> - WRS >>>>>> Added an attribution line as an option
#             Set this in the Definitions file under
#             "attributionLine" definition.
#             Choices for attributionLine setting are "None" which uses the default
#             or "" or "text".
    if self._attributionLine != None:
        fcst = fcst + self._attributionLine
    else:
        fcst = fcst + "\n\nFor more weather information from NOAA's National Weather Service\nvisit...\nhttp://weather.gov (all lower case)\n"

    #<16.f> - WRS >>>>>> added the textdbPil and removed the host to conform with
    #        my new storeAWIPS method.  autoStore definition must be set
    #    to one for this to run
        if self._autoStore == 1:
        self.storeAWIPS(fcst, self._textdbPil)
    self.setProgressPercentage(100)
        self.progressMessage(0, 100, self._displayName + " Complete")

##*********************************************************
## ADDED TO PROCESS DIFFERENCE FILES

        os.system("/data/local/Text/rawCWF/getUser.sh > /data/local/Text/rawCWF/cwf.txt")

        rawCWFFile = file("/data/local/Text/rawCWF/cwf.txt","a")

        rawCWFFile.write(fcst)
        rawCWFFile.close()

        os.system("chmod 777 /data/local/Text/rawCWF/cwf.txt")

        os.system("scp /data/local/Text/rawCWF/cwf.txt ldad@ls1:/ekaLAN/data/afos/products/rawCWF/cwf.txt")

## **********************************************************


        fcst = fcst + "\n\nWWW.NWS.NOAA.GOV/SURVEY/NWS-SURVEY.PHP?CODE=EENWT\n"

    return fcst

#<16.f> - WRS >>>>>> - modified the arguments to remove the "host" as this will be passed
#       in the getPreviousProduct method directly from the definitions
#       set in the definitions file

    def riverBarForecast(self, forecast):
        if self._riverBarForecast_dict is not None:
        # WRS changed the static product id for the previous product
        # to the one supplied in the definitions file
        # Also modified the following line from original version
        # because new version of "getPreviousProduct requires additional variables
            bar = self.getPreviousProduct(self._previousProductID, [(self._riverBarForecast_dict["barzone"],"\$\$",0,4,0,self._lineLength)],self._awipsTEXTDBhost, self._awipsTEXTDBuser)
        forecast = forecast  + self._riverBarForecast_dict["barzone"] + "-" \
                                 + self._expireTimeStr + "-\n" \
                                 + self._riverBarForecast_dict["barname"] \
                                 + "\n" + self._timeLabel \
                                 + "\n\n" + bar + "\n$$"
        return forecast


########################################################################
#
#     SampleAnalysis.TextUtility OVERRIDES
#    AWIPS -  /awips/GFESuite/primary/data/databases/BASE/TEXT/TextUtility/SampleAnalysis.TextUtility
#    RPP -    ~/release/data/databases/BASE/TEXT/TextUtility/SampleAnalysis.TextUtility
#
########################################################################

#<16.f> - WRS >>>>>> Use moderated values of 20% for all elements

    def moderated_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
        dict["Wind"] =  (20, 10)
        dict["WindGust"] =  (20, 20)
    dict["WaveHeight"] =  (20, 20)
    dict["WindWaveHgt"] =  (20, 20)
    dict["Swell"] =  (20, 20)
    dict["Swell2"] =  (20, 20)
    dict["Period"] = (20, 20)
    dict["Period2"] =  (20, 20)
    dict["PoP"] =  (20, 20)
        return dict

########################################################################
#
#       CWF_FPPacific.TextProduct overrides
#
#    AWIPS -  /awips/GFESuite/primary/data/databases/BASE/TEXT/TextProduct/CWF_FPPacific.TextProduct#
#    RPP -    ~/release/data/databases/BASE/TEXT/TextProduct/CWF_FPPacific.TextProduct#
#
#########################################################################

    def _skipAreas(self, argDict):
        # These are edit areas that the formatter will skip
        return []

#<16.f> - WRS >>>>>> Modified to return no inland waters as the default
#             If you have inland waters you need to override this method
#             in your site override file

    def inlandWatersAreas(self, tree, node):
        # List of edit area names that are inland or bay waters
        #  as opposed to "seas"
        # The phrasing for these areas will be treated differently
        #  (see the waveRange_phrase)
        #
        # e.g.
        # return ["TampaBayWaters"]
        return []

    def inlandWatersWave_element(self, tree, node):
        # Weather element first and second choice to use for reporting inland waters waves
        # "WAVES 1 TO 2 FEET."
        # If there is incomplete or no data for the first element, the second will be used.
        return ("WindWaveHgt", "WaveHeight")

    def seasWaveHeight_element(self, tree, node):
        # Weather element to use for reporting seas
        # "COMBINED SEAS 10 TO 15 FEET."
        # IF above wind or swell thresholds
        return "WaveHeight"

    def seasWindWave_element(self, tree, node):
        # Weather element to use for reporting seas waves
        # "WIND WAVES 3 TO 4 FEET."
        # IF above wind or swell thresholds
        return "WindWaveHgt"

    def waveHeight_wind_threshold(self, tree, node):
        # Wind value above which waveHeight (combined seas)
        # is reported vs. wind waves.
        # Also, the Swell phrase is omitted if this threshold is exceeded.
        # Unit is knots
        return 34

    def combinedSeas_threshold(self, tree, node):
        # See wave_phrase
        # If waves and swells are above this threshold,
        # combined seas will be reported AND no Swell phrase will be reported.
        # Units: feet
        return 7

    def marine_wind_flag(self, tree, node):
        # If 1, Wind combining and wording will reflect the
        # crossing of significant thresholds such as gales.
        # E.g. "West gales to 35 knots." instead of "West winds 35 knots."
        return 0

#<16.f> - WRS >>>>>> Modified (see comment in method below)

    def phrase_descriptor_dict(self, tree, node):
        # Descriptors for phrases
        dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        dict["Wind"] = "wind"
        dict["seas"] = "combined seas"
        dict["inland waters"] = "bay and inland waters"
        dict["chop"] = "bay and inland waters"
        dict["mixed swell"] = "mixed swell"
        dict["waves"] = "wind waves"
        dict["dominant period"] = "dominant period"
        # Apply only if marine_wind_flag (see above) is set to 1:
    #<16.f> - WRS >>>>>> modified to remove the "to" part of the phrase
        dict["hurricane force winds to"] = "hurricane force winds"
        dict["storm force winds to"] = "storm force winds"
        dict["gales to"] =  "gales"
        dict["up to"] =  ""
        dict["around"] =  ""
        return dict

    def phrase_connector_dict(self, tree, node):
        # Dictionary of connecting phrases for various
        # weather element phrases
        # The value for an element may be a phrase or a method
        # If a method, it will be called with arguments:
        #   tree, node
        dict = TextRules.TextRules.phrase_connector_dict(self, tree, node)
        dict["rising to"] =  {
                                "Wind": "...rising to ",
                                "Swell": "...building to ",
                                "Swell2": "...building to ",
                                "WaveHeight": "...building to ",
                                "WindWaveHgt": "...building to ",
                         }

        dict["easing to"] =  {
                                "Wind": "...easing to ",
                                "Swell": "...subsiding to ",
                                "Swell2": "...subsiding to ",
                                "WaveHeight": "...subsiding to ",
                                "WindWaveHgt": "...subsiding to ",
                         }
        dict["backing"] =  {
                                "Wind": "...backing to ",
                                "Swell": "...becoming ",
                                "Swell2": "...becoming ",
                                "WaveHeight": "...becoming ",
                                "WindWaveHgt": "...becoming ",
                         }

        dict["veering"] =  {
                                "Wind": "...veering to ",
                                "Swell": "...becoming ",
                                "Swell2": "...becoming ",
                                "WaveHeight": "...becoming ",
                                "WindWaveHgt": "...becoming ",
                         }

        dict["becoming"] =  "...becoming "
        dict["increasing to"] =  {
                                "Wind":  "...rising to ",
                                "Swell": "...building to ",
                                "Swell2": "...building to ",
                                "WaveHeight": "...building to ",
                                "WindWaveHgt": "...building to ",
                             }
        dict["decreasing to"] =  {
                                "Wind":  "...easing to ",
                                "Swell": "...subsiding to ",
                                "Swell2": "...subsiding to ",
                                "WaveHeight": "...subsiding to ",
                                "WindWaveHgt": "...subsiding to ",
                             }
        dict["shifting to the"] =  "...shifting to the "
        dict["becoming onshore"] =  " becoming onshore "
        dict["then"] =  {"Wx": ". ",
                         "Vector": "...becoming ",
                         "Scalar": "...becoming ",
                         "otherwise": "...becoming ",
                         }
        return dict

#<16.f> - WRS >>>>>> Modified (see comment in method below)

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and not reported.
        # Units depend on the element and product
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
    #<16.f> - WRS >>>>>> Modified the values for swell below
        dict["WaveHeight"] =  2
        dict["WindWaveHgt"] =  2
        dict["Wind"] =  5
        dict["WindGust"] = 33
        dict["Swell"] =  2
        dict["Visibility"] = 3 # in nautical miles. Report if less than this value.
        return dict

#<16.f> - WRS >>>>>> Modified (see comment in method below)

    def first_null_phrase_dict(self, tree, node):
        # Phrase to use if values THROUGHOUT the period or
        # in the first period are Null (i.e. below threshold OR NoWx)
        # E.g.  LIGHT WINDS.    or    LIGHT WINDS BECOMING N 5 MPH.
        dict = TextRules.TextRules.first_null_phrase_dict(self, tree, node)
    #<16.f> - WRS >>>>>> Modified the values for wind, waveheight, windwavehgt and swell below
        dict["WaveHeight"] =  "waves 1 foot or less"
        dict["WindWaveHgt"] =  "wind waves 1 foot or less"
        dict["Wind"] =  "light wind"
        dict["Swell"] =  "swell 1 foot or less"
        return dict

#<16.f> - WRS >>>>>> Modified (see comment in method below)

    def null_phrase_dict(self, tree, node):
        # Phrase to use for null values in subPhrases other than the first
        # Can be an empty string
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
    #<16.f> - WRS >>>>>> Modified the values below for wind, waveheight, windwavehgt and swell
        dict["WaveHeight"] =  "1 foot or less"
        dict["WindWaveHgt"] =  "1 foot or less"
        dict["Wind"] =  "light"
        dict["Wx"] =  ""
        dict["Swell"] =  "1 foot or less"
        return dict

#<16.k.1> - WRS >>>>>> Using ranges of values (e.g. 10 to 15 kt) as of
#    version 16.k.1.  Modified baseline values for ranges which are
#    not correct.  If you want single values (e.g. 15 kt) instead of
#    ranges follow the commented out example.

    def maximum_range_nlValue_dict(self, tree, node):
        # Maximum range to be reported within a phrase
        #   e.g. 5 to 10 mph
        # Units depend on the product
        dict = TextRules.TextRules.maximum_range_nlValue_dict(self, tree, node)
#       WRS - Changed following line to do wind ranges of 5 kt as of 12/10/2004
        dict["Wind"] = {
                        'default': 0,
                        (0, 34):   5, #max value between 0 and 33 kt use 5 kt range
                        (34, 200):  10, #max value between 34 and 200 use 10 kt range
                        }
##    values below produce single values instead of ranges
##      dict["Wind"] = 0
        dict["Swell"] = 0
        dict["Swell2"] = 0
        dict["WaveHeight"] = 0
        dict["WindWaveHgt"] = 0

        return dict

#<16.k.1> - WRS >>>>>> Modified (see comment in method below)

    def combine_singleValues_flag_dict(self, tree, node):
        # Dictionary of weather elements to combine using single values
        # rather than ranges.  If you are using single value statistics
        # for a weather element, you will want to set this flag to 1.
        # If there is no entry for an element, min/max combining will
        # be done.
        # The value for an element may be a phrase or a method
        # If a method, it will be called with arguments:
        #   tree, node
        dict = TextRules.TextRules.increment_nlValue_dict(self, tree, node)
#<16.k.1> - WRS >>>>>> commented out the following line enable wind ranges
#        dict["Wind"] = 1
        dict["WindGust"] = 1
        dict["Swell"] = 1
        dict["Swell2"] = 1
        dict["WindWaveHgt"] = 1
        dict["WaveHeight"] = 1
#<16.f> - WRS >>>>>>    Added Period
    dict["Period"] = 1
#<16.k.1> - WRS >>>>>> Added Period2
    dict["Period2"] = 1
        return dict


########################################################################
#
#     Component Product Definitions - Overrides
#
########################################################################

#<16.f> - WRS >>>>>> ????? May want to change to use self.mode rather than
#    self.stdDevMaxAvg. self.mode works better with dominant weather
#    but currently using ranked weather so have left this alone for now

    def _PoP_analysisMethod(self, componentName):
        # Alternative PoP analysis methods for consistency between PoP and Wx
        return self.stdDevMaxAvg
        #return self.maxMode
        #return self.maximum


#<16.f> - WRS >>>>>> Override the component product definitions below if you
#      want local effects.

    def CWFPeriod(self):
        return {
            "type": "component",
            "methodList": [
                          self.assemblePhrases,
                          self.wordWrap,
                          ],

            "analysisList": [
                      # Use the following if you want moderated
                      # single values (e.g. N WIND 20 KT).
                      # Set the moderating percentage in the "moderated_dict"
                      # dictionary module.
                      # Set the combine_singleValues_flag_dict in the Local file.
#                          ("Wind", self.vectorModeratedMax, [6]),
#<16.k.1> - WRS >>>>>> changed this to use "MinMax" for winds so ranges will be included as of
                          ("Wind", self.vectorModeratedMinMax, [6]),
                          ("WindGust", self.moderatedMax, [6]),
                          ("WaveHeight", self.moderatedMax, [6]),
                          ("WindWaveHgt", self.moderatedMax, [6]),
                          ("Swell", self.vectorModeratedMax, [6]),
                          ("Swell2", self.vectorModeratedMax, [6]),
                          ("Period", self.moderatedMax, [6]),
                          ("Period2", self.moderatedMax, [6]),
#                          ("Wx", self.dominantWx, [6]),
              #<16.f> - WRS >>>>>> don't know if dominantWx or rankedWx is better for the CWF
              #        will use rankedWx for now as it is the default
                          ("Wx", self.rankedWx, [6]),
                          ("PoP", self._PoP_analysisMethod("CWFPeriod"), [6]),
                          ("PoP", self.binnedPercent, [6]),
                          ],

             "phraseList":[
                           # WINDS
               self.marine_wind_withGusts_phrase,
                           # Alternative:
                           #self.marine_wind_phrase,
                           #self.gust_phrase,
                           # WAVES
                           self.wave_withPeriods_phrase,
                           # Alternative:
                           #self.wave_phrase,
                           # Optional:
                           #self.chop_phrase,
                           # SWELLS AND PERIODS
                           self.swell_withPeriods_phrase,
                           # Alternative:
                           #self.swell_phrase,
                           #self.period_phrase,
                           # WEATHER
                           self.weather_phrase,
                           ],

          "intersectAreas": []

            }


    def CWFPeriodMid(self):
        return {
            "type": "component",
            "methodList": [
                          self.assemblePhrases,
                          self.wordWrap,
                          ],

            "analysisList": [
                      # Use the following if you want moderated
                      # single values (e.g. N WIND 20 KT).
                      # Set the moderating percentage in the "moderated_dict"
                      # dictionary module.
#                          ("Wind", self.vectorModeratedMax, [6]),
#<16.k.1> - WRS >>>>>> changed this to use "MinMax" for winds so ranges will be included as of
                          ("Wind", self.vectorModeratedMinMax, [6]),
                          ("WindGust", self.moderatedMax, [6]),
                          ("WaveHeight", self.moderatedMax, [6]),
                          ("WindWaveHgt", self.moderatedMax, [6]),
                          ("Swell", self.vectorModeratedMax, [6]),
                          ("Swell2", self.vectorModeratedMax, [6]),
              #<16.f - WRS added POP methods which are absent from the baseline version??
              ("PoP", self._PoP_analysisMethod("CWFPeriodMid")),
                          ("PoP", self.binnedPercent),
              #<16.f> - WRS >>>>>> don't know if dominantWx or rankedWx is better for the CWF
              #        will use rankedWx for now as it is the default
                          ("Wx", self.rankedWx, [6]),
#                          ("Wx", self.dominantWx, [6]),

                        ],

             "phraseList":[
                           # WINDS
               self.marine_wind_withGusts_phrase,
                           # Alternative:
                           #self.marine_wind_phrase,
                           #self.gust_phrase,
                           # WAVES
                           #self.wave_withPeriods_phrase,
                           # Alternative:
                           self.wave_phrase,
                           # Optional:
                           #self.chop_phrase,
                           # SWELLS AND PERIODS
#                           (self.swell_withPeriods_phrase, self._MarineLocalEffects_list),
                           # Alternative:
                           self.swell_phrase,
                           #self.period_phrase,
               #<16.f> - WRS >>>>>> Added required weather phrase
               # WEATHER
                           self.weather_phrase,
                           ],


          "intersectAreas": []

            }



    def CWFExtended(self):
        return { "type": "component",
                 "methodList": [
                          self.assemblePhrases,
                          self.wordWrap,
                          ],
                 "analysisList": [
              #<16.f> - WRS >>>>>> changed wind analysis period from 6 hours to 12 hours
#                          ("Wind", self.vectorModeratedMax, [24]),
#<16.k.1> - WRS >>>>>> changed this to use "MinMax" for winds so ranges will be included as of
                          ("Wind", self.vectorModeratedMinMax, [24]),
                          ("WindGust", self.moderatedMax, [24]),
                          ("WaveHeight", self.moderatedMax, [24]),
                          ("WindWaveHgt", self.moderatedMax, [24]),
                          ("PoP", self._PoP_analysisMethod("CWFExtended")),
                          ("PoP", self.binnedPercent),
              ("Swell", self.vectorModeratedMax, [24]),
                          ("Swell2", self.vectorModeratedMax, [24]),
              ("PoP", self._PoP_analysisMethod("CWFExtended")),

                      ],
                 "phraseList":[

                   #<16.f> - WRS >>>>>> changed wind phrase to marine_wind_withGusts_phrase
                               #self.marine_wind_phrase,
                   self.marine_wind_withGusts_phrase,
                   # WAVEHEIGHT
                               #self.wave_withPeriods_phrase,
                               # Alternative:
                               self.wave_phrase,
                               # Optional:
                               #self.chop_phrase,
                               # SWELLS AND PERIODS
                               #self.swell_withPeriods_phrase,
                               # Alternative:
                               self.swell_phrase,
                               #self.period_phrase,
                               # WEATHER
                               #(self.weather_phrase,
                               ],


          "intersectAreas": []

           }


#
#<16.f> - WRS >>>>>> modified "_issuance_list" so times agree with the marine directive
#      (extended portion goes from 6AM-6AM)
#

    def _issuance_list(self, argDict):
        #  This method sets up configurable issuance times with associated
        #  narrative definitions.  See the Text Product User Guide for documentation.
        if self._definition["includeEveningPeriod"] == 1:
            narrativeDefAM = [
                ("CWFPeriod", "period1"), ("CWFPeriod", 12), ("CWFPeriod", 12),
                ("CWFPeriodMid", 12), ("CWFPeriodMid", 12),
                ("CWFPeriodMid", 12),
                ("CWFExtended", 24), ("CWFExtended", 24)
                ]
            narrativeDefPM = [
                ("CWFPeriod", "period1"),("CWFPeriod", 12), ("CWFPeriod", 12),
                ("CWFPeriodMid", 12), ("CWFPeriodMid", 12), ("CWFPeriodMid", 12),
                ("CWFPeriodMid", 12),
                ("CWFExtended", 24), ("CWFExtended", 24)
                ]
        else:
            narrativeDefAM = [
                ("CWFPeriod", "period1"), ("CWFPeriod", 12), ("CWFPeriod", 12),
                ("CWFPeriodMid", 12), ("CWFPeriodMid", 24),
                ("CWFExtended", 24), ("CWFExtended", 24)
                ]
            narrativeDefPM = [
                ("CWFPeriod", "period1"), ("CWFPeriod", 12), ("CWFPeriod", 12),
                ("CWFPeriodMid", 12), ("CWFPeriodMid", 12),
                ("CWFExtended", 24), ("CWFExtended", 24), ("CWFExtended", 24)
                ]

        return [
            # WRS modified the "label" and issuance starthour and expiration hours
            # early phrases
            # note:  the start, end times and expiration times are local time
            #
            # note: self.DAY = 0600 Local time and self.NIGHT = 1800 Local time
            #
            # description -- text to appear in the startUp dialog for the product (e.g. 330 AM).
            # startHour -- start hour (in local time) for the first period.
            #              These times are relative to self.DAY() and
            #              self.NIGHT() which default to 6 and 18, respectively.
            # endHour -- end hour (in local time) for the first period.
            #              These times are relative to self.DAY() and
            #              self.NIGHT() which default to 6 and 18, respectively. The start
            # expirationHour -- hour when the product expires (in local time)
            #                   This is relitive to midnight local time of the
            #                   current day.
            # period1 Label  -- the label for the first period. e.g. ".TODAY...", ".REST OF TODAY..."
            # period1 lateNight phrase -- phrase to use if the hours of 3am to 6am must be qualified
            #                e.g. "Partly cloudy in the early morning."
            # period1 lateDay phrase -- phrase to use if the hours of 3pm to 6pm must be qualified
            #                e.g. "Partly cloudy in the early evening."
            # todayFlag -- if 1, "TODAY" and "TONIGHT" phrasing will be used in subsequent periods,
            #                otherwise, weekday wording will apply.
            # narrative definition -- component and time period pairs

            # 330 AM Early morning issuance starts at 1200Z or when product is actually
            # is actually issued. Ends
#<16.f> - WRS >>>>>> modify the following list of issuance times, valid times and expiration
#         times for your local office
###### For Pacific Standard Time #########
            ("230 AM", self.DAY()-3, self.NIGHT(), 8.5,
             ".TODAY...", "before sunrise", "late afternoon",
             1, narrativeDefAM),
            ("830 AM", self.DAY()+2, self.NIGHT(), 14.5,
             ".TODAY...", "early this morning", "late afternoon",
             1, narrativeDefAM),
            #  End times are tomorrow:
            ("230 PM", self.DAY()+8, self.NIGHT()+12, 20.5,
             ".TONIGHT...", "late tonight", "before dark",
             1, narrativeDefPM),
            ("830 PM", self.NIGHT()+2, 24 + self.DAY(), 26.5,
             ".TONIGHT...", "late tonight", "before dark",
             1, narrativeDefPM),
##     END PST Section
##
######  Below for Pacific Daylight Time ###
##            ("300 AM", self.DAY()-3, self.NIGHT(), 9,
##             ".TODAY...", "before sunrise", "late afternoon",
##             1, narrativeDefAM),
##            ("900 AM", self.DAY()+3, self.NIGHT(), 15,
##             ".TODAY...", "early this morning", "late afternoon",
##             1, narrativeDefAM),
##            #  End times are tomorrow:
##            ("300 PM", self.DAY()+9, self.NIGHT()+12, 21,
##             ".TONIGHT...", "late tonight", "before dark",
##             1, narrativeDefPM),
##            ("900 PM", self.NIGHT()+3, self.NIGHT()+12, 27,
##             ".TONIGHT...", "late tonight", "before dark",
##             1, narrativeDefPM),
####    End PDT section

            ]

    # Handling visibility within the weather phrase
    def visibility_wx_threshold(self, tree, node):
        # Weather will be reported if the visibility is below
        # this threshold (in NM) OR if it includes a
        # significant_wx_visibility_subkey (see below)
        return None

    def significant_wx_visibility_subkeys(self, tree, node):
        # Weather values that constitute significant weather to
        # be reported regardless of visibility.
        # If your visibility_wx_threshold is None, you do not need
        # to set up these subkeys since weather will always be
        # reported.
        # Set of tuples of weather key search tuples in the form:
        #  (cov type inten)
        # Wildcards are permitted.
        return [("* T"), ("* FS")]

    # Configurable Weather Values
    def wxCoverageDescriptors(self):
         list = TextRules.TextRules.wxCoverageDescriptors(self)
         #list.append(("Chc", "*", "*", "a chance"))
         return list

#<16.f> - WRS >>>>>> Modified (see comment in method below)

    def wxTypeDescriptors(self):
         list = TextRules.TextRules.wxTypeDescriptors(self)
         #list.append( ("*", "T", "*", "Dry", "dry thunderstorms") )
     #<16.f> - WRS >>>>>> modified the "rain showers" phrase to say showers
         list.append( ("*", "RW", "*", "*", "showers") )
         return list

    def wxAttributeDescriptors(self):
         list = TextRules.TextRules.wxAttributeDescriptors(self)
         #list.append( ("*", "T", "*", "Dry", "") )
         return list

#<16.f> - WRS >>>>>> modified the intensity to say light for "--"

    def wxIntensityDescriptors(self):
         list = TextRules.TextRules.wxIntensityDescriptors(self)
     #<16.f> - WRS >>>>>> modified the intensity to say light for "--"
         list.append(("*", "RW", "--", "*", "light"))
         return list

    def wxCombinations(self):
        # This is the list of which wxTypes should be combined into one.
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
                self.combine_T_RW,
            ]

    def combine_T_RW(self, subkey1, subkey2):
        # Combine T and RW only if the coverage of T
        # is dominant over the coverage of RW
        wxType1 = subkey1.wxType()
        wxType2 = subkey2.wxType()
        if wxType1 == "T" and wxType2 == "RW":
            order = self.dominantCoverageOrder(subkey1, subkey2)
            if order == -1 or order == 0:
                return 1, subkey1
        return 0, None

#<16.f> - WRS >>>>>> This is the end of the methods copied and modified
#                 in CWF_Pacific Baseline version and corresponds to
#             line 809 in the CWF_Pacific file.

#<16.f> - WRS >>>>>> Resumed modifications to CWF_Pacific Baseline file
#             corresponds to line 1135 in CWF_Pacific file.

#<16.f> WRS - Override allowedHazards to add in "SMALL CRAFT ADVISORY FOR HAZARDOUS
#    SEAS".  You also need to add the following line to the localConfig file
#    HazardKeys.append(("SS.Y", "SMALL CRAFT ADVISORY FOR HAZARDOUS SEAS"))

    # Returns a list of the Hazards allowed for this product in VTEC format.
    # These are sorted in priority order - most important first.
    def X_allowedHazards(self):
        allActions = ["NEW", "EXA", "EXB", "EXT", "UPG", "CAN", "CON", "EXP"]
        marineActions = ["NEW", "EXA", "EXB", "EXT", "CON"]
        return [
            ('HU.W', marineActions, (12, 36, 120)),  # HURRICANE WARNING
            ('TY.W', marineActions, (12, 36, 120)),  # TYPHOON WARNING
            ('TR.W', marineActions, (12, 36, 120)),  # TROPICAL STORM WARNING
            ('HU.A', allActions),  # HURRICANE WATCH
            ('TY.A', allActions),  # TYPHOON WATCH
            ('TR.A', allActions),  # TROPICAL STORM WATCH
            ('HF.W', marineActions, (12, 36, 120)),  # HURRICANE FORCE WIND WARNING
            ('SR.W', marineActions, (12, 36, 120)),  # STORM WARNING
            ('GL.W', marineActions, (12, 36, 120)), # GALE WARNING
            ('UP.W', allActions),  # ICE ACCRETION WARNING
            ('CF.W', allActions),  # COASTAL FLOOD WARNING
            ('MA.W', allActions),  # MARINE WARNING
            ('SC.Y', marineActions, (12, 36, 120)),  # SMALL CRAFT ADVISORY
        #<16.f> - WRS >>>>>> added in SCA for Hazardous Seas
            ('SS.Y', marineActions, (12, 36, 120)),  # SMALL CRAFT ADVISORY FOR HAZARDOUS SEAS
            ('SU.Y', allActions),  # HIGH SURF ADVISORY
            ('FG.Y', allActions),  # DENSE FOG ADVISORY
            ('SM.Y', allActions),  # DENSE SMOKE ADVISORY
            ('UP.Y', allActions),  # ICE ACCRETION ADVISORY
            ('AF.Y', allActions),  # VOLCANIC ASHFALL ADVISORY
            ('TO.A', allActions),  # TORNADO WATCH
            ('SV.A', allActions),  # SEVERE THUNDERSTORM WATCH
            ]

########################################################################
#
#     TextUtils.TextUtility OVERRIDES - WRS
#
#    AWIPS -  /awips/GFESuite/primary/data/databases/BASE/TEXT/TextUtility/TextUtils.TextUtility
#    RPP -    ~/release/data/databases/BASE/TEXT/TextUtility/TextUtils.TextUtility
#
########################################################################
#<16.f> - WRS >>>>>> modified "storeAWIPS" to use SSH when running server on non-AWIPS
    #    i.e. non PX) workstation.
#<16.k.1> - WRS >>>>>> Override storeAWIPS so it will work for service backup
#   If running on AWIPS store product directly
#   If running on RPP box use the "host" variable to define what machine and
#   user to log in as (e.g. host= "-l fxa pv1)

    def storeAWIPS(self, product, AWIPSkey="",host="dv2",user=""):
        # Stores text in string "product" into
        # the AWIPS text database via the given host if host is defined using
        # ssh technique. Otherwise uses the AWIPS textdb command directly.
        # Note: for the ssh mode, you need to have your ssh keys in order
    # see "getPreviousProduct" for details.
        #

        if not AWIPSkey:
            return    # do nothing

#<16.k.1> - WRS >>>>>> added a call to get the AWIPS host and user for non PX operations
#    from settings in the CWFFP_PacificFP_XXXFP_Definition.TextUtility file
    host = self._awipsTEXTDBhost
    user = self._awipsTEXTDBuser
    if user != None and user:
         user = " -l " + user

    # look for textdb on the machine the program is running on
#<16.k.1> - WRS >>>>>> Added the following "try" statemen
    try:
        textdbfile=open("/awips/fxa/bin/textdb","r")
        textdbfile.close
        # use the command directly - assumes FXA environment setup
            # (code adopted from Paul Jendrowski 9/18/03)
            # set path to textdb command
            if os.environ.has_key('FXA_HOME'):
                cmd = os.environ['FXA_HOME'] + "/bin/textdb -w " + AWIPSkey
            else:
                cmd = "/awips/fxa/bin/textdb -w " + AWIPSkey

            # issue the command
            db = os.popen(cmd, 'w')
            db.write(product)
            db.close()

#<16.f> - WRS >>>>>> use ssh to communicate with the textdb
        except:
    # WRS - modified to use ssh and host and user
        # (code adopted from Bill Schneider of WR)
            command= "ssh " + host + user + " /awips/fxa/bin/textdb -w " + AWIPSkey
            saveProduct = os.popen(command,'w')
            saveProduct.write(product)
            saveProduct.close()



#<16.k.1> - WRS >>>>>> getPreviousProduct (version 2.2) (February 11, 2005)
#<16.f> - WRS >>>>>> getPreviousProduct (version 2.1) (August 20, 2004)
#     Added "ssh" and removed "rsh"
#
# getPreviousProduct (version 2.0) (August 21, 2003)
# Written by William R. Schneider, WFO Portland Oregon
#
# This method will get a product from the AWIPS text database via the specified
# "host" AWIPS computer.  It then searchs the product and returns any text that
# falls between the "beginSearchString" and the "endSearchString".  The search
# strings must be in the "regular expression" format (so for $$ the string would
# be "\$\$"). The resultant text does not include any of the beginSearchString
# or the endSearchString. You may optionally remove blank lines, discard lines
# at the top and/or discard lines at the bottom of the text returned.
#
# Arguments:
#    productID -         (required) specify the AWIPS key for the product
#                              you wish to search
#    SearchStrings-        A list of one or more tuples which describe
#                    the text you want to search for.  The tuples
#                have the following format:
#        [(startSearchString, endSearchString,removeBlankLines,
#            topNumberOfLinesToSkip,bottomNumberOfLinesToSkip,wraplength)]
#    host -            (Optional) host name of AWIPS computer to retrive product from (default = lx1)
#    user -            (Optional) user name for login to AWIPS (default = awipsusr)


# The SearchString tupple elements are described here:
#
#    startSearchString -    (Optional) specify the starting regular expression
#                string of the text to be returned
#    endSearchString -    (Optional) specify the ending regular expression
#                of the text to be returned
#    removeBlankLines -    (Optional) 0 = do not remove blank lines (default)
#                           1 = remove blank lines
#    topNumberOfLinesToSkip -(Optional) number of lines to discard in the text
#                            after the beginSearchString is found (and blank
#                               lines have been removed if that option is set).
#    bottomNumberOfLinesToSkip-(Optional) number of lines to discard at the bottom
#                            of the retruned text.
# Return:
#    A List of strings corresponding to each search request in the searchString
#    (If searchstring is a single request then an string is returned rather
#       than a list of strings.


    def getPreviousProduct(self,
                           productID,
               SearchStrings=[],
               host="pv1",
               user= ""):
        previousProduct = ""
    previousProd = ""
        previousProductStringsList=[]
#<16.k.1> - WRS >>>>>> added a call to get the AWIPS host and user for non PX operations
    host = self._awipsTEXTDBhost
    user = self._awipsTEXTDBuser
    if user != None and user:
         user = " -l " + user
    # look for textdb on the machine the program is running on
#<16.k.1> - WRS >>>>>> Corrected error in the following "try" statment
#    to run the command on AWIPS if formatter running on AWIPS
    try:
        textdbfile=open("/awips/fxa/bin/textdb","r")
        textdbfile.close
            if os.environ.has_key('FXA_HOME'):
                openString = os.environ['FXA_HOME'] + "/bin/textdb -r " + productID
            else:
                openString = "/awips/fxa/bin/textdb -r " + productID

    #  If not found try a secure shell login to "host" as user
    except:
#<16.k.1> - WRS >>>>>> Added the next two lines to login using a uesr
#        if one was specified in the Definitions file
        try:
                openString = "ssh " + host + user + " '/awips/fxa/bin/textdb -r " + productID + "'"
        #  If that doesn't work then you are out of luck
        except:
print("!!!!!! WARNING getPreviousProduct can't find awips text database")
            if len(SearchStrings) == 1:
                return []
            else:
                return ""

    for Line in os.popen(openString,'r'):
        # remove any returns, formfeeds or trailing whitespace on each line
        Line = re.sub(r'\n', r'\n', Line)
        Line = re.sub(r'\f\n', r'\n', Line)
        Line = re.sub(r'', r'\n', Line)
        Line = re.sub(r'\f', r'\n', Line)
        Line = re.sub(r'[  \t]+\n', r'\n', Line)
            previousProd = previousProd + Line


    if type(SearchStrings) is not types.ListType:
print("getPreviousProduct must have a list of one or more tuples as the second argument\n")
        return []


    for item in SearchStrings:
#        print("ITEM=",item)
        beginSearchString=""
        endSearchString=""
        removeBlankLines=0
        topNumberOfLinesToSkip=0
        bottomNumberOfLinesToSkip=0
        wraplength=0

        itemlength=len(item)
        if itemlength > 0:
            beginSearchString = item[0]
        if itemlength > 1:
            endSearchString = item[1]
        if itemlength > 2:
            removeBlankLines = item[2]
        if itemlength > 3:
            topNumberOfLinesToSkip = item[3]
        if itemlength > 4:
         bottomNumberOfLinesToSkip = item[4]
        if itemlength > 5:
         wraplength = item[5]

#        print("SEARCHING\nbeginSearchString=",beginSearchString,"\nendSearchString=",endSearchString,"\nremoveBlankLines=",removeBlankLines,"\ntopNumberOfLinesToSkip=",topNumberOfLinesToSkip,"\nbottomNumberOfLinesToSkip=",bottomNumberOfLinesToSkip)

        previousProduct=previousProd
#        print("PREVIOUSPROD=",previousProd)
#        print("BEGINSEARCHSTRIN={",beginSearchString,"}")
        # Find the start of the text using the beginSearchString
        matchObjstart = re.search(beginSearchString + "(.+)", previousProduct, re.DOTALL)
#        print("loc1")

        if matchObjstart != None:
#            print("loc1")
#        print("STARTMATCH=", matchObjstart.group(1))
        if not endSearchString:
#            print("loc3")
            previousProduct = matchObjstart.group(1)
#            print("NEWPREVPROD=",previousProduct)
        else:
#            print("loc4")
            # find the end of the text using endSearchString
                matchObjend = re.search(endSearchString, matchObjstart.group(1),re.DOTALL)
                if matchObjend != None:
#                    print("END=", matchObjend.start(0))
#                    print( "ENDMATCH=", matchObjend.group(0))
                    previousProduct = matchObjstart.group(1)[:matchObjend.start(0)]
#                    print("PREVIOUSPRODUCT=",previousProduct)

                    else:
                    previousProduct = ""
        else:
            previousProduct = ""
#
        # remove the "topNumberOfLinesToSkip" from top of the text
        if (removeBlankLines == 1):
            #remove leading whitespace or newlines
            previousProduct = re.sub(r'^\s+', r'', previousProduct)
#        print("step1=",previousProduct)
            #remove blank lines
            previousProduct = re.sub(r'\n[ \t]*\n', r'\n', previousProduct)
#        print("step1=",previousProduct)
            #remove trailing white space
            previousProduct = re.sub(r'\s+$', r'', previousProduct)
#        print("step1=",previousProduct)

        while topNumberOfLinesToSkip > 0:
#            print("previousProduct before taking out newline=",previousProduct)
            previousProduct = re.sub(r'^.*\n', r'', previousProduct)
#        print("skiping ",topNumberOfLinesToSkip, "result=",previousProduct)
            topNumberOfLinesToSkip = topNumberOfLinesToSkip - 1
        # remove the "bottomNumberOfLinesToSkip" from bottom of the text
        while bottomNumberOfLinesToSkip > 0:
            previousProduct = re.sub(r'\n.+$', r'', previousProduct)
            bottomNumberOfLinesToSkip = bottomNumberOfLinesToSkip - 1#        # remove blank lines
        #wrap lines to wraplength if set to non-zero
        if wraplength > 0:
            previousProduct = re.sub(r'(.)\n(.)', r'\1 \2', previousProduct)
                previousProduct = self.endline(previousProduct, linelength=wraplength, breakStr=" ")

        previousProductStringsList.append(previousProduct)
#        print("loc7")
        if len(SearchStrings) == 1:
        return previousProduct
        else:
            previousProductStringsList.append(previousProduct)


    return previousProductStringsList

################################################################################
#
#     ConfigVariables.TextUtility OVERRIDES
#
#       AWIPS -  /awips/GFESuite/primary/data/databases/BASE/TEXT/TextUtility ConfigVariables.TextUtility
#    RPP -    ~/release/data/databases/BASE/TEXT/TextUtility ConfigVariables.TextUtility
#
################################################################################

#<16.f> - WRS >>>>>> "modified vector_mag_difference_nlValue_dict" wind, swell and swell2 values
    def vector_mag_difference_nlValue_dict(self, tree, node):
        # Replaces WIND_THRESHOLD
        # Magnitude difference.  If the difference between magnitudes
        # for sub-ranges is greater than this value,
        # the different magnitudes will be noted in the phrase.
        # Units can vary depending on the element and product
        return  {
#    #default values below
#            "Wind": 10,
#            "Wind20ft": 10,
#            "TransWind": 10,
#            "FreeWind": 10,
#            "Swell": 5,  # ft
#            "Swell2": 5,  # ft
        # WRS modified
        "Wind": 5,  # mph
        "Swell": 2,  # ft
        "Swell2": 2,  # ft
        "otherwise": 5,
            }

#<16.f> - WRS >>>>>> modified non-linear values for scalar differences to be reported

    def scalar_difference_nlValue_dict(self, tree, node):
        # Scalar difference.  If the difference between scalar values
    #<16.f> - WRS >>>>>> this next statement is apparently wrong - should be "equal or greater"
        # for 2 sub-periods is greater than this value,
        # the different values will be noted in the phrase.
        return {
            "WindGust": 10, # knots or mph depending on product
            "Period": 4, # seconds
            "PoP": 10, # percentage
#            "WaveHeight": 2, # feet
            "WaveHeight": {
                        'default': 0,
                        (0, 8):   2, #max value between 0 and 7 ft inclusive 2 ft diff
                        (8, 20):  3, #max value between 8 and 20 ft inclusive 3 ft diff
                        },

#            "WindWaveHgt": 5, # feet

            "WindWaveHgt": {
                        'default': 0,
                        (0, 8):   2, #max value between 0 and 7 ft inclusive 2 ft diff
                        (8, 20):  3, #max value between 8 and 20 ft inclusive 3 ft diff
                        },
            "Swell": {
                        'default': 0,
                        (0, 11):   2, #max value between 0 and 10 ft inclusive 2 ft diff
                        (11, 20):  3, #max value between 8 and 20 ft inclusive 3 ft diff
                        },
        "otherwise": 10,
          }



#<16.f> - WRS >>>>>> changed direction differences to 30 degrees from 60.

    def vector_dir_difference_dict(self, tree, node):
        # Replaces WIND_DIR_DIFFERENCE
        # Direction difference.  If the difference between directions
        # for sub-ranges is greater than or equal to this value,
        # the different directions will be noted in the phrase.
        # Units are degrees
        return {

            "Wind": 30, # degrees
            "Wind20ft": 60, # degrees
            "TransWind": 60,  # mph
            "FreeWind": 60,  # mph
            "Swell":30, # degrees
            "Swell2":30, # degrees
            "otherwise": 60,
            }

#<16.f> - WRS >>>>>> Modified (see comment in method below)

    def periodCombining_elementList(self, tree, node):
        # Weather Elements to determine whether to combine periods
#        return ["Sky", "Wind", "Wx", "PoP", "MaxT", "MinT"]
    #<16.f> - WRS >>>>>> put in elements for CWF
#        return ["Wind", "WaveHeight", "Swell", "Swell2", "Period", "Period2"]
        # Marine
        return ["Wind", "Swell"]

    def periodCombining_startHour(self, tree, node):
        # Hour after which periods may be combined
        return 36


    # Automatic Collapsing of Sub-phrases for Combined periods
    def collapseSubPhrase_hours_dict(self, tree, node):
        # If the period is longer than these hours, subphrases will automatically
        # be collapsed.
        return {
            "otherwise": 24,
            #"Wx": 12,
            }

    def collapseSubPhrase_hours(self, tree, node, key, value):
        return self.access_dictionary(tree, node, key, value, "collapseSubPhrase_hours_dict")

    def mergeMethod_dict(self, tree, node):
        # Designates the mergeMethod to use when sub-phrases are automatically collapsed.
        return {
            "otherwise": "MinMax",
            "PoP": "Max",
            "Wx": "Average",
            }
    def mergeMethod(self, tree, node, key, value):
        return self.access_dictionary(tree, node, key, value, "mergeMethod_dict")

    def nextDay24HourLabel_flag(self, tree, node):
        # Return 1 to have the TimeDescriptor module label 24 hour periods starting
        # after 1600 as the next day.
        # This is needed for the Fire Weather Extended product,
        # but not for other products when period combining.
        # NOTE: If you are doing period combining, you should
        # set this flag to zero and set the "splitDat24HourLabel_flag" to 1.
        return 0

    def splitDay24HourLabel_flag(self, tree, node):
        # Return 0 to have the TimeDescriptor module label 24 hour periods
        # with simply the weekday name (e.g. SATURDAY)
        # instead of including the day and night periods
        # (e.g. SATURDAY AND SATURDAY NIGHT)
        # NOTE: If you set this flag to 1, make sure the "nextDat24HourLabel_flag"
        # is set to zero.
        return 0

    def mostImportant_dict(self, tree, node):
        # Can be set to "Min" or "Max". Works for Scalar or Vector elements.
        # Only the most important sub-phrase will be reported
        # using the "mostImportant_descriptor" (see below).
        # For example, instead of:
        #   WIND CHILL READINGS 5 BELOW TO 15 BELOW ZERO IN THE EARLY
        #   MORNING INCREASING TO ZERO TO 10 BELOW ZERO IN THE AFTERNOON
        # we will report
        #   LOWEST WIND CHILL READINGS 5 BELOW TO 15 BELOW IN THE EARLY
        #   MORNING
        return {
            "otherwise": None,
            "WindChill": "Min",
            }
    def mostImportant(self, tree, node, key, value):
        return self.access_dictionary(tree, node, key, value, "mostImportant_dict")

    def mostImportant_descriptor_dict(self, tree, node):
        return {
            "otherwise": None,
            "WindChill": "lowest wind chill readings",
            }
    def mostImportant_descriptor(self, tree, node, key, value):
        return self.access_dictionary(tree, node, key, value, "mostImportant_descriptor_dict")


#<16.f> - WRS >>>>>> modified marineRounding because the base version is wrong

    def marineRounding(self, value, mode, increment, maxFlag):
        # Rounding for marine winds
        mode = "Nearest"
        if maxFlag:
    #<16.f> - WRS >>>>>> added following two lines for Small Craft advisory threshold (21 kt)
            if value > 20 and value < 23:
                mode = "RoundUp"
            elif value > 30 and value < 34:
                mode = "RoundDown"
            elif value > 45 and value < 48:
                mode = "RoundDown"
            else:
                mode = "Nearest"
        return self.round(value, mode, increment)

######################################################################
#
#    VectorRelatedPhrases.TextUtility OVERRIDES
#
#    AWIPS -  /awips/GFESuite/primary/data/databases/BASE/TEXT/TextUtility/VectorRelatedPhrases.TextUtility
#    RPP -    ~/release/data/databases/BASE/TEXT/TextUtility/VectorRelatedPhrases.TextUtility
#
######################################################################
#
#<16.k.1> - WRS >>>>>> changed wording of next line to from "with gusts to around"
#      to "with gusts to".  Warnings and advisories can now be triggered
#      by gusts

    def embedded_gust_phrase(self, tree, node, gustStats, maxWind, subRange):
        # Determine what type of gust phrase to add. Day and night are treated
        # differently with gusts phrases toned down a bit for night.
        gusts = None
        if gustStats is None:
           # If useWindForGusts_flag is set, use max Wind for reporting gusts
           if self.useWindsForGusts_flag(tree,  node) == 1:
               windStats = tree.stats.get(
                   "Wind", subRange, node.getAreaLabel(), statLabel="vectorMinMax",
                   mergeMethod="Max")
               if windStats is None:
                   return ""
               else:
                   gusts, dir = windStats
        else:
            gusts = self.getValue(gustStats,"Max")
#        print("GUSTS IN GRID SAMPLE ARE", gusts)
        if gusts is None:
            return ""
        threshold = self.nlValue(self.null_nlValue(tree, node, "WindGust", "WindGust"), gusts)
#        print("GUSTS IN GRID SAMPLE ARE", gusts), "THREASHOLD is", threshold
        if gusts < threshold:
            return ""
        gustPhrase = ""
        outUnits = self.element_outUnits(tree, node, "WindGust", "WindGust")
        units = self.units_descriptor(tree, node, "units", outUnits)
        windDifference = self.nlValue(self.gust_wind_difference_nlValue(tree, node), maxWind)
        if gusts - maxWind > windDifference:
            # day is 0 for night and 1 for day.
#<16.k.1> - WRS >>>>>> commented out the following because in the CWF you don't want to use
#           these types of phrases, just report the gust value 12/10/2004
#            day = self.getPeriod(subRange,1)
#            if gusts <= 20:
#                if day == self.DAYTIME():
#                    gustPhrase = " and gusty"
#            elif gusts > 20 and gusts <= 30:
#                if day == self.DAYTIME():
#                    gustPhrase = " with higher gusts"
#                else:
#                    gustPhrase = " and gusty"
#            else:
                gustPhrase = " with gusts to " + `int(gusts)` + " " + units
        return gustPhrase


#<16.k.1> - WRS >>>>>> added this in from "VectorRelatedPhrases.UserPython to set the gusts
# difference allowed under the new marine rules for PQR as of 12/10/2004
    ### WindGust
    def gust_wind_difference_nlValue(self, tree, node):
        # Difference between gust and maxWind below which gusts are not mentioned
        # Units are mph
        return 1

######################################################################
#
#    MarinePhrases.TextUtility OVERRIDES
#
#    AWIPS -  /awips/GFESuite/primary/data/databases/BASE/TEXT/TextUtility/MarinePhrases.TextUtility
#    RPP -    ~/release/data/databases/BASE/TEXT/TextUtility/MarinePhrases.TextUtility
#
######################################################################
#
#<16.k.1> - WRS >>>>>> changed wording of swell phrase for two seperate swells to
#           be "N swell 15 ft 20 seconds. Secondary swell S 20 ft at 15 seconds.

    def swell_words(self, tree, node):
        # Create phrase for swell for a given set of stats in statsByRange
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
            swellWords = self.simple_vector_phrase(tree, node, swellInfo, checkRepeating)
            if swellWords == "null" or not swellWords:
                subPhraseParts.append(swellWords)
                continue
            # Add Period
            periodPhrase = ""
            if periodFlag == 1:
                periodStats = self.getStats(statDict, period)
                periodPhrase = self.embedded_period_phrase(tree, node, periodStats)
                swellWords = swellWords + periodPhrase
            subPhraseParts.append(swellWords)

#print("swell", node.getTimeRange(), subPhraseParts)
        if subPhraseParts[1] != "null" and subPhraseParts[1] :
#<16.k.1> - WRS >>>>>> changed wording of next line include ". Secondary Swell"
#            words =  subPhraseParts[0] + " and " + subPhraseParts[1]
            words =  subPhraseParts[0] + ". secondary swell " + subPhraseParts[1]
            # Check for mixed swell on first subPhrase
            if node.getIndex() == 0:
                mixedSwell = self.checkMixedSwell(tree, node, statDict)
                if mixedSwell:
                    mixedSwellDesc = self.phrase_descriptor(tree, node, "mixed swell", "Swell")
                    phrase = node.getParent()
                    phrase.set("descriptor", mixedSwellDesc)
                    phrase.doneList.append(self.embedDescriptor)
        else:
            words =  subPhraseParts[0]

        return self.setWords(node, words)

########################################################################
#
#     WRS methods added
#
########################################################################
#
#<16.f> - WRS >>>>>> WRS added method to post process each forecast line and modify
#       phrases that don't conform to local requirements/specifications
#
    def modifyText(self, fcst):
        return fcst
        fcst = re.sub(r'(\W)WIDESPREAD *\n*RAIN(\W)', r'\1RAIN\2',fcst)
##        fcst = re.sub(r'(\W)RAIN\n* *SHOWERS(\W)', r'\1SHOWERS\2',fcst)
##        fcst = re.sub(r'\.RAIN', r'. RAIN',fcst)
        # remove the words "likely" and "around" to simplify the forecast
#        fcst = re.sub(r'([ \n]+)LIKELY', r'',fcst)
        fcst = re.sub(r'([ \n]+)AROUND', r'',fcst)
    # remove any slight chance of liquid precip
        fcst = re.sub(r'[ \n]+SLIGHT[ \n]+CHANCE[ \n]+OF[ \n]+(RAIN|SHOWERS|DRIZZLE)[ A-Za-z0-9\n]*\.', r'',fcst)
    # remove stuff like "showers in the morning. showers in the afternoon."
#    fcst = re.sub(r'(\.\n* *SNOW SHOWERS)[A-Za-z \n]*\.(\n* *SNOW SHOWERS[A-Za-z \n]*\.)', r'\1.',fcst)
#    fcst = re.sub(r'(\.\n* *RAIN)[A-Za-z \n]*\.(\n* *RAIN[A-Za-z \n]*\.)', r'\1.',fcst)
#    fcst = re.sub(r'(\.\n* *SNOW)[A-Za-z \n]*\.(\n* *SNOW[A-Za-z \n]*\.)', r'\1.',fcst)
#    fcst = re.sub(r'(\.\n* *SHOWERS)[A-Za-z \n]*\.(\n* *SHOWERS[A-Za-z \n]*\.)', r'\1.',fcst)

#<16.f> - WRS >>>>>>  change phrases like "RAIN LIKELY LATE IN THE
#         MORNING...THEN SHOWERS LIKELY
#         IN THE AFTERNOON" to "RAIN LIKLEY LATE IN THE MORNING...TURNING TO
#         SHOWERS LIKLEY IN THE AFTERNOON"
    fcst = re.sub(r'(RAIN[A-Za-z \n]*\.\.\.)THEN([\n ]*SHOWERS[A-Za-z \n]*\.)', r'\1TURNING TO\2',fcst)

#       WRS added these substitutions to reword "expected advisory/warning"
#       headlines
#
        fcst = re.sub(r'SMALL CRAFT ADVISORY EXPECTED', r'SMALL CRAFT ADVISORY WINDS EXPECTED',fcst)
        fcst = re.sub(r'SMALL CRAFT ADVISORY FOR HAZARDOUS SEAS EXPECTED', r'SMALL CRAFT ADVISORY SEAS EXPECTED',fcst)
        fcst = re.sub(r'GALE WARNING EXPECTED', r'GALE FORCE WINDS EXPECTED',fcst)
        fcst = re.sub(r'STORM WARNING EXPECTED', r'STORM FORCE WINDS EXPECTED',fcst)
        fcst = re.sub(r'HURRICANE FORCE WIND WARNING EXPECTED', r'HURRICANE FORCE WINDS EXPECTED',fcst)
#    return fcst

##################  END of OVERRIDES  ##################




