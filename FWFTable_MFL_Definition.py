# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# FWFTable_MFL_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the
#  FWFTable formatter for a site.
#
#edited for mixed case format IRL 12/11-12/12/16
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

#----- WFO MFL FWFTable Definition -----
# Definition Statements must start in column 1.

# REQUIRED CONFIGURATION ITEMS
Definition['displayName'] = "FWFTable"
#Definition['displayName'] = "FWF_Tabular"

Definition["defaultEditAreas"] = "Combinations_FWFTable_MFL"
Definition["mapNameForCombinations"] = "Zones_MFL" # Map background for creating Combinations

# Header configuration items
#Definition["productName"] = "FIRE WEATHER PLANNING FORECAST"  # name of product
Definition["productName"] = "Fire Weather Planning Forecast"  # name of product
#Definition["fullStationID"] = "KMFL"  # full station identifier (4letter)
#Definition["wmoID"] = "FNUS52"        # WMO ID
Definition["pil"] = "FWFMFL"          # product pil
#Definition["areaName"] = "SOUTH FLORIDA" # Name of state, such as "GEORGIA"
Definition["areaName"] = "South Florida" # Name of state, such as "GEORGIA"
#Definition["wfoCityState"] = "MIAMI FL"  # Location of WFO - city state
Definition["textdbPil"] = "MIAFWFMFL"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KMFLFWFMFL"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "/home/apps/xnow/temp/FWFMFL"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Official"    # Source database. "Official", "Fcst", or "ISC"
#Definition["debug"] = 1

#Automatic Functions
Definition["autoSend"] = 0   #set to 1 to automatically transmit product
Definition["autoSendAddress"] = "000"   #transmission address
Definition["autoStore"] = 0   #set to 1 to store product in textDB
Definition["autoWrite"] = 0   #set to 1 to write product to file

Definition["lineLength"] = 69#66   #Product line length

Definition["periodCombining"] = 1     # If 1, do period combining
Definition["columnJustification"] = "l"  # Left (l) or right (r) justification for columns
Definition["useRH"] = 0                  # Use RH grids instead of MaxRH, MinRH
Definition["summaryExtended"] = 0
#Definition["summaryArea"] = "FireWxAOR_MFL"
Definition["individualExtended"] = 1
Definition["extendedLabel"] = 1

# Set the following variable to 1 if you want Mixing Height,
# Transport Wind and Vent Index reported in night periods.
Definition["mixingParmsDayAndNight"] = 1
# Use "Max" or "Avg" for mixHgt
Definition["mixHgtMethod"] = "Max"

# Set the following variable to 1 if you want Lightning Activity
# reported with phrases like "1-8 STRIKES", "9-15 STRIKES", etc.
Definition["lightningPhrases"] = 0

# Winds are reported from the Wind20ft grid if available.
# Otherwise, the Wind grid is used with the magnitude multiplied
# by this wind adjustment factor.
# Winds reported by RAWS sites are frequently lower than ASOS winds
# due to the fact that use a 10-min average.  A common adjustment
# factor is 80% (0.80).  If you want no adjust ment to the winds
# then set this variable to 1.00
#Definition["windAdjustmentFactor"] = 1.00


Definition["windGustDiffMph"] = 5
# Threshold for a light TransWind string in the table
Definition["tableLightTransWindThreshold"] = 5
# Light TransWind string in the table
Definition["tableLightTransWindPhrase"] = "LGT/VAR"
Definition["tableLightWindThreshold"] = 4
Definition["tableLightWindPhrase"] = "LGT/VAR"
# Use a range for the winds in the table 1=yes
#Definition["tableWindRanges"] = 1

# If max humidity is above this percentage, humidity recovery
# will be EXCELLENT.
#Definition["humidityRecovery_percentage"] = 50

# Set the following variable to 1 to include long-range outlook
# placeholders at the end of the product.  These are appended by
# _postProcessProduct
Definition["includeOutlooks"] = 0
Definition["useHolidays"] = 0       # Will use holidays in time period labels
#Definition["areaDictionary"] = "AreaDictionary"     # For product headers

# Weather-related flags
Definition["hoursSChcEnds"] = 206
#Definition["popWxThreshold"] = 1
