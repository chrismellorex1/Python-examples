#
#
# SWELL_NT4_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the 
#  OFF formatter for a site. 
#
# History
# 8/5/2015 - recreated file (CNJ/JL)
# ---------------------------------------------------------------------

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum content of this file is the following Definition statement

Definition = {}

# End MAKE NO CHANGES HERE
#**********************************************************************
#####################################################
# Override VariableList if desired
#
#VariableList = []

#----- WFO ONA OFF Definition -----
# Definition Statements must start in column 1.
# REQUIRED CONFIGURATION ITEMS 
#Definition['displayName'] = None
Definition['displayName'] = "SWELL_NT4"

Definition["showZoneCombiner"] = 0 # 1 to cause zone combiner to display
#Definition["defaultEditAreas"] = "Combinations_OFF_ONA_NT1"
# Definition["defaultEditAreas"] = [
#     ('GMZ011', "NW GULF INCLUDING STETSON BANK"),
#     ('GMZ013', "N CENTRAL GULF INCLUDING FLOWER GARDEN BANKS MARINE SANCTUARY"),
#     ('GMZ015', "NE GULF N OF 25N E OF 87W"),
#     ('GMZ017', "W CENTRAL GULF FROM 22N TO 26N W OF 94W"),
#     ('GMZ019', "CENTRAL GULF FROM 22N TO 26N BETWEEN 87W AND 94W"),
#     ('GMZ021', "E GULF FROM 22N TO 25N E OF 87W INCLUDING STRAITS OF FLORIDA"),
#     ('GMZ023', "SW GULF S OF 22N W OF 94W"),
#     ('GMZ025', "E BAY OF CAMPECHE INCLUDING CAMPECHE BANK"),
#             ]

Definition["defaultEditAreas"] = [
    ('GMZ040', "NW Gulf including Stetson Bank"),
    ('GMZ041', "SW Louisiana Offshore Waters including Flower Garden Banks Marine Sanctuary"),
    ('GMZ056', "N Central Gulf N of 26N between 87W and 91W"),
    ('GMZ057', "NE Gulf N of 26N E of 87W"),
    ('GMZ058', "W Central Gulf from 22N to 26N W of 94W"),
    ('GMZ045', "W Central Gulf from 22N to 26N between 91W and 94W"),
    ('GMZ046', "Central Gulf from 22Nto 26N between 87W and 91W"),
    ('GMZ047', "E Gulf from 22N to 26N E of 87W  Including Straits of Florida"),
    ('GMZ048', "SW Gulf S of 22N W of 94W"),
    ('GMZ049', "Central Bay of Campeche S of 22N between 92W and 94W"),
    ('GMZ050', "E Bay of Campeche S of 22N between 87W and 92W"),
            ]

Definition["mapNameForCombinations"] = "Offshore_Marine_Zones" # Map background for creating Combinations

# Header configuration items
Definition["productName"] = "Offshore Waters Forecast"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "FZNT24"        # WMO ID
Definition["pil"] = "OFFNT4"          # product pil
Definition["areaName"] = "the Gulf of Mexico"  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "National Hurricane Center Miami, FL"  # Location of WFO - city st
Definition["textdbPil"] = "MIAOFFNT4"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCOFFNT4"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/OFFNT4.txt"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
#Definition["editAreaSuffix"] = "_pt"

#Definition["lineLength"] = 65   #Product line length
Definition["hazardSamplingThreshold"] = (0, 1)  #(%cov, #points)

Definition["periodCombining"] = 1     # If 1, do period combining
Definition["includeEveningPeriod"] = 0  # If 1, include Evening Period
Definition["useAbbreviations"] = 1      # If 1, use marine abbreviations

# Weather-related flags
#Definition["hoursSChcEnds"] = 24

#Definition["areaDictionary"] = "AreaDictionary"     # For product headers
Definition["language"] = "english"
#Definition["useHolidays"] = 1

# Trouble-shooting items
#Definition["passLimit"] = 20             # Limit on passes allowed through Narrative Tree
#Definition["trace"] = 1                  # Set to 1 to turn on trace through
                                         # Narrative Tree for trouble-shootin


# Required for BASE OFF!
#  synopsisUGC      UGC code for Synopsis
Definition["synopsisUGC"] = "GMZ001"    # UGC code for synopsis
Definition["synopsisHeading"] = ".SYNOPSIS..."# Heading for synopsis

# Settings to insert text from previous Product.
Definition["prevProdPIL"] = "MIAOFFNT4"
Definition["updatePeriodIndex"] = 0
Definition["includeCombine"] = 0

Definition["lowerCase"] = 1 #added this to test mixed case per T. Hansen 03/06/2016-JRL