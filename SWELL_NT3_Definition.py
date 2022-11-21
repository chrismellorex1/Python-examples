#
#
# SWELL_NT3_Definition.TextUtility
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
#Definition['displayName'] = "SWELL_NT3"
Definition['displayName'] = "SWELL_NT3"

Definition["showZoneCombiner"] = 0 # 1 to cause zone combiner to display
#Definition["defaultEditAreas"] = "Combinations_OFF_ONA_NT1"
#Definition["defaultEditAreas"] = [
#      ('AMZ011', "CARIBBEAN N OF 18N W OF 85W INCLUDING YUCATAN BASIN"),
#      ('AMZ013', "CARIBBEAN N OF 18N BETWEEN 76W AND 85W INCLUDING CAYMAN BASIN"),
#      ('AMZ015', "CARIBBEAN APPROACHES TO THE WINDWARD PASSAGE"),
#      ('AMZ017', "GULF OF HONDURAS"),
#      ('AMZ019', "CARIBBEAN FROM 15N TO 18N BETWEEN 80W AND 85W"),
#      ('AMZ021', "CARIBBEAN FROM 15N TO 18N BETWEEN 72W AND 80W"),
#      ('AMZ023', "CARIBBEAN N OF 15N BETWEEN 64W AND 72W"),
#      ('AMZ025', "OFFSHORE WATERS LEEWARD ISLANDS"),
#      ('AMZ027', "TROPICAL N ATLANTIC FROM 15N TO 19N BETWEEN 55W AND 60W"),
#      ('AMZ029', "W CENTRAL CARIBBEAN FROM 11N TO 15N W OF 80W"),
#      ('AMZ031', "CARIBBEAN FROM 11N TO 15N BETWEEN 72W AND 80W INCLUDING COLOMBIA BASIN"),
#      ('AMZ033', "CARIBBEAN S OF 15N BETWEEN 64W AND 72W INCLUDING VENEZUELA BASIN"),
#      ('AMZ035', "OFFSHORE WATERS WINDWARD ISLANDS INCLUDING TRINIDAD AND TOBAGO"),
#      ('AMZ037', "TROPICAL N ATLC FROM 7N TO 15N BETWEEN 55W AND 65W"),
#      ('AMZ039', "SW CARIBBEAN S OF 11N INCLUDING APPROACHES TO PANAMA CANAL"),
#      ('AMZ111', "ATLANTIC FROM 27N TO 31N W OF 77W"),
#      ('AMZ113', "ATLANTIC FROM 27N TO 31N BETWEEN 70W AND 77W"),
#      ('AMZ115', "ATLANTIC FROM 27N TO 31N BETWEEN 65W AND 70W"),
#      ('AMZ117', "BAHAMAS INCLUDING CAY SAL BANK"),
#      ('AMZ119', "ATLANTIC FROM 22N TO 27N E OF BAHAMAS TO 70W"),
#      ('AMZ121', "ATLANTIC FROM 22N TO 27N BETWEEN 65W AND 70W"),
#      ('AMZ123', "ATLANTIC S OF 22N W OF 70W INCLUDING APPROACHES TO THE WINDWARD PASSAGE"),
#      ('AMZ125', "ATLANTIC S OF 22N BETWEEN 65W AND 70W INCLUDING PUERTO RICO TRENCH"),
#      ('AMZ127', "ATLANTIC FROM 19N TO 22N BETWEEN 55W AND 65W"),
#              ]

Definition["defaultEditAreas"] = [
    ('AMZ040', "Caribbean N of 18N W of 85W including Yucatan Basin"),
    ('AMZ041', "NW Caribbean N of 20N E of 85W"),
    ('AMZ042', "Caribbean from 18N to 20N between 80W and 85W including Cayman Basin"),
    ('AMZ043', "Caribbean from 18N to 20N between 76W and 80W"),
    ('AMZ044', "Caribbean Approaches to the Windward Passage"),
    ('AMZ045', "Gulf of Honduras"),
    ('AMZ046', "Caribbean from 15N to 18N between 80W and 85W"),
    ('AMZ047', "Caribbean from 15N to 18N between 76W and 80W"),
    ('AMZ048', "Caribbean from 15N to 18N between 72W and 76W"),
    ('AMZ049', "Caribbean N of 15N between 68W and 72W"),
    ('AMZ050', "Caribbean N of 15N between 64W and 68W"),
    ('AMZ051', "Offshore Waters Leeward Islands"),
    ('AMZ052', "Tropical N Atlantic from 15N to 19N between 55W and 60W"),
    ('AMZ053', "W Central Caribbean from 11N to 15N W of 80W"),
    ('AMZ054', "Caribbean from 11N to 15N between 76W and 80W"),
    ('AMZ055', "Caribbean from 11N to 15N between 72W and 76W"),
    ('AMZ056', "Caribbean S of 15N between 68W and 72W"),
    ('AMZ057', "Caribbean S of 15N between 64W and 68W"),
    ('AMZ058', "Offshore Waters Windward Islands including Trinidad and Tobago"),
    ('AMZ059', "Tropical N Atlantic from 11N to 15N between 55W and 60W"),
    ('AMZ062', "Tropical N Atlantic from 07N to 11N"),
    ('AMZ060', "SW Caribbean S of 11N W of 80W"),
    ('AMZ061', "SW Caribbean S of 11N E of 80W including Approaches to Panama Canal"),
     
    ('AMZ063', "Atlantic from 29N to 31N W of 77W"),
    ('AMZ064', "Atlantic from 29N to 31N between 74W and 77W"),
    ('AMZ065', "Atlantic from 29N to 31N between 70W and 74W"),
    ('AMZ066', "Atlantic from 29N to 31N between 65W and 70W"),
    ('AMZ067', "Atlantic from 29N to 31N between 60W and 65W"),
    ('AMZ068', "Atlantic from 29N to 31N between 55W and 60W"),
    ('AMZ069', "Atlantic from 27N to 29N W of 77W"),
    ('AMZ070', "Atlantic from 27N to 29N between 74W and 77W"),
    ('AMZ071', "Atlantic from 27N to 29N between 70W and 74W"),
    ('AMZ072', "Atlantic from 27N to 29N between 65W and 70W"),
    ('AMZ073', "Atlantic from 27N to 29N between 60W and 65W"),
    ('AMZ074', "Atlantic from 27N to 29N between 55W and 60W"),
    ('AMZ075', "Northern Bahamas from 24N to 27N"),
    ('AMZ076', "Atlantic from 25N to 27N E of Bahamas to 70W"),
    ('AMZ077', "Atlantic from 25N to 27N between 65W and 70W"),
    ('AMZ078', "Atlantic from 25N to 27N between 60W and 65W"),
    ('AMZ079', "Atlantic from 25N to 27N between 55W and 60W"),
    ('AMZ080', "Central Bahamas from 22N to 24N including Cay Sal Bank"),
    ('AMZ081', "Atlantic from 22N to 25N E of Bahamas to 70W"),
    ('AMZ082', "Atlantic from 22N to 25N between 65W and 70W"),
    ('AMZ083', "Atlantic from 22N to 25N between 60W and 65W"),
    ('AMZ084', "Atlantic from 22N to 25N between 55W and 60W"),
    ('AMZ085', "Atlantic S of 22N W of 70W including Approaches to the Windward Passage"),
    ('AMZ086', "Atlantic S of 22N between 65W and 70W including Puerto Rico Trench"),
    ('AMZ087', "Atlantic from 19N to 22N between 60W and 65W"),
    ('AMZ088', "Atlantic from 19N to 22N between 55W and 60W"),
            ]

Definition["mapNameForCombinations"] = "Offshore_Marine_Zones" # Map background for creating Combinations

# Header configuration items
Definition["productName"] = "Offshore Waters Forecast"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "FZNT23"        # WMO ID
Definition["pil"] = "OFFNT3"          # product pil
Definition["areaName"] = "the SW and Tropical N Atlantic and\n" + \
                         "Caribbean Sea"  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "National Hurricane Center Miami, FL"  # Location of WFO - city st
Definition["textdbPil"] = "MIAOFFNT3"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCOFFNT3"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/OFFNT3.txt"

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
Definition["synopsisUGC"] = "AMZ001"    # UGC code for synopsis
Definition["synopsisHeading"] = ".SYNOPSIS..."# Heading for synopsis
#Definition["synopsis2UGC"] = "AMZ101"    # UGC code for 2nd synopsis
#Definition["synopsis2Heading"] = ".SYNOPSIS..."# Heading for 2nd synopsis

# Settings to insert text from previous Product.
Definition["prevProdPIL"] = "MIAOFFNT3"
Definition["updatePeriodIndex"] = 0
Definition["includeCombine"] = 0
