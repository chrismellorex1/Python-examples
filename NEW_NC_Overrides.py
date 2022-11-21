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
        #(copy.deepcopy(CWF.TextProduct.VariableList)),
        (("Include Tropical?", "includeTropical"), "No", "radio", ["Yes", "No"]),
        #(("Forecaster Name", "forecasterName") , "99", "radio",
        # ["NELSON","STRIPLING","SCHAUER","CHRISTENSEN",
        #  "LEWITSKY", "AL", "GR", "AGUIRRE", "DGS",
        #  "MUNDELL", "COBB", "LANDSEA", "CAB", "PAW",
        #  "FORMOSA", "HUFFMAN", "MT", "NAR"]),
        #(("Period Combining?","pdCombo"), "No", "radio", ["Yes","No"]),
        ((("Keep Previous Text After Period",
                      "updatePeriodIndex"), "No old text",
                      "radio", ["No old text", "Refresh headlines only",
                                1, 2, 3, 4, 5]))
        ]

    # added below section to enable previous text functionality
    # 05/03/11 CNJ/JL
    # Set descriptive label to use in VariableList
#mergeCwfText="""\
#Generate new text
#for this number of
#periods and use
#previous OFF for
#all later periods.
#
#Selecting zero will
#keep all old text but
#will refresh headers."""
#
#mergeCwfEntry = ((mergeCwfText,'updatePeriodIndex'), "No old text", "radio",
#                             ["No old text", 0,1,2,3,4])
#VariableList.append(mergeCwfEntry)

# NC Definitions:
# Definition statements must start in column 1

### Regional settings of baseline options: ###

#Definition["displayName"] = "OFF_NC"
Definition["productName"] = "OFFSHORE WATERS FORECAST"  # name of product
Definition["areaName"] = ""  # Name of state, such as "GEORGIA"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
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

Definition["purgeTime"] = 12               # Expiration Time

# Define which forecasts have the 5th period and should list "night" in warnings for
# that period.
#NT1 - 3/4pm 9:30/10:30pm
#NT2 - 4/5pm 10/11pm
#PZ5/PZ6 - 2:30/3:30pm 8:30/9:30pm
Definition["issueTimesWith5thPeriod"] = ("230 PM", "300 PM", "330 PM", "400 PM", "500 PM", "830 PM", "930 PM", "1000 PM", "1030 PM", "1100 PM")

# END NC definitions
############################################################

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the above Definition = {} line
# plus following class definition and the __init__ method with only
# the "pass" line in it.

class NEW_NC_Overrides:
    """Class NNN_FILETYPE - Version: IFPS"""

    def __init__(self):
        pass

    def _postProcessProduct(self, fcst, argDict):
        """CWF_ER_Overrides version of CWF._postProcessProduct.

        Modified to add the capability of retaining forecast text from the
        previous CWF.
        """
        self.debug_print("\tCWF_ER_Overrides version of " +
                         "CWF._postProcessProduct")

        fcst = fcst.replace("%expireTime", self._expireTimeStr)
        fcst = fcst.upper()

        self._userInfo = UserInfo.UserInfo()
        forecasterName = self._userInfo._getForecasterName(argDict)

        #  Try to preserve text from previous CWF
        try:

            #  Get the module first
            import mergeProds

            #  See if this is the special case of refreshing the headlines only
            if self._updatePeriodIndex == "Refresh headlines only":

                #  Reset the period index to not include ANY new forecast text
                self._updatePeriodIndex = 0

            #  If this option is desired (i.e. a non zero period was chosen)
            if isinstance(self._updatePeriodIndex, type(1)) and \
                    self._updatePeriodIndex >= 0:

                if self._updatePeriodIndex == 0:
                    print('\tRefreshing headlines only...')
                elif self._updatePeriodIndex == 1:
                    print('\tMerging CWF text for the first period only...')
                else:
                    print('\tMerging CWF text for the first %d periods...' % \
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
            print('Failed to parse previous CWF!  New text will be created ' + \
                  'for all periods.')

        #fcst = fcst + """NNNN   """
        # Remember that the product definition calls marine abbreviations
        ## Corresponding to Forecaster Name at top
        ## added by J. Lewitsky/NHC 02/04/11
        ## found duplicate _postProcessProduct - fixed 05/03/11 CNJ/JL
        #fcst = fcst + "FORECASTER " + self._forecasterName
        fcst += "FORECASTER " + forecasterName
        self.setProgressPercentage(100)
        self.progressMessage(0, 100, self._displayName + " Complete")
        fcst = re.sub(r'  ', " ", fcst)
        fcst = fcst.replace("NATIONAL WEATHER SERVICE", "NWS")
        ## Added the following below to try to eliminate unecessary blanks JL/NHC 02/12/12
        fcst = fcst.replace("FT... BUILDING", "FT...BUILDING")
        fcst = fcst.replace("FT... EXCEPT", "FT...EXCEPT")
        fcst = fcst.replace("KT... BECOMING", "KT...BECOMING")
        fcst = fcst.replace("KT... DIMINISHING", "KT...DIMINISHING")
        fcst = fcst.replace("KT... INCREASING", "KT...INCREASING")
        fcst = fcst.replace("FT... SUBSIDING", "FT...SUBSIDING")
        fcst = fcst.replace("... SEAS", "...SEAS")
        fcst = fcst.replace("KT...SEAS", "KT. SEAS")
        fcst = fcst.replace("N... ", "N...")
        fcst = fcst.replace("!--NOT SENT--!", "")
        fcst = fcst.replace("W... ", "W...")
        fcst = fcst.replace("N... ", "N...")
        fcst = fcst.replace("S... ", "S...")
        fcst = fcst.replace("MIDNIGHT...SEAS", "MIDNIGHT. SEAS")
        fcst = fcst.replace("LESS... ", "LESS...")
        fcst = fcst.replace("E OF 90W E OF 90W", "E OF 90W")
        fcst = fcst.replace("E OF 90W E OF", "")
        fcst = fcst.replace("90W", "E OF 90W")
        fcst = fcst.replace("W OF E OF 90W", "W OF 90W")
        fcst = fcst.replace("E OF E OF 90W", "E OF 90W")
        fcst = fcst.replace("OF 90W E OF 90W", "OF 90W")
        fcst = fcst.replace("OF E OF 90W", "OF 90W")
        fcst = fcst.replace("E OF 96W E OF 96W AND", "E OF 96W...AND")
        fcst = fcst.replace("N OF 24N N OF 24N ", "N OF 24N...")
        fcst = fcst.replace("FT N OF 24N", "FT")
        fcst = fcst.replace(" ...AND S OF 27N", "N OF 27N...AND S OF 27N")
        fcst = fcst.replace("N OF 27N N", "N")
        fcst = fcst.replace("N OF 27N N OF 27N ", "N OF 27N...")
        fcst = fcst.replace("E OF 77W E OF 77W AND", "E OF 77W...AND")
#        fcst = string.replace(fcst, "E OF 77W E OF 77W", "E OF 77W")
        fcst = fcst.replace("E OF 77W E OF", "E OF")
        fcst = fcst.replace("E OF 77W E", "E")
#        fcst = string.replace(fcst, "N OF 10N N OF 10N AND", "N OF 10N...AND")
#        fcst = string.replace(fcst, "E OF 80W E OF 80W AND", "E OF 80W...AND")
#        fcst = string.replace(fcst, "N OF 29N N OF 29N AND", "N OF 29N...AND")
#        fcst = string.replace(fcst, "N OF 25N N OF 25N AND", "N OF 25N...AND")
#        fcst = string.replace(fcst, "W OF 60W W OF 60W AND", "W OF 60W...AND")
        #fcst = string.replace(fcst, "SCATTERED SHOWERS.", "")
        fcst = fcst.replace("SCATTERED SHOWERS AND TSTMS.", "SCATTERED TSTMS.")
        fcst = fcst.replace("SHOWERS AND TSTMS.", "TSTMS.")
        #fcst = string.replace(fcst, "SCATTERED.", "")
        fcst = fcst.replace(". SCATTERED AND", ". SCATTERED")
        fcst = fcst.replace("FOOT", "FT")
        fcst = fcst.replace("0 TO 1 FT", "1 FT OR LESS")
#        fcst = string.replace(fcst, " LATE", "LATE")
        fcst = fcst.replace("AFTER MIDNIGHT", "LATE")
        fcst = fcst.replace("AFTER", "")
        fcst = fcst.replace("MIDNIGHT", "LATE")
        fcst = fcst.replace("IN THE AFTERNOON", "LATE")
        #fcst = string.replace(fcst, "IN THE", "")
        fcst = fcst.replace("NOON", "LATE")
        fcst = fcst.replace("AFTERLATE", "LATE")
        fcst = fcst.replace("THE LATE", "LATE")
        fcst = fcst.replace("KT IN", "KT")
        fcst = fcst.replace("KT  LATE", "KT LATE")
        fcst = fcst.replace("KTLATE", "KT LATE")
        fcst = fcst.replace(" EVENING", "IN THE EVENING")
        fcst = fcst.replace("THIS LATE", "THIS AFTERNOON")
        fcst = fcst.replace("IN LATE.", "LATE.")
        fcst = fcst.replace("IN THE LATE.", "LATE.")
        #fcst = string.replace(fcst, "ANEGADA PASSAGE AND ELSEWHERE...", "...EXCEPT")
        fcst = fcst.replace("IN ...EXCEPT", "")
        fcst = fcst.replace("EXPOSURES... ", "EXPOSURES...")
        fcst = fcst.replace("FEET", "FT...BECOMING ")
        fcst = fcst.replace("IN THE EVENING.", " EVENING.")
        fcst = fcst.replace("VERACRUZ... AND", "VERACRUZ...AND")
        fcst = fcst.replace("CHANNEL... AND", "CHANNEL...AND")
        fcst = fcst.replace("FT  LATE", "FT LATE")
      #  fcst = string.replace(fcst, "  LATE", " LATE")
        fcst = fcst.replace("S OF 25N S OF 25N", "S OF 25N")
        fcst = fcst.replace("S OF 25N S OF 25N...", "S OF 25N...")
        fcst = fcst.replace("N OF 10N N", "N")
        fcst = fcst.replace("N OF 10N N OF 10N", "N OF 10N")
        fcst = fcst.replace("10N N OF 10N", "10N")
        fcst = fcst.replace("ELSEWHERE IN", "ELSEWHERE")
        fcst = fcst.replace("ELSEWHERE IN", "ELSEWHERE")
        fcst = fcst.replace("N OF 10N N OF 10N", "N OF 10N")
        fcst = fcst.replace("W OF 60W W OF 60W", "W OF 60W")
        fcst = fcst.replace("W OF 60W W", "W")
        fcst = fcst.replace("S OF 25N S OF", "S OF")
        fcst = fcst.replace("S OF 25N S", "S")
        fcst = fcst.replace("S OF 29N S OF 29N...", "S OF 29N...")
        fcst = fcst.replace("S OF 29N S OF", "S OF")
        fcst = fcst.replace("S OF 29N S OF 29N", "S OF 29N")
        fcst = fcst.replace("S OF 29N S", "S OF 29N")
        fcst = fcst.replace("OF 29N S OF 29N", "OF 29N")
        fcst = fcst.replace("E OF 80W E OF 80W", "E OF 80W")
        fcst = fcst.replace("E OF 80W E OF", "E OF")
        fcst = fcst.replace("80W E OF 80W", "80W")
        fcst = fcst.replace("E OF 80W E", "E")
        fcst = fcst.replace("FT IN", "FT")
        fcst = fcst.replace("LATE...SEAS", "LATE. SEAS")
        fcst = fcst.replace("IN ...EXCEPTSEAS", "SEAS")
        fcst = fcst.replace("ELSEWHERE... ", "ELSEWHERE...")
        fcst = fcst.replace("E OF 96W E OF 96W", "E OF 96W")
        fcst = fcst.replace("E OF 96W E OF", "E OF")
        fcst = fcst.replace("25N S OF 25N", "25N")
        fcst = fcst.replace("OF 60W W OF 60W", "OF 60W")
        fcst = fcst.replace("N OF 27N N OF", "N OF")
        fcst = fcst.replace("N OF 27N N OF 27N...", "N OF 27N...")
        fcst = fcst.replace("OF 27N N OF 27N", "OF 27N")
        fcst = fcst.replace("E OF 90W E", "E")
##        fcst = string.replace(fcst, "IN THE", "")
        fcst = fcst.replace("FT N", "FT IN N")
        fcst = fcst.replace("FT E", "FT IN E")
        fcst = fcst.replace("FT S", "FT IN S")
        fcst = fcst.replace("FT W", "FT IN W")
        fcst = fcst.replace("FT IN W OF", "FT W OF")
        fcst = fcst.replace("FT E OF", "FT E OF")
        fcst = fcst.replace("FT IN S OF", "FT S OF")
        fcst = fcst.replace("FT IN N OF", "FT N OF")
        fcst = fcst.replace("FT IN WITHIN 60", "FT WITHIN 60")
        fcst = fcst.replace("IN WITHIN 60", "WITHIN 60")
        fcst = fcst.replace("FT IN ELSEWHERE", "FT ELSEWHERE")
        fcst = fcst.replace("IN ELSEWHERE", "ELSEWHERE")
        fcst = fcst.replace("FT... BECOMING", "FT...BECOMING")
        fcst = fcst.replace("SHIFT IN", "SHIFT")
##        fcst = string.replace(fcst, "FT IN WITHIN", " FT WITHIN")
##        fcst = string.replace(fcst, "FT ELSEWHERE", " FT ELSEWHERE")
##        fcst = string.replace(fcst, "FT WITHIN 60", " FT WITHIN 60")
##        fcst = string.replace(fcst, "FT N OF", " FT N OF")
##        fcst = string.replace(fcst, "FT S OF", " FT S OF")
##        fcst = string.replace(fcst, "  FT IN WITHIN", " FT WITHIN")
##        fcst = string.replace(fcst, "  FT ELSEWHERE", " FT ELSEWHERE")
##        fcst = string.replace(fcst, "  FT WITHIN 60", " FT WITHIN 60")
##        fcst = string.replace(fcst, "  FT N OF", " FT N OF")
##        fcst = string.replace(fcst, "  FT S OF", " FT S OF")
        fcst = fcst.replace("IN WITHIN", "WITHIN")
        fcst = fcst.replace("KT THE", "KT")
        fcst = fcst.replace("FT THE", "FT")
        fcst = fcst.replace(" EVENING.", " .")
        fcst = fcst.replace(" AFTERNOON.", " .")
        fcst = fcst.replace(" MORNING.", " .")
        fcst = fcst.replace("THIS .", "TODAY.")
        fcst = fcst.replace(" SE IN", "SE")
        fcst = fcst.replace(" SW IN", "SW")

        #fcst = string.replace(fcst, " S IN", "S")
       # fcst = string.replace(fcst, " S TO S", " S TO SW")
        #fcst = string.replace(fcst, " SW IN", "S")
        fcst = fcst.replace(" W IN", "W")
        fcst = fcst.replace(" NW IN", "NW")
        fcst = fcst.replace(" N IN", "N")
        fcst = fcst.replace(" NE IN", "NE")
        fcst = fcst.replace(" E IN", "E")
        fcst = fcst.replace("CLUDING", " INCLUDING")
        fcst = fcst.replace("IN INCLUDING", "INCLUDING")
        fcst = fcst.replace("CREASES", " INCREASES")
        fcst = fcst.replace("KT .", "KT.")
        fcst = fcst.replace(" IN EFFECT", "")
        fcst = fcst.replace("TONW THE", "TO NW ")
        fcst = fcst.replace("TON THE", "TO N ")
        fcst = fcst.replace("TONE THE", "TO NE ")
        fcst = fcst.replace("TOE THE", "TO E ")
        fcst = fcst.replace("TOSE THE", "TO SE ")
        fcst = fcst.replace("TOS THE", "TO S ")
        fcst = fcst.replace("TOSW THE", "TO SW ")
        fcst = fcst.replace("TOW THE", "TO W ")
        fcst = fcst.replace("FT IN E OF", "FT E OF")
        fcst = fcst.replace("HAZE. VSBY ", "HAZE WITH VSBY ")
        fcst = fcst.replace("FOG. VSBY ", "FOG WITH VSBY ")
        fcst = fcst.replace("SMOKE. VSBY ", "SMOKE WITH VSBY ")
        fcst = fcst.replace("VOLCANIC ASH. VSBY ", "VOLCANIC ASH WITH VSBY ")
        fcst = fcst.replace("TONW", "TO NW")
        fcst = fcst.replace("TOW", "TO W")
        fcst = fcst.replace("LATE...SEAS", "LATE. SEAS")
        fcst = fcst.replace("N OF 10N ...", "N OF 10N...")
        fcst = fcst.replace("BECOMINGSE THE", "BECOMING SE")
        fcst = fcst.replace("TOSE", "TO SE")
        fcst = fcst.replace("W OF E OF 90W", "E OF 90W")
        fcst = fcst.replace("FT IN W OF 90W", "FT W OF 90W")
        fcst = fcst.replace("NE TOE", "NE TO E")
        fcst = fcst.replace("FT IN N OF", "FT N OF")
        fcst = fcst.replace("BECOMINGN", "BECOMING N")
        fcst = fcst.replace("BECOMINGSE", "BECOMING SE")
        fcst = fcst.replace("BECOMINGS", "BECOMING S")
        fcst = fcst.replace("BECOMINGE", "BECOMING E")
        fcst = fcst.replace("BECOMINGW", "BECOMING W")
        fcst = fcst.replace("BECOMINGNW", "BECOMING NW")
        fcst = fcst.replace("BECOMINGNE", "BECOMING NE")
        fcst = fcst.replace("BECOMINGSW", "BECOMING SW")
        fcst = fcst.replace("BECOMING W THE", "BECOMING W")
        fcst = fcst.replace("THE LATE", "LATE")
        fcst = fcst.replace("BECOMING S TOS", "BECOMING S TO SW")
        fcst = fcst.replace("THISIN THE EVENING", "THIS EVENING")
        fcst = fcst.replace("KT... SHIFTING", "KT...SHIFTING")
        fcst = fcst.replace("TONE", "TO NE")
        fcst = fcst.replace("FT IN N", "FT N")
        fcst = fcst.replace("FT... BUILDING", "FT...BUILDING")
        fcst = fcst.replace("FT .", "FT.")
        fcst = fcst.replace("LATE...", "LATE.")
        fcst = fcst.replace("N IN THE", "N")
        fcst = fcst.replace("NE IN THE", "NE")
        fcst = fcst.replace("E IN THE", "E")
        fcst = fcst.replace("SE IN THE", "SE")
        fcst = fcst.replace("S IN THE", "S")
        fcst = fcst.replace("SW IN THE", "SW")
        fcst = fcst.replace("W IN THE", "W")
        fcst = fcst.replace("NW IN THE", "NW")
        fcst = fcst.replace("29N S OF 29N", "29N")
        fcst = fcst.replace("FT IN E", "FT E")
        fcst = fcst.replace("FT IN W", "FT W")
        fcst = fcst.replace("FT IN S", "FT S")
        fcst = fcst.replace("FT IN N", "FT N")
        fcst = fcst.replace("LESS...BECOMING", "LESS...BUILDING TO")
        fcst = fcst.replace("FT...BECOMING", "FT...SUBSIDING TO")
        fcst = fcst.replace("TOSW", "TO SW")
        #fcst = string.replace(fcst, "AND...CORRECTED", "AND CARIBBEAN SEA...CORRECTED")
        return fcst
