# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# FWF_MFL_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the
#  FWF formatter for a site.
#
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

#----- WFO MFL FWF Definition -----
# Definition Statements must start in column 1.
# REQUIRED CONFIGURATION ITEMS
Definition['displayName'] = None
#Definition['displayName'] = "FWF"

Definition["defaultEditAreas"] = "Combinations_FWF_MFL"
Definition["mapNameForCombinations"] = "FireWxZones_MFL" # Map background for creating Combinations

#Definition["tempLocalEffects"] = 1   # Set to 1 to enable Temp and RH local effects AFTER
                                      # creating AboveElev and BelowElev edit areas
#Definition["windLocalEffects"] = 1   # Set to 1 to enable wind local effects AFTER
                                      # creating Ridges and Valleys edit areas

# Header configuration items
#Definition["productName"] = "FIRE WEATHER PLANNING FORECAST"  # name of product
#Definition["fullStationID"] = "KMFL"  # full station identifier (4letter)
#Definition["wmoID"] = "FNUS52"        # WMO ID
#Definition["pil"] = "FWFMFL"          # product pil
#Definition["areaName"] = "STATENAME" # Name of state, such as "GEORGIA"
#Definition["wfoCityState"] = "MIAMI FL"  # Location of WFO - city st
#Definition["textdbPil"] = "MIAFWFMFL"       # Product ID for storing to AWIPS text database.
#Definition["awipsWANPil"] = "KMFLFWFMFL"   # Product ID for transmitting to AWIPS WAN.
#Definition["outputFile"] =  "{prddir}/TEXT/FWF.txt"

# OPTIONAL CONFIGURATION ITEMS
#Definition["database"] = "Official"    # Source database. "Official", "Fcst", or "ISC"
#Definition["debug"] = 1

#Automatic Functions
#Definition["autoSend"] = 1    #set to 1 to automatically transmit product
#Definition["autoSendAddress"] = "000"   #transmission address
#Definition["autoStore"] = 1   #set to 1 to store product in textDB
#Definition["autoWrite"] = 1   #set to 1 to write product to file

#Definition["periodCombining"] = 1     # If 1, do period combining
Definition["useRH"] = 0                # Use RH grids instead of MaxRH, MinRH
#Definition["summaryExtended"] = 0
#Definition["summaryArea"] = "FireWxAOR_MFL"
#Definition["individualExtended"] = 1
#Definition["extendedLabel"] = 1
Definition["useHolidays"] = 0       # Will use holidays in time period labels
#Definition["includeTrends"] = 0     # Set to 1 to include Temp and RH trends

#Definition["lineLength"] = 66   #Product line length

# Set the following variable to 1 if you want Lightning Activity
# reported with phrases like "1-8 STRIKES", "9-15 STRIKES", etc.
Definition["lightningPhrases"] = 0

# The following variable sets a wind adjustment factor for surface
# (20 ft) winds.  Wind speeds will be multiplied by this factor.
# Winds reported by RAWS sites are frequently lower than ASOS winds
# due to the fact that they use a 10-min average.  A common adjustment
# factor is 80% (0.80).  If you want no adjustment to the winds
# then set this variable to 1.00
#Definition["windAdjustmentFactor"] = 1.00

#Definition["includeMultipleElementTable"] = 1       # Will include a MultipleElementTable
#Definition["includeMultipleElementTable_perPeriod"] = 1 # Will include a MultipleElementTable
                                                     # per area per period.
                                                     # ("singleValueFormat" must be 1)
# Uncomment just one elementList below
#Definition["elementList"] = ["Temp", "Humidity", "PoP"] # Default
#Definition["elementList"] = ["Temp", "PoP"]
#Definition["singleValueFormat"] = 1                     # Default is 0

# Weather-related flags
#Definition["periodSChcEnds"] = 2

#Definition["areaDictionary"] = "AreaDictionary"     # For product headers
#Definition["language"] = "english"

# Trouble-shooting items
#Definition["passLimit"] = 20              # Limit on passes allowed through
                                          # Narrative Tree
#Definition["trace"] = 1                   # Set to 1 to turn on trace
