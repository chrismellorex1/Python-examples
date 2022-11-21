import string
import time
import re
import os
import types
import copy
import AbsTime
import TimeRange

import TextRules
import SampleAnalysis

import sys

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class FWFTable_MFL_Overrides:
    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************
    # Make sure to indent methods inside the class statement.
    #----- WFO MFL FWFTable Overrides -----

    # It is helpful to put a debug statement at the beginning of each
    # method to help with trouble-shooting.
    #def _method(self):
        #self.debug_print("Debug: _method in FWFTable_SR_Overrides")

    # Example of Overriding a dictionary from TextRules
    #def phrase_descriptor_dict(self, tree, node):
        #dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        #dict["PoP"] = "chance of"
        #return dict

    def maximum_range_nlValue_dict(self, tree, node):
        dict = TextRules.TextRules.maximum_range_nlValue_dict(self, tree, node)
        # Maximum range to be reported within a phrase
        #   e.g. 5 to 10 mph
        # Units depend on the product
        dict ["MaxT"] = 4
        dict ["MinT"] = 4
        dict ["HeatIndex"] = 0
        dict ["Wind"] = {
            (0, 4): 0,
            (4, 33): 5,
            (33, 52): 10,
            (52, 200): 20,
            "default": 5,
            }
        return dict

    def _rowList(self):
        # The rowList is controls what parameters go into the table.
        # The list is a set of (label:method) pairs.
        # You may change the label if you like.
        # The order of the list determines the order of the rows in the table
        # so you may re-arrange the order if you like.
        return [
            # Directive requirements
            #("CLOUD COVER", self._cloudCover_row),
            ("Cloud cover", self._cloudCover_row),
            #("CHANCE PRECIP (%)", self._chancePrecip_row),
            ("Chance precip (%)", self._chancePrecip_row),
            #("PRECIP TYPE", self._precipType_row),
            ("Precip type", self._precipType_row),
            #("TEMP (24HR TREND)", self._tempWithTrend_row),
            ("Temp (24hr trend)", self._tempWithTrend_row),
            #("RH % (24HR TREND)",self._rhWithTrend_row),
            ("RH % (24hr trend)", self._rhWithTrend_row),
            # Use these if you do not want trends
            #("TEMP", self._temp_row),
            #("RH %", self._rh_row),
            #("20FT WIND MPH (AM)", self._windValleyMph_row),
            ("20ft wind mph (AM)", self._windValleyMph_row),
            #("20FT WIND MPH (PM)", self._windRidgeMph_row),
            ("20ft wind mph (PM)", self._windRidgeMph_row),
            #("20FT WIND GUST MPH", self._windgust_row),
            ("20ft wind gust mph", self._windgust_row),
            # Directive optional products
            #("PRECIP DURATION", self._precipDuration_row),
            ("Precip duration", self._precipDuration_row),
            #("PRECIP BEGIN", self._precipBegin_row),
            ("Precip begin", self._precipBegin_row),
            #("PRECIP END", self._precipEnd_row),
            ("Precip end", self._precipEnd_row),
            #("PRECIP AMOUNT", self._precipAmount_row),
            ("Precip amount", self._precipAmount_row),
##            ("MIXING HGT(M-AGL/MSL)", self._mixHgtM_row),
            ("LAL", self._lal_row),
            #("MIXING HGT(FT-AGL)", self._mixHgtFt_row),
            ("Mixing hgt(ft-AGL)", self._mixHgtFt_row),
##            ("TRANSPORT WND (KTS)", self._transWindKts_row),
##            ("TRANSPORT WND (M/S)", self._transWindMS_row),
            ##("VENT RATE (KT-FT)", self._ventRateKtFt_row),
##            ("VENT RATE (M/S-M)", self._ventRate_row),
##            ("DISPERSION", self._dispersion_row),
##            ("SUNSHINE HOURS", self._sunHours_row),
##            # If you need Ceiling, uncomment the Ceiling line in _getAnalysisList
            #("TRANSPORT WND (MPH)", self._transWindMph_row),
            ("Transport wnd (mph)", self._transWindMph_row),
            #("DISPERSION INDEX", self._dsi_row),
            ("Dispersion index", self._dsi_row),
##            ("CEILING", self._ceiling_row),
            #("MAX LVORI", self._lvori_row),
            ("Max LVORI", self._lvori_row),
##            ("CWR", self._cwr_row),
##            ("HAINES INDEX", self._haines_row),
##            ("RH RECOVERY", self._rhRecovery_row),
##            # If you need 500m Mix Hgt Temp, uncomment the MixHgt500
##            # line in _getAnalysisList
##            #("MIX HGT 500", self._mixHgt500_row),
##            ("STABILITY CLASS", self._stability_row),
            ]

    def _tempWithTrend_row(self, fcst, label, statList, priorStatDict):
        dayElement = "MaxT"
        nightElement = "MinT"
        dayMinMax = "Max"
        nightMinMax = "Min"
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self.dayOrNightVal, [dayElement, nightElement, dayMinMax,
            nightMinMax, "Ttrend", priorStatDict, statList,
            self._timeRangeList], self._rowLabelWidth,
            self._fixedValueWidth, self._columnJustification)
        return fcst

#########################################################################################
#added 2/26/13

    def _windgust_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self._windgust, ["mph"], self._rowLabelWidth,
            self._fixedValueWidth, self._columnJustification)
        return fcst


    def _windgust(self, statDict, timeRange, argList):
        gust = self.getStats(statDict, "WindGust")
        period1, period2 = gust
        print("Period 1", period1)
        print("Period 2", period2)

        gust1, time1 = period1
        gust2, time2= period2
        print("gust1 = ", gust1)
        print("gust2 = ", gust2)

        print("Max Gust", max(gust1, gust2))
        maxgust = max(gust1, gust2)

        # uncomment if you want the formatter to stop here so you can see the values
          # I had to add "import sys" to the top of the formatter to get this to work
          # allows to you avoid waiting till the formatter completes to see the values
          # it is going to output
#        sys.exit("abort") #

        if gust1 is None:
            return "N/A"
        else:
            maxgust = self.ktToMph(maxgust)*self._windAdjustmentFactor
            return self.getScalarVal(maxgust)

#########################################################################################

    def moderated_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        return {
                "Wind": (0, 15),
                "WindGust": (0, 15),
                "Wind20ft": (0, 15),
                "TransWind": (0, 15),
                }

    def periodCombining_startHour(self, tree, node):
        # Hour after which periods may be combined
        return 72

    def nextDay24HourLabel_flag(self, tree, node):
        # Return 1 to have the TimeDescriptor module label 24 hour periods starting
        # after 1600 as the next day.
        # This is needed for the Fire Weather Extended product,
        # but not for other products when period combining.
        # NOTE: If you are doing period combining, you should
        # set this flag to zero and set the "splitDay24HourLabel_flag" to 1.
        return 0

    def splitDay24HourLabel_flag(self, tree, node):
        # Return 0 to have the TimeDescriptor module label 24 hour periods
        # with simply the weekday name (e.g. SATURDAY)
        # instead of including the day and night periods
        # (e.g. SATURDAY AND SATURDAY NIGHT)
        # NOTE: If you set this flag to 1, make sure the "nextDat24HourLabel_flag"
        # is set to zero.
        return 1

    def _getAnalysisList(self):
        return[
          ("Sky", self.avg),
          ("PoP", self.stdDevMaxAvg),
          ("Wx", self.dominantWx, [3]),
          ("Wx", self.dominantWx, [0]),
          ("MaxT", self.stdDevMinMax),
          ("MinT", self.stdDevMinMax),
          ("T", self.minMax),
          ("Wind", self.vectorModeratedMax, [6]),
          ("Wind20ft", self.vectorModeratedMax, [6]),
          ("WindGust", self.moderatedMax, [6]),
          ("QPF", self.minMaxSum),
          ("MaxRH", self.stdDevMinMax),
          ("MinRH", self.stdDevMinMax),
          ("RH", self.minMax),
          ("MixHgt", self.minMax, [0]),
          ("MixHgt", self.avg, [0]),
          ("TransWind", self.vectorModeratedMax, [0]),
         # ("VentRate", self.minMax, [0]), # aka "Dispersion" prior to RPP20
          ("LDSI", self.stdDevMinMax),#minMaxAvg),
         # ("HrsOfSun", self.avg),
          # Uncomment the next line if you're carrying Cig Height
          ("Ceiling", self.minMax),
         # ("CWR", self.stdDevMaxAvg),
         # ("Haines", self.minMaxAvg),
          ##("LAL", self.minMax, [3]),
          ("LAL", self.maximum),
          ("Ttrend", self.minMax),
          ("RHtrend", self.minMax),
         # ("Stability", self.avg),
          ("LVORI", self.minMax),
          # Uncomment the next line if you're carrying 500m mix height temp
          #("MixHgt500", self.avg),
          ]

#     def _determineTimeRanges(self, argDict):
#         # Determine the time ranges which need to be samplePM
#         # Set up self._timeRangeList, self._extendedRange
#         # Create a list (or lists) of tuples:  (timeRange, timeRangeLabel)
#         self._currentTime = argDict['creationTime']#time.time()
#         self._isDST = time.localtime(self._currentTime)[8]
#         self._currentHour = time.gmtime(self._currentTime)[3]
#
#         if self._productIssuance == "Morning":
#            # if self._issuanceType == "UPDATE" or self._issuanceType == "CORRECTION":
#            #     Today = self.createTimeRange(self._currentHour+1, 24 - self._isDST, "Zulu")
#            #     print "Morning update detected: altering Today timeRange to ", `Today`
#             rangeNames = ["Today", "Tonight", "Tomorrow"]
#             #else:
#             #    rangeNames = ["Today", "Tonight", "Tomorrow"]
#
#         else:
#             dayTime3 = self.createTimeRange(56, 68, "LT")
#             #if self._issuanceType == "UPDATE" or self._issuanceType == "CORRECTION":
#             #    if self._currentHour < 12:
#             #        Tonight = self.createTimeRange(self._currentHour, 12 - self._isDST, "Zulu")
#             #        print "Evening update detected: altering Tonight timeRange to ", `Tonight`
#             #    rangeNames = [Tonight, "Tomorrow", "Tomorrow Night", dayTime3]
#             #    else:
#             rangeNames = ["Tonight", "Tomorrow", "Tomorrow Night", dayTime3]
#             #else:
#             #    rangeNames = ["Tonight", "Tomorrow", "Tomorrow Night", dayTime3]
#
#         self._timeRangeList = self.getTimeRangeList(
#             argDict, rangeNames, self._getLabel)
#
#         # Determine time range to BEGIN the extended forecast
#         length = len(self._timeRangeList)
#         lastPeriod = self._timeRangeList[length-1][0]
#
#         self._extendedRange = self.IFP().TimeRange(
#             lastPeriod.endTime(), lastPeriod.endTime() + 3600)
#
#         # Determine prior time range
#         firstPeriod, label = self._timeRangeList[0]
#         self._priorTimeRange = self.IFP().TimeRange(
#             firstPeriod.startTime() - 24*3600, firstPeriod.startTime())
#
#         # Get entire timeRange of table for Headlines
#         # Tom says: I'm very unsure about removing this line...........
#         self._timeRange = self.IFP().TimeRange(
#             firstPeriod.startTime(), lastPeriod.endTime())
#         argDict["productTimeRange"] = self._timeRange
#
#         # Determine issue time
#         self._issueTime = self.IFP().AbsTime.current()
#
#         # Sets up the expiration time
#         self._expireTime, self._ddhhmmTimeExpire = \
#           self.getExpireTimeFromLToffset(self._currentTime,
#           self.expireOffset(), "")
#
#         # Calculate current times
#         self._ddhhmmTime = time.strftime(
#             "%d%H%M", time.gmtime(self._currentTime))
#         self._timeLabel = self.getCurrentTime(
#            argDict, "%l%M %p %Z %a %b %e %Y", stripLeading=1).upper()
#
#         return

    def _preProcessProduct(self, fcst, argDict):
        # Add product heading to fcst string
        if self._areaName:
             productName = self._productName.strip() + " for " + \
                           self._areaName.strip()
        else:
             productName = self._productName.strip()

        issuedByString = self.getIssuedByString()
        productName = self.checkTestMode(argDict, productName)

        fcst =  fcst + self._wmoID + " " + self._fullStationID + " " + \
               self._ddhhmmTime + "\n" + self._pil + "\n\n" +\
               productName + "\n" +\
               "National Weather Service " + self._wfoCityState + \
               "\n" + issuedByString + self._timeLabel + "\n\n"

        # Put in a place holder for the headlines to be substituted in
        # "postProcessProduct"
        fcst += "|*HEADLINES*|" + "\n\n"
        self._prodHeadlines = []

        #fcst = fcst + ".DISCUSSION..." + "\n\n\n" + "FOG DEVELOPMENT IS |*NOT*| EXPECTED AT THIS TIME." + "\n\n\n"
        fcst += ".DISCUSSION..." + "\n\n\n" + "Fog development is |*not*| expected at this time." + "\n\n\n"
        return fcst

    def phrase_connector_dict(self, tree, node):
        # Dictionary of connecting phrases for various
        # weather element phrases
        # The value for an element may be a phrase or a method
        # If a method, it will be called with arguments:
        #   tree, node
        return {
            # Used for Scalar and Wx elements
            "then": {
                 "Sky": " then becoming ",
                 "otherwise": " then ",
                 },
            # Used for Scalar and Vector elements
            "increasing to": {
                  "Sky": " then becoming ",
                  "WaveHeight": " building to ",
                  "otherwise": " becoming ",
                  },
            "decreasing to": {
                  "Sky": " then becoming ",
                  "WaveHeight": " subsiding to ",
                  "otherwise": " decreasing to ",
                  },
            "becoming": " becoming ",
            "shifting to the": " becoming ", #" shifting to the ",

            # Used for Marine Vector weather elements
            "rising to": " rising to ",
            "easing to": " easing to ",
            "backing": " backing ",
            "veering": " veering ",
            "becoming onshore": " becoming onshore",
            }

    def getPopType(self, tree, node, pop, wxWords, attrDict):
        popType = "rain"
        if self.wxQualifiedPoP_flag(tree, node) == 1:
            #  Examine reported weather type(s) from phrase.
            #  If there is more than one descriptor for precipitating weather
            #   or if they are general weather types,
            #     return "precipitation"
            #  Otherwise, describe the weather type
            #     e.g. chance of rain, chance of snow
            wxTypes = []
            if "reportedRankList" in attrDict:
                rankList = attrDict["reportedRankList"]
                for subkey, rank in rankList:
                    wxTypes.append(subkey.wxType())
            generalTypes = ["IP", "ZL", "ZR", "ZF", "ZY"]
            for general in generalTypes:
                if general in wxTypes:
                    return "precipitation"
            descriptors = {
                "R": "rain",
                "RW": "showers",
                "S": "snow",
                "SW": "snow",
                "T": "thunderstorms",
                }
            popTypes = []
            for wxType in wxTypes:
                if wxType in ["R", "RW", "T"]:
                    desc = descriptors[wxType]
                    if desc not in popTypes:
                        popTypes.append(desc)
            if len(popTypes) > 1:
                popType = "rain"
            elif len(popTypes) == 1:
                popType = "rain"#popTypes[0]
        return popType

    # This version will report only the weather types that
    # match the reported PoP
##    def getPopType(self, tree, node, pop, wxWords, attrDict):
##        popType = "precipitation"
##        if self.wxQualifiedPoP_flag(tree, node) == 1:
##            ## Need to find weather type(s) from phrase.
##            ## "wxWords" is the concatenation of all weather phrases
##            ## for this component.
##            ## Returns "popType" e.g. chance of rain, chance of rain and snow
##            wxTypes = []
##            if attrDict.has_key("reportedRankList"):
##                rankList = attrDict["reportedRankList"]
##                for subkey, rank in rankList:
##                    # Check the coverage against the reported PoP
##                    covLow, covHigh = self.coveragePoP_value(subkey.coverage())
##                    if covHigh >= pop:
##                        wxTypes.append(subkey.wxType())
##            popType = None
##            generalTypes = ["IP", "ZL", "ZR", "ZF", "ZY"]
##            for general in generalTypes:
##                if general in wxTypes:
##                    popType = "precipitation"
##            if popType is None:
##                rain = 0
##                snow = 0
##                thunder = 0
##                showers = 0
##                snowShowers = 0
##                rainShowers = 0
##                if "R" in wxTypes:
##                    rain = 1
##                if "S" in wxTypes:
##                    snow = 1
##                if "RW" in wxTypes:
##                    showers = 1
##                if "SW" in wxTypes:
##                    snowShowers = 1
##                if "T" in wxTypes:
##                    thunder = 1
##                if showers and not snowShowers:
##                    rainShowers = 1
##                if (rain or rainShowers or thunder) and snow:
##                    popType = "precipitation"
##                else:
##                    if snow or snowShowers:
##                        if rain or rainShowers:
##                            if wxWords.find(" or ") > -1:
##                                popType = "rain or snow"
##                            else:
##                                popType = "rain and snow"
##                        else:
##                            popType = "snow"
##                    elif rain and not rainShowers:
##                        popType = "rain"
##                    elif showers:
##                        popType = "showers"
##                        if thunder:
##                            popType = "showers and thunderstorms"
##                    elif thunder:
##                        popType = "thunderstorms"
##                    else:
##                        popType = "precipitation"
##                if popType is None:
##                    popType = "precipitation"
##        return popType

    def pop_sky_lower_threshold(self, tree, node):
        # Sky condition will not be reported if Pop is above this threshold
        return 90

   # def _precipDuration_row(self, fcst, label, statList, priorStatDict):
   #     fcst = fcst + self.makeRow(
   #         label, self._colWidth, self._timeRangeList, statList,
   #         self.maxVal, ["WxDur"], self._rowLabelWidth,
   #         self._fixedValueWidth, self._columnJustification)
   #     return fcst

    def _dsi_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self.minOrMaxLDSIVal, ["LDSI"], self._rowLabelWidth,
            self._fixedValueWidth, self._columnJustification)
        return fcst

    def _lvori_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
           # self._lvori, ["LVORI"], self._rowLabelWidth,
            self.maxNightVal, ["LVORI"], self._rowLabelWidth,
            self._fixedValueWidth, self._columnJustification)
        return fcst

    def maxNightVal(self, stats, timeRange, argList):
        # Return a scalar text string value representing the max value
        # The desired element name must be the first element of argList
        localTimeRange = self.shiftedTimeRange(timeRange)
        dayNight = self.getPeriod(localTimeRange)
        element = argList[0]
        value = self.getStats(stats, element)
        if value is None:
            return ""
        min, max = value
        if dayNight == self.DAYTIME():
            return ""#self.getScalarVal(max)
        else:
            return self.getScalarVal(max)

       # return self.getScalarVal(max)

    def minOrMaxLDSIVal(self, statDict, timeRange, argList):
        localTimeRange = self.shiftedTimeRange(timeRange)
        dayNight = self.getPeriod(localTimeRange)
        element = argList[0]
        value = self.getStats(statDict, element)
#print("stats is", stats)
        if value is None:
            return ""
       # min, max, avg = value
        min, max = value
        print("value", value)
        print("max DSI value is", max)
        print("min DSI value is", min)
       # avg = int((min + max)/2)
# print("avg DSI", avg)
# print("nightDSI", nightDSI)
        if dayNight == self.DAYTIME():
            return self.getScalarVal(max)
        else:
            return self.getScalarVal(min)

    def _ceiling_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self._cigHeight, None, self._rowLabelWidth,
            self._fixedValueWidth, self._columnJustification)
        return fcst

    def _cigHeight(self, statDict, timeRange, argList):
        # Return ceiling height in feet
        cigStats = self.getStats(statDict, "Ceiling")
        if cigStats is None:
            return "N/A"
        else:
            min, max = cigStats
            min = self.round(min, "Nearest", 1)
            if min <=  3000:
                value = int(self.round(min, "Nearest", 100))
            elif min <= 6500:
                value = int(self.round(min, "Nearest", 500))
            elif min < 30000:
                value = int(self.round(min, "Nearest", 1000))
            else:
                return "NO CIG"
        return repr(value)

    def _cloudCover_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self._sky, ["Sky"], self._rowLabelWidth, self._fixedValueWidth,
            self._columnJustification)
        return fcst

    def _sky(self, statDict, timeRange, argList):
        # Return a sky value
        sky = self.getStats(statDict, "Sky")
        if sky is None:
            value = ""
        elif  sky < 11:
            #value = "CLEAR"
            value = "Clear"
        elif sky <= 25:
            #value = "MCLEAR"
            value = "Mclear"
        elif sky <= 61:
            #value = "PCLDY"
            value = "Pcldy"
        elif sky <= 91:
            #value = "MCLDY"
            value = "Mcldy"
        else:
            #value = "CLOUDY"
            value = "Cloudy"
        return value

    def temporalCoverage_dict(self, parmHisto, timeRange, componentName):
        # This is temporalCoverage percentage by weather element
        # Used by temporalCoverage_flag
        return {
                "PoP": 20,
                #"LAL" : 20,
                }

    def ExtendedNarrative(self):
        # check for period combining first
        if self._periodCombining:
            methodList = [self.combineComponentStats, self.assembleChildWords]
        else:
            methodList = [self.assembleChildWords]

        return {
          "type": "narrative",
          "displayName": None,
          "timePeriodMethod ": self.timeRangeLabel,
         ## Components
          "methodList": methodList,
          "narrativeDef": [
              # ("Extended",24), ("Extended",24),("Extended",24),
              # ("Extended",24), ("Extended",24)],
              ("Extended", 12), ("Extended", 12), ("Extended", 12),
              ("Extended", 12), ("Extended", 12), ("Extended", 12),
              ("Extended", 12), ("Extended", 12), ("Extended", 12),
              ("Extended", 12)],

          }

    def Extended(self):
         return {
             "type": "component",
             "methodList": [self.orderPhrases, self.assemblePhrases, self.wordWrap],
             "analysisList": [
                        ("MinT", self.stdDevMinMax),
                        ("MaxT", self.stdDevMinMax),
                        ("MinRH", self.avg, [0]),
                        ("T", self.hourlyTemp),
                        ("T", self.minMax),
                        ("PoP", self.stdDevMax, [6]),
                        ("PoP", self.binnedPercent, [6]),
                        ("Sky", self.median, [6]),
                        ("Wind", self.vectorMedianRange, [6]),
                       # ("Wind", self.vectorModeratedMinMax, [6]),
                       # ("WindGust", self.moderatedMinMax, [6]),
                       # ("Wind20ft", self.vectorMedian),
                       # ("Wind20ft", self.vectorMinMax),
                        ("Wx", self.rankedWx, [6]),
                      #  ("Wx", self.rankedWx, [0]),
                       ],

             "phraseList": [
                    self.wind_summary,
                    self.sky_phrase,
                    self.skyPopWx_phrase,
                    self.reportTrends,
                    self.weather_phrase,
                    self.severeWeather_phrase,
                    self.heavyPrecip_phrase,
                    (self.lows_phrase, self._tempLocalEffects_list()),
                    (self.highs_phrase, self._tempLocalEffects_list()),
                    self.highs_phrase,
                    self.rh_phrase,
                    self.wind_withGusts_phrase,
                    self.popMax_phrase,
                    ],

            "intersectAreas": [
                #Areas listed by weather element that will be
                #intersected with the current area then
                #sampled and analyzed.
                #E.g. used in local effects methods.
                ("MaxT", ["e_inland_metro", "e_coast", "w_inland", "w_coast"]),
                ("MinT", ["e_inland_metro", "e_coast", "w_inland", "w_coast"]),
                ("MaxT", ["lakevcnty", "lake_inland"]),
                ("MinT", ["lakevcnty", "lake_inland"]),
               # ("MaxT", ["WDADE_coast", "WDADE_inland"]),
               # ("MinT", ["WDADE_coast", "WDADE_inland"]),
                ("Wind", ["e_inland_metro", "e_coast", "w_inland", "w_coast", "lakevcnty", "lake_inland"]),

                #("WindGust", ["e_coast", "metro", "e_inland", "lakevcnty", "lake_inland", "WDADE_coast", "WDADE_inland", "inland_metro", "metro_coast"]),
                ],
            }


    def _tempLocalEffects_list(self):#, tree, node):
        #inland_metro = ["e_inland", "metro"]
        #metro_coast = ["metro", "e_coast"]
        #if self.currentAreaContains(tree, inland_metro):
        #    leArea1 = self.LocalEffectArea("e_inland", "inland")
        #    leArea2 = self.LocalEffectArea("metro", "over the metro areas")
        #elif self.currentAreaContains(tree, metro_coast):
        #    leArea2 = self.LocalEffectArea("metro", "over the metro areas")
        #    leArea3 = self.LocalEffectArea("e_coast", "near the coast")
        ##return [self.LocalEffect([leArea1, leArea2], 2.5, " to "),
               # self.LocalEffect([leArea2, leArea3], 2.5, " to "),
        ##       ]

        leArea1 = self.LocalEffectArea("e_inland_metro", "over the inland areas")
        leArea2 = self.LocalEffectArea("e_coast", "near the coast")
        #leArea3 = self.LocalEffectArea("metro", "over the metro areas")
       # leArea4 = self.LocalEffectArea("metro_coast", "over the metro and coastal areas")
       # leArea5 = self.LocalEffectArea("inland", "inland")
       # leArea6 = self.LocalEffectArea("coast", "near the coast")

        ##leArea1 = self.LocalEffectArea("e_inland", "inland")

        #leArea2 = self.LocalEffectArea("inland_metro", "over the inland and metro areas")

        ##leArea2 = self.LocalEffectArea("metro", "over the metro areas")
        #leArea4 = self.LocalEffectArea("metro_coast", "over the metro and coastal areas")

        ##leArea3 = self.LocalEffectArea("e_coast", "near the coast")

        leArea3 = self.LocalEffectArea("w_inland", "inland")
        leArea4 = self.LocalEffectArea("w_coast", "near the coast")

        leArea5 = self.LocalEffectArea("lake_inland", "inland")
        leArea6 = self.LocalEffectArea("lakevcnty", "near the lake")

        #leArea8 = self.LocalEffectArea("WDADE_inland", "inland")
        #leArea9 = self.LocalEffectArea("WDADE_coast", "near florida bay")

        return [self.LocalEffect([leArea1, leArea2], 2.3, " to "),
                self.LocalEffect([leArea3, leArea4], 2.5, " to "),
                self.LocalEffect([leArea5, leArea6], 2.7, " to "),
                #self.LocalEffect([leArea7, leArea8], 2.7, " except "),
                #self.LocalEffect([leArea9, leArea10], 2.7, " except "),
               ## self.LocalEffect([leArea6, leArea7], 2.5, " except "),
                #self.LocalEffect([leArea8, leArea9], 2.7, " except "),
                ]



    def reportTrends_valueStr(self, tree, node, diff, temp):
        # Given a difference between current and 24-hour prior
        # MaxT or MinT grids, report a trend.

        var = self.colder_warmer_dict(tree, node)
        timeRange = node.getTimeRange()
        dayNight = self.getPeriod(timeRange, 1)
        if dayNight == self.DAYTIME():
            if diff >= 7:
                return self.nlValue(var["HighWarmer"], temp)
            elif diff <= -13:
                return self.nlValue(var["HighMuchColder"], temp)
            elif diff <= -7 and diff > -13:
                return self.nlValue(var["HighColder"], temp)
            else:
                return ""

        else:
            if diff >= 7:
                return self.nlValue(var["LowWarmer"], temp)
            elif diff <= -13:
                return self.nlValue(var["LowMuchColder"], temp)
            elif diff <= -7 and diff > -13:
                return self.nlValue(var["LowColder"], temp)
            else:
                return ""

        return ""

    # colder_warmer_Dict
    # Dictionary of non-linear dictionaries each with
    # phrases to use instead of colder/warmer
    # based on the temperature

    def colder_warmer_dict(self, tree, node):
        # This dictionary of non-linear dictionaries controls what phrase is returned
        # for cold/much colder warmer/much warmer.  It is based off
        # of the maxT or MinT
        dict =  {}
        dict["LowColder"] = {
           (-80, 45): "colder",
           (45, 70): "cooler",
           #(70,150): "COOLER",
           (70, 150): "Cooler",
           "default": "",
           }
        dict["LowMuchColder"] = {
           (-80, 45): "much colder",
           (45, 70): "much cooler",
           #(70,150): "COOLER",
           (70, 150): "Cooler",
           "default": "",
           }
        dict["LowWarmer"] = {
           (-80, 35): "not as cold",
           (35, 50): "not as cool",
           (50, 150): "not as cool",
           "default": "",
           }
        dict["HighColder"]= {
           (-80, 45): "colder",
           (45, 75): "cooler",
           (75, 90): "not as warm",
           (90, 150): "not as hot",
           "default": "",
           }
        dict["HighMuchColder"]= {
           (-80, 45): "much colder",
           (45, 75): "much cooler",
           (75, 90): "not as warm",
           (90, 150): "not as hot",
           "default": "",
           }
        dict["HighWarmer"]= {
           (-80, 45): "not as cold",
           (45, 65): "not as cool",
           (65, 150): "warmer",
           "default": "",
           }
        return dict

    def skyPopWx_excludePoP_flag(self, tree, node):
        # If set to 1, PoP will not be included in the skyPopWx_phrase
        return 1

    def sky_valueList(self, tree, node):
        # Phrases for sky given values.  Tuples consist of:
        #  (threshold, dayTime phrase, nightTime phrase)
        # Used by skyRange_phrase
        return [
#OLD
           # (10, "sunny", "clear"), #0-10%
          #  (24, "mostly sunny", "mostly clear"),  #11-24%
          #  (60, "partly sunny", "partly cloudy"), #25-60%
          #  (75, "considerably cloudy", "considerably cloudy"), #61-75%
          #  (90, "mostly cloudy", "mostly cloudy"), #76-90%
         #   (100, "cloudy", "cloudy"), #91-100%
         #   ]

            # MLB's

            #(12, "sunny", "clear"),                     # 0-12%
            #(24, "mostly sunny", "mostly clear"),       #13-24%
            #(49, "partly sunny", "partly cloudy"),      #25-49%
            #(62, "partly cloudy", "partly cloudy"),
            #(74, "considerable cloudiness", "considerable cloudiness"),
            #(87, "mostly cloudy", "mostly cloudy"),
            #(100, "cloudy", "cloudy"),
            #]

            (12, "sunny", "clear"),                     # 0-12%
            (25, "mostly sunny", "mostly clear"),       #13-24%
            (49, "partly sunny", "partly cloudy"),      #25-49%
            (69, "partly cloudy", "partly cloudy"),     #50-69%
            #(74, "considerable cloudiness", "considerable cloudiness"),
            (89, "mostly cloudy", "mostly cloudy"),  #70-89
            (100, "cloudy", "cloudy"),
            ]

    def _postProcessProduct(self, fcst, argDict):
        #Include any local string replacements here (CP 08/05/03)
        #fcst = string.upper(fcst)
        fcst = re.sub(r'THUNDERSTORMS AND RAIN SHOWERS', r'SHOWERS AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'THUNDERSTORMS AND SHOWERS', r'SHOWERS AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'THUNDERSTORMS AND RAIN', r'RAIN AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'RAIN SHOWERS AND THUNDERSTORMS', r'SHOWERS AND THUNDERSTORMS', fcst)
        fcst = re.sub(r'RAIN SHOWERS', r'SHOWERS', fcst)
        fcst = re.sub(r'RAIN\nSHOWERS', r'SHOWERS', fcst)

        #fcst = string.upper(fcst)

        return fcst


    def _pop_or_cwr(self, statDict, timeRange, argList):
        # Return the max PoP or CWR.  Make sure that weather is not "NONE"
        weather = self.wxVal(statDict, timeRange, ["Wx"])
        if weather == "NONE":
            return "0"
        else:
            element = argList[0]
            val = self.getStats(statDict, element)
            if val is None:
                return " "
            val = self.round(val, "Nearest", 10)
            return self.getScalarVal(val)


    def vector_mag(self, tree, node, minMag, maxMag, units,
                   elementName="Wind"):
        "Create a phrase for a Range of magnitudes"

        # Check for "null" value (below threshold)
        threshold = self.nlValue(self.null_nlValue(
            tree, node, elementName, elementName), maxMag)
        if maxMag < threshold:
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
            around = self.phrase_descriptor(tree, node, "around ", elementName)
            words =  around + repr(int(maxMag)) + " " + units
        else:
            if int(minMag) < threshold:
                upTo = self.phrase_descriptor(tree, node, " ", elementName) # eliminated "up to"
                if upTo:
                    upTo += " "
                words = upTo + repr(int(maxMag)) + " " + units
            else:
                valueConnector = self.value_connector(tree, node, elementName, elementName)
                words =  repr(int(minMag)) + valueConnector + repr(int(maxMag)) + " " + units

        # This is an additional hook for customizing the magnitude wording
        words = self.vector_mag_hook(tree, node, minMag, maxMag, units, elementName, words)
        return words

#if windMag is not None:
#            if windMag < self._tableLightWindThreshold:
#                windString = self._tableLightWindPhrase
#            elif self._tableWindRanges:
#                windString = self._getVectorRange(((windMag-2, windMag+2), windDir))
#            else:
#                windString = self.getVectorVal((windMag, windDir))

    def _transWind(self, statDict, timeRange, argList):
        # Return the transport wind as a string
        day = self.getPeriod(timeRange, 1)
        if day:
            minMax = "Max"
        else:
            minMax = "Min"
        if self._mixingParmsDayAndNight:
            day = 1
        if day == 1:
            transWind = self._transWindValue(statDict, timeRange, argList)
            if transWind is None:
                return "N/A"
            mag, dir = transWind
            if transWind is not None:
                if mag < self._tableLightTransWindThreshold:
                    transWindString = self._tableLightTransWindPhrase
                else:
                    transWindString = self.getVectorVal((mag, dir))
            return transWindString# self.getVectorVal((mag,dir))
        else:
            return ""

    def vector_summary(self, tree, node, elementName):
        "Determine summary of given element"
        # Uses vectorAvg, vectorMedian, vectorMinMax
        stats = tree.stats.get(
            elementName, node.getTimeRange(), node.getAreaLabel(),
            mergeMethod="Max")
        if stats is None:
            return ""
        max, dir = stats
        #desc = 0
        #desc = self.phrase_descriptor(tree,node,desc,desc)

        #if desc:
#    print("phrase descriptor", desc)
        #    return self.vector_summary_NovalueStr(max, elementName)

        #elif not desc:
        return self.vector_summary_valueStr(max, elementName)

    def vector_summary_valueStr(self, value, elementName):
        # Thresholds and corresponding phrases
        # Defaults are for Winds converted to  mph
        words = ""
        if value <= 17:
            words = ""
        elif value < 21:
            words = "breezy"
        elif value < 31:
            words = "windy"
        elif value < 41:
            words = "very windy"
        elif value < 74:
            words = "strong winds"
        else:
           # words = "hurricane force winds"
            words = ""
        return words

    def _checkPrecip(self, statDict, timeRange, argList):
        """This sets a flag to indicate precip or no precip
        in the time range. Checks Wx, PoP and QPF to allow
        different rows with precip related info to be consistent.
        Also provides the value for the Wx, QPF and PoP rows. This is
        so the same rounded value is used for all checks. So if you
        need to change rounding for PoP or QPF, it is all in one
        place. Finally, new Definition['popWxThreshold'] is required
        (Default value should be 1). PoP < popWxThreshold indicates
        no precip."""
        precipFlag = 1
        weather = self.wxVal(statDict, timeRange, ["Wx"])
        if weather == "NONE":
            precipFlag = 0
       # Weather could be non-precipitating so next check QPF
        qpfStats = self.getStats(statDict, "QPF")
        if qpfStats is None:
            precipFlag = 0
            qpf = None
        else:
            min, max, sum = qpfStats
            qpf = self.round(sum, "Nearest", .01)
            if qpf <= 0.0:
                precipFlag = 0
        # Next check pop:
        pop = self.getStats(statDict, "PoP")
        if pop is None:
            precipFlag = 0
        #elif pop < 15:
        #   precipFlag = 0
        else:
            pop = self.round(pop, "Nearest", 10)
            if pop < self._popWxThreshold:
                precipFlag = 0
        return precipFlag, weather, qpf, pop

    def _chancePrecip_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self._popVal, None, self._rowLabelWidth,
            self._fixedValueWidth, self._columnJustification)
        return fcst

    def _popVal(self, statDict, timeRange, argList):
        # Return the max PoP if weather in this period
        pop = self.getStats(statDict, "PoP")
        pop =self.round(pop, "Nearest", 10)
        if pop is None:
            return " "
        if pop >= 10:#pop < 20 and pop >= 10:
            return self.getScalarVal(pop)
        if pop < 10:
            return "0"
        precipFlag, wx, qpf, pop = \
                    self._checkPrecip(statDict, timeRange, argList)
        if precipFlag:
            return self.getScalarVal(pop)
        else:
            return "0"

    def temporalCoverage_hours(self, parmHisto, timeRange, componentName):
        self.debug_print("version of " +
                         "SampleAnalysis.temporalCoverage_hours")
        # This is the required hours of overlap of a grid with the TIMERANGE
        #    in order to include it in the analysis.
        #    In addition, if the temporalCoverage_hours is greater than or equal to the
        #    TIMERANGE duration and the grid covers the entire TIMERANGE,
        #    it will be included.
        # Temporal coverage hours default value
        #     (if not found in temporalCoverage_hours_dict)
        # Used by temporalCoverage_flag
        #
        # COMMENT: At WFO MFL we use 3 hrly wind grids. If you use 1 hrly wind grids
        # and this parameter is 2 or higher, tropical cyclone winds affecting the very
        # early or latter part of a forecast period might be neglected. 1 assures
        # maximum sensitivity.

        return 1


    def temporalCoverage_hours_dict(self, parmHisto, timeRange, componentName):
        self.debug_print("version of " +
                         "SampleAnalysis.temporalCoverage_hours_dict")
        # This is the temporalCoverage_hours specified per weather element.
        # Used by temporalCoverage_flag

        # Get Baseline thresholds
        dict = SampleAnalysis.SampleAnalysis.temporalCoverage_hours_dict(self,
                                            parmHisto, timeRange, componentName)

        # COMMENT: Add local site override entries here if any.
        # KMFL
        dict["PoP"] = 1
        dict["Wx"] = 1
        dict["WindChill"] = 2
        dict["LAL"] = 1

        #  Print debug message if flag is set
        self.debug_print("\tdict = %s" % (dict), 1)

        return dict

    # Returns a list of the Hazards allowed for this product in VTEC format.
    # These are sorted in priority order - most important first.
    def allowedHazards(self):
        allActions = ["NEW", "EXA", "EXB", "EXT", "CAN", "CON", "EXP"]
        tropicalActions = ["NEW", "EXA", "EXB", "EXT", "UPG", "CAN", "CON",
          "EXP"]
        return [
            ('HU.W', tropicalActions, 'Tropical'),     # HURRICANE WARNING
            ('TY.W', tropicalActions, 'Tropical'),     # TYPHOON WARNING
            ('TR.W', tropicalActions, 'Tropical1'),     # TROPICAL STORM WARNING
            ('HU.A', tropicalActions, 'Tropical'),     # HURRICANE WATCH
            ('TR.A', tropicalActions, 'Tropical1'),     # TROPICAL STORM WATCH
            ('HI.W', allActions, 'TropicalNPW'),  # INLAND HURRICANE WARNING
            ('TI.W', allActions, 'TropicalNPW1'),  # INLAND TROPICAL STORM WARNING
            ('HF.W', allActions, 'Marine'),       # HURRICANE FORCE WIND WARNING
            ('HI.A', allActions, 'TropicalNPW'),  # INLAND HURRICANE WATCH
            ('TI.A', allActions, 'TropicalNPW1'),  # INLAND TROPICAL STORM WATCH
           # ('WS.A', allActions, 'WinterWx'),     # WINTER STORM WATCH
           # ('WC.W', allActions, 'WindChill'),    # WIND CHILL WARNING
           # ('WC.Y', allActions, 'WindChill'),    # WIND CHILL ADVISORY
           # ('WC.A', allActions, 'WindChill'),    # WIND CHILL WATCH
           # ('DS.W', allActions, 'Dust'),         # DUST STORM WARNING
           # ('DU.Y', allActions, 'Dust'),         # BLOWING DUST ADVISORY
           # ('EH.W', allActions, 'Heat'),         # EXCESSIVE HEAT WARNING
           # ('EH.A', allActions, 'Heat'),         # EXCESSIVE HEAT WATCH
           # ('HT.Y', allActions, 'Heat'),         # HEAT ADVISORY
            ('FG.Y', allActions, 'Fog'),          # DENSE FOG ADVISORY
           # ('HZ.W', allActions, 'FrostFreeze'),  # HARD FREEZE WARNING
           # ('FZ.W', allActions, 'FrostFreeze'),  # FREEZE WARNING
          #  ('FR.Y', allActions, 'FrostFreeze'),  # FROST ADVISORY
          #  ('HZ.A', allActions, 'FrostFreeze'),  # HARD FREEZE WATCH
          #  ('FZ.A', allActions, 'FrostFreeze'),  # FREEZE WATCH
          #  ('HW.W', allActions, 'Wind'),         # HIGH WIND WARNING
            ('WI.Y', allActions, 'Wind'),         # WIND ADVISORY
            ('HW.A', allActions, 'Wind'),         # HIGH WIND WATCH
            ('SM.Y', allActions, 'Smoke'),        # DENSE SMOKE ADVISORY
           # ('FF.A', allActions, 'Flood'),        # FLASH FLOOD WATCH
           # ('FA.A', allActions, 'Flood'),        # FLOOD WATCH
           # ('FA.W', allActions, 'Flood'),        # FLOOD WARNING
           # ('FA.Y', allActions, 'Flood'),        # FLOOD ADVISORY
          #  ('CF.W', allActions, 'CoastalFlood'), # COASTAL FLOOD WARNING
          #  ('LS.W', allActions, 'CoastalFlood'), # LAKESHORE FLOOD WARNING
          #  ('CF.Y', allActions, 'CoastalFlood'), # COASTAL FLOOD ADVISORY
          #  ('LS.Y', allActions, 'CoastalFlood'), # LAKESHORE FLOOD ADVISORY
          #  ('CF.A', allActions, 'CoastalFlood'), # COASTAL FLOOD WATCH
          #  ('LS.A', allActions, 'CoastalFlood'), # LAKESHORE FLOOD WATCH
          #  ('AS.Y', allActions, 'AirStag'),      # AIR STAGNATION ADVISORY
          #  ('TO.A', allActions, 'Convective'),   # TORNADO WATCH
          #  ('SV.A', allActions, 'Convective'),   # SEVERE THUNDERSTORM WATCH
            ('FW.W', allActions, 'FireWx'),  # RED FLAG WARNING
            ('FW.A', allActions, 'FireWx'),  # FIRE WEATHER WATCH
            ]

    def moderated_dict(self, parmHisto, timeRange, componentName):
        """
           Modifed to lower the high end filter threshold from 20 MPH to
           15 MPH for Tropical.
        """
        # COMMENT: This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values. The thresholds chosen below gave best results
        # during testing with 2004 and 2005 tropical cyclones. This dict
        # is used with the moderatedMinMax analysis method specified in the
        # TropicalPeriod definitions specified further down for use with
        # tropical cyclones with wind parameters.

        # Get Baseline thresholds
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto,
                                                    timeRange, componentName)

        #  Change thresholds for Wind, WindGust, WaveHeight and Swell
        #dict["PoP"] = (0, 10)
        dict["Wind"] = (0, 15)
        dict["WindGust"] = (0, 15)

        ##if self._includeTropical:
        ##    dict["Wind"] = (0, 15)
        ##    dict["WindGust"] = (0, 15)
        ##    dict["WaveHeight"] = (0, 15)
        ##    dict["Swell"] = (0, 15)
        ##else:
        ##    dict["Wind"] = (0, 15)
        ##    dict["WindGust"] = (0, 15)
        return dict
        ##return {
                #"T" : (10, 10),
        ##        "Wind": (0, 15),
                #"LAL": (10, 10),
                #"MinRH":  (10, 10),
                #"MaxRH":  (10, 10),
                #"MinT": (10, 10),
                #"MaxT": (10, 10),
                #"Haines": (10, 10),
                #"PoP" : (10, 10),
        ##        "WindGust": (0, 15),
        ##        }


    def stdDev_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating stdDev stats.
        # These tuples represent the (low, high) number of standard
        # deviations.  Any values falling outside this range will
        # not be included in the calculated statistic.
        return {
               # "LAL": (1.0, 1.0),
               # "MinRH":  (1.0, 1.0),
               # "MaxRH":  (1.0, 1.0),
                "MinT": (2.0, 2.0),
                "MaxT": (2.0, 2.0),
               # "ApparentT": (0, 2.0),
               # "Haines": (1.0, 1.0),
                "PoP": (1.0, 1.0),
                #"T" : (1.0, 1.0),
               # "Wind" : (1.0, 1.0),
                "Sky": (2.0, 2.0),
                }

    def similarWind(self, tree, comp1, comp2):
        # Returns true if the wind stats are similar
        # Also, return true (combine) if past the first 5 period since
        # wind is not reported in these periods

        # these numbers determine if components are close enough to combine
        magThreshold = 5.0
        dirThreshold = 40

        al1 = comp1.getAreaLabel()
        al2 = comp2.getAreaLabel()
        tr1 = comp1.getTimeRange()
        tr2 = comp2.getTimeRange()
        stats1 = tree.stats.get("Wind", tr1, al1, mergeMethod = "Max")
        stats2 = tree.stats.get("Wind", tr2, al2, mergeMethod = "Max")

        # If past the first 5 periods, return 1 (combine)
        #hours = self.hoursPastProductStart(tree, comp1)
        #if hours >= 5*12:
        #    return 1

        # check for none
        if stats1 is None or stats2 is None:
            return 0

        mag1 = stats1[0]
        mag2 = stats2[0]
        dir1 = stats1[1]
        dir2 = stats2[1]
        # calculate the differences, mag and dir
        magDiff = abs(mag1 - mag2)
        dirDiff = abs(dir1 - dir2)

        # account for the 360 to 0 problem
        if dirDiff > 180:
            dirDiff = abs(dirDiff - 360.0)

        if magDiff <= magThreshold and dirDiff <= dirThreshold:
            return 1

        return 0

    def nextDay24HourLabel_flag(self, tree, node):
        # Return 1 to have the TimeDescriptor module label 24 hour periods starting
        # after 1600 as the next day.
        # This is needed for the Fire Weather Extended product,
        # but not for other products when period combining.
        # NOTE: If you are doing period combining, you should
        # set this flag to zero and set the "splitDay24HourLabel_flag" to 1.
        return 0

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
        return 1

    def periodCombining_elementList(self, tree, node):
        # Weather Elements to determine whether to combine periods
        return ["Sky", "Wind", "Wx", "PoP", "MaxT", "MinT"]
        # Marine
        #return ["Wind", "Wx", "MaxT", "MinT", "PoP"]
        # Diurnal Sky Wx pattern
        #return ["DiurnalSkyWx"]

    def periodCombining_startHour(self, tree, node):
        # Hour after which periods may be combined
        return 48

    def similarPoP(self, tree, comp1, comp2):
        # returns true if PoP stats are similar
        stats1 = self.matchToWx(tree, comp1, "PoP")
        stats2 = self.matchToWx(tree, comp2, "PoP")

        if stats1 is None and stats2 is None:
            return 1

        # check for none
        if stats1 is None or stats2 is None:
            return 0

        if stats1 == stats2:
            return 1

        if stats1 < self.pop_lower_threshold(tree, comp1) and \
               stats2 < self.pop_lower_threshold(tree, comp2):
            return 1

        if stats1 > self.pop_upper_threshold(tree, comp1) and \
               stats2 > self.pop_upper_threshold(tree, comp2):
            return 1


       #  return 0

    def similarSkyLogic(self, tree, comp1, comp2, tr1, al1, tr2, al2):
        stats1 = tree.stats.get("Sky", tr1, al1, mergeMethod ="Average")
        stats2 = tree.stats.get("Sky", tr2, al2, mergeMethod ="Average")
        # check for none
#print("stats1", stats1)
#print("stats2", stats2)
        if stats1 is None or stats2 is None:
            return 0
        if stats1 is None or stats2 is None:
            return 0
        saveTR1 = comp1.timeRange
        saveTR2 = comp2.timeRange
        comp1.timeRange = tr1
        comp2.timeRange = tr2
        words1 = self.sky_value(tree, comp1, self.getValue(stats1), -1)
        words2 = self.sky_value(tree, comp2, self.getValue(stats2), -1)
        comp1.timeRange = saveTR1
        comp2.timeRange = saveTR2
#print("words1, words2", words1, words2)
        if words1 == words2:
            return 1
        #if words1.find("partly") > -1 and words2.find("partly")> -1:
        #    return 1
        if words1 == "partly cloudy" and words2 == "partly sunny":
            return 1
        if words1 == "partly sunny" and words2 == "partly cloudy":
            return 1
        if words1 == "mostly sunny" and words2 == "clear":
            return 1
        if words1 == "clear" and words2 == "mostly sunny":
            return 1
        if words1 == "mostly clear" and words2 == "clear":
            return 1
        if words1 == "clear" and words2 == "mostly clear":
            return 1
      #  return 0

    def similarSkyWords_list(self, tree, node):
        # The following pairs of sky words will be considered
        # "equal" when comparing for phrase combining
        # and redundancy
        #
        # For trends, (e.g. Sunny in the morning then partly cloudy in the afternoon.)
        # the following transitions are not allowed:
        #  Day time:
        #    Sunny <--> mostly sunny
        #    Mostly sunny <--> partly sunny
        #    Partly cloudy <--> mostly cloudy
        #  Night time:
        #    Clear <--> mostly clear
        #    Mostly clear <--> partly cloudy
        #    Mostly cloudy <--> cloudy
        #
        # In other words these transitions are allowed:
        #  Day time:
        #    sunny <--> partly sunny or above
        #    mostly sunny <--> mostly cloudy or above
        #    partly sunny <-->  sunny or cloudy
        #    mostly cloudy <--> mostly sunny
        #  Night time:
        #    clear can go to partly cloudy or above
        #    mostly clear <--> mostly cloudy or above
        #    partly cloudy <--> mostly cloudy or above
        #    mostly cloudy <--> partly cloudy or below

      ##  dayNight = self.getPeriod(node.getTimeRange(), 1)
      ##  if dayNight == self.DAYTIME():
           return [
            ("clear", "mostly clear"),
            ("mostly clear", "mostly sunny"),
            ("mostly sunny", "mostly clear"), #added 11/14/10
            ("clear", "sunny"),
            ("clear", "mostly sunny"), #added 11/8/10
            ("partly sunny", "mostly clear"), #added 11/8/10
            ("mostly sunny", "partly sunny"),
            ("partly sunny", "partly cloudy"),
            ("mostly sunny", "sunny"),
            ]
       ## else:
       ##     return [
       ##         ("clear", "mostly clear"),
       ##         ("mostly clear", "partly cloudy"),
       ##         ("mostly cloudy", "cloudy"),
       ##         ]

    def similarSkyWords_flag(self, tree, node, words1, words2):
        # Returns 1 if the pair of words is equal or similar
        # according to the "similarSkyWords_list"
        if words1 == words2:
            return 1
        # Check for similarity
        for value1, value2 in self.similarSkyWords_list(tree, node):
            if (words1 == value1 and words2 == value2) or \
               (words2 == value1 and words1 == value2):
                return 1
        else:
            return 0

    def _precipBegin_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self._begin, ["Wx__dominantWx_0", self._timeRangeList, statList],
            self._rowLabelWidth, self._fixedValueWidth,
            self._columnJustification)
        return fcst

    def _precipEnd_row(self, fcst, label, statList, priorStatDict):
        fcst += self.makeRow(
            label, self._colWidth, self._timeRangeList, statList,
            self._end, ["Wx__dominantWx_0", self._timeRangeList, statList],
            self._rowLabelWidth, self._fixedValueWidth,
            self._columnJustification)
        return fcst

    def _duration(self, statDict, timeRange, argList):
        precipFlag, wx, qpf, pop = \
                    self._checkPrecip(statDict, timeRange, argList)
        if wx == "NONE":
            return ""
        if not precipFlag:
            return ""
        statsByRange = self.getStats(statDict, "Wx__dominantWx_0")
        if statsByRange is None:
            return ""
        # Found in TableBuilder:
        return self.wxDuration(statsByRange, timeRange)

    def _begin(self, statDict, timeRange, argList):
        # Check if this period should have precip based on Wx, QPF, PoP
        precipFlag, wx, qpf, pop = \
                    self._checkPrecip(statDict, timeRange, argList)
#print("_begin:",timeRange,precipFlag, wx, qpf, pop)
        if not precipFlag:
            return ""

        durationRange = self._getTR(statDict, timeRange, argList)
        if durationRange is None:
            return ""
        durStart = durationRange.startTime()
        if durStart < timeRange.startTime():
            #return "CONTINUING"
            return "Continuing"
        value =  self.localHourLabel(durStart).strip()
        return value

    def _end(self, statDict, timeRange, argList):
        # Check if this period should have precip based on Wx, QPF, PoP
        precipFlag, wx, qpf, pop = \
                    self._checkPrecip(statDict, timeRange, argList)
#print("_end:",timeRange,precipFlag, wx, qpf, pop)
        if not precipFlag:
            return ""

        durationRange = self._getTR(statDict, timeRange, argList, ending=1)
        if durationRange is None:
            return ""
        durEnd = durationRange.endTime()
        if durEnd > timeRange.endTime():
            #return "CONTINUING"
            return "Continuing"
        value =  self.localHourLabel(durEnd).strip()
        return value

    def _getTR(self, statDict, timeRange, argList, ending=0):
        # Get a beginning or ending timeRange for weather occuring.
#print("_getTR:",timeRange,ending)

        # Parse the argList
        element = argList[0]
        trList = argList[1]
        statList = argList[2]

        # Get the length of the statList, so we know how many periods we have
        statLength = len(statList)

        # Get index for current time range
        currentIndex = self._getIndex(timeRange, trList)
#print("_getTR: currentIndex = ", currentIndex, "tr = ", timeRange, "Ending = ", ending)
        # Use the index to access the previous and next time range in the
        # statList.
        if currentIndex is None:
#print("_getTR: no currentIndex returning none")
            return None
        nextIndex = currentIndex + 1

        # Set prevIndex to one less than the current, unless this is the first
        # period...then just use the current index.
        if currentIndex > 0:
            prevIndex = currentIndex - 1
        else:
            prevIndex = currentIndex
        prevTR = trList[prevIndex]
        # If we're on the last period of the table, we need to access the stats
        # from the extended portion.
        if currentIndex < statLength - 1:
            nextStatDict = statList[nextIndex]
            nextTR = trList[nextIndex]
        else:
            nextStatDict = self._extStatDict
            nextTR = self._extTR

        if prevIndex != currentIndex:
            prevStatDict = statList[prevIndex]
            prevStats = self.getStats(prevStatDict, element)
        nextStats = self.getStats(nextStatDict, element)
        eStats = self.getStats(statDict, element)
#print("_getTR: element, estats=",element,eStats)
        if eStats is None:
#print("_getTR: no eStats returning none")
            return None

        # if looking for ending time, reverse so last time range is first
        if ending == 1:
            eStats.reverse()

        # "range" will be first time range found where there is "<NoWx>"
        range = None

        for values, tr in eStats:
#print("_getTR: values, tr=",values, tr)
            for subKey in values:
#print("_getTR: subKey=",subKey)
                if self.precip_related(subKey):
                    range = tr
                    break
            if range is not None:
                break

        if currentIndex > 0 and not ending:
            # If the precip startTime found in the previous for-loop equals the
            # startTime for the current timeRange, then we need to look at the
            # previous timeRange to see if precip is "CONTINUING".
            if range is not None and range.startTime() == timeRange.startTime():
                #PJ Make sure previous period has Wx/QPF/PoP
                precipFlag, wx, qpf, pop = \
                    self._checkPrecip(prevStatDict, prevTR, argList)
#print("getTR beg _checkPrecip:",prevTR,precipFlag, wx, qpf, pop)
                if precipFlag:
                    prevRange = range
                    prevLength = len(prevStats)
                    lastIndex = prevLength - 1
                    val, tr = prevStats[lastIndex]
                    for subKey in val:
                        if self.precip_related(subKey):
                            prevRange = tr
                            break
                    range = prevRange

        if ending == 1:
            # If range has not been set OR the precip endTime equals the
            # endTime for the current timeRange, then we need to look at the
            # next timeRange to determine if precip is "CONTINUING".
            if range is not None and range.endTime() == timeRange.endTime():
                #PJ Make sure next period has Wx/QPF/PoP
                precipFlag, wx, qpf, pop = \
                    self._checkPrecip(nextStatDict, nextTR, argList)
#print("getTR end _checkPrecip:",nextTR,precipFlag, wx, qpf, pop)
                if precipFlag:
                    nextRange = None
                    val, tr = nextStats[0]
                    if not val:
                        return range
                    for subKey in val:
                        if self.precip_related(subKey):
                            nextRange = tr
                            break

                    if nextRange is None:
                        return range

                    range = nextRange
#print("_getTR: returning:",range)
        return range

    def _getIndex(self, timeRange, trList):
        index = 0
        for tr, label in trList:
            if timeRange == tr:
                return index
            index += 1
        return
