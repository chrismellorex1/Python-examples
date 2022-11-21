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
Definition['displayName'] = "FRENCH_NT3"

Definition["showZoneCombiner"] = 0 # 1 to cause zone combiner to display
#Definition["defaultEditAreas"] = "Combinations_OFF_ONA_NT1"

VariableList = [
        #(copy.deepcopy(CWF.TextProduct.VariableList)),
        (("Include Tropical?", "includeTropical"), "No", "radio", ["Yes", "No"]),
        (("Forecaster Name", "forecasterName"), "TAFB", "radio",
         ["NELSON", "STRIPLING", "LEVINE", "CHRISTENSEN",
          "LEWITSKY", "ASL", "GR", "AGUIRRE", "MUNDELL",
          "MCROY", "LANDSEA", "FORMOSA", "RIVERA", "MT", "NAR"]),
        (("Period Combining?", "pdCombo"), "No", "radio", ["Yes", "No"]),
        ((("Keep Previous Text After Period",
                      "updatePeriodIndex"), "No old text",
                      "radio", ["No old text", "Refresh headlines only",
                                1, 2, 3, 4, 5]))
        ]

Definition["defaultEditAreas"] = [
    ('AMZ011', "CARIBBEAN N OF 18N W OF 85W INCLUDING YUCATAN BASIN"),
    ('AMZ013', "CARIBBEAN N OF 18N BETWEEN 76W AND 85W INCLUDING CAYMAN BASIN"),
    ('AMZ015', "CARIBBEAN APPROACHES TO THE WINDWARD PASSAGE"),
    ('AMZ017', "GULF OF HONDURAS"),
    ('AMZ019', "CARIBBEAN FROM 15N TO 18N BETWEEN 80W AND 85W"),
    ('AMZ021', "CARIBBEAN FROM 15N TO 18N BETWEEN 72W AND 80W"),
    ('AMZ023', "CARIBBEAN N OF 15N BETWEEN 64W AND 72W"),
    ('AMZ025', "OFFSHORE WATERS LEEWARD ISLANDS"),
    ('AMZ027', "TROPICAL N ATLANTIC FROM 15N TO 19N BETWEEN 55W AND 60W"),
    ('AMZ029', "W CENTRAL CARIBBEAN FROM 11N TO 15N W OF 80W"),
    ('AMZ031', "CARIBBEAN FROM 11N TO 15N BETWEEN 72W AND 80W INCLUDING COLOMBIA BASIN"),
    ('AMZ033', "CARIBBEAN S OF 15N BETWEEN 64W AND 72W INCLUDING VENEZUELA BASIN"),
    ('AMZ035', "OFFSHORE WATERS WINDWARD ISLANDS INCLUDING TRINIDAD AND TOBAGO"),
    ('AMZ037', "TROPICAL N ATLC FROM 7N TO 15N BETWEEN 55W AND 65W"),
    ('AMZ039', "SW CARIBBEAN S OF 11N INCLUDING APPROACHES TO PANAMA CANAL"),
    ('AMZ111', "ATLANTIC FROM 27N TO 31N W OF 77W"),
    ('AMZ113', "ATLANTIC FROM 27N TO 31N BETWEEN 70W AND 77W"),
    ('AMZ115', "ATLANTIC FROM 27N TO 31N BETWEEN 65W AND 70W"),
    ('AMZ117', "BAHAMAS INCLUDING CAY SAL BANK"),
    ('AMZ119', "ATLANTIC FROM 22N TO 27N E OF BAHAMAS TO 70W"),
    ('AMZ121', "ATLANTIC FROM 22N TO 27N BETWEEN 65W AND 70W"),
    ('AMZ123', "ATLANTIC S OF 22N W OF 70W INCLUDING APPROACHES TO THE WINDWARD PASSAGE"),
    ('AMZ125', "ATLANTIC S OF 22N BETWEEN 65W AND 70W INCLUDING PUERTO RICO TRENCH"),
    ('AMZ127', "ATLANTIC FROM 19N TO 22N BETWEEN 55W AND 65W"),
            ]

Definition["mapNameForCombinations"] = "Offshore_Marine_Zones" # Map background for creating Combinations

# Header configuration items
#Definition["productName"] = "COASTAL WATERS FORECAST"  # name of product
Definition["fullStationID"] = "KNHC"  # full station identifier (4letter)
Definition["wmoID"] = "FZNT23"        # WMO ID
#Definition["wmoID"] = "TEST05"        # WMO ID
Definition["pil"] = "OFFNT3"          # product pil
Definition["areaName"] = "THE SW AND TROPICAL N ATLANTIC AND\n" + \
                         "CARIBBEAN SEA"  # Name of state, such as "GEORGIA"
Definition["wfoCityState"] = "NATIONAL HURRICANE CENTER MIAMI FL"  # Location of WFO - city st
Definition["textdbPil"] = "MIAOFFNT3"       # Product ID for storing to AWIPS text database.
Definition["awipsWANPil"] = "KNHCOFFNT3"   # Product ID for transmitting to AWIPS WAN.
Definition["outputFile"] =  "{prddir}/TEXT/OFFNT3.txt"

# OPTIONAL CONFIGURATION ITEMS
Definition["database"] = "Fcst"    # Source database. "Official", "Fcst", or "ISC"
Definition["debug"] = 1
#Definition["editAreaSuffix"] = "_pt"

#Definition["lineLength"] = 65   #Product line length
Definition["hazardSamplingThreshold"] = (0, 1)  #(%cov, #points)

Definition["periodCombining"] = 1     # If 1, do period combining
Definition["includeEveningPeriod"] = 0  # If 1, include Evening Period
Definition["useAbbreviations"] = 0      # If 1, use marine abbreviations

# Weather-related flags
#Definition["hoursSChcEnds"] = 24

#Definition["areaDictionary"] = "AreaDictionary"     # For product headers
Definition["language"] = "french"
#Definition["useHolidays"] = 1
Definition['lowerCase'] = 0
# Trouble-shooting items
#Definition["passLimit"] = 20             # Limit on passes allowed through Narrative Tree
#Definition["trace"] = 1                  # Set to 1 to turn on trace through
                                         # Narrative Tree for trouble-shootin

# Required for BASE OFF!
#  synopsisUGC      UGC code for Synopsis
Definition["synopsisUGC"] = "AMZ001"    # UGC code for synopsis
Definition["synopsisHeading"] = ".SYNOPSIS..."# Heading for synopsis
#Definition["productName"] = "LA PREVISION POUR LES EAUX AU LARGE"

#Definition["synopsis2UGC"] = "AMZ101"    # UGC code for 2nd synopsis
#Definition["synopsis2Heading"] = ".SYNOPSIS..."# Heading for 2nd synopsis
