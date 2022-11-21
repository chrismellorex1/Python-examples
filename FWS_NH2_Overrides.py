import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis

import TimeRange

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class FWS_NH2_Overrides:
    def __init__(self):
        pass

    def _determineTimeRanges(self, argDict):
        # Set up the Narrative Definition and initial Time Range
        self._issuanceInfo = self.getIssuanceInfo(
            self._productIssuance, self._issuance_list(argDict), argDict["creationTime"])

        if self._tableStartTimeMode == "current":
            # Add a "custom" component to sample data from current time
            # to product start time
            ct = self._issuanceInfo.issueTime()
            currentTime = AbsTime.absTimeYMD(ct.year, ct.month, ct.day,
                                          ct.hour)
            productStart = self._issuanceInfo.timeRange().startTime()
            tr = TimeRange.TimeRange(currentTime, productStart)
            if tr.duration() > 0:
                self._issuanceInfo.narrativeDef().append(\
                    ("Custom", ("PreFirePeriod1", tr)))

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
        # Determine the extended range
        if self._individualExtended == 1:
            self._extendedStart = self._timeRange.endTime() - 24*5*3600
        else:
            self._extendedStart = self._timeRange.endTime()
        self._extendedRange = TimeRange.TimeRange(
            self._extendedStart, self._extendedStart + 3600)

        # Calculate current times
        self._ddhhmmTime = self.getCurrentTime(
            argDict, "%d%H%M", shiftToLocal=0, stripLeading=0)
        self._timeLabel = self.getCurrentTime(argDict, "%k%M %Z %a %b %e %Y",
            shiftToLocal=0, upperCase=0, stripLeading=1)
        return None

    def getCurrentTime(self, argDict=None, format="%H%M %Z %a %b %d %Y",
                        shiftToLocal=1, upperCase=0, stripLeading=1):
        # Return a text string of the current time in the given format
        if argDict is not None and "creationTime" in argDict:
            ctime = argDict['creationTime']
        else:
            ctime = time.time()
        if shiftToLocal == 1:
            curTime = time.localtime(ctime)
        else:
            curTime = time.gmtime(ctime)
#            localTime = time.localtime(ctime)
#            zoneName = time.strftime("%Z",localTime)
        timeStr = time.strftime(format, curTime)
        if shiftToLocal == 0:
            timeStr = timeStr.replace("PST", "UTC")
            timeStr = timeStr.replace("PDT", "UTC")
        if stripLeading==1 and (timeStr[0] == "0" or timeStr[0] == " "):
            timeStr = timeStr[1:]
        if argDict is None:
            language = "english"
        else:
            language = argDict["language"]
        timeStr = self.translateExpr(timeStr, language)
        if upperCase == 1:
            timeStr = timeStr.upper()
        timeStr = timeStr.replace("  ", " ")
        return timeStr

    def element_outUnits_dict(self, tree, node):
        dict = TextRules.TextRules.element_outUnits_dict(self, tree, node)
        dict["Wind"] = "kts"
        dict["Wind20ft"] = "kts"
        dict["TransWind"] = "kts"
        dict["FreeWind"] = "kts"
        dict["WindGust"] = "kts"
        return dict

   # From FWF. Modified to append the fire name and agency name to the
    # product name. Modified to eliminate the discussion from method.
    # Modified to include Matt Davis' enhancement (unlisted agency)
    def _preProcessProduct(self, fcst, argDict):

        if self._requestingAgency == "Unlisted":
            newFireName = self._incidentName + "..." + self._otherAgencyName
        else:
            newFireName = self._incidentName + "..." + self._requestingAgency
        productLabel = self._productName + " FOR " + newFireName

        productLabel = self.checkTestMode(argDict, productLabel)

        issuedByString = self.getIssuedByString()

        # Product header
        fcst =  fcst + self._wmoID + " " + self._fullStationID + " " + \
               self._ddhhmmTime + "\n" + self._pil + "\n\n" + productLabel + \
               "\nNWS " + self._wfoCityState + \
               "\n" + issuedByString + self._timeLabel + "\n\n"

        # Add time disclaimer
        self._fireTR = None
        if self._withIgnitionTimes == "yes" or self._tableStartTimeMode == "ignitionTime":
            fcst = self._makeFcstTimeStatement(fcst, argDict)
        try:
            timeTup = time.strptime(self._timeLabel, '%I%M %p %Z %a %b %d %Y')
            issueTime = time.mktime(timeTup)
        except:
            issueTime = time.time()
        now = time.time()
        if ((issueTime - now) < -24*3600) or ((issueTime - now) > 9*24*3600):
            message = \
'''|* The start time for this product is %s.
This is either more than a day in the past or more than 9 days
in the future. *|''' % self._timeLabel
            fcst = '%s\n%s\n\n' % (fcst, message)
        return fcst

   # Import the discussion from a previously edited discussion file.
    def _makeDiscussion(self, fcst, argDict):

        discussionHeader = ""
        discussionHeader = ".DISCUSSION...\n Latitude = \n Longitude = \n"

        if self._insertDiscussionFromFile == 1:
            discussion = ""
            if os.path.isfile(self._discussionFile):
                input = open(self._discussionFile)
                text = input.readlines()
                for line in text:
                    discussion += line
                discussion = "\n".join(discussion.split("\n\n"))
                discussion = "\n".join(discussion.split("\n\n"))
                return fcst + discussionHeader + discussion + "\n"
            else:
                discussion = "|*...PUT DISCUSSION TEXT HERE...*|"
                return fcst + discussionHeader + discussion + "\n\n"
        elif self._insertDiscussionFromFile == 2:
            version = 0
            fwfPil = self._statePil + self._fwfPil
            searchString=""
            product = self.getPreviousProduct(fwfPil, searchString, version=version)
            product = product.split("\n")
            discussion = ""
            disFlag = 0
            foundDiscussion = 0
            for line in product:
                if "DISCUSSION..." in line:
                    disFlag = 1
                    foundDiscussion = 1
                try:
                    if line[2] == "Z" and line[-1] == "-" and \
                       (line[6] == "-" or line[6] == ">"):
                        disFlag = 0
                except IndexError:
#print("Discussion Index Error",line)
                    a = 0
                if line[:2] == "$$":
                    disFlag = 0
                if disFlag:
                    discussion += line + "\n"
            if foundDiscussion:
                return fcst + discussion + "\n\n"
            else:
                discussion = "|*...PUT DISCUSSION TEXT HERE...*|"
                return fcst + discussionHeader + discussion + "\n\n"
        else:
            return fcst + discussionHeader + "\n\n\n"

#     def getFirePeriod_analysisList(self):
#         # Note: Some weather elements are commented out because they generate red-banners
#         #       for some offices. If you need any of the commented elements, then move
#         #       this method into your Spot_???_Overrides file and uncoment the elements
#         #       you need.
#         if self._forecastType in ["Tabular/Narrative", "Tabular Only"] or \
#                self._withIgnitionTimes == "yes":
#             analysisList = [
#                 #("Sky", self.median, [1]),
#                 #("Wx", self.rankedWx, [1]),
# #                ("PoP", self.stdDevMaxAvg, [1]),
# #                ("PoP", self.binnedPercent, [1]),
# #                ("LAL", self.maximum, [1]),
# #                ("LAL", self.binnedPercent, [1]),
#                 ##("PotRain", self.stdDevMaxAvg, [1]),
#                 ##("PotRain", self.binnedPercent, [1]),
#                 ##("PotThunder", self.stdDevMaxAvg, [1]),
#                 ##("PotThunder", self.binnedPercent, [1]),
#                 #("MaxT", self.moderatedMinMax),
#                 #("MinT", self.moderatedMinMax),
#                 #("MaxRH", self.moderatedMinMax),
#                 #("MinRH", self.moderatedMinMax),
#                 #("RH", self.avg, [1]),
#                 #("RH", self.moderatedMinMax),
#                 #("MaxT", self.avg),   # for trends
#                 #("MinT", self.avg),   # for trends
#                 #("MaxRH", self.avg),  # for trends
#                 #("MinRH", self.avg),  # for trends
#                 #("RH", self.avg),     # for trends
#                 #("T", self.avg, [1]),
#                 #("T", self.hourlyTemp),
#                 #("T", self.minMax),
#                 #("Td", self.avg, [1]),
#                 #("Td", self.hourlyTemp),
#                 #("Td", self.minMax),
#                 ("Wind", self.vectorMinMax, [1]),
#                 ("WindGust", self.minMax, [1]),
# #                ("Wind20ft", self.vectorMinMax, [1]),
#  #               ("Haines", self.maximum, [1]),
#  #               ("HainesMid", self.maximum, [1]),
# #                ("TransWind", self.vectorAvg, [1]),
# #                ("FreeWind", self.vectorAvg, [1]),
#                 ##("Wnd1000Ft", self.vectorAvg, [1]),
#                 ##("Wnd2000Ft", self.vectorAvg, [1]),
#                 ##("Wnd3000Ft", self.vectorAvg, [1]),
#                 ##("Wnd4000Ft", self.vectorAvg, [1]),
#                 ##("Wnd5000Ft", self.vectorAvg, [1]),
# #                ("MixHgt", self.moderatedMin, [1]),
# #                ("VentRate", self.minMax, [1]),
# #                ("DSI", self.maximum,[1]),
#                 ##("LDSI", self.maximum,[1]),
#                 ##("LVORI", self.maximum,[1]),
#                 ##("ADI", self.maximum,[1]),
#                 ##("GFDI", self.maximum,[1]),
# #                ("CWR", self.maximum, [1]),
# #                ("Stability", self.maximum, [1]),
# #                ("MarineLayer", self.maximum, [1]),
#                 ("Swell", self.vectorMinMax, [1]),
#                 ("Period", self.maximum, [1]),
#                 ("WindWaveHgt", self.maximum, [1]),
#                 ("WaveHeight", self.maximum, [1]),
#                 ##("HiOneTenth", self.maximum, [1]),
#                 ##("IceC", self.maximum, [1]),
#                 ("SST", self.maximum, [1]),
#                 ##("FrzngSpry",self.dominantDiscreteValue, [1]),
# #                ("QPF", self.accumSum, [6]),
# #                ("SnowAmt", self.accumSum, [6]),
# #                ("FzLevel", self.median, [1]),
# #                ("SnowLevel", self.median, [1]),
#                 ("Hazards", self.dominantDiscreteValue, [1]),
#                 #("Vsby", self.minimum, [1]),
#                 #("PredHgt", self.minimum, [1]),
# #                ("Visibility", self.minimum, [1]),
# #                ("CloudBasePrimary", self.minimum, [1]),
#   #              ("Pres", self.minimum, [1]),
# #                ("HeatIndex", self.maximum, [1]),
# #                ("WindChill", self.minimum, [1]),
# #                ("ApparentT", self.minMax, [1]),
#                 ]
#         else:
#             analysisList = [
#                 #("Sky", self.median, [6]),
# #                ("PoP", self.stdDevMaxAvg, [6]),
# #                ("PoP", self.binnedPercent, [6]),
#                 ##("PotRain", self.stdDevMaxAvg, [6]),
#                 ##("PotRain", self.binnedPercent, [6]),
#                 ##("PotThunder", self.stdDevMaxAvg, [6]),
#                 ##("PotThunder", self.binnedPercent, [6]),
#                 #("Wx", self.rankedWx, [6]),
# #                ("LAL", self.maximum, [12]),
# #                ("LAL", self.binnedPercent, [0]),
#                 #("MaxT", self.moderatedMinMax),
#                 #("MinT", self.moderatedMinMax),
# #                ("MaxRH", self.moderatedMinMax),
# #                ("MinRH", self.moderatedMinMax),
# #                ("RH", self.avg, [1]),
# #                ("RH", self.moderatedMinMax),
#                 #("MaxT", self.avg),   # for trends
#                 #("MinT", self.avg),   # for trends
#                 #("MaxRH", self.avg),  # for trends
#                 #("MinRH", self.avg),  # for trends
#                 #("RH", self.avg),     # for trends
#                 #("T", self.avg, [1]),
#                 #("T", self.hourlyTemp),
#                 #("T", self.minMax),
#                 #("Td", self.avg, [1]),
#                 #("Td", self.hourlyTemp),
#                 #("Td", self.minMax),
#                 ("Wind", self.vectorMinMax, [6]),
#                 ("WindGust", self.maximum, [6]),
# #                ("Wind20ft", self.vectorMinMax, [6]),
# #                ("Haines", self.maximum),
# #                ("HainesMid", self.maximum),
# #                ("TransWind", self.vectorAvg, [12]),
# #                ("FreeWind", self.vectorAvg, [12]),
#                 ##("Wnd1000Ft", self.vectorAvg, [12]),
#                 ##("Wnd2000Ft", self.vectorAvg, [12]),
#                 ##("Wnd3000Ft", self.vectorAvg, [12]),
#                 ##("Wnd4000Ft", self.vectorAvg, [12]),
#                 ##("Wnd5000Ft", self.vectorAvg, [12]),
# #                ("MixHgt", self.moderatedMin, [1]),
# #                ("VentRate", self.minMax),
#  #               ("CWR", self.maximum),
#  #               ("DSI", self.maximum,[12]),
#                 ##("LDSI", self.maximum,[12]),
#                 ##("LVORI", self.maximum,[12]),
#                 ##("ADI", self.maximum,[12]),
#                 ##("GFDI", self.maximum,[12]),
# #                ("Stability", self.maximum),
# #                ("MarineLayer", self.maximum),
#                 ("Swell", self.vectorMinMax, [6]),
#                 ("Period", self.maximum, [6]),
#                 ("WindWaveHgt", self.maximum, [6]),
#                 ("WaveHeight", self.maximum, [6]),
#                 ##("HiOneTenth", self.maximum, [6]),
#                 ##("IceC", self.maximum, [6]),
#                 ("SST", self.maximum, [6]),
#                 ##("FrzngSpry",self.dominantDiscreteValue, [6]),
#  #               ("QPF", self.accumMinMax, [6]),
#  #               ("SnowAmt", self.accumMinMax, [6]),
# #                ("FzLevel", self.median, [6]),
# #                ("SnowLevel", self.median, [6]),
#                 ("Hazards", self.dominantDiscreteValue),
#                 #("Vsby", self.minimum, [6]),
#                 #("PredHgt", self.minimum, [6]),
#  #               ("Visibility", self.minimum, [6]),
#  #               ("CloudBasePrimary", self.minimum, [6]),
#  #               ("Pres", self.minimum, [6]),
# #                ("HeatIndex", self.maximum, [6]),
# #                ("WindChill", self.minimum, [6]),
# #                ("ApparentT", self.minMax, [6]),
#                 ]
#         return analysisList

    def _weInfoList(self):
        self.debug_print("Debug: _weInfoList in FWS.py")
        # This is the list of possible weather parameters listed under the
        # ...WEATHER PARAMETERS REQUESTED... section in your STQ Product.
        # These are listed in the order they will appear in the product.
        #
        # Weather Elements: If you have a weather element to add,
        # then send an email to Virgil.Middendorf@noaa.gov with your addition.
        # I will baseline it.
        #
        # Phrases: You can override this method and edit the phrase method if you
        # don't like the one used in baseline.

        # For each element, we list:
        #     --an identifier
        #     --flag to indicate if this is a default element
        #     --the FWF phrase (or list of phrases) to include in the product
        #     --a list of search strings that must appear in
        #       the STQ product to specify the element.
        #       Each search string in the list may be a tuple in which case any of
        #       the entries in the tuple will satsify the search.

        if self._useRH:
            dayRH = "RH"
            nightRH = "RH"
        else:
            dayRH = "MinRH"
            nightRH = "MaxRH"
        if self._wind20ftHeader:
            wind = [self.fireWind_label_phrase, self.fireWind_compoundPhrase]
        else:
            wind = [self.fireWind_compoundPhrase]
        return [

            # Weather Related Phrases
            ("SKY/WEATHER", 1, self.skyWeather_byTimeRange_compoundPhrase,
             [("SKY", "CLOUDS"), "WEATHER"]),
            ("CWR", 0, self.cwr_phrase,
             [("CWR", "WETTING RAIN")]),
            ("POP", 0, self.pop_phrase,
             [("CHANCE OF PRECIPITATION", "CHANCE OF PCPN", "POP")]),
            ("CHANCE OF RAIN", 0, self.chanceOfRain_phrase,
             ["CHANCE OF RAIN"]),
            ("CHANCE OF THUNDER", 0, self.chanceOfThunder_phrase,
             ["CHANCE OF THUNDER"]),
            ("CHANCE OF LIGHTNING", 0, self.chanceOfLightning_phrase,
             ["CHANCE OF LIGHTNING"]),
            ("LIGHTNING ACTIVITY LEVEL", 0, self.lal_phrase,
             [("LAL", "LIGHTNING")]),
            ("BEGIN/END OF PCPN", 0, self.pcpnTiming_phrase,
             ["BEGIN", "END", "PRECIPITATION"]),

            ("TEMPERATURE", 1, (self.dayOrNight_phrase, ["MaxT", "MinT", 1, 1]),
             ["TEMPERATURE"]),
            ("HUMIDITY", 0, (self.dayOrNight_phrase, [dayRH, nightRH, 1, 1]),
             [("RH", "HUMIDITY")]),
            ("DEWPOINT", 0, self.td_phrase,
             ["DEWPOINT"]),
            ("HEAT INDEX", 0, self.heatIndex_phrase,
             ["HEAT", "INDEX"]),
            ("WIND CHILL", 0, self.windChill_phrase,
             ["WIND", "CHILL"]),
            ("APPARENT TEMPERATURE", 0, self.apparentTemperature_phrase,
             ["APPARENT TEMPERATURE"]),
            ("EYE LEVEL WINDS", 0, self.fireEyeWind_compoundPhrase,
             ["EYE", "WIND"]),
            ("SURFACE WINDS", 1, self.sfcWind_compoundPhrase,
             ["SURFACE", "WIND"]),
            ("SURFACE WINDS KTS", 0, self.sfcKtsWind_compoundPhrase,
             ["SURFACE", "WIND", "(KTS)"]),
            ("WIND SHIFT", 0, self.fireWindShift_label_phrase,
             ["WIND", "SHIFT"]),

            # Very Important that the next 5 wind entries remain together and
            # remain in same order.
            ("SLOPE/VALLEY WINDS", 0, wind,
             ["SLOPE/VALLEY WINDS"]),
            ("VALLEY/LOWER SLOPE WINDS", 0, wind,
             ["VALLEY/LOWER SLOPE WINDS"]),
            ("20 FOOT WINDS", 0, wind,
             ["WIND (20 FT)"]),
            ("RIDGE/UPPER SLOPE WINDS", 0, self.upperSlopeWind_phrase,
             ["RIDGE/UPPER SLOPE WINDS"]),
            ("RIDGE TOP WIND", 0, self.freeWind_phrase,
             ["RIDGE TOP WINDS"]),

            ("SURROUNDING RIDGE", 0, self.surroundingRidgeWind_phrase,
             ["SURROUNDING", "RIDGE", "WIND"]),
            ("SMOKE DISPERSION", 0, [self.mixingHgt_phrase, self.transportWind_phrase],
             ["SMOKE", "DISPERSION"]),
            ("MIXING HEIGHT", 0, self.mixingHgt_phrase,
             ["MIXING HEIGHT"]),
            ("MIXING HEIGHT MSL", 0, self.mixingHgtMsl_phrase,
             ["MIXING HEIGHT (MSL)"]),
            ("MIXING HEIGHT METRIC", 0, self.mixingHgtMetric_phrase,
             ["MIXING HEIGHT (KM OR M)"]),
            ("TRANSPORT WINDS", 0, self.transportWind_phrase,
             ["TRANSPORT WINDS"]),
            ("TRANSPORT WINDS METRIC", 0, self.transportWindMetric_phrase,
             ["TRANSPORT WINDS (M/S)"]),
            ("MIXING WINDS", 0, self.mixingWind_phrase,
             ["MIXING WINDS"]),
            ("MIXING WINDS METRIC", 0, self.mixingWindMetric_phrase,
             ["MIXING WINDS (M/S)"]),
            ("100 FT WIND", 0, self.wind100ft_phrase,
             ["100 FT WINDS"]),
            ("1000 FT WIND", 0, self.wind1000ft_phrase,
             ["1000 FT WIND"]),
            ("2000 FT WIND", 0, self.wind2000ft_phrase,
             ["2000 FT WIND"]),
            ("3000 FT WIND", 0, self.wind3000ft_phrase,
             ["3000 FT WIND"]),
            ("4000 FT WIND", 0, self.wind4000ft_phrase,
             ["4000 FT WIND"]),
            ("5000 FT WIND", 0, self.wind5000ft_phrase,
             ["5000 FT WIND"]),
            ("SMOKE DISPERSAL", 0, self.smokeDispersal_phrase,
             ["SMOKE", "DISPERSAL"]),
            ("CLEARING INDEX", 0, self.smokeDispersal_phrase,
             ["CLEARING", "INDEX"]),
            ("VENTILATION RATE", 0, self.smokeDispersal_phrase,
             ["VENTILATION", "RATE"]),
            ("LDSI", 0, self.ldsi_phrase,
             ["LDSI"]),
            ("LVORI", 0, self.lvori_phrase,
             ["LVORI"]),
            ("ADI", 0, self.adi_phrase,
             ["ADI"]),
            ("GFDI", 0, self.gfdi_phrase,
             ["GFDI (GRASS FIRE DANGER INDEX)"]),
            ("DISPERSION INDEX", 0, self.dsi_phrase,
             ["DISPERSION", "INDEX"]),
            ("STABILITY CLASS", 0, self.stabilityClass_phrase,
             ["STABILITY"]),
            ("MARINE LAYER", 0, self.marineLayer_phrase,
             ["MARINE", "LAYER"]),
            ("HAINES INDEX", 0, self.haines_phrase,
             ["HAINES", "INDEX"]),
            ("MID LEVEL HAINES INDEX", 0, self.hainesMid_phrase,
             ["HAINES INDEX (MID-LEVEL)"]),
            ("SWELL HEIGHT", 1, self.swell_phrase,
             ["SWELL", "HEIGHT"]),
            ("WAVE HEIGHT", 1, self.waveHeight_phrase,
             ["WAVE", "HEIGHT"]),
            ("HIONETENTH", 0, self.hiOneTenth_phrase,
             ["HIONETENTH"]),
            ("SWELL PERIOD", 1, self.period_phrase,
             ["SWELL", "PERIOD"]),
            ("WAVE PERIOD", 1, self.wavePeriod_phrase,
             ["WAVE", "PERIOD"]),
            ("WIND WAVE", 1, self.windWave_phrase,
             ["WIND", "WAVE"]),
            ("FREEZING SPRAY", 0, self.freezingSpray_phrase,
             ["FREEZING SPRAY"]),
            ("SEA ICE CONCENTRATION", 0, self.seaIceConcentration_phrase,
             ["SEA ICE CONCENTRATION"]),
            ("SEA SURFACE TEMPERATURE", 1, self.seaSurfaceTemperature_phrase,
             ["SEA SURFACE TEMPERATURE"]),

            ("RAINFALL AMOUNT", 0, self.qpf_phrase,
             ["RAINFALL", "AMOUNT"]),
            ("PRECIPITATION AMOUNT", 0, self.precipitationAmount_phrase,
             ["PRECIPITATION AMOUNT"]),
            ("SNOWFALL AMOUNT", 0, self.snow_phrase,
             ["SNOWFALL", "AMOUNT"]),
            ("FREEZING LEVEL", 0, self.freezingLevel_phrase,
             ["FREEZING", "LEVEL"]),
            ("SNOW LEVEL", 0, self.snowLevel_phrase,
             ["SNOW LEVEL"]),
            ("CEILING", 0, self.ceiling_phrase,
             ["CEILING"]),
            ("VISIBILITY", 0, self.visibility_phrase,
             ["VISIBILITY"]),
            ("PRESSURE", 0, self.pressure_phrase,
             ["PRESSURE (IN)"]),
            ("ICING", 0, self.icing_phrase,
             ["ICING"]),
            ("RIVER LEVEL", 0, self.riverLevel_phrase,
             ["RIVER LEVEL"]),
            ("RIVER TEMPERATURE", 0, self.riverTemperature_phrase,
             ["RIVER TEMPERATURE"]),
            ("WATER TEMPERATURE", 0, self.waterTemperature_phrase,
             ["WATER TEMPERATURE"]),
            ("HAZARDS", 0, self.ceiling_phrase,
             ["HAZARDS"]),
            ("SUNRISE/SUNSET", 0, self.sunriseSunset_label_phrase,
             ["SUNRISE", "SUNSET"]),
            ("MOONLIGHT", 0, self.moonlight_label_phrase,
             ["MOONLIGHT"]),
            ("INVERSION SETUP/BURNOFF", 0, self.inversionSetupBurnoff_label_phrase,
             ["INVERSION", "SETUP", "BURNOFF"]),
            ("TIDES", 0, self.tides_label_phrase,
             ["TIDES"]),
        ]


    def getFirePeriod_analysisList(self):
        # Note: Some weather elements are commented out because they generate red-banners
        #       for some offices. If you need any of the commented elements, then move
        #       this method into your Spot_???_Overrides file and uncoment the elements 
        #       you need.
        if self._forecastType in ["Tabular/Narrative", "Tabular Only"] or \
               self._withIgnitionTimes == "yes":
            analysisList = [
                ("Sky", self.median, [1]),            
                ("Wx", self.rankedWx, [1]),           
#                ("PoP", self.stdDevMaxAvg, [1]),
#                ("PoP", self.binnedPercent, [1]),
#                ("LAL", self.maximum, [1]),               
#                ("LAL", self.binnedPercent, [1]),
                ##("PotRain", self.stdDevMaxAvg, [1]),
                ##("PotRain", self.binnedPercent, [1]),
                ##("PotThunder", self.stdDevMaxAvg, [1]),
                ##("PotThunder", self.binnedPercent, [1]),
                ("MaxT", self.moderatedMinMax),
                ("MinT", self.moderatedMinMax),
                ("MaxRH", self.moderatedMinMax),
                ("MinRH", self.moderatedMinMax),
                ("RH", self.avg, [1]),
                ("RH", self.moderatedMinMax),
                ("MaxT", self.avg),   # for trends
                ("MinT", self.avg),   # for trends
                ("MaxRH", self.avg),  # for trends
                ("MinRH", self.avg),  # for trends
                ("RH", self.avg),     # for trends
                ("T", self.avg, [1]),
                ("T", self.hourlyTemp),
                ("T", self.minMax),
                ("Td", self.avg, [1]),
                ("Td", self.hourlyTemp),
                ("Td", self.minMax),
                ("Wind", self.vectorMinMax, [1]),
                ("WindGust", self.minMax, [1]),
#                ("Wind20ft", self.vectorMinMax, [1]),
 #               ("Haines", self.maximum, [1]),
 #               ("HainesMid", self.maximum, [1]),
#                ("TransWind", self.vectorAvg, [1]),
#                ("FreeWind", self.vectorAvg, [1]),
                ##("Wnd1000Ft", self.vectorAvg, [1]),
                ##("Wnd2000Ft", self.vectorAvg, [1]),
                ##("Wnd3000Ft", self.vectorAvg, [1]),
                ##("Wnd4000Ft", self.vectorAvg, [1]),
                ##("Wnd5000Ft", self.vectorAvg, [1]),
#                ("MixHgt", self.moderatedMin, [1]),          
#                ("VentRate", self.minMax, [1]),
#                ("DSI", self.maximum,[1]),
                ##("LDSI", self.maximum,[1]),
                ##("LVORI", self.maximum,[1]),
                ##("ADI", self.maximum,[1]),
                ##("GFDI", self.maximum,[1]),
#                ("CWR", self.maximum, [1]),
#                ("Stability", self.maximum, [1]),
#                ("MarineLayer", self.maximum, [1]),
                ("Swell", self.vectorMinMax, [1]),
                ("Period", self.maximum, [1]),
                ("WindWaveHgt", self.maximum, [1]),
                ("WaveHeight", self.maximum, [1]),
                ##("HiOneTenth", self.maximum, [1]),
                ##("IceC", self.maximum, [1]),
                ("SST", self.maximum, [1]),
                ##("FrzngSpry",self.dominantDiscreteValue, [1]),
#                ("QPF", self.accumSum, [6]),
#                ("SnowAmt", self.accumSum, [6]),
#                ("FzLevel", self.median, [1]),
#                ("SnowLevel", self.median, [1]),
                ("Hazards", self.dominantDiscreteValue, [1]),
                #("Vsby", self.minimum, [1]),
                #("PredHgt", self.minimum, [1]),
#                ("Visibility", self.minimum, [1]),
#                ("CloudBasePrimary", self.minimum, [1]),
  #              ("Pres", self.minimum, [1]),
#                ("HeatIndex", self.maximum, [1]),
#                ("WindChill", self.minimum, [1]),
#                ("ApparentT", self.minMax, [1]),
                ]
        else:
            analysisList = [
                ("Sky", self.median, [6]),            
#                ("PoP", self.stdDevMaxAvg, [6]),
#                ("PoP", self.binnedPercent, [6]),
                ##("PotRain", self.stdDevMaxAvg, [6]),
                ##("PotRain", self.binnedPercent, [6]),
                ##("PotThunder", self.stdDevMaxAvg, [6]),
                ##("PotThunder", self.binnedPercent, [6]),
                ("Wx", self.rankedWx, [6]),           
#                ("LAL", self.maximum, [12]),               
#                ("LAL", self.binnedPercent, [0]),
                ("MaxT", self.moderatedMinMax),
                ("MinT", self.moderatedMinMax),
#                ("MaxRH", self.moderatedMinMax),
#                ("MinRH", self.moderatedMinMax),
#                ("RH", self.avg, [1]),
#                ("RH", self.moderatedMinMax),
                ("MaxT", self.avg),   # for trends
                ("MinT", self.avg),   # for trends
                ("MaxRH", self.avg),  # for trends
                ("MinRH", self.avg),  # for trends
                ("RH", self.avg),     # for trends
                ("T", self.avg, [1]),
                ("T", self.hourlyTemp),
                ("T", self.minMax),
                ("Td", self.avg, [1]),
                ("Td", self.hourlyTemp),
                ("Td", self.minMax),
                ("Wind", self.vectorMinMax, [6]),
                ("WindGust", self.maximum, [6]),
#                ("Wind20ft", self.vectorMinMax, [6]),
#                ("Haines", self.maximum),
#                ("HainesMid", self.maximum),
#                ("TransWind", self.vectorAvg, [12]),
#                ("FreeWind", self.vectorAvg, [12]),
                ##("Wnd1000Ft", self.vectorAvg, [12]),
                ##("Wnd2000Ft", self.vectorAvg, [12]),
                ##("Wnd3000Ft", self.vectorAvg, [12]),
                ##("Wnd4000Ft", self.vectorAvg, [12]),
                ##("Wnd5000Ft", self.vectorAvg, [12]),
#                ("MixHgt", self.moderatedMin, [1]),          
#                ("VentRate", self.minMax),
 #               ("CWR", self.maximum),
 #               ("DSI", self.maximum,[12]),
                ##("LDSI", self.maximum,[12]),
                ##("LVORI", self.maximum,[12]),
                ##("ADI", self.maximum,[12]),
                ##("GFDI", self.maximum,[12]),
#                ("Stability", self.maximum),
#                ("MarineLayer", self.maximum),
                ("Swell", self.vectorMinMax, [6]),
                ("Period", self.maximum, [6]),
                ("WindWaveHgt", self.maximum, [6]),
                ("WaveHeight", self.maximum, [6]),
                ##("HiOneTenth", self.maximum, [6]),
                ##("IceC", self.maximum, [6]),
                ("SST", self.maximum, [6]),
                ##("FrzngSpry",self.dominantDiscreteValue, [6]),
 #               ("QPF", self.accumMinMax, [6]),
 #               ("SnowAmt", self.accumMinMax, [6]),
#                ("FzLevel", self.median, [6]),
#                ("SnowLevel", self.median, [6]),
                ("Hazards", self.dominantDiscreteValue),
                #("Vsby", self.minimum, [6]),
                #("PredHgt", self.minimum, [6]),
 #               ("Visibility", self.minimum, [6]),
 #               ("CloudBasePrimary", self.minimum, [6]),
 #               ("Pres", self.minimum, [6]),
#                ("HeatIndex", self.maximum, [6]),
#                ("WindChill", self.minimum, [6]),
#                ("ApparentT", self.minMax, [6]),
                ]
        return analysisList

    def _seaSurfaceTemperature_value(self, statDict, timeRange, argList):
        tree, node, colWidth = tuple(argList)        
        sst = self._getTableStats(tree, "SST", timeRange, node.getAreaLabel())
        if sst is None:
            return "M"
        if sst >= 0:
            isst = int(sst + 0.5)
        else:
            isst = int(sst - 0.5)
        return isst

    def seaSurfaceTemperature_phrase(self):
        return {
            "setUpMethod": self.seaSurfaceTemperature_setUp,
            "wordMethod": self.seaSurfaceTemperature_words,
            "phraseMethods": self.standard_phraseMethods(), 
            }
    
    def seaSurfaceTemperature_setUp(self, tree, node):
        elementInfoList = [self.ElementInfo("SST", "Min")]
        self.subPhraseSetUp(tree, node, elementInfoList, self.scalarConnector) 
        node.set("descriptor", "")
        node.set("indentLabel", "SEA SURFACE TEMP....")
        return self.DONE()
    
    def seaSurfaceTemperature_words(self, tree, node):
        statDict = node.getStatDict()
        sst = self.getValue(self.getStats(statDict, "SST"), "Min")
        if sst is None:
            return self.setWords(node.parent, "MISSING")
        isst = int(sst+0.5)
        words = str(isst)+ " Degrees Fahrenheit"
        return self.setWords(node, words)