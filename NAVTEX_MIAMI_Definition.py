#
# This software was developed and / or modified by Raytheon Company,
# pursuant to Contract DG133W-05-CQ-1067 with the US Government.
#
# U.S. EXPORT CONTROLLED TECHNICAL DATA
# This software product contains export-restricted data whose
# export/transfer/disclosure is restricted by U.S. law. Dissemination
# to non-U.S. persons whether in the United States or abroad requires
# an export license or other authorization.
#
# Contractor Name:        Raytheon Company
# Contractor Address:     6825 Pine Street, Suite 340
#                         Mail Stop B8
#                         Omaha, NE 68106
#                         402.291.0100
#
# See the AWIPS II Master Rights File ("Master Rights File.pdf") for
# further licensing information.
##
# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# OFF_ONA_NT1_Definition.TextUtility
#
#  This file sets up all the Product Definition overrides for the
#  OFF formatter for a site.
#
# History
# F.Achorn/K.Achorn/OPC    11/07/2011    Migrated from WNOR
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
Definition['displayName'] = "NAVTEX_MIAMI"

Definition["showZoneCombiner"] = 0 # 1 to cause zone combiner to display
#Definition["defaultEditAreas"] = "Combinations_OFF_ONA_NT1"
Definition["defaultEditAreas"] = [
            ('NAV04A', "Southeast Gulf of Mexico"),
            ('NAV04B', "WITHIN 200 NM EAST OF THE COAST OF FLORIDA")
            ]

Definition["mapNameForCombinations"] = "None" # Map background for creating Combinations

# Header configuration items
Definition["productName"] = "NAVTEX Marine Forecast"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "FZNT25"        # WMO ID
Definition["pil"] = "OFFN04"          # product pil
Definition["areaName"] = ""  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "National Hurricane Center Miami, FL"  # Location of WFO - city st
Definition["textdbPil"] = "MIAOFFN04"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCOFFN04"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/OFFN04.txt"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
#Definition["editAreaSuffix"] = "_pt"

#Definition["lineLength"] = 66   #Product line length
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
Definition["synopsisHeading"] = "Southeast Gulf of Mexico\n\n" + ".SYNOPSIS..."# Heading for synopsis

# Settings to insert text from previous Product.
Definition["prevProdPIL"] = "MIAOFFN04"
Definition["updatePeriodIndex"] = 0
Definition["includeCombine"] = 0
