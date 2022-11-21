import string
import time
import re
import os
import types
import copy

import TextRules
import SampleAnalysis
import mergeProds



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
        (("Forecaster Name", "forecasterName"), "99", "radio",
         ["WALLY BARNES", "NELSON", "STRIPLING", "SCHAUER", "CHRISTENSEN",
          "LEWITSKY", "AL", "GR", "AGUIRRE", "DGS",
          "MUNDELL", "COBB", "LANDSEA", "CAB", "PAW",
          "FORMOSA", "HUFFMAN", "MT", "NAR"]),
        (("Period Combining?", "pdCombo"), "No", "radio", ["Yes", "No"]),
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

class OFF_LAN2_Overrides:
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
        fcst += "FORECASTER " + self._forecasterName
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
        #fcst = string.replace(fcst, "ANEGADA PASSAGE AND ELSEWHERE...", "...EXCEPT")
        fcst = fcst.replace("IN ...EXCEPT", "")
        fcst = fcst.replace("EXPOSURES... ", "EXPOSURES...")
        fcst = fcst.replace("FEET", "FT...BECOMING ")
        fcst = fcst.replace("IN THE EVENING.", " EVENING.")
        fcst = fcst.replace("VERACRUZ... AND", "VERACRUZ...AND")
        fcst = fcst.replace("CHANNEL... AND", "CHANNEL...AND")
        fcst = fcst.replace("FT  LATE", "FT LATE")
        fcst = fcst.replace("  LATE", " LATE")
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
        fcst = fcst.replace(" S IN", "S")
        fcst = fcst.replace(" SW IN", "S")
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
        ######################
        ######
        ####
        ### FRENCH OVERRIDES

#         fcst = re.sub(r'EARLY\sIN\sTHE\sEVENING',r'EN DEBUT DE PERIODE',fcst)
#         fcst = re.sub(r'EARLY\sIN\sTHE\sAFTERNOON',r'EN DEBUT DE PERIODE',fcst)
#         fcst = re.sub(r'EARLY\sIN\sTHE\sMORNING',r'EN DEBUT DE PERIODE',fcst)
#         fcst = re.sub(r'LATE\sIN\sTHE\sEVENING',r'EN FIN DE PERIODE',fcst)
#         fcst = re.sub(r'LATE\sIN\sTHE\sAFTERNOON',r'EN FIN DE PERIODE',fcst)
#         fcst = re.sub(r'LATE\sIN\sTHE\sMORNING',r'EN FIN DE PERIODE',fcst)
#
#         fcst = re.sub(r'VARIABLE\sWINDS\s',r'VENTS DE BEAUCOUP DE DIRECTIONS ',fcst)
#
#
#
#
#         fcst = re.sub(" FT", " PIEDS" ,fcst)
#         fcst = re.sub("TODAY", "AUJOURD'HUI" ,fcst)
#         fcst = re.sub("TONIGHT", "POUR LA NUIT" ,fcst)
#         fcst = re.sub("UNTIL","PRESQUE",fcst)
#
#
#         fcst = re.sub("KT", "NOEUDS" ,fcst)
#
#         fcst = re.sub("BECOMING", "VIRANT", fcst)
#
#
#
#
#
#
#         fcst = re.sub("SEAS","MER DE",fcst)
#
#         fcst = re.sub("N TO NE WINDS","VENTS DE NORD A NORD-EST",fcst)
#         fcst = re.sub("NE TO E WINDS","VENTS DE NORD-EST A EST",fcst)
#         fcst = re.sub("E TO SE WINDS","VENTS DE EST A SUD-EST",fcst)
#         fcst = re.sub("SE TO S WINDS","VENTS DE SUD-EST A SUD",fcst)
#         fcst = re.sub("S TO SW WINDS","VENTS DE SUD A SUD-OUEST",fcst)
#         fcst = re.sub("SW TO W WINDS","VENTS DE SUD-OUEST A OUEST",fcst)
#         fcst = re.sub("W TO NW WINDS","VENTS DE OUEST A NORD-OUEST",fcst)
#         fcst = re.sub("NW TO N WINDS","VENTS DE NORD-OUEST A NORD",fcst)
#
#         fcst = re.sub("...N WINDS","...VENTS DE NORD",fcst)
#         fcst = re.sub("...NE WINDS","...VENTS DE NORD-EST",fcst)
#         fcst = re.sub("...E WINDS","...VENTS DE EST",fcst)
#         fcst = re.sub("...SE WINDS","...VENTS DE SUD-EST",fcst)
#         fcst = re.sub("...S WINDS","...VENTS DE SUD",fcst)
#         fcst = re.sub("...SW WINDS","...VENTS DE SUD-OUEST",fcst)
#         fcst = re.sub("...W WINDS","...VENTS DE OUEST",fcst)
#         fcst = re.sub("...NW WINDS","...VENTS DE NORD-OUEST",fcst)
#
#
#
#
#
#         fcst = re.sub("VIRANT N TO NE","VIRANT NORD A NORD-EST",fcst)
#         fcst = re.sub("VIRANT NE TO E","VIRANT NORD-EST A EST",fcst)
#         fcst = re.sub("VIRANT E TO SE","VIRANT EST A SUD-EST",fcst)
#         fcst = re.sub("VIRANT SE TO S","VIRANT SUD-EST A SUD",fcst)
#         fcst = re.sub("VIRANT S TO SW","VIRANT SUD A SUD-OUEST",fcst)
#         fcst = re.sub("VIRANT SW TO W","VIRANT SUD-OUEST A OUEST",fcst)
#         fcst = re.sub("VIRANT W TO NW","VIRANT OUEST A NORD-OUEST",fcst)
#         fcst = re.sub("VIRANT NW TO N","VIRANT NORD-OUEST A NORD",fcst)
#
#         fcst = re.sub("VIRANT N","VIRANT NORD",fcst)
#         fcst = re.sub("VIRANT NE","VIRANT NORD-EST",fcst)
#         fcst = re.sub("VIRANT E","VIRANT EST",fcst)
#         fcst = re.sub("VIRANT SE","VIRANT SUD-EST",fcst)
#         fcst = re.sub("VIRANT S","VIRANT SUD",fcst)
#         fcst = re.sub("VIRANT SW","VIRANT SUD-OUEST",fcst)
#         fcst = re.sub("VIRANT W","VIRANT OUEST",fcst)
#         fcst = re.sub("VIRANT NW","VIRANT NORD-EST",fcst)
#         fcst = re.sub("THROUGH THE DAY","PENDANT LE JOUR",fcst)
#
#         fcst = re.sub("\sN\s"," NORD ",fcst)
#         fcst = re.sub("\sNE\s"," NORD-EST ",fcst)
#         fcst = re.sub("\sE\s"," EST ",fcst)
#         fcst = re.sub("\sSE\s"," SUD-EST ",fcst)
#         fcst = re.sub("\sS\s"," SUD ",fcst)
#         fcst = re.sub("\sSW\s"," SUD-OUEST ",fcst)
#         fcst = re.sub("\sW\s"," OUEST ",fcst)
#         fcst = re.sub("\sNW\s"," NORD-OUEST ",fcst)
#
#
#
#
#         fcst = re.sub(".SUN NIGHT...", ".DIM POUR LA NUIT..." ,fcst)
#         fcst = re.sub(".MON NIGHT...", ".LUN POUR LA NUIT..." ,fcst)
#         fcst = re.sub(".TUE NIGHT...", ".MAR POUR LA NUIT..." ,fcst)
#         fcst = re.sub(".WED NIGHT...", ".MER POUR LA NUIT..." ,fcst)
#         fcst = re.sub(".THU NIGHT...", ".JEU POUR LA NUIT..." ,fcst)
#         fcst = re.sub(".FRI NIGHT...", ".VEN POUR LA NUIT..." ,fcst)
#         fcst = re.sub(".SAT NIGHT...", ".SAM POUR LA NUIT..." ,fcst)
#
#         fcst = re.sub("SUN", "DIM" ,fcst)
#         fcst = re.sub("MON", "LUN" ,fcst)
#         fcst = re.sub("TUE", "MAR" ,fcst)
#         fcst = re.sub("WED", "MER" ,fcst)
#         fcst = re.sub("THU", "JEU" ,fcst)
#         fcst = re.sub("FRI", "VEN" ,fcst)
#         fcst = re.sub("SAT", "SAM" ,fcst)
#
#
#
# #        fcst = re.sub("TUE MAY", "MAR MAY" ,fcst)
# #        fcst = re.sub("MON MAY 25", "LUN 25 DE MAYO", fcst)
# #        fcst = re.sub("TUE MAY 26", "MAR 26 DE MAYO", fcst)
# #        fcst = re.sub("WED MAY 27", "MIE 27 DE MAYO", fcst)
# #        fcst = re.sub("THU MAY 28", "JUE 28 DE MAYO", fcst)
# #        fcst = re.sub("FRI MAY 29", "VIE 25 DE MAYO", fcst)
# #        fcst = re.sub("SAT MAY 30", "SAB 25 DE MAYO", fcst)
# #        fcst = re.sub("SUN MAY 31", "DOM 25 DE MAYO", fcst)
# #        fcst = re.sub("MON JUN 01", "LUN 01 DE JUNIO", fcst)
# #        fcst = re.sub("TUE JUN 02", "MAR 02 DE JUNIO", fcst)
# #        fcst = re.sub("WED JUN 03", "MIE 03 DE JUNIO", fcst)
# #        fcst = re.sub("THU JUN 04", "JUE 04 DE JUNIO", fcst)
# #        fcst = re.sub("FRI JUN 05", "VIE 05 DE JUNIO", fcst)
# #        fcst = re.sub("SAT JUN 06", "SAB 06 DE JUNIO", fcst)
# #        fcst = re.sub("SUN JUN 07", "DOM 07 DE JUNIO", fcst)
# #        fcst = re.sub("MON JUN 08", "LUN 08 DE JUNIO", fcst)
# #        fcst = re.sub("TUE JUN 09", "MAR 09 DE JUNIO", fcst)
# #        fcst = re.sub("WED JUN 10", "MIE 10 DE JUNIO", fcst)
# #        fcst = re.sub("THU JUN 11", "JUE 11 DE JUNIO", fcst)
# #        fcst = re.sub("FRI JUN 12", "VIE 12 DE JUNIO", fcst)
# #        fcst = re.sub("SAT JUN 13", "SAB 13 DE JUNIO", fcst)
# #        fcst = re.sub("SUN JUN 14", "DOM 14 DE JUNIO", fcst)
# #        fcst = re.sub("MON JUN 15", "LUN 15 DE JUNIO", fcst)
#
#
# #        fcst = re.sub("SUN", "DOM" ,fcst)
# #        fcst = re.sub("MON", "LUN" ,fcst)
# #        fcst = re.sub("TUE ", "MAR" ,fcst)
# #        fcst = re.sub("WED ", "MIE" ,fcst)
# #        fcst = re.sub("THU ", "JUE" ,fcst)
# #        fcst = re.sub("FRI ", "VIE" ,fcst)
# #        fcst = re.sub("SAT ", "SAB" ,fcst)
# #        fcst = re.sub("SUN ", "DOM" ,fcst)
#
# #        fcst = re.sub("JAN", "ENE" ,fcst)
# #        fcst = re.sub("FEB", "FEB" ,fcst)
# #        fcst = re.sub("MAR", "MAR" ,fcst)
# #        fcst = re.sub("APR", "ABR" ,fcst)
# #        fcst = re.sub("MAY", "MAY" ,fcst)
# #        fcst = re.sub("JUN", "JUN" ,fcst)
# #        fcst = re.sub("JUL", "JUL" ,fcst)
# #        fcst = re.sub("AUG", "SEP" ,fcst)
# #        fcst = re.sub("OCT", "OCT" ,fcst)
# #        fcst = re.sub("NOV", "NOV",fcst)
# #        fcst = re.sub("DEC", "DIC" ,fcst)
#
#
#         fcst = re.sub("SUN MAY", "DIM MAI" ,fcst)
#         fcst = re.sub("MON MAY", "LUN MAI" ,fcst)
#         fcst = re.sub("TUE MAY", "MAR MAI" ,fcst)
#         fcst = re.sub("WED MAY", "MER MAI" ,fcst)
#         fcst = re.sub("THU MAY", "JEU MAI" ,fcst)
#         fcst = re.sub("FRI MAY", "VEN MAI" ,fcst)
#         fcst = re.sub("SAT MAY", "SAM MAI" ,fcst)
#
#         fcst = re.sub("SUN JUN", "DIM JUN" ,fcst)
#         fcst = re.sub("MON JUN", "LUN JUN" ,fcst)
#         fcst = re.sub("TUE JUN", "MAR JUN" ,fcst)
#         fcst = re.sub("WED JUN", "MER JUN" ,fcst)
#         fcst = re.sub("THU JUN", "JEU JUN" ,fcst)
#         fcst = re.sub("FRI JUN", "VEN JUN" ,fcst)
#         fcst = re.sub("SAT JUN", "SAM JUN" ,fcst)
#
#         fcst = re.sub("SUN JUL", "DIM JUL" ,fcst)
#         fcst = re.sub("MON JUL", "LUN JUL" ,fcst)
#         fcst = re.sub("TUE JUL", "MAR JUL" ,fcst)
#         fcst = re.sub("WED JUL", "MER JUL" ,fcst)
#         fcst = re.sub("THU JUL", "JEU JUL" ,fcst)
#         fcst = re.sub("FRI JUL", "VEN JUL" ,fcst)
#         fcst = re.sub("SAT JUL", "SAM JUL" ,fcst)
#
#         fcst = re.sub("SUN AUG", "DIM AOU" ,fcst)
#         fcst = re.sub("MON AUG", "LUN AOU" ,fcst)
#         fcst = re.sub("TUE AUG", "MAR AOU" ,fcst)
#         fcst = re.sub("WED AUG", "MER AOU" ,fcst)
#         fcst = re.sub("THU AUG", "JEU AOU" ,fcst)
#         fcst = re.sub("FRI AUG", "VEN AOU" ,fcst)
#         fcst = re.sub("SAT AUG", "SAM AOU" ,fcst)
#
#         fcst = re.sub("SUN SEP", "DIM SEP" ,fcst)
#         fcst = re.sub("MON SEP", "LUN SEP" ,fcst)
#         fcst = re.sub("TUE SEP", "MAR SEP" ,fcst)
#         fcst = re.sub("WED SEP", "MER SEP" ,fcst)
#         fcst = re.sub("THU SEP", "JEU SEP" ,fcst)
#         fcst = re.sub("FRI SEP", "VEN SEP" ,fcst)
#         fcst = re.sub("SAT SEP", "SAM SEP" ,fcst)
#
#         fcst = re.sub("SUN OCT", "DIM OCT" ,fcst)
#         fcst = re.sub("MON OCT", "LUN OCT" ,fcst)
#         fcst = re.sub("TUE OCT", "MAR OCT" ,fcst)
#         fcst = re.sub("WED OCT", "MER OCT" ,fcst)
#         fcst = re.sub("THU OCT", "JEU OCT" ,fcst)
#         fcst = re.sub("FRI OCT", "VEN OCT" ,fcst)
#         fcst = re.sub("SAT OCT", "SAM OCT" ,fcst)
#
#         fcst = re.sub("SUN NOV", "DIM NOV" ,fcst)
#         fcst = re.sub("MON NOV", "LUN NOV" ,fcst)
#         fcst = re.sub("TUE NOV", "MAR NOV" ,fcst)
#         fcst = re.sub("WED NOV", "MER NOV" ,fcst)
#         fcst = re.sub("THU NOV", "JEU NOV" ,fcst)
#         fcst = re.sub("FRI NOV", "VEN NOV" ,fcst)
#         fcst = re.sub("SAT NOV", "SAM NOV" ,fcst)
#
#         fcst = re.sub("SUN DEC", "DIM DEC" ,fcst)
#         fcst = re.sub("MON DEC", "LUN DEC" ,fcst)
#         fcst = re.sub("TUE DEC", "MAR DEC" ,fcst)
#         fcst = re.sub("WED DEC", "MER DEC" ,fcst)
#         fcst = re.sub("THU DEC", "JEU DEC" ,fcst)
#         fcst = re.sub("FRI DEC", "VEN DEC" ,fcst)
#         fcst = re.sub("SAT DEC", "SAM DEC" ,fcst)
#
#         fcst = re.sub("SUN JAN", "DIM JAN" ,fcst)
#         fcst = re.sub("MON JAN", "LUN JAN" ,fcst)
#         fcst = re.sub("TUE JAN", "MAR JAN" ,fcst)
#         fcst = re.sub("WED JAN", "MER JAN" ,fcst)
#         fcst = re.sub("THU JAN", "JEU JAN" ,fcst)
#         fcst = re.sub("FRI JAN", "VEN JAN" ,fcst)
#         fcst = re.sub("SAT JAN", "SAM JAN" ,fcst)
#
#         fcst = re.sub("SUN FEB", "DIM FEV" ,fcst)
#         fcst = re.sub("MON FEB", "LUN FEB" ,fcst)
#         fcst = re.sub("TUE FEB", "MAR FEV" ,fcst)
#         fcst = re.sub("WED FEB", "MER FEV" ,fcst)
#         fcst = re.sub("THU FEB", "JEU FEV" ,fcst)
#         fcst = re.sub("FRI FEB", "VEN FEV" ,fcst)
#         fcst = re.sub("SAT FEB", "SAM FEV" ,fcst)
#
#         fcst = re.sub("SUN MAR", "DIM MAR" ,fcst)
#         fcst = re.sub("MON MAR", "LUN MAR" ,fcst)
#         fcst = re.sub("TUE MAR", "MAR MAR" ,fcst)
#         fcst = re.sub("WED MAR", "MER MAR" ,fcst)
#         fcst = re.sub("THU MAR", "JEU MAR" ,fcst)
#         fcst = re.sub("FRI MAR", "VEN MAR" ,fcst)
#         fcst = re.sub("SAT MAR", "SAM MAR" ,fcst)
#
#         fcst = re.sub("SUN APR", "DIM AVR" ,fcst)
#         fcst = re.sub("MON APR", "LUN AVR" ,fcst)
#         fcst = re.sub("TUE APR", "MAR AVR" ,fcst)
#         fcst = re.sub("WED APR", "MER AVR" ,fcst)
#         fcst = re.sub("THU APR", "JEU AVR" ,fcst)
#         fcst = re.sub("FRI APR", "VEN AVR" ,fcst)
#         fcst = re.sub("SAT APR", "SAM AVR" ,fcst)
#
#         fcst = re.sub("DOM NOCHE", "DOM POR LA NOCHE" ,fcst)
#         fcst = re.sub("LUN NOCHE", "LUN POR LA NOCHE" ,fcst)
#         fcst = re.sub("MAR NOCHE", "MAR POR LA NOCHE" ,fcst)
#         fcst = re.sub("MIE NOCHE", "MIE POR LA NOCHE" ,fcst)
#         fcst = re.sub("JUE NOCHE", "JUE POR LA NOCHE" ,fcst)
#         fcst = re.sub("VIE NOCHE", "VIE POR LA NOCHE" ,fcst)
#         fcst = re.sub("SAB NOCHE", "SAB POR LA NOCHE" ,fcst)
#
#
#  #       fcst = re.sub("JAN", "ENE" ,fcst)
#  #       fcst = re.sub("FEB", "FEB" ,fcst)
#  #       fcst = re.sub("MAR", "MAR" ,fcst)
#  #       fcst = re.sub("APR", "ABR" ,fcst)
#  #       fcst = re.sub("MAY", "MAY" ,fcst)
#  #       fcst = re.sub("JUN", "JUN" ,fcst)
#  #       fcst = re.sub("JUL", "JUL" ,fcst)
#  #       fcst = re.sub("AUG", "SEP" ,fcst)
#  #       fcst = re.sub("OCT", "OCT" ,fcst)
#  #       fcst = re.sub("NOV", "NOV", fcst)
#  #       fcst = re.sub("DEC", "DIC" ,fcst)
#  #       fcst = re.sub("...CHE", " NOCHE" ,fcst)
#
# #        fcst = re.sub(".DOM...Y", " DOM MAY" ,fcst)
#
#
#
#
# #        fcst = re.sub(".DOM.", " DOM " ,fcst)
# #        fcst = re.sub(".LUN.", " LUN " ,fcst)
# #        fcst = re.sub(".MAR.", " MAR " ,fcst)
# #        fcst = re.sub(".MIE.", " MIE " ,fcst)
# #        fcst = re.sub(".JUE.", " JUE " ,fcst)
# #        fcst = re.sub(".VIE.", " VIE " ,fcst)
# #        fcst = re.sub(".SAB.", " SAB " ,fcst)
#
#         fcst = re.sub("MORNING","MATIN",fcst)
#         fcst = re.sub("AFTERNOON","L'APRES MIDI",fcst)
#         fcst = re.sub("EVENING","SOIR",fcst)
#
#         fcst = re.sub("LESS THAN","INFERIORES A",fcst)
#
#
#
#         fcst = re.sub("TSTMS","AVERSES",fcst)
#         fcst = re.sub("FOG","NIEBLA",fcst)
#         fcst = re.sub("SMOKE","FUME",fcst)
#         fcst = re.sub("SAHARAN DUST","POLVO DEL SAHARA",fcst)
#
#         fcst = re.sub("THEN","PUIS",fcst)
#         fcst = re.sub("OR LESS","O MENOS",fcst)
#
#         fcst = re.sub("THEN","PUIS",fcst)
#         fcst = re.sub("LATE","TARD",fcst)
#         fcst = re.sub("BUILDING","AUMENTANDO",fcst)
#         fcst = re.sub("SUBSIDING","DISMINUYENDO",fcst)
#         fcst = re.sub("OVERNIGHT","PENDANT LA NUIT",fcst)
#
#         fcst = re.sub("TO ","A ",fcst)
#         fcst = re.sub("AND","ET",fcst)
#
#         fcst = re.sub("AFTER MIDNIGHT","APRES MINUIT",fcst)
#         fcst = re.sub("NIGHT", "NOIR" ,fcst)
#         fcst = re.sub("SUDUD", "SUD" ,fcst)
#
#
#
#
#         fcst = re.sub(" THROUGH"," PENDANT",fcst)
# #        fcst = re.sub(" THE"," EL",fcst)
#         fcst = re.sub(" DAY"," JOUR",fcst)
#         fcst = re.sub(" IN "," EN",fcst)
#         fcst = re.sub("EN LA","LA",fcst)
#         fcst = re.sub("AFTER","APRES",fcst)
#         fcst = re.sub("MIDNIGHT","MINUIT",fcst)
#         fcst = re.sub("TEMPRANO ENTHE TEMPRANO EN LA NOCHE", "TEMPRANO EN LA NOCHE", fcst)
#         fcst = re.sub("TORNYOSE","TORNANDOSE",fcst)
#         fcst = re.sub("WIDESPREAD","AREAS EXTENSIVE DE", fcst)
#         fcst = re.sub("ISOLATED","AREAS ISOLEE DE", fcst)
#         fcst = re.sub("RAIN","PLUIE", fcst)
#         fcst = re.sub("TARDE DE LA TARDE","AL FINAL DE LA TARDE", fcst)
#         fcst = re.sub("IN THE TARDE", "EN LA TARDE", fcst)
#         fcst = re.sub("LATE IN THE LA TARDE","AL FINAL DE LA TARDE", fcst)
#         fcst = re.sub("LATE IN THE EVENING AND OVERNIGHT","EN LA NOCHE Y LA MADRUGADA", fcst)
#         fcst = re.sub("IN THE LATE LA MANANA","EN AL FINAL DE LA MANANA", fcst)
#         fcst = re.sub("IN THE LATE MORNING","EN AL FINAL DE LA MANANA", fcst)
#         fcst = re.sub("ENTHE", "EN", fcst)
#         fcst = re.sub("0 A 2 PIEDS","2 PIES OU MOINS", fcst)
#         fcst = re.sub(" OR"," OU", fcst)
#         fcst = re.sub("LESS","MOINS",fcst)
#         fcst = re.sub("INFERIORES","MOINS",fcst)
#         fcst = re.sub("CENTRAL","CENTRALE",fcst)
        return fcst
