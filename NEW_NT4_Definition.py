##
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
Definition['displayName'] = "NEW_NT4"

Definition["showZoneCombiner"] = 0 # 1 to cause zone combiner to display
#Definition["defaultEditAreas"] = "Combinations_OFF_ONA_NT1"
Definition["defaultEditAreas"] = [
     ('TEST011', "1"),
     ('TEST013', "2"),
     ('TEST015', "3"),
     ('TEST017', "4"),
     ('TEST019', "5"),
     ('TEST021', "6"),
     ('TEST023', "7"),
     ('TEST025', "8"),
     ('TEST027', "9"),
     ('TEST029', "10"),
     ('TEST031', "11"),
     ('TEST033', "12"),
            ]

Definition["mapNameForCombinations"] = "Offshore_Marine_Zones" # Map background for creating Combinations

# Header configuration items
#Definition["productName"] = "COASTAL WATERS FORECAST"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "FZNT24"        # WMO ID
Definition["pil"] = "NEWNT4"          # product pil
Definition["areaName"] = "THE GULF OF MEXICO"  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "NATIONAL HURRICANE CENTER MIAMI FL"  # Location of WFO - city st
Definition["textdbPil"] = "MIANEWNT4"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCNEWNT4"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/NEWNT4.txt"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 0
#Definition["editAreaSuffix"] = "_pt"

#Definition["lineLength"] = 66   #Product line length
Definition["hazardSamplingThreshold"] = (0, 1)  #(%cov, #points)

Definition["periodCombining"] = 0     # If 1, do period combining
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

