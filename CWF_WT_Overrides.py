# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# CWF_WT_Overrides.TextUtility
#
#  This file is used for WFO specific overrides of the CWF_
#  formatter.
#
#
# Methods:
#   Overrides:
#
#   Additions:
#
# ---------------------------------------------------------------------

import string, time, re, os, types, copy, AFPS
import TextRules
import ModuleAccessor
import SampleAnalysis

# for UTC Overrides
import TimeDescriptor
#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class CWF_WT_Overrides:
    def __init__(self):
        pass

# End MAKE NO CHANGES HERE
#**********************************************************************


#*********************************************************************
# EKA Over-rides

    # Example of Overriding a dictionary from TextRules
    def phrase_descriptor_dict(self, tree, node):
        dict = TextRules.TextRules.phrase_descriptor_dict(self, tree, node)
        dict["seas"] = "seas"
        dict["WaveHeight"] = "seas"
        dict["waves"] = ""#"including..."
        return dict

    def element_inUnits_dict(self, tree, node):
        dict = TextRules.TextRules.element_inUnits_dict(self, tree, node)
        dict["Wave1"] = "ft"
        dict["Wave2"] = "ft"
        dict["Wave3"] = "ft"
        dict["Wave4"] = "ft"
        dict["Period1"] = "s"
        dict["Period2"] = "s"
        dict["Period3"] = "s"
        dict["Period4"] = "s"
        return dict

    def value_connector_dict(self, tree, node):
        dict = TextRules.TextRules.value_connector_dict(self, tree, node)
        dict["Wave1"] = " to "
        dict["Wave2"] = " to "
        dict["Wave3"] = " to "
        dict["Wave4"] = " to "
        dict["Period1"] = " to "
        dict["Period2"] = " to "
        dict["Period3"] = " to "
        dict["Period4"] = " to "
        return dict

    def element_outUnits_dict(self, tree, node):
        dict = TextRules.TextRules.element_outUnits_dict(self, tree, node)
        dict["Wave1"] = "ft"
        dict["Wave2"] = "ft"
        dict["Wave3"] = "ft"
        dict["Wave4"] = "ft"
        dict["Period1"] = "s"
        dict["Period2"] = "s"
        dict["Period3"] = "s"
        dict["Period4"] = "s"
        return dict

    def embedded_vector_descriptor_flag_dict(self, tree, node):
        dict = TextRules.TextRules.embedded_vector_descriptor_flag_dict(self, tree, node)
        dict["Wave1"] = 0
        dict["Wave2"] = 0
        dict["Wave3"] = 0
        dict["Wave4"] = 0
        return dict
#NE_CWF
    def generateForecast(self, argDict):
        # Get variables
        error = self._getVariables(argDict)
        if error is not None:
            return error

        # Get the areaList -- derived from defaultEditAreas and
        # may be solicited at run-time from user if desired
        self._areaList = self.getAreaList(argDict)
        if len(self._areaList) == 0:
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
        fcst = string.replace(fcst, "... ", "...")
        fcst = string.replace(fcst, ". INCLUDING", "...including")
        fcst = string.replace(fcst, "TO SEAS", "to")
        fcst = self._postProcessProduct(fcst, argDict)

        return fcst


    def _determineTimeRanges(self, argDict):
        # Set up the Narrative Definition and initial Time Range
#print("PRODUCT ISSUANCE:::", self._productIssuance, "\n")
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
        self._ddhhmmTime = string.upper(self.getCurrentTime(
            argDict, "%d%H%M", shiftToLocal=0, stripLeading=0))
        staticIssueTime=re.sub(r'(\d{3,4} [AP]M).*',r'\1',self._productIssuance)
        self._timeLabel =  staticIssueTime + " " + string.upper(self.getCurrentTime(
            argDict, " %Z %a %b %e %Y", stripLeading=1))
        # Re-calculate issueTime
        #self._issueTime = self.strToGMT(staticIssueTime)
        self._issueTime = self.strToGMT(staticIssueTime)

        expireTimeRange = self.IFP().TimeRange(self._expireTime, self._expireTime + 3600)
        self._expireTimeStr = string.upper(self.timeDisplay(expireTimeRange, "", "", "%d%H%M", ""))
        return None

    def _preProcessArea(self, fcst, editArea, areaLabel, argDict):
        # This is the header for an edit area combination
#print("Generating Forecast for", areaLabel)

        areaHeader = self.makeAreaHeader(
            argDict, areaLabel, self._issueTime, self._expireTime,
            self._areaDictionary, self._defaultEditAreas)

        fcst = fcst + areaHeader
#        if self._issuanceType == "UPDATE":
#            fcst = fcst + "UPDATED\n\n"
#        elif self._issuanceType == "CORRECTION":
#            fcst = fcst + "CORRECTED\n\n"

        # get the hazards text
        self._hazards = argDict['hazards']
        self._combinations = argDict["combinations"]

        headlines = self.generateProduct("Hazards", argDict, area = editArea,
                                         areaLabel=areaLabel,
                                         timeRange = self._timeRange)
        fcst = fcst + headlines

        return fcst

    def postProcessPhrase(self, tree, node):
        words = node.get("words")
        rval = None
        if words is not None:
            words = words.replace("1 foot", "1 foot or less")
            #words = words.replace("gusts up to", "occasional gusts to")
            # Translate phrase
            # This is necessary so that word-wrap works correctly
            try:
                words = self.translateForecast(words, self._language)
            except:
                words = self.translateForecast(words, "english")
            rval = self.setWords(node, words)
        return rval


    def makeAreaHeader(self, argDict, areaLabel, issueTime, expireTime,
                       areaDictName, defaultEditAreas,
                       cityDescriptor ="INCLUDING THE CITIES OF",
                       areaList=None, includeCities=1, includeZoneNames=1,
                       includeIssueTime=1, includeCodes=1, includeVTECString=1,
                       hVTECString=None):
        # Make a UGC area header for the given areaLabel
        # Determine list of areas (there could be more than one if we are using a combination)

        if areaDictName == None or areaDictName == "None":
            return areaLabel + "\n"

        # If we didn't supply an areaList,
        #     Use combinations file or defaultEditAreas
        usingCombo = 0
        if areaList is None:
            combinations = argDict["combinations"]
            if combinations is not None:
                areaList = self.getCurrentAreaNames(argDict, areaLabel)
                usingCombo = 1
            else:
                for editArea, label in defaultEditAreas:
                    if label == areaLabel:
                        areaList = [editArea]

        # Access the UGC information for the area(s) if available
        accessor = ModuleAccessor.ModuleAccessor()
        areaDict = accessor.variable(areaDictName, "AreaDictionary")
        if areaDict is None:  # create a dummy header
            codeString = "STZxxx-"
            nameString = areaLabel
            cityString = ""
        else:
            codeString = ""
            nameString = ""
            cityString = ""
            lastPrefix = ""

# Changed 8/23
            areaList, ugcList = self.makeUGCList(areaDict, areaList)
            codeString = self.makeUGCString(ugcList)

#            codeString = self.makeUGCString(self.makeUGCList(areaDict, areaList))
            for areaName in areaList:
                if areaName in areaDict.keys():
                    entry = areaDict[areaName]
                    ugcName = entry["ugcName"]
                    if entry.has_key("ugcCityString"):
                        ugcCityString = entry["ugcCityString"]
                    else:
                        ugcCityString = ""
                    nameString = nameString + ugcName + "-"
                    cityString = cityString + ugcCityString
                else:
                    if usingCombo != 1:
                        nameString = nameString + areaName + "-"
                    cityString = ""

        # get the VTEC string from the HazardsTable
        VTECString = ""
        if argDict.has_key("hazards") and includeVTECString:
            hazards = argDict["hazards"]
            VTECString = hazards.getVTECString(areaList) #, self._timeRange) changed 8/23
            if hVTECString is not None:
                VTECString = VTECString + hVTECString + "\n"

        # format the expiration time
        expireTimeRange = AFPS.TimeRange(expireTime, expireTime + 3600)
        expireTime = string.upper(self.timeDisplay(expireTimeRange, "", "",
          "%d%H%M", ""))
        codeString = self.endline(codeString + "-" + expireTime + "-",
          linelength=self._lineLength, breakStr=["-"])

        # get this time zone
        thisTimeZone = os.environ["TZ"]
#print("THIS TIME ZONE : ", thisTimeZone, "\n\n")
        zoneList = []
        # check to see if we have any areas outside our time zone
        for areaName in areaList:
            if areaName in areaDict.keys():
                entry = areaDict[areaName]
                if not entry.has_key("ugcTimeZone"):   #add your site tz
                    if thisTimeZone not in zoneList:
                        zoneList.append(thisTimeZone)
                    continue  # skip this entry
                timeZoneList = entry["ugcTimeZone"]
                if type(timeZoneList) == types.StringType:  # a single value
                    timeZoneList = [timeZoneList]   # make it into a list
                for timeZone in timeZoneList:
                    if timeZone not in zoneList:
                        zoneList.append(timeZone)

        # if the resulting zoneList is empty, put in our time zone
        if len(zoneList) == 0:
            zoneList.append(thisTimeZone)

        # if the resulting zoneList has our time zone in it, be sure it
        # is the first one in the list
        try:
            index = zoneList.index(thisTimeZone)
            if index != 0:
                del zoneList[index]
                zoneList.insert(0, thisTimeZone)
        except:
            pass

        # now create the time string
#        issueTimeStr = ''
        issueTimeStr = self._timeLabel

        try:
            if self._useRegionLabel == 1:
                if (areaLabel):
                    nameString = areaLabel
        except:
            pass
        nameString = self.endline(nameString, linelength=self._lineLength,
          breakStr=["-"])
        if cityString:
            numCities = len(string.split(cityString, "...")[1:])
            if numCities == 1:
                cityDescriptor = string.replace(cityDescriptor, "CITIES", "CITY")
            cityString = self.endline(cityDescriptor + cityString,
              linelength=self._lineLength, breakStr=["..."])
# These are the same at this point (and good)
        issueTimeStr = issueTimeStr + "\n\n"
        timeLabel = self._timeLabel + "\n\n"

        try:
            if self._includeHeader == 0:
                issueTimeStr = "\n"
                codeString = ""
                cityString = ""
        except:
            pass
        if includeCities == 0:
            cityString = ""
        if includeZoneNames == 0:
            nameString = ""
        if includeIssueTime == 0:
            issueTimeStr = ""
        if includeCodes == 0:
            codeString = ""
        if includeVTECString == 0:
            VTECString = ""
        header = codeString + VTECString + nameString + cityString  + timeLabel #Not issueTimeStr
#        print("\nHEADER ::: \n", header)
        return header



    def _issuance_list(self, argDict):
        #  This method sets up configurable issuance times with associated
        #  narrative definitions.  See the Text Product User Guide for documentation.
        if self._definition["includeEveningPeriod"] == 1:
            narrativeDefAM = [
                ("CWFFirstPeriod", "period1"), ("CWFPeriod", 12), ("CWFPeriod", 12),
                ("CWFPeriodMid", 12), ("CWFPeriodMid", 12),
                ("CWFPeriodMid", 12),
                ("CWFExtended", 24), ("CWFExtended", 24)
                ]
            narrativeDefPM = [
                ("CWFFirstPeriod", "period1"),("CWFPeriod", 12), ("CWFPeriod", 12),
                ("CWFPeriodMid", 12), ("CWFPeriodMid", 12), ("CWFPeriodMid", 12),
                ("CWFPeriodMid", 12),
                ("CWFExtended", 24), ("CWFExtended", 24)
                ]
        else:
            narrativeDefAM = [
                ("CWFFirstPeriod", "period1"), ("CWFPeriod", 12), ("CWFPeriod", 12),
                ("CWFPeriodMid", 12), ("CWFExtended", 24),#("CWFPeriodMid", 24),
                ("CWFExtended", 24) , ("CWFExtended", 24)
                ]
            narrativeDefPM = [
                ("CWFFirstPeriod", "period1") , ("CWFPeriod", 12), ("CWFPeriod", 12), # period1=this afternoon through tonight
                ("CWFPeriodMid", 12) , ("CWFPeriodMid", 12),             # then tomorrow,tomorrow night, and next day and night (12hr)
                ("CWFExtended", 24), ("CWFExtended", 24), ("CWFExtended", 24)     # then 3 night/day combos?
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
            ("300 AM", self.DAY()-2, self.NIGHT(), 9,
             ".TODAY...", "early in the morning", "late in the afternoon",
             1, narrativeDefAM),
            ("900 AM", self.DAY()+2, self.NIGHT(), 15,
             ".TODAY...", "early in the morning", "late in the afternoon",
             1, narrativeDefAM),
###            #  End times are tomorrow:
            ("300 PM", self.DAY()+8, self.NIGHT()+12, 21,
             ".TONIGHT...", "late tonight", "this evening",
             1, narrativeDefPM),
            ("900 PM", self.NIGHT()+2, self.DAY()+24, 27,
             ".TONIGHT...", "late tonight", "this evening",
             1, narrativeDefPM),
##     END PST Section
##
######  Below for Pacific Daylight Time ###
###            ("300 AM", self.DAY()-1, self.NIGHT(), 9,
###             ".TODAY...", "early in the morning", "late in the afternoon",
###             1, narrativeDefAM),
            #("300 AM - Update", "issuanceHour", self.NIGHT(), 9,
            # ".TODAY...", "early in the morning", "late in the afternoon",
            # 1, narrativeDefAM),
###            ("900 AM", self.DAY()+3, self.NIGHT(), 15,
###             ".TODAY...", "this morning", "late in the afternoon",
###             1, narrativeDefAM),
            #("900 AM - Update", "issuanceHour", self.NIGHT(), 15,
            # ".REST OF TODAY...", "this morning", "late in the afternoon",
            # 1, narrativeDefAM),
            #  End times are tomorrow:
###            ("300 PM", self.DAY()+11, self.NIGHT()+12, 21,
###             ".TONIGHT...", "late tonight", "this evening",
###             1, narrativeDefPM),
            #("300 PM - Update", "issuanceHour", self.NIGHT()+12, 21,
            # ".TONIGHT...", "late tonight", "this evening",
            # 1, narrativeDefPM),
###            ("900 PM", self.NIGHT()+3, self.NIGHT()+12, 27,
###             ".TONIGHT...", "late tonight", "this evening",
###             1, narrativeDefPM),
            #("900 PM - Update", "issuanceHour", self.NIGHT()+12, 27,
            # ".REST OF TONIGHT...", "late tonight", "this evening",
            # 1, narrativeDefPM),
####    End PDT section
        ]

    def moderated_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating moderated stats.
        # By convention the first value listed is the percentage
        # allowed for low values and second the percentage allowed
        # for high values.
        dict = SampleAnalysis.SampleAnalysis.moderated_dict(self, parmHisto, timeRange, componentName)
        dict["Wind"] = (5, 5)
        dict["WindGust"] = (50, 1)
    dict["WaveHeight"] = (5, 5)
    dict["Wave1"] = (5,5)
    dict["Wave2"] = (5,5)
    dict["Wave3"] = (5,5)
    dict["Wave4"] = (5,5)
    dict["Period"] = (5, 5)
    dict["Period1"] = (5, 5)
    dict["Period2"] = (5, 5)
    dict["Period3"] = (5, 5)
    dict["Period4"] = (5, 5)
    dict["PoP"] =  (5, 5)
        return dict

    def stdDev_dict(self, parmHisto, timeRange, componentName):
        # This dictionary defines the low and high limit at which
        # outliers will be removed when calculating stdDev stats.
        # These tuples represent the (low, high) number of standard
        # deviations.  Any values falling outside this range will
        # not be included in the calculated statistic.
        return {
                "WindGust": (1.0, 1.0),
                }

    def seasFlag(self, tree, node):
       return

    def phrase_connector_dict(self, tree, node):
        # Dictionary of connecting phrases for various
        # weather element phrases
        # The value for an element may be a phrase or a method
        # If a method, it will be called with arguments:
        #   tree, node
        dict = TextRules.TextRules.phrase_connector_dict(self, tree, node)
        dict["rising to"] =  {
                                "Wind": "...rising to ",
                                "WindGust": "...rising to ",
                                "WaveHeight": "...building to ",
                                "Wave1": " building to ",
                                "Wave2": " building to ",
                                "Wave3": " building to ",
                                "Wave4": " building to ",
                         }

        dict["easing to"] =  {
                                "Wind": "...easing to ",
                                "WindGust": "...easing to ",
                                "WaveHeight": "...subsiding to ",
                                "Wave1": " subsiding to ",
                                "Wave2": " subsiding to ",
                                "Wave3": " subsiding to ",
                                "Wave4": " subsiding to ",
                         }
        dict["backing"] =  {
                                "Wind": "...becoming ",
                                "WindGust": "...becoming ",
                                "WaveHeight": "...becoming ",
                                "Wave1": "becoming ",
                                "Wave2": "becoming ",
                                "Wave3": "becoming ",
                                "Wave4": "becoming ",
                         }

        dict["veering"] =  {
                                "Wind": "...becoming ",
                                "WindGust": "...becoming ",
                                "WaveHeight": "...becoming ",
                                "Wave1": " becoming ",
                                "Wave2": " becoming ",
                                "Wave3": " becoming ",
                                "Wave4": " becoming ",
                         }

        dict["becoming"] =  "...becoming "
        dict["increasing to"] =  {
                                "Wind":  "...rising to ",
                                "WindGust":  "...rising to ",
                                "WaveHeight": "...building to ",
                                "Wave1": " building to ",
                                "Wave2": " building to ",
                                "Wave3": " building to ",
                                "Wave4": " building to ",
                             }
        dict["decreasing to"] =  {
                                "Wind":  "...easing to ",
                                "WindGust":  "...easing to ",
                                "WaveHeight": "...subsiding to ",
                                "Wave1": " subsiding to ",
                                "Wave2": " subsiding to ",
                                "Wave3": " subsiding to ",
                                "Wave4": " subsiding to ",
                             }
        dict["shifting to the"] =  "...becoming "
        dict["becoming onshore"] =  " becoming onshore "
        dict["then"] =  {"Wx": ". ",
                         "Vector": " becoming ",
                         "Scalar": "...becoming ",
                         "otherwise": "...and then ",
                         }
        return dict


    def CWFFirstPeriod(self):
        return {
            "type": "component",
            "methodList": [
                          self.assemblePhrases,
                          self.wordWrap,
                          ],
            "analysisList": [
                          ("Wind", self.vectorModeratedMinMax, [3]),
                          ("WindGust", self.stdDevAvg, [3]),
                          ("WaveHeight", self.moderatedMinMax, [6]),
                          ("Wave1", self.vectorModeratedMinMax, [6]),
                          ("Wave2", self.vectorModeratedMinMax, [6]),
                          ("Wave3", self.vectorModeratedMinMax, [6]),
                          ("Wave4", self.vectorModeratedMinMax, [6]),
                          ("Period1", self.moderatedMinMax, [6]),
                          ("Period2", self.moderatedMinMax, [6]),
                          ("Period3", self.moderatedMinMax, [6]),
                          ("Period4", self.moderatedMinMax, [6]),
                          ("Wx", self.rankedWx, [12]),
              #("Sky", self.moderatedMinMax, [12]),
                          #("PoP", self._PoP_analysisMethod("CWFPeriod"), [12]),
                          #("PoP", self.binnedPercent, [12]),
                          ],
             "phraseList":[
                           # WINDS
                           #(self.marine_wind_withGusts_phrase, self._windLocalEffectList, self._windGustLocalEffectList),
                           # Alternative:
                           self.marine_wind_phrase, #self._windLocalEffectList),
                           (self.gust_phrase, self._windGustLocalEffectList),
                           # WAVES
                           self.first_period_seas_phrase,
                           #self.waves_phrase,
                           # WEATHER
                           self.weather_phrase,
                           #self.skyPopWx_phrase,
                ],
            "additionalAreas": [
                   ("Wind", ["Cape_Mendo_450", "Cape_Mendo_455", "Pt_St_George", "Pt_Arena", "Capes_450", "Capes_455",
                              "N450", "N455",  "E450", "E455",  "S450", "S455",  "W450", "W455"]),
                   ("WindGust", ["Cape_Mendo_450", "Cape_Mendo_455", "Pt_St_George", "Pt_Arena", "Capes_450", "Capes_455",
                              "N450", "N455",  "E450", "E455",  "S450", "S455",  "W450", "W455"]),
                   ],
             "intersectAreas": []
            }





    def CWFPeriod(self):
        return {
            "type": "component",
            "methodList": [
                          self.assemblePhrases,
                          self.wordWrap,
                          ],
            "analysisList": [
                          ("Wind", self.vectorModeratedMinMax, [3]),
                          ("WindGust", self.stdDevAvg, [3]),
                          ("WaveHeight", self.moderatedMinMax, [6]),
                          ("Wave1", self.vectorModeratedMinMax, [6]),
                          ("Wave2", self.vectorModeratedMinMax, [6]),
                          ("Wave3", self.vectorModeratedMinMax, [6]),
                          ("Wave4", self.vectorModeratedMinMax, [6]),
                          ("Period1", self.moderatedMinMax, [6]),
                          ("Period2", self.moderatedMinMax, [6]),
                          ("Period3", self.moderatedMinMax, [6]),
                          ("Period4", self.moderatedMinMax, [6]),
                          ("Wx", self.rankedWx, [12]),
                          #("PoP", self._PoP_analysisMethod("CWFPeriod"), [12]),
                          #("PoP", self.binnedPercent, [12]),
                          ],
             "phraseList":[
                           # WINDS
                           #(self.marine_wind_withGusts_phrase, self._windLocalEffectList, self._windGustLocalEffectList),
                           # Alternative:
                           self.marine_wind_phrase, #self._windLocalEffectList),
                           (self.gust_phrase, self._windGustLocalEffectList),
                           # WAVES
                           self.seas_phrase,
                           #self.waves_phrase,
                           # WEATHER
                           self.weather_phrase,
                           ],
            "additionalAreas": [
                   ("Wind", ["Cape_Mendo_450", "Cape_Mendo_455", "Pt_St_George", "Pt_Arena", "Capes_450", "Capes_455",
                              "N450", "N455",  "E450", "E455",  "S450", "S455",  "W450", "W455"]),
                   ("WindGust", ["Cape_Mendo_450", "Cape_Mendo_455", "Pt_St_George", "Pt_Arena", "Capes_450", "Capes_455",
                              "N450", "N455",  "E450", "E455",  "S450", "S455",  "W450", "W455"]),
                   ],
              "intersectAreas": []
            }

#########################
# Local Effects         #
#########################

    def _windGustLocalEffectList(self, tree, node):
        if self.currentAreaContains(tree, ["PZZ450"]):
print("*************Checking WindGust in PZZ450*************")
            leArea1 = self.LocalEffectArea("__Current__", "",intersectFlag=0)
            leArea2 = self.LocalEffectArea("Cape_Mendo_450", "around Cape Mendocino",intersectFlag=0)
            leArea3 = self.LocalEffectArea("Pt_St_George", "around Pt St George",intersectFlag=0)
            leArea4 = self.LocalEffectArea("Capes_450", "around Cape Mendocino and Pt St George",intersectFlag=0)
            leArea5 = self.LocalEffectArea("W450", "beyond 5 nm",intersectFlag=0)
            leArea6 = self.LocalEffectArea("E450", "within 5 nm",intersectFlag=0)
            leArea7 = self.LocalEffectArea("N450", "northern portion",intersectFlag=0)
            leArea8 = self.LocalEffectArea("S450", "southern portion",intersectFlag=0)
            return [self.LocalEffect([leArea1, leArea2], 5, " except "),
                    self.LocalEffect([leArea1, leArea3], 5, " except "),
                    self.LocalEffect([leArea1, leArea4], 5, " except "),
                    self.LocalEffect([leArea1, leArea5], 5, " except "),
                    self.LocalEffect([leArea1, leArea6], 5, " except "),
                    self.LocalEffect([leArea1, leArea7], 5, " except "),
                    self.LocalEffect([leArea1, leArea8], 5, " except "),
                    ]
        if self.currentAreaContains(tree, ["PZZ455"]):
print("*************Checking WindGust in PZZ455*************")
            leArea1 = self.LocalEffectArea("__Current__", "",intersectFlag=0)
            leArea2 = self.LocalEffectArea("Cape_Mendo_455", "around Cape Mendocino",intersectFlag=0)
            leArea3 = self.LocalEffectArea("Pt_Arena", "around Pt Arena",intersectFlag=0)
            leArea4 = self.LocalEffectArea("Capes_455", "around Cape Mendocino and Pt Arena",intersectFlag=0)
            leArea5 = self.LocalEffectArea("W455", "beyond 5 nm",intersectFlag=0)
            leArea6 = self.LocalEffectArea("E455", "within 5 nm",intersectFlag=0)
            leArea7 = self.LocalEffectArea("N455", "northern portion",intersectFlag=0)
            leArea8 = self.LocalEffectArea("S455", "southern portion",intersectFlag=0)
            return [self.LocalEffect([leArea1, leArea2], 5, " except "),
                    self.LocalEffect([leArea1, leArea3], 5, " except "),
                    self.LocalEffect([leArea1, leArea4], 5, " except "),
                    self.LocalEffect([leArea1, leArea5], 5, " except "),
                    self.LocalEffect([leArea1, leArea6], 5, " except "),
                    self.LocalEffect([leArea1, leArea7], 5, " except "),
                    self.LocalEffect([leArea1, leArea8], 5, " except "),
                    ]
        else:
            return[]

    def CWFPeriodMid(self):
        return {
            "type": "component",
            "methodList": [
                          self.assemblePhrases,
                          self.wordWrap,
                          ],
            "analysisList": [
                          ("Wind", self.vectorModeratedMinMax, [12]),
                          ("WindGust", self.stdDevAvg, [12]),
                          ("WaveHeight", self.moderatedMinMax, [12]),
                          ("Wave1", self.vectorModeratedMinMax, [12]),
                          ("Wave2", self.vectorModeratedMinMax, [12]),
                          ("Wave3", self.vectorModeratedMinMax, [12]),
                          ("Wave4", self.vectorModeratedMinMax, [12]),
                          ("Period1", self.moderatedMinMax, [12]),
                          ("Period2", self.moderatedMinMax, [12]),
                          ("Period3", self.moderatedMinMax, [12]),
                          ("Period4", self.moderatedMinMax, [12]),
              #("PoP", self._PoP_analysisMethod("CWFPeriodMid")),
                          #("PoP", self.binnedPercent),
                          ("Wx", self.rankedWx, [12]),
                        ],
             "phraseList":[
                           # WINDS
               self.marine_wind_withGusts_phrase,
                           # WAVES
                           self.seas_phrase,
                           #self.waves_phrase,
               # WEATHER
                           self.EXT_weather_phrase,
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
                          ("Wind", self.vectorModeratedMinMax, [12]),
                          ("WindGust", self.stdDevAvg, [12]),
                          ("WaveHeight", self.moderatedMinMax, [12]),
                          ("Wave1", self.vectorModeratedMinMax, [12]),
                          ("Wave2", self.vectorModeratedMinMax, [12]),
                          ("Wave3", self.vectorModeratedMinMax, [12]),
                          ("Wave4", self.vectorModeratedMinMax, [12]),
                          ("Period1", self.moderatedMinMax, [12]),
                          ("Period2", self.moderatedMinMax, [12]),
                          ("Period3", self.moderatedMinMax, [12]),
                          ("Period4", self.moderatedMinMax, [12]),
                          ###("PoP", self._PoP_analysisMethod("CWFExtended")),
                          ###("PoP", self.binnedPercent),
                          ("Wx", self.rankedWx, [12]),
                      ],
                 "phraseList":[
                               # WINDS
                   self.marine_wind_withGusts_phrase,
                   # WAVES
                               self.seas_phrase,
                               #self.waves_phrase,
                               # WEATHER
                               self.EXT_weather_phrase,
                               ],
          "intersectAreas": []
           }

    def EXT_weather_phrase(self):
        return {
            "setUpMethod": self.weather_setUp,
            "wordMethod": self.EXT_weather_words,
            "phraseMethods": self.standard_weather_phraseMethods()
            }

    def EXT_weather_words(self, tree, node):
        # Create a phrase to describe a list of weather sub keys for one sub-period

        # Get rankList
        statDict = node.getStatDict()
        rankList = self.getStats(statDict, "Wx")
#print("\n SubKeys in weather_words", rankList)
#print("   TimeRange", node.getTimeRange(), node.getAreaLabel())
#print("   Phrase name", node.getAncestor("name"))
        if rankList is None or len(rankList) == 0:
            return self.setWords(node, "")

        # Get the weather words for T only
        #subkey = self.getSubkeys(rankList)

    words=""
        for subkey, rank in rankList:
            if subkey.wxType() == "T":
                words = self.getWeatherWords(tree, node, rankList)
            else:
                #words = ""
        pass

        node.set('reportedRankList', rankList)

        # To replace multiple "and's" with ellipses
        words = self.useEllipses(tree, node, words)

        return self.setWords(node, words)



    def timePeriod_descriptor_list(self, tree, node):
        day = self.DAY()
        return [
                (day, (day+3)%24, "early in the morning"), # 6a-9a
                (day, (day+6)%24, "in the morning"),   # 6a-noon
                (day, (day+9)%24, "until early afternoon"),   # 6a-3p
                (day, (day+12)%24, ""),                       # 6a-6p
                (day, (day+15)%24, "until early evening"),    # 6a-9p
                (day, (day+18)%24, "through the evening"),    # 6a-midnite
                ((day+2)%24, (day+3)%24, "early in the morning"),  # 8a-9a
                ((day+3)%24, (day+6)%24, "late in the morning"), # 9a-noon
                ((day+3)%24, (day+9)%24, "late in the morning and early afternoon"), # 9a-3p
                ((day+3)%24, (day+12)%24, "late in the morning and afternoon"),      # 9a-6p
                ((day+3)%24, (day+15)%24, "until early evening"),      # 9a-9p
                ((day+3)%24, (day+18)%24, "through the evening"),      # 9a-midnite
                ((day+5)%24, (day+6)%24, "late in the morning"),      # 11a-noon
                ((day+6)%24, (day+9)%24,  "early in the afternoon"), # noon-3p
                ((day+6)%24, (day+12)%24, "in the afternoon"),     # noon-6p
                ((day+6)%24, (day+15)%24, "in the afternoon and early evening"),# noon-9p
                ((day+6)%24, (day+18)%24, "in the afternoon and evening"),# noon-midnite
                ((day+8)%24, (day+9)%24, "early"), # 2pm-3pm
                ((day+9)%24, (day+12)%24, self.lateDay_descriptor),   # 3p-6p
                ((day+9)%24, (day+15)%24, "early in the evening"),    # 3p-9p
                ((day+9)%24, (day+18)%24, "in the evening"),   # 3p-midnite
                ((day+9)%24, (day+21)%24, "until late in the night"),  # 3p-3a
                ((day+9)%24,  day, ""),                               # 3p-6a
                ((day+11)%24, (day+12)%24, "early in the evening"), # 5p-6p
                ((day+12)%24, (day+15)%24, "early in the evening"),   # 6p-9p
                ((day+12)%24, (day+18)%24, "in the evening"),   # 6p-midnite
                ((day+12)%24, (day+21)%24, "until late in the night"),    # 6p-3a
                ((day+12)%24, day, ""),                               # 6p-6a
                ((day+14)%24, (day+15)%24, "in the evening"), # 8p-9p
                ((day+15)%24, (day+18)%24, "late in the evening"),            # 9p-midnite
                ((day+15)%24, (day+21)%24, "late in the evening and overnight"),# 9p-3a
                ((day+15)%24, day, "late in the evening and overnight"),         # 9p-6a
                ((day+17)%24, (day+18)%24, "late in the evening"), # 11p-midnight
                ((day+18)%24, (day+21)%24, "overnight"),               # midnite-3a
                ((day+18)%24, day, "overnight"),                       # midnite-6a
                ((day+18)%24, (day+6)%24, ""),                              # midnite-noon
                ((day+20)%24, (day+21)%24, "overnight"), # 2a-3a
                ((day+21)%24, day, self.lateNight_descriptor),              # 3a-6a
                ((day+21)%24, (day+3)%24, "early in the morning"),          # 3a-9a
                ((day+21)%24, (day+6)%24, "early in the morning"),          # 3a-noon
                ((day+21)%24, (day+9)%24, "until afternoon"),               # 3a-3p
                ((day+21)%24, (day+12)%24, ""),                             # 3a-6p
                ((day+23)%24, (day)%24, self.lateNight_descriptor), # 5a-6a
                ]

    def periodCombining_elementList(self, tree, node):
        # Elements to determine whether to combine periods
        return #["Wind","Wx","WaveHeight"]

    def periodCombining_startHour(self, tree, node):
        # Hour after which periods may be combined
        return 120

    def null_nlValue_dict(self, tree, node):
        # Threshold below which values are considered "null" and  not reported.
        dict = TextRules.TextRules.null_nlValue_dict(self, tree, node)
        dict["WaveHeight"] = 2
    dict["Waves"] = 2
        dict["Wave1"] = 2
        dict["Wave2"] = 2
        dict["Wave3"] = 2
        dict["Wave4"] = 2
        dict["Wind"] =  4.5
        dict["WindGust"] = 30
        dict["Visibility"] = 3 # in nautical miles.
        return dict

    def first_null_phrase_dict(self, tree, node):
        # Phrase to use if values THROUGHOUT the period or
        # in the first period are Null (i.e. below threshold OR NoWx)
        # E.g.  LIGHT WINDS.    or    LIGHT WINDS BECOMING N 5 MPH.
        dict = TextRules.TextRules.first_null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "waves 2 ft or less"
        dict["Wave1"] =  "2 ft or less"
        dict["Wave2"] =  "2 ft or less"
        dict["Wave3"] =  "2 ft or less"
        dict["Wave4"] =  "2 ft or less"
        dict["Wind"] =  "wind variable less than 5 knots"
        return dict

    def null_phrase_dict(self, tree, node):
        # Phrase to use for null values in subPhrases other than the first
        #  E.g.  "NORTH WINDS 20 to 25 KNOTS BECOMING LIGHT"
        dict = TextRules.TextRules.null_phrase_dict(self, tree, node)
        dict["WaveHeight"] =  "2 ft or less"
        dict["Wave1"] =  "2 ft or less"
        dict["Wave2"] =  "2 ft or less"
        dict["Wave3"] =  "2 ft or less"
        dict["Wave4"] =  "2 ft or less"
        dict["Wind"] =  "variable less than 5 knots"
        dict["Wx"] =  ""
        return dict

    def maximum_range_nlValue_dict(self, tree, node):
        # Maximum range to be reported within a phrase
        # e.g. 5 to 10 mph
        dict = TextRules.TextRules.maximum_range_nlValue_dict(self, tree, node)
        dict["Wind"] = {'default': 10,
                           (0.0, 10.0): 5,
                          (10.0, 200.0): 10,
                          }
        dict["WaveHeight"] = {'default': 2,
                           (0.0, 15.0): 2,
                          (15.0, 25.0): 4,
                          (25.0, 200.0): 5,
                          }
        dict["Wave1"] = {'default': 2,
                         (0.0, 15.0): 2,
                         (15.0, 25.0): 4,
                         (25.0, 200.0): 5,
                         }
        dict["Wave2"] = {'default': 2,
                         (0.0, 15.0): 2,
                         (15.0, 25.0): 4,
                         (25.0, 200.0): 5,
                         }
        dict["Wave3"] = {'default': 2,
                         (0.0, 15.0): 2,
                         (15.0, 25.0): 4,
                         (25.0, 200.0): 5,
                         }
        dict["Wave4"] = {'default': 2,
                         (0.0, 15.0): 2,
                         (15.0, 25.0): 4,
                         (25.0, 200.0): 5,
                         }
        return dict

    def marineRounding(self, value, mode, increment, maxFlag):
        mode = "Nearest"
        if maxFlag:
            if value > 20 and value < 23:
                mode = "Nearest"
            elif value > 30 and value < 34:
                mode = "Nearest"
            elif value > 45 and value < 48:
                mode = "Nearest"
            else:
                mode = "Nearest"
        return self.round(value, mode, increment)

    def combine_singleValues_flag_dict(self, tree, node):
        # Dictionary of weather elements to combine using single values
        # rather than ranges.  If you are using single value statistics
        # for a weather element, you will want to set this flag to 1.
        dict = TextRules.TextRules.increment_nlValue_dict(self, tree, node)
        dict["Wind"] = 0
        dict["WindGust"] = 0
        dict["WaveHeight"] = 0
        dict["Wave1"] = 0
        dict["Wave2"] = 0
        dict["Wave3"] = 0
        dict["Wave4"] = 0
    dict["Period1"] = 1
    dict["Period2"] = 1
    dict["Period3"] = 1
    dict["Period4"] = 1
        return dict

    def vector_mag_difference_nlValue_dict(self, tree, node):
        # Magnitude difference.  If the difference between magnitudes
        # for sub-ranges is greater than this value,
        # the different magnitudes will be noted in the phrase.
        return  {
            "Wind": 10,  # kt
        "otherwise": 50,
            }

    def scalar_difference_nlValue_dict(self, tree, node):
        # Scalar difference.  If the difference between scalar values
        # for 2 sub-periods is equal or greater than this value,
        # the different values will be noted in the phrase.
        return {
            "WindGust": 10, # kt
            "PoP": 10, # percentage
            "otherwise": 100,
          }

    def vector_dir_difference_dict(self, tree, node):
        # Direction difference.  If the difference between directions
        # for sub-ranges is greater than or equal to this value,
        # the different directions will be noted in the phrase.
        return {
            "Wind": 180, # degrees
            "Wave1": 360,
            "Wave2": 360,
            "Wave3": 360,
            "Wave4": 360,
            "otherwise": 60,
            }

    def X_seas_phrase(self):
        return {
            "setUpMethod": self.seas_setUp,
            "wordMethod": self.seas_words,
            "phraseMethods": self.standard_phraseMethods(),
            #"phraseMethods": self.standard_vector_phraseMethods(),
            }
    def X_waves_phrase(self):
        return {
            #"setUpMethod": self.seas_setUp,
            "wordMethod": self.waves_words,
            "phraseMethods": self.standard_phraseMethods(),
            #"phraseMethods": self.standard_vector_phraseMethods(),
            }
    def seas_setUp(self, tree, node, periodFlag=0):
    FILE = open("/data/local/seas_setUpLog", "a")

        areaLabel = node.getAreaLabel()
        timeRange = node.getTimeRange()
        elementName = self.seasWaveHeight_element(tree, node)
    FILE.write("ELEMENT: " + elementName + "\n")

        descriptor = self.phrase_descriptor(tree, node, "seas", elementName)
        node.set("descriptor", descriptor)

        seas = self.ElementInfo(elementName, "List")

        elementInfoList = [seas]
        self.subPhraseSetUp(tree, node, elementInfoList, self.scalarConnector)
        return self.DONE()

    def X_check_SeaState(self, tree, node):
        areaLabel = node.getAreaLabel()
        timeRange = node.getTimeRange()
        Cstate = 0
        SeasOnly = 0
        elements = ("WaveHeight","Wave1", "Wave2", "Wave3", "Wave4")
        WAVES = ("Wave1", "Wave2", "Wave3", "Wave4")

        for x in elements:
            threshold = self.nlValue(self.null_nlValue(tree, node, x,x),max)#"Wave1", "Wave1"), max)
            nulldict = self.null_nlValue_dict(tree,node)
            threshold = nulldict[x]

        for i in WAVES:
            w= tree.stats.get(i, timeRange, areaLabel, mergeMethod="vectorModeratedMinMax")
            if w is None:
                mag = 0
                Dir = 0
            else:
                mag, Dir = w

            if mag > threshold:
                Cstate = Cstate + 1
                wnum = int(string.replace(i,"Wave",""))
print("wnum",wnum)
                SeasOnly = str(wnum)
            else:
                Cstate = Cstate
                SeasOnly = SeasOnly

print("Cstate is", Cstate)
print("SeasOnly is", SeasOnly)

        return Cstate, SeasOnly


    def seas_words(self, tree, node):
        elementInfo = node.getAncestor("firstElement")
        elementName = elementInfo.name
        areaLabel = node.getAreaLabel()
        timeRange = node.getTimeRange()
        argDict = tree.get("argDict")
        cstate, wavenum = self.check_SeaState(tree,node)
        wave1 = tree.stats.get("Wave1", timeRange, areaLabel, mergeMethod="MinMax")
        wave2 = tree.stats.get("Wave2", timeRange, areaLabel, mergeMethod="MinMax")
        wave3 = tree.stats.get("Wave3", timeRange, areaLabel, mergeMethod="MinMax")
        wave4 = tree.stats.get("Wave4", timeRange, areaLabel, mergeMethod="MinMax")
        #per1 = tree.stats.get("Period1", timeRange, areaLabel, mergeMethod="MinMax")#"Avg")
        #per2 = tree.stats.get("Period2", timeRange, areaLabel, mergeMethod="MinMax")#"Avg")
        #per3 = tree.stats.get("Period3", timeRange, areaLabel, mergeMethod="MinMax")#"Avg")
        #per4 = tree.stats.get("Period4", timeRange, areaLabel, mergeMethod="MinMax")#"Avg")
        per1 = tree.stats.get("Period1", timeRange, areaLabel, mergeMethod="Avg")
        per2 = tree.stats.get("Period2", timeRange, areaLabel, mergeMethod="Avg")
        per3 = tree.stats.get("Period3", timeRange, areaLabel, mergeMethod="Avg")
        per4 = tree.stats.get("Period4", timeRange, areaLabel, mergeMethod="Avg")

        statDict = node.getStatDict()
        stats = self.getStats(statDict, elementName)
        units = self.units_descriptor(tree, node, "units", "ft")
        waveUnit = self.units_descriptor(tree, node, "unit", "ft")
        if statDict is None:
            return
        WH = self.getStats(statDict, "WaveHeight")
        if WH is None:
            return self.setWords(node, "")
        waveWords = self.waves_words(tree, node)
print("########### wave words", waveWords)
        desc = ""
        if cstate == 4:
            desc = "confused seas"
        else:
            desc = "seas"
        min, max = self.getValue(WH, "MinMax")
        threshold = self.nlValue(self.null_nlValue(tree, node, "WaveHeight", "WaveHeight"), max)
        if int(min) < threshold and int(max) < threshold:
            return self.setWords(node, "seas 2 ft or less")
        if int(min) == 1 and int(max) == 1:
            units = waveUnit
        if int(min) < threshold and int(max) < threshold:
            return self.setWords(node, "seas 2 ft or less")
        if int(min) == 1 and int(max) == 1:
            units = waveUnit
        waveStr = "|* place holder *|"
print("sea state ==", cstate)
        if cstate == 0:
            magStr = self.format(self.getScalarRangeStr(tree, node, "WaveHeight", min, max))
            waveStr = magStr +" " + units
            phrase = node.getParent()
            phrase.set("descriptor",desc)
            phrase.doneList.append(self.embedDescriptor)
        if cstate == 1:
            wave = "Wave" + wavenum
print("cstate=1 wave",wave)
            per = "Period" + wavenum
print("per", per)
            wave1 = tree.stats.get(wave, timeRange, areaLabel, mergeMethod="MinMax")#Avg")
            #per_1 = tree.stats.get(per, timeRange, areaLabel, mergeMethod="MinMax")#Avg")
            per1 = tree.stats.get(per, timeRange, areaLabel, mergeMethod="Avg")
            mag1, dir1 = wave1
            #if mper1 == 0:
            #    per1 = xper1
            #else:
            #    per1 = per_1#self.average(mper1,xper1)
print("per1", per1)
            #xmag1 = self.getValue(mag1, "Max")
            #xmag1 = int(xmag1)
            #mmag1 = self.getValue(mag1, "Min")
            #mmag1 = int(mmag1)
            magStr = self.format(self.getScalarRangeStr(tree, node, "WaveHeight", min, max))
            #self.vector_mag(tree, node, mmag1, xmag1, units, wave)
            dirStr = self.vector_dir(dir1)
            periodPhrase = self.embedded_period_phrase(tree, node, per1)
print("periodPhrase", periodPhrase)
            waveStr = desc+ " " + dirStr + magStr + " " + units + periodPhrase
        if cstate == 2 or cstate == 3:
            magStr = self.getScalarRangeStr(tree, node, "WaveHeight", min, max)
            waveStr = desc + " "+ magStr + " " + units
            waveStr = waveStr + "...including "
            waveStr = waveStr + waveWords
print("waveStr", waveStr)
print("waveWords", waveWords)
        if cstate == 4:
            magStr = self.getScalarRangeStr(tree, node, "WaveHeight", min, max)
            waveStr = desc + " "+ magStr + " " + units

print(waveStr)

print("#### done set the wave words")
        return self.setWords(node, waveStr)



    def X_waves_words(self, tree, node):
        FILE = open("/data/local/wavewordCheck","a")
    # Check SEA STATE so we can adjust the threshold if necessary
        mySeaState = self.check_SeaState(tree,node)

        wave1 = self.ElementInfo("Wave1", "List", self.VECTOR())
        wavesPhrase = self.waves_words
        wave2 = self.ElementInfo("Wave2", "MinMax", self.VECTOR(), phraseDef=wavesPhrase, primary=0)
        wave3 = self.ElementInfo("Wave3", "MinMax", self.VECTOR(), phraseDef=wavesPhrase, primary=0)
        wave4 = self.ElementInfo("Wave4", "MinMax", self.VECTOR(), phraseDef=wavesPhrase, primary=0)
        elementInfoList = [wave1, wave2, wave3, wave4]
        node.set("periodFlag", 1)
        period1 = self.ElementInfo("Period1", "MinMax", primary=0)
        period2 = self.ElementInfo("Period2", "MinMax", primary=0)
        period3 = self.ElementInfo("Period3", "MinMax", primary=0)
        period4 = self.ElementInfo("Period4", "MinMax", primary=0)
        elementInfoList.append(period1)
        elementInfoList.append(period2)
        elementInfoList.append(period3)
        elementInfoList.append(period4)


##        words = self.subPhraseSetUp(tree, node, elementInfoList, self.vectorConnector)
#########################################################################
        ### ABOVE IS FROM WAVES_SETUP
        periodFlag = node.getAncestor("periodFlag")
        statDict = node.getStatDict()
        ### initialize the subPhrase list
        subPhrases = []
        elementInfoList = node.getAncestor("elementInfoList")

        ### loop through all the wave grids
        for waves, period in [("Wave1", "Period1"),("Wave2", "Period2"),("Wave3", "Period3"),("Wave4", "Period4")]:

            ### grab the info for wave grids
            for elementInfo in elementInfoList:
                if elementInfo.name == waves:
                    wavesInfo = elementInfo
                    break

#print("################## waves period", waves, period)
            ### create the wave phrase
            wavesWords = ""#self.simple_vector_phrase(tree, node, wavesInfo, checkRepeating=1)

            wavestats = tree.stats.get(waves, node.getTimeRange(), node.getAreaLabel(), mergeMethod="List")
            statsByRange = self.makeRangeStats(tree, self.VECTOR(), wavestats, node.getTimeRange())
            if statsByRange is None:
                break
            # Get values for each part of time range
print("SBR length", len(statsByRange), node.getTimeRange())
            nulldict = self.null_nlValue_dict(tree,node)
print("waves", waves)
            threshold = nulldict[waves]
            dirdict = self.vector_dir_difference_dict(tree,node)
            magdict = self.vector_mag_difference_nlValue_dict(tree,node)
            perdict = self.scalar_difference_nlValue_dict(tree,node)
            dirthresh = dirdict[waves]
            magthresh = magdict[waves]
            perthresh = perdict[period]
print("dirthresh-",dirthresh)
print("magthresh-",magthresh)
print("perthresh-",perthresh)
            if len(statsByRange) == 1:
                mperiodStats = tree.stats.get(period, node.getTimeRange(), node.getAreaLabel(), mergeMethod="Min")#Average")
                xperiodStats = tree.stats.get(period, node.getTimeRange(), node.getAreaLabel(), mergeMethod="Max")#Average")
                periodStats = tree.stats.get(period, node.getTimeRange(), node.getAreaLabel(), mergeMethod="Average")
                if mperiodStats == 0:
                    periodStats = xperiodStats
        FILE.write("PERIOD STATS: "+str(periodStats)+"\n")
        FILE.write("BASE THRESHOLD: "+str(threshold)+"\n")
        # ADJUST THRESHOLD BASED ON PERIOD STATS
        if periodStats > 17.0 and mySeaState[0] > 1:
            threshold+=2
        elif periodStats > 12.0 and mySeaState[0] > 1:
            threshold+=1
        FILE.write("ADJUSTED THRESHOLD: "+str(threshold)+"\n")
                periodPhrase = self.embedded_period_phrase(tree, node, periodStats)
                wd1, pd1 = statsByRange[0]
                wMag1, wDir1 = wd1
                xMag1 = max(wMag1)
                mMag1 = min(wMag1)
                if mMag1 == 0.0:
                    mMag1 = xMag1
                XMag1 = self.average(xMag1,mMag1)
                magStr1 = self.vector_mag(tree, node, XMag1, XMag1, elementInfo.outUnits, waves)#units was wavesInfo.outUnitsu
                dirStr1 = self.vector_dir(wDir1)
                if mMag1 <=threshold and xMag1 <= threshold:
                    wavesWords = ""
                elif xMag1 > threshold:
                    wavesWords = dirStr1 + self.format(magStr1) + periodPhrase
            elif len(statsByRange) == 2:
print(waves)
print("SBR 0", statsByRange[0])
print("SBR 1", statsByRange[1])
                wd1, pd1 = statsByRange[0]
                wd2, pd2 = statsByRange[1]
                wMag1, wDir1 = wd1
                wMag2, wDir2 = wd2
                xMag1 = max(wMag1)
                xMag2 = max(wMag2)
                mMag1 = min(wMag1)
                mMag2 = min(wMag2)
                if mMag1 == 0.0:
                    mMag1 = xMag1
                if mMag2 == 0.0:
                    mMag2 = xMag2
print("sb2 parts1",wMag1,pd1)
                XMag1 = self.average(xMag1, mMag1)
                XMag2 = self.average(xMag2, mMag2)
                XMagA = self.average(xMag1, xMag2)
                magStr1 = self.vector_mag(tree, node, XMag1, XMag1, elementInfo.outUnits, waves)
                dirStr1 = self.vector_dir(wDir1)

                magStr2 = self.vector_mag(tree, node, XMag2, XMag2, elementInfo.outUnits, waves)
                dirStr2 = self.vector_dir(wDir2)
                magStrA = self.vector_mag(tree, node, XMagA, XMagA, elementInfo.outUnits, waves)
                mperiodStats1 = tree.stats.get(period, pd1, node.getAreaLabel(), mergeMethod="Min")
                xperiodStats1 = tree.stats.get(period, pd1, node.getAreaLabel(), mergeMethod="Max")
                periodStats1 = tree.stats.get(period, pd1, node.getAreaLabel(), mergeMethod="Average")
                if periodStats1 is None:
                    periodStats1 = 0
                if mperiodStats1 == 0:
                    periodStats1 = xperiodStats1
                mperiodStats2 = tree.stats.get(period, pd2, node.getAreaLabel(), mergeMethod="Min")
                xperiodStats2 = tree.stats.get(period, pd2, node.getAreaLabel(), mergeMethod="Max")
                periodStats2 = tree.stats.get(period, pd2, node.getAreaLabel(), mergeMethod="Average")
                if periodStats2 is None:
                    periodStats2 = 0
                if mperiodStats2 == 0:
                    periodStats2 = xperiodStats2
                if periodStats1 == 0:
                    periodStats1 == periodStats2
                if periodStats2 == 0:
                    periodStats2 == periodStats1
                magdiff = abs(xMag1 - xMag2)
                dirdiff = abs(int(wDir1) - int(wDir2))
                perdiff = abs(periodStats1 - periodStats2)
        FILE.write("PERIOD STATS: "+str(periodStats1)+" - "+str(periodStats2)+"\n")
        FILE.write("SEA STATE: "+str(mySeaState)+"\n")
         # ADJUST THRESHOLD BASED ON PERIOD STATS
                if periodStats1 > 17.0 or periodStats2 > 17.0:
            if  mySeaState[0] > 1:
                        threshold+=2
                elif periodStats1 > 12.0 or periodStats2 > 12.0:
            if mySeaState[0] > 1:
                        threshold+=1
                FILE.write("ADJUSTED THRESHOLD: "+str(threshold)+"\n")

                if xMag1 <= threshold and xMag2 <=threshold:
print("both below thresh; setting to null")
                    wavesWords = ""
                elif xMag1 <= threshold and xMag2 > threshold:
                    periodPhrase = self.embedded_period_phrase(tree, node, periodStats2)
                    wavesWords = dirStr2 + " building to" + self.format(magStr2) + periodPhrase
                elif xMag1 > threshold and xMag2 <= threshold:
print("subsiding waves; setting phrase")
                    periodPhrase = self.embedded_period_phrase(tree, node, periodStats1)
                    wavesWords = dirStr1 + " subsiding from" + self.format(magStr1) + periodPhrase
                elif xMag1 > threshold and xMag2 > threshold:
print("both above thresh; setting words")
                    if dirdiff >= dirthresh and magdiff < magthresh and perdiff < perthresh:
print("step 1")
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)
                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase + " becoming " + dirStr2
                    elif dirdiff >= dirthresh and magdiff >= magthresh and perdiff < perthresh:
print("step 2")
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)
                        #periodPhrase = self.embedded_period_phrase(tree, node, periodStats1)
                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase + " becoming " + dirStr2 + self.format(magStr2)
                        wavesWords = self.checkRepeatingString(tree, node, wavesWords, "wavesWords")
                    elif dirdiff >= dirthresh and magdiff >= magthresh and perdiff >= perthresh:
print("step 3")
                        periodPhrase1 = self.embedded_period_phrase(tree, node, periodStats1)
                        periodPhrase2 = self.embedded_period_phrase(tree, node, periodStats2)
                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase1 + " becoming " + dirStr2 + self.format(magStr2)+\
                                     periodPhrase2
                    elif dirdiff < dirthresh and magdiff >= magthresh and perdiff >= perthresh:
print("step 4")
                        periodPhrase1 = self.embedded_period_phrase(tree, node, periodStats1)
                        periodPhrase2 = self.embedded_period_phrase(tree, node, periodStats2)
                        wavesWords = dirStr1 + self.format(magStr1) +periodPhrase1 + " becoming" + self.format(magStr2)+\
                                     periodPhrase2
                    elif dirdiff < dirthresh and magdiff < magthresh and perdiff >= perthresh:
print("step 5")
                        periodPhrase1 = self.embedded_period_phrase(tree, node, periodStats1)
                        periodPhrase2 = self.embedded_period_phrase(tree, node, periodStats2)
                        wavesWords = dirStr1 + self.format(magStr1) +periodPhrase1 + " becoming" + self.format(magStr2)+\
                                     periodPhrase2
                    elif dirdiff < dirthresh and magdiff < magthresh and perdiff < perthresh:
print("step 6")
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)

                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase
                    else:
print("step 7")
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)

                        wavesWords = dirStr1 +  self.format(magStrA) + periodPhrase

print("SB2 words::::::",wavesWords)

            elif len(statsByRange) == 3:
print(waves)
                wd1, pd1 = statsByRange[0]
                wd2, pd2 = statsByRange[1]
                wd3, pd3 = statsByRange[2]
                wMag1, wDir1 = wd1
                wMag2, wDir2 = wd2
                wMag3, wDir3 = wd3
print("sb3 parts1",wMag1,pd1)
print("sb3 parts2",wMag2,pd2)
print("sb3 parts3",wMag3,pd3)
                for statsByRange[0] in statsByRange:
print("SBR",statsByRange)
print("in sbr[0]", max(wMag1), ",",max(wMag2),",",max(wMag3))
                    if max(wMag1) <= threshold and max(wMag3) > threshold:
print("dropping sbr0 cuz sbr2 above thresh and sbr0 below")
                        wd1, pd1 = statsByRange[1]
                        wd2, pd2 = statsByRange[2]
                    elif self.temporalCoverage_flag == 0:
print("dropping sbr0 cuz temporalCoverage_flag")
                        wd1, pd1 = statsByRange[1]
                        wd2, pd2 = statsByRange[2]
                    elif max(wMag1) > threshold and max(wMag3) > threshold:
                        if max(wMag2) > threshold:
                            if max(wMag3) > max(wMag1):
print("dropping sbr0 cuz all above thresh and sbr2 > sbr0")
                                wd1, pd1 = statsByRange[1]
                                wd2, pd2 = statsByRange[2]
                        else:
print("dropping sbr1 cuz its below thresh and sbr0 & sbr2 above")
                            wd1, pd1 = statsByRange[0]
                            wd2, pd2 = statsByRange[2]

                    elif max(wMag1) > threshold and max(wMag3) <= threshold:
print("dropping sbr2 cuz sbr0 above thresh and sbr2 below")
                        wd1, pd1 = statsByRange[0]
                        wd2, pd2 = statsByRange[1]
print(pd1, "|print(pd1, "|",pd2))|print(pd1, "|print(pd1, "|",pd2))
                    elif self.temporalCoverage_flag == 0:
print("dropping sbr2 cuz temporalCoverage_flag")
                        wd1, pd1 = statsByRange[0]
                        wd2, pd2 = statsByRange[1]
print(pd1, "|print(pd1, "|",pd2))|print(pd1, "|print(pd1, "|",pd2))
                    elif max(wMag1) > threshold and max(wMag3) > threshold:
                        if max(wMag2) > threshold:
                            if max(wMag3) > max(wMag1):
print("dropping sbr0 cuz all above thresh and sbr2 > sbr0")
                                wd1, pd1 = statsByRange[0]
                                wd2, pd2 = statsByRange[2]
                        else:
print("dropping sbr1 cuz its below thresh and sbr0 & sbr2 above")
                            wd1, pd1 = statsByRange[0]
                            wd2, pd2 = statsByRange[1]
                wMag1, wDir1 = wd1
                wMag2, wDir2 = wd2

                xMag1 = max(wMag1)
                xMag2 = max(wMag2)

                mMag1 = min(wMag1)
                mMag2 = min(wMag2)

                if mMag1 == 0.0:
                    mMag1 = xMag1
                if mMag2 == 0.0:
                    mMag2 = xMag2

print("NEW sb3 parts1",wMag1,pd1)
print("NEW sb3 parts2",wMag2,pd2)
                XMag1 = self.average(xMag1, mMag1)
                XMag2 = self.average(xMag2, mMag2)
                XMagA = self.average(xMag1, xMag2)


                magStr1 = self.vector_mag(tree, node, XMag1, XMag1, elementInfo.outUnits, waves)
print("sb3 magStr1",magStr1)
                dirStr1 = self.vector_dir(wDir1)


                magStr2 = self.vector_mag(tree, node, XMag2, XMag2, elementInfo.outUnits, waves)
print("sb3 magStr2",magStr2)
                dirStr2 = self.vector_dir(wDir2)
print("sb3 dirStrs", dirStr1, dirStr2)
                magStrA = self.vector_mag(tree, node, XMagA, XMagA, elementInfo.outUnits, waves)
                mperiodStats1 = tree.stats.get(period, pd1, node.getAreaLabel(), mergeMethod="Min")
                xperiodStats1 = tree.stats.get(period, pd1, node.getAreaLabel(), mergeMethod="Max")
                periodStats1 = tree.stats.get(period, pd1, node.getAreaLabel(), mergeMethod="Average")

                if periodStats1 is None:
                    periodStats1 = 0
                if mperiodStats1 == 0:
                    periodStats1 = xperiodStats1

                mperiodStats2 = tree.stats.get(period, pd2, node.getAreaLabel(), mergeMethod="Min")
                xperiodStats2 = tree.stats.get(period, pd2, node.getAreaLabel(), mergeMethod="Max")
                periodStats2 = tree.stats.get(period, pd2, node.getAreaLabel(), mergeMethod="Average")

                if periodStats2 is None:
                    periodStats2 = 0
                if mperiodStats2 == 0:
                    periodStats2 = xperiodStats2

                if periodStats1 == 0:
                    periodStats1 == periodStats2
                if periodStats2 == 0:
                    periodStats2 == periodStats1

                magdiff = abs(xMag1 - xMag2)
                dirdiff = abs(int(wDir1) - int(wDir2))
                perdiff = abs(periodStats1 - periodStats2)
print("magdiff, dirdiff", magdiff, "|", dirdiff)|print("magdiff, dirdiff", magdiff, "|", dirdiff)
                if xMag1 <= threshold and xMag2 <=threshold:
print("both below thresh; setting to null")
                    wavesWords = ""
                elif xMag1 <= threshold and xMag2 > threshold:
                    periodPhrase = self.embedded_period_phrase(tree, node, periodStats2)
                    wavesWords = dirStr2 + " building to" + self.format(magStr2) + periodPhrase
                elif xMag1 > threshold and xMag2 <= threshold:
print("subsiding waves; setting phrase")
                    periodPhrase = self.embedded_period_phrase(tree, node, periodStats1)
                    wavesWords = dirStr1 +" subsiding from" +  self.format(magStr1) + periodPhrase
                elif xMag1 > threshold and xMag2 > threshold:
print("both above thresh; setting words")
                    if dirdiff >= dirthresh and magdiff < magthresh and perdiff < perthresh:
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)
                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase + " becoming " + dirStr2
                    elif dirdiff >= dirthresh and magdiff >= magthresh and perdiff < perthresh:
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)
                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase + " becoming " + dirStr2 + self.format(magStr2)
                    elif dirdiff >= dirthresh and magdiff >= magthresh and perdiff >= perthresh:
                        periodPhrase1 = self.embedded_period_phrase(tree, node, periodStats1)
                        periodPhrase2 = self.embedded_period_phrase(tree, node, periodStats2)
                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase1 + " becoming " + dirStr2 + self.format(magStr2)+\
                                     periodPhrase2
                    elif dirdiff < dirthresh and magdiff >= magthresh and perdiff >= perthresh:
                        periodPhrase1 = self.embedded_period_phrase(tree, node, periodStats1)
                        periodPhrase2 = self.embedded_period_phrase(tree, node, periodStats2)
                        wavesWords = dirStr1 + self.format(magStr1) +periodPhrase1 + " becoming" + self.format(magStr2)+\
                                     periodPhrase2
                    elif dirdiff < dirthresh and magdiff < magthresh and perdiff >= perthresh:
                        periodPhrase1 = self.embedded_period_phrase(tree, node, periodStats1)
                        periodPhrase2 = self.embedded_period_phrase(tree, node, periodStats2)
                        wavesWords = dirStr1 + self.format(magStr1) +periodPhrase1 + " becoming" + self.format(magStr2)+\
                                     periodPhrase2
                    elif dirdiff < dirthresh and magdiff < magthresh and perdiff < perthresh:
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)
                        wavesWords = dirStr1 + self.format(magStr1) + periodPhrase
                    else:
                        perStats = self.average(periodStats1, periodStats2)
                        periodPhrase = self.embedded_period_phrase(tree, node, perStats)
                        wavesWords = dirStr1 +  self.format(magStrA) + periodPhrase




            ### if there is no wave phrase skip to the next wave grid
            if wavesWords == "null" or not wavesWords:
                continue
            else:
                subPhrases.append(wavesWords)

#print("####### subPhrases:", subPhrases)
        ### check the length of the subPhrase list
        ### return nothing if there are no wave/period sub phrases
        if len(subPhrases) == 0:
            words = "null"

        connector = " and "
        desc =  self.phrase_descriptor(tree, node, "waves", "Wave1")
        phrase = node.getParent()
        phrase.set("descriptor", desc)
        phrase.doneList.append(self.embedDescriptor)

        ### assemble the subPhrases
        i = 0
        words = ""  ### initialize the words variable
        for i in range (len(subPhrases)):
            if (len(subPhrases) - i) == 1:  ### one entry or last entry
                words = words + subPhrases[i]
            elif (len(subPhrases) - i) > 2:  ### 2 or more sub phrases
                words = words + subPhrases[i] + "..."
            else: ### next to last
                words = words + subPhrases[i] + " and "

print("######## final phrase:", words)

        return words


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
            around = self.addSpace(
                self.phrase_descriptor(tree, node, "around", elementName))
            #words =  around + `int(maxMag)` + " " + units
            words =  `int(maxMag)` + " " + units
        else:
            if int(minMag) < threshold:
                upTo = self.addSpace(
                    self.phrase_descriptor(tree, node, "up to", elementName))
                words = upTo + `int(maxMag)` + " " + units
            else:
                valueConnector = self.value_connector(tree, node, elementName, elementName)
                words =  `int(minMag)` + valueConnector + `int(maxMag)` + " " + units

        # This is an additional hook for customizing the magnitude wording
        words = self.vector_mag_hook(tree, node, minMag, maxMag, units, elementName, words)
        return words


###################################################################################################

##############################################################
#  Overrides for UTC vs Local
##############################################################

    def temporalCoverage_percentage(self, parmHisto, timeRange, componentName):
       # This is the percentage of the TIMERANGE covered by the
       #    grid in order to include it in the analysis.  In addition, if a grid
       #    is completely contained within the time range, it will be included.
       # Percentage of temporal coverage default value (if not found in temporalCoverage_dict)
       # Used by temporalCoverage_flag
        return 40

    def temporalCoverage_dict(self, parmHisto, timeRange, componentName):
       # This is the percentage of the TIMERANGE covered by the
       #    grid in order to include it in the analysis. In addition, if a grid
       #    is completely contained within the time range, it will be included.
       # Percentage of temporal coverage by weather element
       # Used by temporalCoverage_flag
        return {
               "LAL": 0,
               "MinRH": 0,
               "MaxRH": 0,
               "MinT": 10,
               "MaxT": 5,
               "Haines": 0,
               "PoP" : 20,
               "Hazards" : 0,
               "Wind" : 25,
               "WindGust" : 25,
               "Wave1" : 35,
               "Wave2" : 35,
               "Wave3" : 35,
               "Wave4" : 35,
               "Wave5" : 35,
               "Wave6" : 35,
               "Wave7" : 35,
               }

   #=================================================================
   #  override TemporalCoverage_flag (from SampleAnalysis) because:
   #    2005-01-27 - When using 3-hourly sub-periods, and a grid
   #                 overlaps by only 1 hour - the old way would
   #                 always include it.  Now, if a grid the overlaps
   #                 the end covers less than the percentage of the
   #                 time period, it is not included unless more than
   #                 percentage of IT is inside the time period.
   #
    def temporalCoverage_flag(self, parmHisto, timeRange, componentName,
                             histSample):

       debug=0
       # Return 1 if the histSample time range sufficiently covers the timeRange
       #   OR the histSample time range is completely included in the timeRange
       # Sub-methods:
       #   temporalCoverage_dict
       #   temporalCoverage_percentage
       #   temporalCoverage_hours
       #   temporalCoverage_hours_dict
       #
       validTime = histSample.validTime()
       compositeNameUI = parmHisto.parmID().compositeNameUI()
       if debug:
print("\n",compositeNameUI," validTime=",validTime," timeRange=",timeRange,"contains=",timeRange.contains_tr(validTime))

       ####################################################################
       # Check #1
       # Is the histSample time range completely included in the timeRange?
       # If yes, then use this grid, with no further checking
       if debug:
print("Check #1-----------------")
       if timeRange.contains_tr(validTime):
           if debug:
print("  Passed!")
           result = 1

       # If we failed check #1, then we need to
       # Look at intersection of histSample and timeRange
       else:

           # Get the covDict and hoursDict for this element
           covDict = self.temporalCoverage_dict(parmHisto, timeRange, componentName)
           if compositeNameUI in covDict.keys():
               percentage = covDict[compositeNameUI]
           else:
               percentage = self.temporalCoverage_percentage(
                   parmHisto, timeRange, componentName)

           hoursDict = self.temporalCoverage_hours_dict(
               parmHisto, timeRange, componentName)
           if compositeNameUI in hoursDict.keys():
               hours = hoursDict[compositeNameUI]
           else:
               hours = self.temporalCoverage_hours(
                   parmHisto, timeRange, componentName)

           # Compute the number of hours of the intersection of the time ranges
           # of the grid (validTime) and the sub-period (timeRange)
           intersect = validTime.intersection(timeRange).duration()

           # get the duration of the sub-period
           fullPeriod=timeRange.duration()

           # now compute the percentage of the period covered by the grid.
           try:
               percentOfPeriod = float(intersect)/fullPeriod * 100.0
           except:
               percentOfPeriod = -1.0

           #  Also compute the percentage of the grid covered by the period.
           gridPeriod=validTime.duration()
           try:
               percentOfGrid=float(intersect)/gridPeriod * 100.0
           except:
               percentOfGrid = -1.0

           #####################################################################
           # Check #2
           # See if the Grid covers XXX% of the sub-period.
           # The intersection should be at least the percentage of the timeRange
           if debug:
print("Check #2------------------")
           # check the percentage against the criteria for this element
           if percentOfPeriod >= percentage:
               if debug:
print("    ",percentOfPeriod," >= ",percentage," so result=1")
               result = 1
           else: # saying no - not enough is inside timeRange"
               if debug:
print("    ",percentOfPeriod," < ",percentage," so result=0")
               result = 0

           ####################################################################
           # Check #3
           #  See if the time period covers 50% or more of the grid.
           #
           #  if grid does not cover enough of the time - but is
           #  a large part of ITs time period - then it should be
           #  considered.  This handles the case of small grids (e.g. 4 hours)
           #  that overlap parts of 2 subperiods.  The overlap might not
           #  be enough to pass Test #2 for either subperiod.  But rather
           #  than ignore this grid entirely, use it in the period that
           #  covers 50% or more of the grid.
           #
           #  An example would be a thunderstorm grid from 4pm-8pm with 6-hour
           #  subperiods.  The 2 hours in each grid might not be enough to
           #  pass Check #2, but it will pass Check #3
           #
           if result == 0:
               if debug:
print("Check #3----------------")
               if percentOfGrid>=50.0:
                   if debug:
print("       percent of Grid >= 50%, so result=1")
                   result=1
               else:
                   if debug:
print("       percent of Grid < 50%, so result=0")
                   result=0

           ############################################################################
           #  Check #4

           #  The last check is to prevent slop over from one full 12-hour period into
           #  either the period before or after it.  This mainly occurs from aligning
           #  grids according to UTC instead of Local Time.  This slop-over can be
           #  2 hours for PST or EDT.  We do this by checking if the
           #  sub-period we're working with is at the beginning or end of a full 12-hour
           #  period (i.e. start or end time of the current sub-period is 6am or 6pm).
           #  In that case, we don't want the grid to slop over if
           #       1. it's not covering 100% of the period.
           #       2. less than 50% of the grid is in this period (i.e. it will get
           #          covered by the previous or next period).
           #       3. it's slopping over from before or after 6 am or 6 pm
           #          (defined by self.DAY and self.NIGHT).
           #       4. it's equal to the amount of slop-over you get when taking the
           #          difference between UTC and the user defined start/end of DAY
           #          and NIGHT.  Assuming a baseline 6am/6pm definition of DAY
           #          and NIGHT, for the timezones you'd get:
           #               EDT, PST, Puerto Rico, AKDT     2 hours
           #               EST, CDT, MST, PDT              1 hour
           #               CST, MDT                        0 hours
           #               AKST                            3 hours
           #               Hawaii                          4 hours
           #
           #  Example:  say you have 3-hrly sub periods for TODAY, and 6-hrly for TONIGHT.
           #            You have a rain grid from 4pm-4pm (00UTC-12UTC).
           #            Check #2 will put it in the LATE AFTERNOON period, because it's more
           #            than 50% of the period.  But this grid is really just intended
           #            for the TONIGHT period so it shouldn't be mentioned in the LATE
           #            AFTERNOON period.
           #
           #  Example:  same as above, but you have thunderstorms from 4pm-7pm.  In
           #            this case, you want to keep the mention of thunder in the LATE
           #            AFTERNOON because the 6-7pm part of the grid won't be enough
           #            to pass Check #2 or #3 from the EVENING period.
           #
           if result == 1:
               if debug:
print("Check #4-------------------")

               #  convert the start and end times of the subperiod to local time and store the hour.
               shift = self.determineShift()
               startTime_LT = timeRange.startTime() + shift
               startHour_LT = startTime_LT.hour()
               endTime_LT = timeRange.endTime() + shift
               endHour_LT = endTime_LT.hour()

               #  compute the expected slop-over for the given timezone and the user definition
               #  of DAY and NIGHT.
               slop_over_morning = int(abs(abs(shift) - (self.DAY() * 3600)))
               slop_over_afternoon = int(abs(abs(shift) - ((self.NIGHT() % 12) * 3600)))

               if (startHour_LT == self.DAY() or startHour_LT == self.NIGHT()):
                   if debug:
print("            ***************This subperiod is at the start of a 12 hour period")
                   if (startHour_LT == self.DAY()):
                       slop_over = slop_over_morning
                   else:
                       slop_over = slop_over_afternoon
                   #  check to see if the current grid extends into the previous
                   #  period (i.e. slopping over from an earlier time period).
                   #  we'll do this by constructing a 1 hour time range that is the
                   #  hour previous to the start of the forecast period.
                   timeCheck = AFPS.TimeRange(timeRange.startTime()-3600, timeRange.startTime())
                   # Now we'll see if that hour intersects the current grid.  If it does,
                   # intersectCheck=3600, if not it's 0.
                   intersectCheck = validTime.intersection(timeCheck).duration()
                   if debug:
                       print "percentOfPeriod ",percentOfPeriod," < 100.0?"
                       print "percentOfGrid   ",percentOfGrid," < 50.0?"
                       print "timeCheck=",timeCheck," intersectCheck=",intersectCheck," > 0?"
                       print "intersect ",intersect," = slop_over ",slop_over," ?"
                   if percentOfPeriod < 100.0 and percentOfGrid < 50.0 and \
                      intersectCheck > 0 and intersect == slop_over:
                       if debug:
print("      Grid is a UTC slop-over and thus will NOT be used")
                       result=0

               if (endHour_LT == self.DAY() or endHour_LT == self.NIGHT()):
                   if debug:
print("            ***************This subperiod is at the end of a 12 hour period")
                   if (endHour_LT == self.DAY()):
                       slop_over = slop_over_morning
                   else:
                       slop_over = slop_over_afternoon
                   #  check to see if the current grid extends into the next
                   #  period (i.e. slopping over from a later time period)
                   #  we'll do this by constructing a 1 hour time range that is the
                   #  hour after the end of the forecast period.
                   timeCheck = AFPS.TimeRange(timeRange.endTime(), timeRange.endTime()+3600)
                   # Now we'll see if that hour intersects the current grid.  If it does,
                   # intersectCheck=3600, if not it's 0.
                   intersectCheck = validTime.intersection(timeCheck).duration()
                   if debug:
                       print "percentOfPeriod ",percentOfPeriod," < 100.0?"
                       print "percentOfGrid   ",percentOfGrid," < 50.0?"
                       print "timeCheck=",timeCheck," intersectCheck=",intersectCheck," > 0?"
                       print "intersect ",intersect," = slop_over ",slop_over," ?"
                   if percentOfPeriod < 100.0 and percentOfGrid < 50.0 and \
                      intersectCheck > 0 and intersect == slop_over:
                       if debug:
print("      Grid is a UTC slop-over and thus will NOT be used")
                       result=0

       return result


    def checkRepeatingString(self, tree, node, str, strName, matchAreaLabels=1):
        # Given a text string, str, and a descriptive name for that string,
        # see if it repeats in the previous phrase, sub-phrase or embedded phrase.
        # If we find a repeating string, return an empty string
        # Otherwise return the original string.
        # If matchAreaLabels, the areaLabel of previous node must match
        # that of the current if we are to return an empty string.
        # This prevents phrases such as:
        #    Chance of rain and snow 20 percent windward rain and snow 40 percent leeward.
        #

        # Check sub-phrases
print("Check Repeating", node.getAncestor('name'), str)
print("   matchAreaLabels", matchAreaLabels)
        prevNode = node.getPrev()
        if prevNode is not None:
            if matchAreaLabels and \
               prevNode.getAreaLabel() != node.getAreaLabel():
                return str
            prevStr = prevNode.get(strName)
print("prevStr", prevStr)
            if prevStr is not None and str == prevStr:
                # Do not repeat previous str
print("return 1")
                return ""
        # Check degenerate conjunctive local effect
        # We are looking for these conditions:
        #  --This phrase has only one sub-phrase
        #  --The previous phrase has only one sub-phrase AND
        #  has the same name as the current phrase (e.g. popMax_phrase
        #  --The str for the sub-phrases are the same
        phrase = node.getParent()
        #tree.printNode(phrase.parent)
        if len(phrase.childList) == 1:
            prevPhrase = phrase.getPrev()
print("prevPhrase", prevPhrase)
            if prevPhrase is not None:
                if matchAreaLabels and \
                   prevPhrase.getAreaLabel() != node.getAreaLabel():
                    return str
                if prevPhrase.get("name") == phrase.get("name"):
                    if len(prevPhrase.childList) == 1:
                        prevSubPhrase = prevPhrase.childList[0]
                        prevStr = prevSubPhrase.get(strName)
                        if prevSubPhrase.get('words') is None:
                            # Must wait for previous words to finish
                            return -1
                        if prevStr is not None and str == prevStr:
                            # Do not repeat previous str
print("return 2")
                            return ""
        elif len(phrase.childList) > 1:
print("length of childList", len(phrase.childList))
            prevPhrase = phrase.getPrev()
            prevSubPhrase = prevPhrase.childList[0]
            prevStr = prevSubPhrase.get(strName)
print("line 1824 prevstr", prevStr)

        return str

    def subPhrase_limit(self, tree, node):
        # If the number of sub-phrases is greater than this limit, the weather
        # phrase will use 6-hour instead of the higher resolution to produce:
        #
        #    OCCASIONAL SNOW POSSIBLY MIXED WITH SLEET AND FREEZING
        #    DRIZZLE IN THE MORNING...THEN A CHANCE OF RAIN POSSIBLY MIXED WITH SNOW
        #    AND SLEET AND FREEZING DRIZZLE IN THE AFTERNOON.
        #
        # instead of:
        #    OCCASIONAL SNOW IN THE MORNING. CHANCE OF LIGHT SLEET AND
        #    SLIGHT CHANCE OF LIGHT FREEZING DRIZZLE IN THE LATE MORNING AND
        #    EARLY AFTERNOON. CHANCE OF SNOW EARLY IN THE AFTERNOON. CHANCE OF
        #    RAIN IN THE AFTERNOON.
        return 12
